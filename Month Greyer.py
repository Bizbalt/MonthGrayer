import calendar
import datetime
import numpy as np


''' 
an alternative Doodle in which you only cross-out on which days you are not available. 
    At best there will be a calendar where you grey-out if you don't have time. Otherwise, they're green. If someone
     frees a space again it gets orange. There is an extra list to see who voted. Depending on which ~~Person~~ Campaign
      you choose you can only grey out for that Campaign. There should be an option to write to multiple campaigns at
       the same time. When you're done you Save the "Greying" with your Name. Automatic push when all voted, or if all
        greyed out would be nice. Month-wise - Month and year can be chosen in the beginning. Should also have the
         possibility to see who grey-ed what with a "correct" function, where you can undo your own grey-ing. While
          greying the changed (also prior changed) days should be marked somehow, and also the only possible changeable.

How do I display the calender via raspy on a website? ask Nialing maybe. Hopefully I only need a bit o java, html and
 css. The Site should just update if somebody looks up the site or enters a new entry. The information could be saved
  file-wise per month on the raspy.

I need a file format: array  for each day: 0-gray, 1-green, 2 orange. Every days "number" should also have none or the
 respective changer so one can see what he changed only.

Standard look should be dark, so I better go inspired by the Dracula theme with dark grey background grey boxes. The
 greying makes dark grey, otherwise it's a dimmed green, a dimmed orange :shrug:
'''


def flash(day):
    # do alert animation on day which cannot be changed
    print("not allowed action")
    pass


class MonthGreyer:
    def __init__(self, year, month, current_user, grey_arr=None):
        self.year = year
        self.month = month
        self.user = current_user
        # creating the array of dates of days
        first_weekday, self.days_in_month = calendar.monthrange(year, month)
        self.days = [datetime.date(year, month, day + 1) for day in range(self.days_in_month)]

        if grey_arr:
            self.grey_arr = grey_arr
        else:  # if the class is completely new, the days are all set green
            self.grey_arr = np.array([[1, None]*self.days_in_month])

    def __str__(self):  # https://docs.python.org/3.8/library/datetime.html#strftime-strptime-behavior
        return datetime.date(
            self.year, self.month, 1).strftime("MonthGreyer for %B of the year %Y for the user "
                                               ) + self.user

    def grey_day(self, day: int):
        self.grey_arr[day-1] = 0, self.user

    def free_day(self, day: int):
        if self.grey_arr[day-1, 1] == self.user:
            self.grey_arr[day-1] = 2, None
        else:
            flash(day-1)

    def get_month_days_color(self):
        return self.grey_arr[:, 0]


# testing:
my_month = MonthGreyer(2022, 12, "Nex")
print(my_month)
# this is a comment
my_month.grey_day(1)
my_month.grey_day(3)
my_month.free_day(1)
my_month.free_day(2)
print(my_month.grey_arr)
