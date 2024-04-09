# mailing_service/views.py
from .forms import ClientForm, MailingForm, MessageForm, ClientDeleteConfirmationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Client, Mailing, Message, Log
from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect
from django.views.generic import DetailView
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib import messages
from django.conf import settings
from django.db.models import Q
from .tasks import EmailTask
from blog.models import Post
from django.views.generic import (
    TemplateView,
    CreateView,
    UpdateView,
    DeleteView,
    FormView,
    ListView,
    View
)


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'mailing_service/client_list.html'
    context_object_name = 'clients'

    def get_queryset(self):
        return Client.objects.filter(created_by=self.request.user)

    def post(self, request, *args, **kwargs):
        selected_clients = request.POST.getlist('selected_clients[]')

        if 'select_all' in request.POST:
            selected_clients = list(Client.objects.values_list('pk', flat=True))

        if 'delete_selected' in request.POST:
            if selected_clients:
                return redirect(reverse_lazy('mailing_service:client_confirm_delete', args=[','.join(selected_clients)]))

        return redirect(reverse_lazy('mailing_service:client_list'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['clients'] = self.get_queryset()
        return context


class ClientDeleteConfirmationView(FormView):
    template_name = 'mailing_service/client_confirm_delete.html'
    form_class = ClientDeleteConfirmationForm
    success_url = reverse_lazy('mailing_service:client_list')

    def form_valid(self, form):
        selected_clients = self.kwargs['selected_clients'].split(',')
        if selected_clients:
            Client.objects.filter(pk__in=selected_clients).delete()
            return super().form_valid(form)
        else:
            return HttpResponseRedirect(self.success_url)


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'mailing_service/client_form.html'
    success_url = reverse_lazy('mailing_service:client_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        email = form.cleaned_data['email']
        full_name = form.cleaned_data['full_name']

        if Client.objects.filter(Q(email=email) | Q(full_name=full_name)).exists():
            messages.error(self.request, 'Клиент с таким email или именем уже существует.')
            return self.form_invalid(form)

        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'mailing_service/client_form.html'
    success_url = reverse_lazy('mailing_service:client_list')

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        full_name = form.cleaned_data.get('full_name')
        client = self.get_object()

        if Client.objects.exclude(pk=client.pk).filter(Q(email=email) | Q(full_name=full_name)).exists():
            messages.error(self.request, 'Клиент с таким email или именем уже существует.')
            return self.form_invalid(form)

        return super().form_valid(form)


class ClientDeleteView(View):
    template_name = 'mailing_service/client_delete.html'
    form_class = ClientDeleteConfirmationForm
    success_url = reverse_lazy('mailing_service:client_list')

    def get(self, request, *args, **kwargs):
        selected_clients = request.GET.getlist('selected_clients[]')
        clients = Client.objects.filter(pk__in=selected_clients)
        return render(request, self.template_name, {'clients': clients})

    def post(self, request, *args, **kwargs):
        selected_clients = request.POST.getlist('selected_clients[]')
        if 'delete' in request.POST:
            Client.objects.filter(pk__in=selected_clients).delete()
        return HttpResponseRedirect(self.success_url)


class LogListView(LoginRequiredMixin, ListView):
    model = Log
    template_name = 'mailing_service/log_list.html'
    context_object_name = 'logs'
    paginate_by = 100

    def get_queryset(self):
        return Log.objects.all().order_by('-attempt_time')


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = 'mailing_service/mailing_list.html'
    context_object_name = 'mailings'

    def get_queryset(self):
        return Mailing.objects.filter(created_by=self.request.user)


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing_service/mailing_form.html'
    success_url = reverse_lazy('mailing_service:mailing_list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['clients'].queryset = Client.objects.filter(created_by=self.request.user)
        return form

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.activate_mailing()
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class MailingBlockView(UpdateView):
    model = Mailing
    fields = []

    def post(self, request, *args, **kwargs):
        mailing = self.get_object()
        mailing.block_mailing()
        return HttpResponseRedirect(reverse_lazy('mailing_service:mailing_list'))


class MailingUnblockView(UpdateView):
    model = Mailing
    fields = []

    def post(self, request, *args, **kwargs):
        mailing = self.get_object()
        mailing.unblock_mailing()
        return HttpResponseRedirect(reverse_lazy('mailing_service:mailing_list'))


class MailingDetailView(DetailView):
    model = Mailing
    template_name = 'mailing_service/mailing_detail.html'
    context_object_name = 'mailing'


class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing_service/mailing_form.html'
    success_url = reverse_lazy('mailing_service:mailing_list')

    def form_valid(self, form):
        result = super().form_valid(form)
        try:
            EmailTask.send_emails(self.object.id)
        except Exception as e:
            messages.error(self.request, f'Ошибка при отправке рассылки: {e}')
        return result


class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = 'mailing_service/mailing_delete.html'
    success_url = reverse_lazy('mailing_service:mailing_list')

    def get_success_url(self):
        return self.success_url

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'mailing_service/message_list.html'
    context_object_name = 'messages'

    def get_queryset(self):
        return Message.objects.all()


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailing_service/message_form.html'
    success_url = reverse_lazy('mailing_service:message_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailing_service/message_form.html'
    success_url = reverse_lazy('mailing_service:message_list')


class MessageDeleteView(DeleteView):
    model = Message
    template_name = 'mailing_service/message_delete.html'
    success_url = reverse_lazy('mailing_service:message_list')

    def post(self, request, *args, **kwargs):
        selected_messages = request.POST.getlist('selected_messages')

        if 'delete_selected' in request.POST:
            Message.objects.filter(pk__in=selected_messages).delete()

        return redirect(reverse_lazy('mailing_service:message_list'))


def send_test_email_view(request):
    try:
        send_mail(
            'Тестовое письмо',
            'Это тестовое письмо от вашего Django-приложения.',
            settings.EMAIL_HOST_USER,
            ['djermak3000@mail.ru'],  # Замените на реальный адрес получателя
            fail_silently=False,
        )
        return HttpResponse('Тестовое письмо успешно отправлено!')
    except Exception as e:
        return HttpResponse(f'Ошибка при отправке тестового письма: {e}')


class HomeView(TemplateView):
    template_name = 'mailing_service/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_mailings'] = Mailing.objects.count()
        context['active_mailings'] = Mailing.objects.filter(status='started').count()
        context['unique_clients'] = Client.objects.count()
        context['latest_posts'] = Post.objects.order_by('-publication_date')[:3]
        context['most_viewed_posts'] = Post.objects.order_by('-views')[:3]
        return context


class SentMailingsReportView(TemplateView):
    template_name = 'mailing_service/sent_mailings_report.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sent_mailings'] = Mailing.objects.filter(status='completed')
        return context
