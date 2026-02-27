# Datetime Module

The `datetime` module is Python's comprehensive solution for working with dates and times. It provides classes for manipulating dates, times, and time intervals, handling time zones, and formatting datetime objects. Mastering this module is essential for any application that deals with temporal data, from scheduling systems to data analysis.

## Date and Time Objects

The datetime module provides several classes for representing dates and times. Understanding the difference between `date`, `time`, `datetime`, and `timedelta` is crucial for effective time manipulation.

```python
from datetime import date, time, datetime, timedelta

# Date objects (year, month, day)
today = date.today()
print(f"Today: {today}")  # 2024-06-15

birthday = date(1990, 5, 15)
print(f"Birthday: {birthday}")

# Date components
print(f"Year: {today.year}")
print(f"Month: {today.month}")
print(f"Day: {today.day}")
print(f"Weekday: {today.weekday()}")  # 0=Monday, 6=Sunday

# Time objects (hour, minute, second, microsecond)
current_time = datetime.now().time()
print(f"Current time: {current_time}")

meeting_time = time(14, 30, 0)  # 2:30 PM
print(f"Meeting: {meeting_time}")

# Time components
print(f"Hour: {meeting_time.hour}")
print(f"Minute: {meeting_time.minute}")
print(f"Second: {meeting_time.second}")

# Datetime objects (combines date and time)
now = datetime.now()
print(f"Now: {now}")

specific_datetime = datetime(2024, 12, 25, 18, 30, 0)
print(f"Christmas dinner: {specific_datetime}")

# Current UTC time
utc_now = datetime.utcnow()
print(f"UTC now: {utc_now}")
```

| Class | Represents | Example |
|-------|------------|---------|
| `date` | Calendar date | `date(2024, 6, 15)` |
| `time` | Time of day | `time(14, 30, 0)` |
| `datetime` | Date and time | `datetime(2024, 6, 15, 14, 30)` |
| `timedelta` | Duration | `timedelta(days=7)` |

## Time Arithmetic and Timedelta

Timedelta objects represent durations and can be added to or subtracted from datetime objects to perform date arithmetic.

```python
from datetime import datetime, timedelta, date

# Creating timedelta objects
one_day = timedelta(days=1)
one_week = timedelta(weeks=1)
two_hours = timedelta(hours=2)
ninety_minutes = timedelta(minutes=90)

print(f"One week: {one_week}")  # 7 days, 0:00:00
print(f"Ninety minutes: {ninety_minutes}")  # 1:30:00

# Date arithmetic
today = date.today()
tomorrow = today + timedelta(days=1)
yesterday = today - timedelta(days=1)
next_week = today + timedelta(weeks=1)

print(f"Today: {today}")
print(f"Tomorrow: {tomorrow}")
print(f"Next week: {next_week}")

# Datetime arithmetic
now = datetime.now()
in_two_hours = now + timedelta(hours=2)
two_days_ago = now - timedelta(days=2)

print(f"In 2 hours: {in_two_hours}")
print(f"2 days ago: {two_days_ago}")

# Calculate difference between dates
birthday = date(1990, 5, 15)
age_days = today - birthday
age_years = age_days.days // 365

print(f"Age in days: {age_days.days}")
print(f"Age in years: {age_years}")

# Complex timedelta
meeting_start = datetime(2024, 6, 15, 14, 0)
meeting_end = datetime(2024, 6, 15, 16, 30)
duration = meeting_end - meeting_start

print(f"Meeting duration: {duration}")
print(f"Duration in seconds: {duration.total_seconds()}")
print(f"Duration in minutes: {duration.total_seconds() / 60}")

# Combining timedeltas
work_day = timedelta(hours=8)
lunch_break = timedelta(minutes=30)
actual_work = work_day - lunch_break
print(f"Actual work time: {actual_work}")

# Practical example: Project deadline tracker
def days_until_deadline(deadline_date):
    """Calculate days until project deadline."""
    today = date.today()
    remaining = deadline_date - today

    if remaining.days < 0:
        return f"Deadline passed {abs(remaining.days)} days ago"
    elif remaining.days == 0:
        return "Deadline is today!"
    else:
        return f"{remaining.days} days remaining"

deadline = date(2024, 12, 31)
print(f"Project status: {days_until_deadline(deadline)}")
```

## Date and Time Formatting

Python provides powerful string formatting capabilities for datetime objects using the `strftime` and `strptime` methods.

