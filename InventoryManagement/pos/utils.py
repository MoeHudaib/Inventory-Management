from .models import Inbound, Outbound, InboundItem, OutboundItem
from sales.models import MaterialReport
from django.contrib import messages  # Use 'django.contrib.messages' instead of 'flash_messages'
from django.shortcuts import get_object_or_404
from inventory.models import Stock

def process_inbound(user, products, source):
    # Create or update the Inbound object
    inbound, created = Inbound.objects.update_or_create(
        responsible_staff=user,
        source=source,
    )

    for id, qty, exp_date in products:
        # Create or update the InboundItem
        InboundItem.objects.update_or_create(
            inbound=inbound,
            material_id=id,  # Use material_id if 'id' is the primary key
            defaults={
                'quantity': int(qty),
                'expiration_date': exp_date,
            }
        )
        
        # Create or update the MaterialReport
        MaterialReport.objects.update_or_create(
            inbound=inbound,
            material_id=id,  # Use material_id if 'id' is the primary key
            defaults={
                'quantity': int(qty),
                'expiration_date': exp_date,
            }
        )
        material = get_object_or_404(Stock, id=id)
        material.save()


    # Use messages to provide feedback
    messages= 'Inbound processed successfully!'
    return messages

def process_outbound(product, quantity):
    stock = get_object_or_404(Stock, id=product.id)

    # Check if product and quantity are valid
    if product is None or quantity is None:
        return 'Null values are passed, track your process!'

    if stock.stocks_availability < quantity:
        message = f"{product.name}'s quantity cannot be processed due to a lack of availability!"
        print(message)
        return message

    inbound_items = InboundItem.objects.filter(material=product).order_by('expiration_date')

    for item in inbound_items:
        if item.quantity <= 0:
            continue  # Skip items with zero quantity

        # Process the outbound quantity
        if quantity > 0:
            if item.quantity >= quantity:
                item.quantity -= quantity
                item.save()
                print(f"Processed {quantity} from {item.material.name}. Remaining quantity: {item.quantity}")
                quantity = 0  # All quantity has been processed
                break
            else:
                quantity -= item.quantity
                print(f"Processed {item.quantity} from {item.material.name}. Remaining quantity to process: {quantity}")
                item.quantity = 0  # All of this item is consumed
                item.save()
        else:
            break  # No quantity left to process

    if quantity > 0:
        message = f"Not all of the requested quantity for {product.name} could be processed."
        print(message)
        stock.save()
        return message
    stock.save()
    return "Outbound processing completed successfully."
