import random
from .models import Inventory, Stock, InventoryLocation
from django.db import connection
import pandas as pd
import plotly.express as px
import plotly.io as pio

def generate_rgba_colors(n):
    colors = []
    #random.seed(seed)  # Set the seed for reproducibility
    for _ in range(n):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        a = 1  # Fixed alpha value
        color = f'rgba({r}, {g}, {b}, {a})'
        colors.append(color)
    return colors

def prepare_inventory_data():
    inventories = Inventory.objects.all()
    stocks = Stock.objects.all()
    inventory_data = []
    for inventory in inventories:
        rows = []
        for row_num in range(1, inventory.rows_number + 1):
            total_spaces = inventory.columns_number * inventory.layers_number
            reserved_spaces = InventoryLocation.objects.filter(
                inventory=inventory, row=row_num, reserved=True
            ).count()
            
            available_spaces = total_spaces - reserved_spaces
            rows.append({
                'row': row_num,
                'empty_spaces': available_spaces
            })

        inventory_data.append({
            'inventory': inventory,
            'rows': rows,
        })

    return {
        'inventory_data': inventory_data,
        'stocks': stocks,
    }

def fetch_top_stocks():
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM inventory_stock ORDER BY sold_number DESC LIMIT 10;')
        rows = cursor.fetchall()
        # Assuming the columns are known and in the correct order
        columns = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(rows, columns=columns)
    return df

def top_10_stocks_chart():
    stocks = Stock.objects.raw('SELECT * FROM inventory_stock;')  # Fetch all stock items
    data = fetch_top_stocks()  # Fetch the top 10 selling items data
    chart_type = 'bar'

    try:
        # Check if data is not empty and has the necessary columns
        if not data.empty and 'name' in data.columns and 'sold_number' in data.columns:
            if chart_type == 'bar':
                fig = px.bar(
                    data,
                    x='name',  # Column name for the x-axis (item names)
                    y='sold_number',  # Column name for the y-axis (selling numbers)
                    title='Top 10 Selling Items',
                    color='name'  # Optional: Color bars by item names
                )
                
                fig.update_layout(
                    xaxis_title='Item Name',
                    yaxis_title='Selling Number'
                )
                
            # Convert Plotly figure to HTML
            plot_html = pio.to_html(fig, full_html=False)
        else:
            plot_html = None
            context ={
                'error': 'Data is empty or missing necessary columns.',
                'chart_type': chart_type,
                'stocks':stocks,
            }
            return context

    except Exception as e:
        plot_html = None
        context =  {
            'error': f'Error generating plot: {e}',
            'chart_type': chart_type,
            'stocks':stocks,
        }
        return context

    context = {
        'plot_html': plot_html,
        'chart_type': chart_type,
        'stocks':stocks,
    }
    return context

def generate_charts(order_labels, order_data, products):
    # Validate input data
    if len(order_labels) != len(order_data):
        raise ValueError("The length of order_labels must match the length of order_data.")
    
    if not products:
        raise ValueError("The products list cannot be empty.")
    
    # Pie Chart using Plotly Express
    pie_chart = px.pie(
        names=order_labels,
        values=order_data,
        title='Order Requisitions',
        hover_data={'values': order_data},  # Improved hover data for clarity
    )
    pie_chart.update_traces(textinfo='percent+label')
    pie_chart.update_layout(title_x=0.5)

    pie_chart_html = pio.to_html(pie_chart, full_html=False)

    # Bar Chart using Plotly Express
    product_names = [product.name for product in products]
    stocks_availability = [product.stocks_availability for product in products]

    bar_chart = px.bar(
        x=product_names,
        y=stocks_availability,
        title='Product Availability',
        color=stocks_availability,  # Use actual stock values for coloring
        color_continuous_scale='Viridis',
        text=stocks_availability
    )

    bar_chart.update_traces(texttemplate='%{text}', textposition='outside')
    bar_chart.update_layout(
        xaxis_title='Products',  # Improved axis title
        yaxis_title='Stocks Availability',
        plot_bgcolor='rgba(0,0,0,0)',
        title_x=0.5,
        showlegend=False
    )
    
    bar_chart_html = pio.to_html(bar_chart, full_html=False)

    return pie_chart_html, bar_chart_html