```python
from datetime import datetime

now = datetime.now()

# Common format patterns
print(now.strftime("%Y-%m-%d"))           # 2024-06-15
print(now.strftime("%Y/%m/%d"))           # 2024/06/15
print(now.strftime("%d-%m-%Y"))           # 15-06-2024
print(now.strftime("%B %d, %Y"))          # June 15, 2024
print(now.strftime("%b %d, %Y"))          # Jun 15, 2024
print(now.strftime("%A, %B %d, %Y"))      # Saturday, June 15, 2024

# Time formatting
print(now.strftime("%H:%M:%S"))           # 14:30:45 (24-hour)
print(now.strftime("%I:%M:%S %p"))        # 02:30:45 PM (12-hour)
print(now.strftime("%H:%M"))              # 14:30

# Combined date and time
print(now.strftime("%Y-%m-%d %H:%M:%S"))  # 2024-06-15 14:30:45
print(now.strftime("%c"))                 # Locale's date and time
print(now.strftime("%x"))                 # Locale's date
print(now.strftime("%X"))                 # Locale's time

# ISO format
print(now.isoformat())                    # 2024-06-15T14:30:45.123456

# Custom formats
print(now.strftime("Today is %A"))        # Today is Saturday
print(now.strftime("The time is %I:%M %p"))  # The time is 02:30 PM

# Parsing strings to datetime (strptime)
date_string = "2024-06-15 14:30:00"
parsed = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
print(f"Parsed: {parsed}")

# Various string formats
formats = [
    ("June 15, 2024", "%B %d, %Y"),
    ("15/06/2024", "%d/%m/%Y"),
    ("2024-06-15", "%Y-%m-%d"),
    ("06-15-2024 2:30 PM", "%m-%d-%Y %I:%M %p")
]

for date_str, format_str in formats:
    parsed = datetime.strptime(date_str, format_str)
    print(f"{date_str} -> {parsed}")
```

| Format Code | Meaning | Example |
|-------------|---------|---------|
| `%Y` | Year (4 digits) | 2024 |
| `%m` | Month (01-12) | 06 |
| `%d` | Day (01-31) | 15 |
| `%H` | Hour 24-hour (00-23) | 14 |
| `%I` | Hour 12-hour (01-12) | 02 |
| `%M` | Minute (00-59) | 30 |
| `%S` | Second (00-59) | 45 |
| `%p` | AM/PM | PM |
| `%A` | Weekday full name | Saturday |
| `%B` | Month full name | June |

## Working with Weekdays and Calendars

The datetime module provides methods for working with weekdays, calculating business days, and navigating calendars.

```python
from datetime import datetime, timedelta, date
import calendar

# Weekday operations
today = date.today()
weekday = today.weekday()  # 0=Monday, 6=Sunday
iso_weekday = today.isoweekday()  # 1=Monday, 7=Sunday

weekday_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday',
                 'Friday', 'Saturday', 'Sunday']
print(f"Today is {weekday_names[weekday]}")

# Check if weekend
def is_weekend(date_obj):
    return date_obj.weekday() >= 5

print(f"Is weekend: {is_weekend(today)}")

# Find next specific weekday
def next_weekday(target_day):
    """Find next occurrence of target weekday (0=Monday)."""
    today = date.today()
    days_ahead = target_day - today.weekday()
    if days_ahead <= 0:
        days_ahead += 7
    return today + timedelta(days=days_ahead)

next_friday = next_weekday(4)  # 4 = Friday
print(f"Next Friday: {next_friday}")

# Calculate business days
def add_business_days(start_date, days):
    """Add business days (excluding weekends)."""
    current = start_date
    added = 0

    while added < days:
        current += timedelta(days=1)
        if current.weekday() < 5:  # Monday to Friday
            added += 1

    return current

start = date(2024, 6, 14)  # Friday
result = add_business_days(start, 3)
print(f"3 business days after Friday: {result}")  # Wednesday

# Calendar operations
year = 2024
month = 6

# Check if leap year
print(f"2024 is leap year: {calendar.isleap(2024)}")

# Days in month
days_in_june = calendar.monthrange(year, month)[1]
print(f"Days in June 2024: {days_in_june}")

# First weekday of month (0=Monday)
first_weekday = calendar.monthrange(year, month)[0]
print(f"June 2024 starts on: {weekday_names[first_weekday]}")

# Print calendar
print("\nJune 2024 Calendar:")
print(calendar.month(year, month))

# Find all Fridays in a month
def get_all_weekday_dates(year, month, weekday):
    """Get all dates for a specific weekday in a month."""
    first_day = date(year, month, 1)
    last_day = date(year, month, calendar.monthrange(year, month)[1])

    dates = []
    current = first_day

    # Find first occurrence
    while current.weekday() != weekday:
        current += timedelta(days=1)

    # Collect all occurrences
    while current <= last_day:
        dates.append(current)
        current += timedelta(weeks=1)

    return dates

fridays = get_all_weekday_dates(2024, 6, 4)
print(f"\nAll Fridays in June 2024:")
for friday in fridays:
    print(f"  {friday.strftime('%B %d, %Y')}")
```

