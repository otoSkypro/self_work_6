# users/context_processors.py

def has_perm_can_view_dashboard(request):
    return {'has_perm_can_view_dashboard': request.user.has_perm('users.can_view_dashboard')}
