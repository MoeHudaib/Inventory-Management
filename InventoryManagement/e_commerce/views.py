from django.shortcuts import render,redirect,HttpResponse, get_object_or_404
from inventory.models import Contact_us, Color, Category, Stock
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from cart.cart import Cart


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
    cart = Cart(request)
    product = Stock.objects.get(id=id)
    cart.add(product=product)
    return redirect("e_commerce:home")


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
    return render(request, 'cart/cart_details.html')


@login_required(login_url="e_commerce:login")
def Check_out(request):
    if request.method == 'POST':
        pass
    user = request.user
    context = {
        'user':user,
    }
    return render(request, 'cart/checkout.html', context)


@login_required(login_url="e_commerce:login")
def PLACE_ORDER(request):
    if request.method=="POST":
       firstname = request.POST.get('firstname')

    return render(request, 'cart/placeorder.html')