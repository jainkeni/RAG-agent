# src/hr_specific/holiday_calendar.py
import csv
from datetime import datetime

class HolidayCalendar:
    def __init__(self, csv_path="data/employee_data/holidays.csv"):
        self.csv_path = csv_path
        self.holidays = self.load_holidays()
    
    def load_holidays(self):
        """Load holidays from CSV"""
        holidays = []
        try:
            with open(self.csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    holidays.append({
                        'date': datetime.strptime(row['date'], '%Y-%m-%d'),
                        'name': row['name'],
                        'type': row.get('type', 'national')
                    })
        except FileNotFoundError:
            print(f"⚠️  Holidays file not found: {self.csv_path}")
        except Exception as e:
            print(f"❌ Error loading holidays: {e}")
        return holidays
    
    def is_holiday(self, date):
        """Check if a date is a holiday"""
        for holiday in self.holidays:
            if holiday['date'].date() == date.date():
                return True
        return False
    
    def get_holidays_in_range(self, from_date, to_date):
        """Get all holidays between two dates"""
        return [h for h in self.holidays if from_date <= h['date'] <= to_date]
    
    def get_all_holidays(self):
        """Get all holidays"""
        return self.holidays