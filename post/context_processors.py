from auth1.models import RegisterUser, Notification

def notification_to_base(request):
    user = request.user.id
    notifications = Notification.objects.filter(receiver=user)
    unread_notifications = Notification.objects.filter(receiver=user).exclude(read_by=user)
    total_unread_notifications = len(unread_notifications)
    return {
        'total_unread_notifications': total_unread_notifications,
        'notifications': notifications,
        }
