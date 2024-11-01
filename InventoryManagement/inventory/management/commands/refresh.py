# your_app/management/commands/refresh_data.py

from django.core.management.base import BaseCommand
from inventory.models import Stock

class Command(BaseCommand):
    help = 'Refresh data in the database'

    def handle(self, *args, **kwargs):
        # Example: refresh stock availability
        stocks = Stock.objects.all()
        for stock in stocks:
            stock.save()  # or update specific fields as necessary
        self.stdout.write(self.style.SUCCESS('Successfully refreshed data'))