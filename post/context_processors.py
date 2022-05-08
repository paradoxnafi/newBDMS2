from auth1.models import RegisterUser, Notification

def notification_to_base(request):
    user = request.user.id
    notifications = Notification.objects.filter(receiver=user).order_by('-creation_date')
    unread_notifications = Notification.objects.filter(receiver=user).exclude(read_by=user).order_by('-creation_date')
    total_unread_notifications = len(unread_notifications)
    # Get all pk of unread_notifications
    pk_unread_notifications = []
    for item in unread_notifications:
        pk_unread_notifications.append(item.pk)

    # Get all pk of notifications
    pk_notifications = []
    for item in notifications:
        pk_notifications.append(item.pk)    
    # Get all pk of read_notifications
    pk_read_notifications = list(set(pk_notifications) ^ set(pk_unread_notifications) )

    read_notifications = Notification.objects.filter(receiver=user, pk__in=pk_read_notifications).order_by('-creation_date')
#    read_notifications = notifications.objects.filter(pk__in=pk_read_notifications)

    return {
        'total_unread_notifications': total_unread_notifications,
        'notifications': notifications,
        'unread_notifications': unread_notifications,
        'read_notifications': read_notifications,
        }

