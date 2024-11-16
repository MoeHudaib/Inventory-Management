from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from e_commerce.models import Order

@receiver(post_save, sender=Order)
def notify_new_order(sender, instance, created, **kwargs):
    if created:  # Only notify when a new order is created
        channel_layer = get_channel_layer()
        message = f"New order {instance.id} created!"

        # Send message to the user's WebSocket group
        async_to_sync(channel_layer.group_send)(
            f'user_{instance.user.id}_orders',  # The group name
            {
                'type': 'send_order_update',  # The consumer's method to call
                'message': message,  # The message to send
            }
        )
