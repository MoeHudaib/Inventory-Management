from django.shortcuts import render,redirect,HttpResponse, get_object_or_404
from inventory.models import Contact_us, Color, Category, Stock, SHIPPING_FEES, TAX_RATE
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from decimal import Decimal
from e_commerce.models import Order, OrderItem
from django.contrib import messages 
from sales.models import MaterialReport
from pos.models import InboundItem

# Complete Place order Part To link this app properly to the project
def ABOUT(request):
    return render(request,'main/about.html')


def base(request):
    return render(request, 'main/base.html')

def Home(request):
    product = Stock.objects.all()
    context = {
        'product':product,
    }
    return render(request,'main/index.html',context)


def SEARCH(request):
    query = request.GET.get('query')
    product = Stock.objects.filter(name__icontains=query)
    context = {
        'product': product
    }
    return render(request, 'main/search.html', context)

@login_required(login_url="e_commerce:login")
def PRODUCT_DETAILS_PAGE(request,id):
    prod = get_object_or_404(Stock, id=id)
    context = {
        'prod': prod
    }
    return render(request, 'main/product_single.html',context)


@login_required(login_url="e_commerce:login")
def PRODUCT(request):
    # Default product list
    product = Stock.objects.filter(active=True)
    mhm = "Default"  # Default label

    # Handling sorting
    if 'ATOZ' in request.GET:
        product = product.order_by('name')
        mhm = "A to Z"
    elif 'ZTOA' in request.GET:
        product = product.order_by('-name')
        mhm = "Z to A"
    elif 'NTOD' in request.GET:
        product = product.order_by('-id')  # Assuming 'id' is creation date or similar
        mhm = "New"
    elif 'DTON' in request.GET:
        product = product.order_by('id')  # Oldest first
        mhm = "Old"

    # Fetch categories and colors
    categories = Category.objects.all()
    product_colors = Color.objects.all()

    # Pass context to the template
    context = {
        "mhm": mhm,
        "product_colors": product_colors,
        "categories": categories,
        "product": product,
    }

    return render(request, 'main/product.html', context)