## Real-World Applications

Datetime operations are essential for building scheduling systems, analyzing time-series data, and managing time-sensitive operations.

```python
from datetime import datetime, timedelta, date, time
import calendar

# 1. Age Calculator
def calculate_age(birth_date):
    """Calculate exact age in years, months, and days."""
    today = date.today()

    years = today.year - birth_date.year
    months = today.month - birth_date.month
    days = today.day - birth_date.day

    if days < 0:
        months -= 1
        # Days in previous month
        prev_month = today.month - 1 if today.month > 1 else 12
        prev_year = today.year if today.month > 1 else today.year - 1
        days += calendar.monthrange(prev_year, prev_month)[1]

    if months < 0:
        years -= 1
        months += 12

    return years, months, days

birth = date(1990, 3, 15)
years, months, days = calculate_age(birth)
print(f"Age: {years} years, {months} months, {days} days")

# 2. Meeting Scheduler
class MeetingScheduler:
    """Schedule meetings with conflict detection."""

    def __init__(self):
        self.meetings = []

    def add_meeting(self, title, start, duration_minutes):
        """Add a meeting if no conflicts."""
        end = start + timedelta(minutes=duration_minutes)

        # Check for conflicts
        for meeting in self.meetings:
            if self._conflicts(start, end, meeting['start'], meeting['end']):
                return False, f"Conflicts with: {meeting['title']}"

        self.meetings.append({
            'title': title,
            'start': start,
            'end': end
        })
        return True, "Meeting scheduled"

    def _conflicts(self, start1, end1, start2, end2):
        """Check if two time ranges conflict."""
        return start1 < end2 and start2 < end1

    def get_schedule(self, day):
        """Get all meetings for a specific day."""
        day_meetings = [m for m in self.meetings
                       if m['start'].date() == day]
        return sorted(day_meetings, key=lambda x: x['start'])

scheduler = MeetingScheduler()
base_date = datetime(2024, 6, 15, 9, 0)

scheduler.add_meeting("Team Standup", base_date, 30)
scheduler.add_meeting("Client Call", base_date + timedelta(hours=2), 60)
success, msg = scheduler.add_meeting("Conflict Test", base_date, 45)

print(f"\nScheduler: {msg}")
print("\nToday's schedule:")
for meeting in scheduler.get_schedule(date(2024, 6, 15)):
    print(f"{meeting['start'].strftime('%I:%M %p')} - {meeting['title']}")

# 3. Time Zone Aware Applications
from datetime import timezone

def get_time_until_event(event_datetime):
    """Calculate time remaining until event."""
    now = datetime.now()
    remaining = event_datetime - now

    if remaining.total_seconds() < 0:
        return "Event has passed"

    days = remaining.days
    hours = remaining.seconds // 3600
    minutes = (remaining.seconds % 3600) // 60

    return f"{days}d {hours}h {minutes}m"

event = datetime(2024, 12, 25, 0, 0, 0)
print(f"\nTime until Christmas: {get_time_until_event(event)}")

# 4. Work Hours Tracker
class WorkTracker:
    """Track work hours and overtime."""

    def __init__(self, standard_hours=8):
        self.standard_hours = standard_hours
        self.time_logs = []

    def clock_in(self, timestamp):
        """Record clock in time."""
        self.time_logs.append({'in': timestamp, 'out': None})

    def clock_out(self, timestamp):
        """Record clock out time."""
        if self.time_logs and self.time_logs[-1]['out'] is None:
            self.time_logs[-1]['out'] = timestamp

    def get_daily_hours(self, day):
        """Calculate hours worked on a specific day."""
        total = timedelta()

        for log in self.time_logs:
            if log['in'].date() == day and log['out']:
                total += log['out'] - log['in']

        return total.total_seconds() / 3600

    def get_overtime(self, day):
        """Calculate overtime hours."""
        hours = self.get_daily_hours(day)
        overtime = max(0, hours - self.standard_hours)
        return overtime

tracker = WorkTracker()
work_day = date(2024, 6, 15)

tracker.clock_in(datetime(2024, 6, 15, 8, 30))
tracker.clock_out(datetime(2024, 6, 15, 17, 45))

hours = tracker.get_daily_hours(work_day)
overtime = tracker.get_overtime(work_day)

print(f"\nHours worked: {hours:.2f}")
print(f"Overtime: {overtime:.2f}")
```

