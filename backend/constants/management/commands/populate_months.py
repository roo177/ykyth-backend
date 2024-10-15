from django.core.management.base import BaseCommand
from constants.models import Month
from datetime import datetime
import calendar

class Command(BaseCommand):
    help = 'Populate the Month table from 2022-12-01 to 2028-12-01'

    def handle(self, *args, **kwargs):
        start_date = datetime(2022, 12, 1)
        end_date = datetime(2028, 12, 1)
        current_date = start_date

        while current_date <= end_date:
            Month.objects.create(
                month=current_date.date(),
                month_no=current_date.month,
                year_no=current_date.year
            )

            # Move to the first day of the next month
            if current_date.month == 12:
                current_date = datetime(current_date.year + 1, 1, 1)
            else:
                current_date = datetime(current_date.year, current_date.month + 1, 1)

        self.stdout.write(self.style.SUCCESS('Successfully populated the Month table'))