def CONTACT_US(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        contact = Contact_us(
            name=name,
            email=email,
            subject=subject,
            message=message,
        )

        # Define the email subject, message, and sender
        email_subject = subject
        email_message = f"From: {name} <{email}>\n\nMessage:\n{message}"
        email_from = settings.EMAIL_HOST_USER

        try:
            # Send the email
            send_mail(
                subject=email_subject,
                message=email_message,
                from_email=email_from,
                recipient_list=['Hammodehyaser79@gmail.com'],  
                fail_silently=False,
            )
            contact.save()  # Save to the database if email was sent successfully
            return redirect('e_commerce:home')
        
        except Exception as e:
            print(f"Error sending email: {e}")  # For debugging
            return redirect('e_commerce:contact')
    return render(request,'main/contact.html')

def HandleRegister(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        email=request.POST.get('email')
        pass1=request.POST.get('pass1')
        pass2=request.POST.get('pass2')
        customer = User.objects.create_user(username,email,pass1)
        customer.first_name = first_name
        customer.last_name = last_name
        customer.save()
        return redirect('e_commerce:home')
    return render(request,'main/registration/auth.html')

def HandleLogin(request):
     if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user = authenticate(username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('e_commerce:home')
        else:
            return redirect('e_commerce:login')
     return render(request,'main/registration/auth.html')

def HandleLogout(request):
    logout(request)
    return redirect('e_commerce:home')

@login_required(login_url="e_commerce:login")
def cart_add(request, id):
    user = request.user
    if not user.is_superuser or not user.is_staff:
        cart = Cart(request)
        product = Stock.objects.get(id=id)
        cart.add(product=product)
        return redirect("e_commerce:product")
    else:
        return redirect("inventory:index")


@login_required(login_url="e_commerce:login")
def item_clear(request, id):
    
    cart = Cart(request)
    product = Stock.objects.get(id=id)
    cart.remove(product)
    return redirect("e_commerce:cart_detail")


@login_required(login_url="e_commerce:login")
def item_increment(request, id):
    cart = Cart(request)
    product = Stock.objects.get(id=id)
    cart.add(product=product)
    return redirect("e_commerce:cart_detail")


@login_required(login_url="e_commerce:login")
def item_decrement(request, id):
    cart = Cart(request)
    product = Stock.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("e_commerce:cart_detail")


@login_required(login_url="e_commerce:login")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()

    return redirect("e_commerce:cart_detail")


@login_required(login_url="e_commerce:login")
def cart_detail(request):
    context = {
        'user':request.user,
        'shipping_fees':SHIPPING_FEES,
        'tax_rate':TAX_RATE
    }
    return render(request, 'cart/cart_details.html', context)

def generate_order_pdf(request, pk):
    order = get_object_or_404(Order, pk=pk)
    pdf = order.generate_pdf()
    
    if pdf is None:
        return HttpResponse("Error generating PDF", status=500)
    
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="order_requisition_{pk}.pdf"'
    return response

def order_confirmation(request, pk):
    order = get_object_or_404(Order, pk = pk)

    context = {
        'order':order,
    }
    return render(request, 'bills/order_confirmation.html', context)

@login_required(login_url="e_commerce:login")
def Check_out(request):
    if request.method == 'POST':
        pass
    user = request.user

    context = {
        'user':user,
        'shipping_fees':SHIPPING_FEES,
        'tax_rate':TAX_RATE
    }
    return render(request, 'cart/checkout.html', context)

from django.db import transaction

@login_required(login_url="e_commerce:login")
def PLACE_ORDER(request):
    """Handle the process of placing an order."""
    if request.method == "POST":
        # Retrieve order data from the POST request
        order_data = {
            'firstname': request.POST.get('firstname'),
            'lastname': request.POST.get('lastname'),
            'country': request.POST.get('country'),
            'city': request.POST.get('city'),
            'address': request.POST.get('address'),
            'postcode': request.POST.get('postcode'),
            'phone': request.POST.get('phone'),
            'email': request.POST.get('email'),
            'additional_info': request.POST.get('additional_info')
        }

        # Validate that all required fields are filled
        if all(order_data.values()):
            try:
                # Start a database transaction to ensure data integrity
                with transaction.atomic():
                    # Create the Order object
                    order = Order(
                        user=request.user,
                        firstname=order_data['firstname'],
                        lastname=order_data['lastname'],
                        country=order_data['country'],
                        city=order_data['city'],
                        address=order_data['address'],
                        postcode=order_data['postcode'],
                        phone=order_data['phone'],
                        email=order_data['email'],
                        additional_info=order_data['additional_info'],
                    )
                    order.save()  # Save the order to the database

                    # Process the cart items
                    cart = Cart(request)
                    cart_items = cart.cart
                    cart_total = calculate_cart_total(cart_items)

                    # Process each item in the cart and update the stock
                    for item in cart_items.values():
                        product = get_object_or_404(Stock, id=item['product_id'])
                        quantity = float(item['quantity'])

                        # Lock the inbound items for this product to prevent concurrent access
                        inbound_items = InboundItem.objects.filter(
                            material=product, active=True
                        ).select_for_update().order_by('expiration_date')

                        # If not enough stock available, raise an exception
                        available_quantity = product.stocks_availability
                        if available_quantity < quantity:
                            raise ValueError(f"Not enough stock available for {product.name}.")

                        # Create an OrderItem for the product
                        OrderItem.objects.create(
                            order=order,
                            product=product,
                            quantity=item['quantity'],
                        )

                        # Process inbound items and commit stock
                        remaining_quantity = quantity
                        for inbound_item in inbound_items:
                            if remaining_quantity <= 0:
                                break  # No more quantity to process

                            if inbound_item.quantity >= remaining_quantity:
                                # Commit this stock to the order
                                inbound_item.quantity -= remaining_quantity
                                product.stocks_committed += remaining_quantity
                                inbound_item.save()
                                product.save()
                                # Create MaterialReport to track committed stock
                                MaterialReport.objects.create(
                                    material=product,
                                    quantity=remaining_quantity,
                                    order=order,
                                    location=inbound_item.location,
                                    expiration_date=inbound_item.expiration_date,
                                )
                                remaining_quantity = 0  # All quantity has been processed
                            else:
                                # Use up all the available stock in this inbound item
                                remaining_quantity -= inbound_item.quantity
                                inbound_item.quantity = 0
                                inbound_item.save()

                                # Create MaterialReport to track the usage
                                MaterialReport.objects.create(
                                    material=product,
                                    quantity=inbound_item.quantity,
                                    order=order,
                                    location=inbound_item.location,
                                    expiration_date=inbound_item.expiration_date,
                                )

                        if remaining_quantity > 0:
                            raise ValueError(f"Not all of the requested quantity for {product.name} could be processed.")

                    # Calculate tax and total amount
                    tax = cart_total * TAX_RATE
                    total_amount = cart_total + SHIPPING_FEES + tax

                    # Update the order with the final amount
                    order.amount = str(total_amount)
                    order.save()

                    # Clear the cart after placing the order
                    cart.clear()

                    # Display success message
                    messages.success(request, 'Your Order Has Been Successfully Created!')

                    # Provide context for the confirmation page
                    context = {
                        'order': order,
                        'cart_total': cart_total,
                        'tax': tax,
                        'shipping_cost': SHIPPING_FEES,
                        'total_amount': total_amount,
                    }
                    return render(request, 'cart/placeorder.html', context)

            except ValueError as e:
                messages.warning(request, str(e))
                return redirect('e_commerce:checkout')

            except Exception as e:
                messages.error(request, "An error occurred while processing your order. Please try again.")
                return redirect('e_commerce:checkout')

        else:
            messages.warning(request, 'Please fill in all required fields.')
            return redirect('e_commerce:checkout')

    # If GET request, render the order page with the necessary context
    context = {
        'tax': TAX_RATE,
        'shipping_cost': SHIPPING_FEES,
    }
    return render(request, 'cart/placeorder.html', context)


def calculate_cart_total(cart_items):
    """Calculate the total value of items in the cart."""
    total = Decimal('0.00')
    for item in cart_items.values():
        total += Decimal(item['price']) * Decimal(item['quantity'])
    return total


def billing(request, pk):
    order = get_object_or_404(Order, pk = pk)
    order_items = OrderItem.objects.filter(order = order)
    context = {
        'order':order,
        'order_items':order_items
    }

    return render(request, 'cart/Billing.html',context)