---

## Exercises

<!-- EXERCISE_START -->
```yaml
exercises:
  - title: "Date Arithmetic"
    difficulty: basic
    description: "Calculate your age in days and determine what day of the week you were born."
    starter_code: |
      from datetime import date

      # Your birthday
      birthday = date(1995, 7, 20)
      today = date.today()

      # Calculate age in days
      age_in_days =

      # Get day of week (0=Monday, 6=Sunday)
      day_of_week =
      days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

      print(f"You are {age_in_days} days old")
      print(f"You were born on a {days[day_of_week]}")
    expected_output: |
      You are 10565 days old
      You were born on a Thursday
    hints:
      - "Subtract dates to get timedelta, then use .days"
      - "Use .weekday() method to get day of week"
    solution: |
      from datetime import date

      # Your birthday
      birthday = date(1995, 7, 20)
      today = date.today()

      # Calculate age in days
      age_in_days = (today - birthday).days

      # Get day of week (0=Monday, 6=Sunday)
      day_of_week = birthday.weekday()
      days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

      print(f"You are {age_in_days} days old")
      print(f"You were born on a {days[day_of_week]}")

  - title: "Date Formatting"
    difficulty: basic
    description: "Format a datetime object in multiple ways including ISO format, US format, and European format."
    starter_code: |
      from datetime import datetime

      dt = datetime(2024, 6, 15, 14, 30, 45)

      # Format in different ways
      iso_format =
      us_format =
      european_format =
      full_text =

      print(f"ISO: {iso_format}")
      print(f"US: {us_format}")
      print(f"European: {european_format}")
      print(f"Full: {full_text}")
    expected_output: |
      ISO: 2024-06-15T14:30:45
      US: 06/15/2024 02:30 PM
      European: 15/06/2024 14:30
      Full: Saturday, June 15, 2024
    hints:
      - "Use .isoformat() for ISO format"
      - "Use strftime() with format codes"
      - "US: %m/%d/%Y %I:%M %p"
      - "European: %d/%m/%Y %H:%M"
      - "Full: %A, %B %d, %Y"
    solution: |
      from datetime import datetime

      dt = datetime(2024, 6, 15, 14, 30, 45)

      # Format in different ways
      iso_format = dt.isoformat()
      us_format = dt.strftime("%m/%d/%Y %I:%M %p")
      european_format = dt.strftime("%d/%m/%Y %H:%M")
      full_text = dt.strftime("%A, %B %d, %Y")

      print(f"ISO: {iso_format}")
      print(f"US: {us_format}")
      print(f"European: {european_format}")
      print(f"Full: {full_text}")

  - title: "Time Duration Calculator"
    difficulty: intermediate
    description: "Calculate the duration between two datetime objects and express it in hours and minutes."
    starter_code: |
      from datetime import datetime

      start = datetime(2024, 6, 15, 9, 30, 0)
      end = datetime(2024, 6, 15, 17, 45, 0)

      # Calculate duration
      duration =

      # Convert to hours and minutes
      total_seconds =
      hours =
      minutes =

      print(f"Start: {start.strftime('%I:%M %p')}")
      print(f"End: {end.strftime('%I:%M %p')}")
      print(f"Duration: {hours} hours and {minutes} minutes")
    expected_output: |
      Start: 09:30 AM
      End: 05:45 PM
      Duration: 8 hours and 15 minutes
    hints:
      - "Subtract datetime objects to get timedelta"
      - "Use .total_seconds() to get duration in seconds"
      - "Hours = total_seconds // 3600"
      - "Minutes = (total_seconds % 3600) // 60"
    solution: |
      from datetime import datetime

      start = datetime(2024, 6, 15, 9, 30, 0)
      end = datetime(2024, 6, 15, 17, 45, 0)

      # Calculate duration
      duration = end - start

      # Convert to hours and minutes
      total_seconds = duration.total_seconds()
      hours = int(total_seconds // 3600)
      minutes = int((total_seconds % 3600) // 60)

      print(f"Start: {start.strftime('%I:%M %p')}")
      print(f"End: {end.strftime('%I:%M %p')}")
      print(f"Duration: {hours} hours and {minutes} minutes")

  - title: "Deadline Reminder"
    difficulty: intermediate
    description: "Create a function that takes a deadline and returns a status message with urgency level based on time remaining."
    starter_code: |
      from datetime import datetime, timedelta

      def deadline_status(deadline):
          """Return status message based on time until deadline."""
          now = datetime.now()
          remaining = deadline - now

          if remaining.total_seconds() < 0:

          elif remaining.days == 0:

          elif remaining.days <= 3:

          elif remaining.days <= 7:

          else:


      # Test cases
      now = datetime.now()
      deadlines = [
          ("Overdue", now - timedelta(days=1)),
          ("Today", now + timedelta(hours=5)),
          ("Soon", now + timedelta(days=2)),
          ("This week", now + timedelta(days=5)),
          ("Future", now + timedelta(days=15))
      ]

      for name, deadline in deadlines:
          print(f"{name}: {deadline_status(deadline)}")
    expected_output: |
      Overdue: ⚠️ OVERDUE by 1 days!
      Today: 🔴 URGENT: Due today!
      Soon: 🟡 WARNING: 2 days remaining
      This week: 🟢 NOTICE: 5 days remaining
      Future: ✅ OK: 15 days remaining
    hints:
      - "Check if remaining.total_seconds() < 0 for overdue"
      - "Use remaining.days to determine urgency"
      - "Return different messages based on days remaining"
    solution: |
      from datetime import datetime, timedelta

      def deadline_status(deadline):
          """Return status message based on time until deadline."""
          now = datetime.now()
          remaining = deadline - now

          if remaining.total_seconds() < 0:
              return f"⚠️ OVERDUE by {abs(remaining.days)} days!"
          elif remaining.days == 0:
              return "🔴 URGENT: Due today!"
          elif remaining.days <= 3:
              return f"🟡 WARNING: {remaining.days} days remaining"
          elif remaining.days <= 7:
              return f"🟢 NOTICE: {remaining.days} days remaining"
          else:
              return f"✅ OK: {remaining.days} days remaining"

      # Test cases
      now = datetime.now()
      deadlines = [
          ("Overdue", now - timedelta(days=1)),
          ("Today", now + timedelta(hours=5)),
          ("Soon", now + timedelta(days=2)),
          ("This week", now + timedelta(days=5)),
          ("Future", now + timedelta(days=15))
      ]

      for name, deadline in deadlines:
          print(f"{name}: {deadline_status(deadline)}")

  - title: "Business Days Calculator"
    difficulty: advanced
    description: "Implement a function that calculates the number of business days (Monday-Friday) between two dates."
    starter_code: |
      from datetime import date, timedelta

      def count_business_days(start_date, end_date):
          """Count business days between two dates (inclusive)."""
          if start_date > end_date:
              start_date, end_date = end_date, start_date

          business_days = 0
          current = start_date

          while current <= end_date:
              # Check if it's a weekday (Monday=0 to Friday=4)


              current += timedelta(days=1)

          return business_days

      start = date(2024, 6, 10)  # Monday
      end = date(2024, 6, 21)    # Friday

      days = count_business_days(start, end)
      total_days = (end - start).days + 1

      print(f"Period: {start} to {end}")
      print(f"Total days: {total_days}")
      print(f"Business days: {days}")
      print(f"Weekend days: {total_days - days}")
    expected_output: |
      Period: 2024-06-10 to 2024-06-21
      Total days: 12
      Business days: 10
      Weekend days: 2
    hints:
      - "Use weekday() method: 0-4 is Monday-Friday"
      - "Loop through each day from start to end"
      - "Increment counter if weekday < 5"
    solution: |
      from datetime import date, timedelta

      def count_business_days(start_date, end_date):
          """Count business days between two dates (inclusive)."""
          if start_date > end_date:
              start_date, end_date = end_date, start_date

          business_days = 0
          current = start_date

          while current <= end_date:
              # Check if it's a weekday (Monday=0 to Friday=4)
              if current.weekday() < 5:
                  business_days += 1

              current += timedelta(days=1)

          return business_days

      start = date(2024, 6, 10)  # Monday
      end = date(2024, 6, 21)    # Friday

      days = count_business_days(start, end)
      total_days = (end - start).days + 1

      print(f"Period: {start} to {end}")
      print(f"Total days: {total_days}")
      print(f"Business days: {days}")
      print(f"Weekend days: {total_days - days}")

  - title: "Recurring Event Generator"
    difficulty: advanced
    description: "Create a function that generates dates for recurring events (e.g., every Monday for 8 weeks, or 1st of every month for 6 months)."
    starter_code: |
      from datetime import date, timedelta
      import calendar

      def generate_weekly_events(start_date, weekday, num_occurrences):
          """Generate dates for weekly recurring events.

          weekday: 0=Monday, 6=Sunday
          """
          events = []
          current = start_date

          # Find first occurrence of the weekday


          # Generate subsequent occurrences


          return events

      def generate_monthly_events(start_date, day_of_month, num_months):
          """Generate dates for monthly recurring events on specific day."""
          events = []

          for i in range(num_months):
              # Calculate year and month


              # Get number of days in that month


              # Use the lesser of day_of_month and days_in_month


              events.append(event_date)

          return events

      # Test weekly events (every Monday for 4 weeks)
      start = date(2024, 6, 15)
      mondays = generate_weekly_events(start, 0, 4)

      print("Every Monday for 4 weeks:")
      for event in mondays:
          print(f"  {event.strftime('%A, %B %d, %Y')}")

      # Test monthly events (15th of each month for 3 months)
      start = date(2024, 6, 1)
      monthly = generate_monthly_events(start, 15, 3)

      print("\n15th of each month for 3 months:")
      for event in monthly:
          print(f"  {event.strftime('%B %d, %Y')}")
    expected_output: |
      Every Monday for 4 weeks:
        Monday, June 17, 2024
        Monday, June 24, 2024
        Monday, July 01, 2024
        Monday, July 08, 2024

      15th of each month for 3 months:
        June 15, 2024
        July 15, 2024
        August 15, 2024
    hints:
      - "For weekly: find first occurrence of target weekday"
      - "Then add 7 days repeatedly"
      - "For monthly: calculate target month = start_month + i"
      - "Handle year rollover: year = start_year + (target_month - 1) // 12"
      - "Use calendar.monthrange() to get days in month"
    solution: |
      from datetime import date, timedelta
      import calendar

      def generate_weekly_events(start_date, weekday, num_occurrences):
          """Generate dates for weekly recurring events.

          weekday: 0=Monday, 6=Sunday
          """
          events = []
          current = start_date

          # Find first occurrence of the weekday
          days_ahead = weekday - current.weekday()
          if days_ahead < 0:
              days_ahead += 7
          current = current + timedelta(days=days_ahead)

          # Generate subsequent occurrences
          for _ in range(num_occurrences):
              events.append(current)
              current = current + timedelta(weeks=1)

          return events

      def generate_monthly_events(start_date, day_of_month, num_months):
          """Generate dates for monthly recurring events on specific day."""
          events = []

          for i in range(num_months):
              # Calculate year and month
              target_month = start_date.month + i
              year = start_date.year + (target_month - 1) // 12
              month = ((target_month - 1) % 12) + 1

              # Get number of days in that month
              days_in_month = calendar.monthrange(year, month)[1]

              # Use the lesser of day_of_month and days_in_month
              day = min(day_of_month, days_in_month)
              event_date = date(year, month, day)

              events.append(event_date)

          return events

      # Test weekly events (every Monday for 4 weeks)
      start = date(2024, 6, 15)
      mondays = generate_weekly_events(start, 0, 4)

      print("Every Monday for 4 weeks:")
      for event in mondays:
          print(f"  {event.strftime('%A, %B %d, %Y')}")

      # Test monthly events (15th of each month for 3 months)
      start = date(2024, 6, 1)
      monthly = generate_monthly_events(start, 15, 3)

      print("\n15th of each month for 3 months:")
      for event in monthly:
          print(f"  {event.strftime('%B %d, %Y')}")
```
<!-- EXERCISE_END -->
