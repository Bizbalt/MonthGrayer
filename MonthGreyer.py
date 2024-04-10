import calendar
from datetime import datetime, timedelta, date

'''
import calendar
import datetime
import locale
# for German locale
locale.setlocale(locale.LC_TIME, "de_DE")
'''

'''
An alternative Doodle in which you cross-out on which days you are not available (on default, if you can only on a few
 days "greening" should also be possible ;). At best there will be a calendar where you grey-out if you don't have time.
  Otherwise, they're green. If someone frees a space again it gets orange (As it's a "new" date for all others). There
   is an extra list to see who voted. Depending on which Person and or Group you choose you can only grey out what that
    person is signed up for or only grey out for that Group. There should be an option to write to multiple campaigns
     at the same time, eg. tick multiple groups. When you're done you save the "Greying" with your Name. Automatic push
      when all voted, or if all greyed out would be nice. Month-wise - Month and year can be chosen in the beginning.
       Should also have the possibility to see who grey-ed what with a "correct" function, where you can undo your own
        grey-ing. While greying the changed (also prior changed) days should be marked somehow, and also the only
         possible changeable. 

Maybe let the users vote over this what they prefer. Collect their answer + ip

How do I display the calender via raspy on a website? ask Nialing maybe. Hopefully I only need a bit o java, html and
 css. The Site should just update if somebody looks up the site or enters a new entry. The information could be saved
  file-wise per month on the raspy.

I need a file format: array  for each day: 0-gray, "none"-green, 2 orange. Every days "number" should also have none or the
 respective changer so one can see what he changed only. So I actually need a fourth color 1-dark grey so the person
  which grayed it can see that he can ungray it.
Storing wise the greying of persons should be stored and if not applicable, the greying
 for the "group"-account. Then on load the overall greying should be computed out of those. 

Standard look should be dark, so I better go inspired by the Dracula theme with dark grey background grey boxes. The
 greying makes dark grey, otherwise it's a dimmed green, a dimmed orange :shrug:

the program should notice which day the last day was, everybody has seen, and then check if in the time from now to
 this specific last shared date any dates exist where everybody has time. 
'''


def flash(day):
    # do alert animation on day which cannot be changed
    print("not allowed action")
    pass


# I build a dictionary for storage of all infos
def load_user_dictionary():
    # search for file, if not present create one
    # returning empty dict now just for testing:
    return dict()


def load_user_groups(user):
    # see above
    return dict()


def generate_group_dictionary(group):
    # see above
    # compute group from users
    return dict()


# TODO: Do I want dictionaries for every Person and the group or maybe every group?
#  a good idea rn seems to be users only and a group dic for the interface gets created when needed.
#  Since I also sometimes need groups as combinations of groups for a user who is in multiple - like me :P
#
class MonthGreyer:
    def __init__(self, current_user, day_range=60):
        self.user = current_user
        self.user_groups = load_user_groups(self.user)
        self.all_markings = generate_group_dictionary(self.user_groups)
        self.markings = load_user_dictionary()
        self.today = datetime.today()
        end_date = self.today + timedelta(days=day_range)

        self.days = [self.today + timedelta(days=i) for i in range((self.today - end_date).days)]
        # first_weekday, self.days_in_month = calendar.monthrange(year, month)

    def __str__(self):  # https://docs.python.org/3.8/library/datetime.html#strftime-strptime-behavior
        return date(
            self.today.year, self.today.month, 1).strftime("MonthGreyer for %B of the year %Y for the user "
                                                           ) + self.user

    def grey_day(self, day: datetime.date):
        self.markings[day] = "grayed"

    def free_day(self, day: datetime.date):
        if day in self.markings and self.markings[day] == "grayed":
            self.markings[day] = "freed"
        else:
            flash(day)

    def get_markings(self):
        return self.markings


def date_range(start, end):
    start_date = datetime.strptime(start, '%Y-%m-%d').date()
    end_date = datetime.strptime(end, '%Y-%m-%d').date()
    delta = end_date - start_date
    days = [start_date + timedelta(days=i) for i in range(delta.days + 1)]
    return days