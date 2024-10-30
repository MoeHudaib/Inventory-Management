from django.shortcuts import render, HttpResponse,get_object_or_404, redirect
from django.contrib import messages
from inventory.models import Stock
from django.contrib.auth.decorators import login_required
import json, sys
from datetime import date, datetime
from sales.models import Sale, SaleItem, MaterialReport
from .models import Outbound, OutboundItem
from django.utils import timezone
from .utils import process_outbound,process_inbound 
from django.http import JsonResponse
# To Do List 
# Work On the Inbound First, To determine a specific quantity for each product 
# Then recover The reporting system we had in the previous project is_expiring_soon, Low_in_stock
# Work On the outbound and link it to the sales
#  29/10/2024 Almost Done 

@login_required
def pos(request):
    products = Stock.objects.filter(active = True)
    product_json = []
    for product in products:
        product_json.append({'id':product.id, 'name':product.name, 'price':float(product.unit_cost)})
    context = {
        'page_title' : "Point of Sale",
        'products' : products,
        'product_json' : json.dumps(product_json)
    }
    # return HttpResponse('')
    return render(request, 'pos/pos.html',context)

@login_required
def checkout_modal(request):
    grand_total = 0
    if 'grand_total' in request.GET:
        grand_total = request.GET['grand_total']
    context = {
        'grand_total' : grand_total,
    }
    return render(request, 'pos/checkout.html',context)

@login_required
def save_pos(request):
    resp = {'status': 'failed', 'msg': ''}
    data = request.POST

    # Debug: Log incoming data
    print("Incoming POST data:", data)

    # Generate unique sale code based on the current year
    pref = datetime.now().year * 10000  # Ensure unique prefix
    sale_code = generate_unique_code(Sale, pref)
    out_code = generate_unique_code(Outbound, pref)

    try:
        # Loop through products and save SaleItems
        for i, product_id in enumerate(data.getlist('product_id[]')):
            qty = int(data.getlist('qty[]')[i])  # Convert quantity to int
            price = float(data.getlist('price[]')[i])  # Convert price to float
            total = qty * price

            product = Stock.objects.filter(id=product_id).first()
            if product:  # Ensure product exists

                # Process outbound
                var = process_outbound(product, qty)
                if 'quantity cannot be processed' == var:
                    messages.warning(request, var)
                elif 'Null values are passed, track your process!' == var:
                    messages.warning(request, var)
                elif "Outbound processing completed successfully." == var:
                    # Create Sale instance
                    sales = Sale(
                        code=sale_code,
                        sub_total=float(data['sub_total']),
                        tax=float(data['tax']),
                        tax_amount=float(data['tax_amount']),
                        grand_total=float(data['grand_total']),
                    )
                    sales.save()

                    # Create Outbound instance
                    outbound = Outbound(
                        code=out_code,
                        responsible_staff=request.user,
                        sale=sales,
                    )
                    outbound.save()
                    SaleItem.objects.create(
                    sale=sales,
                    item=product,
                    qty=qty,
                    price=price,
                    total=total
                    )
                    OutboundItem.objects.create(
                        material=product,
                        outbound=outbound,
                        quantity=qty,
                        total_price=total,
                        sold_date=timezone.now()
                    )
                    product.save()

            else:
                var = f"Product with id {product_id} not found."
                print(var)
                messages.warning(request, var)

        resp['status'] = 'success'
        resp['sale_id'] = sales.pk  # Use the primary key from the created instance
        messages.success(request, "Sale Record has been saved.")


    except Exception as e:
        resp['msg'] = "An error occurred: " # when quantity > availability 
        print("Unexpected error:", e)
        messages.error(request, resp['msg'])

    return JsonResponse(resp)

def generate_unique_code(model, prefix):
    """ Generate a unique code for the given model based on a prefix. """
    i = 1
    while True:
        code = '{:0>5}'.format(i)
        check = model.objects.filter(code=f"{prefix}{code}").exists()
        if not check:
            return f"{prefix}{code}"
        i += 1


def inbound(request):
    if request.method == 'POST':
        product_ids = request.POST.getlist('product_id[]')
        quantities = request.POST.getlist('qty[]')
        expiration_dates = request.POST.getlist('expiry[]')
        source = request.POST.get('source')
        products = []  # List to hold product details for processing

        for product_id, qty, expiry in zip(product_ids, quantities, expiration_dates):
            products.append((product_id, qty, expiry))
        
        # Call the process_inbound function
        result_message = process_inbound(request.user, products, source)
        messages.success(request, result_message)
        # After processing, render a new context with messages
        return redirect('inventory:product')

    else:
        # On GET request, prepare the product list
        products = Stock.objects.filter(active=True)
        product_json = [{'id': product.id, 'name': product.name} for product in products]
        context = {
            'page_title': "Inbound",
            'products': products,
            'product_json': json.dumps(product_json)
        }
    
    return render(request, 'pos/inbound.html', context)

