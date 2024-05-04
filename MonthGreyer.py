import calendar
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
import locale
# for German locale
locale.setlocale(locale.LC_TIME, "de_DE.utf8")
import json

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

Maybe let the users vote over this what they prefer. Collect their answer + ~~ip~~ name.

I need a file format: array  for each day: 0-grey, "none"-green, 2 orange. Every days "number" should also have none or 
 the respective changer so one can see what he changed only. So I actually need a fourth color 1-light_grey so the
  person which greyed it can see that he can ungrey it.
Storing wise the greying of persons should be stored and if not applicable, the greying
 for the "group"-account. Then on load the overall greying should be computed out of those. 

Standard look should be dark, so I better go inspired by the Dracula theme with dark grey background grey boxes. The
 greying makes dark grey, otherwise it's a dimmed green, a dimmed orange :shrug:

the program should notice which day the last day was, everybody has seen, and then check if in the time from now to
 this specific last shared date any dates exist where everybody has time. 
 
The automatic storage of votes on blur/close of the Tab should be done in the REST architectural style like adviced by 
 Minutenreis.
Alike the transfer of data from front-end to back-end and vice versa should be in the same fashion and flexible:
    Only an arbitrary length (month-wise (e.g. 30, 61, 91, ...)) of dates is sent, the starting point is always current times month. 
    An initial safety check would be that the expected lengths are the same - once at the start (at client side only and per every blur/reload) 
        (which would raise errors when the local time on one machine is different, the user reloaded an old instance
         from cache from the day before or over midnight 23:59:59 -> 00:00:00)     
'''

STATE_description = {"free": "green - day has not not been voted to be blocked",
                     "freed": "orange - day was blocked and then freed by same user after a time",
                     "blocked": "grey - day has been voted to be blocked",
                     "self_blocked": "light_greyed - day has been voted to be blocked by the user himself",
                     "past": "colorless - day lies in the past and is not of interest anymore"}


def date_range(start, end):
    start_date = datetime.strptime(start, '%Y-%m-%d').date()
    end_date = datetime.strptime(end, '%Y-%m-%d').date()
    delta = end_date - start_date
    days = [start_date + timedelta(days=i) for i in range(delta.days + 1)]
    return days


# Build a dictionary for storage of all infos user-wise and group-wise
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
    def __init__(self, current_user, month_range=2):
        # ToDo: add user to group as seen (today.month + m_range)
        self.user = current_user
        self.user_groups = load_user_groups(self.user)
        self.all_markings = generate_group_dictionary(self.user_groups)
        self.today = datetime.today().date()

        # compute the days of the month in range
        months = [self.today + relativedelta(months=mon) for mon in range(month_range + 1)]
        dates = []
        for month in months:
            num_days = calendar.monthrange(month.year, month.month)[1]
            dates += [date(month.year, month.month, day) for day in range(1, num_days + 1)]
        # compute the past days
        self.current_dates = dates
        self.past_dates = [day for day in dates if day < self.today]
        # compute the future days
        self.future_dates = [day for day in dates if day > self.today]

        self.markings = self.load_user_markings()

    def __str__(self):  # https://docs.python.org/3.8/library/datetime.html#strftime-strptime-behavior
        return date(
            self.today.year, self.today.month, 1).strftime("MonthGreyer for %B of the year %Y for the user "
                                                           ) + self.user

    def grey_day(self, distance: int):  # distance from the first day of the month
        if self.markings[distance] == "freed" or self.markings[distance] == "free":
            self.markings[distance] = "self_blocked"
            self.save_user_markings()
            return True
        else:
            raise ValueError("Day already blocked")

    def free_day(self, distance: int):  # distance from the first day of the month
        if self.markings[distance] == "self_blocked":
            self.markings[distance] = "freed"
            self.save_user_markings()
            return True
        else:
            raise ValueError("Day cannot be freed (again)")

    def de_grey_day(self, distance: int):  # distance from the first day of the month
        if self.markings[distance] == "self_blocked":
            self.markings[distance] = "free"
            self.save_user_markings()
            return True
        else:
            raise ValueError("Day cannot be freed (again)")

    def save_user_markings(self):
        markings_dict = {str(self.current_dates[i]): self.markings[i] for i in range(len(self.current_dates))}
        with open("data/" + self.user + ".json", "w") as file:
            json.dump(markings_dict, file, indent=1)

    def load_user_markings(self):
        try:
            with open("data/" + self.user + ".json", "r") as file:
                markings = json.load(file)
        except (json.JSONDecodeError,FileNotFoundError):
            raise FileNotFoundError("No markings found for user " + self.user)
        # decode the marking to an array
        current_user_markings = len(self.past_dates) * ["past"]
        for day in [self.today] + self.future_dates:
            current_user_markings.append(markings[str(day)] if str(day) in markings else "free")
        return current_user_markings

    def get_choice_markings(self):  # ToDo: Compute the combined markings for all groups of the user.
        return self.markings

