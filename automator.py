import robobrowser
import re
import os

User_Agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'


class FetlifeAutomator(object):
    """Automate publishing and scraping data from fetlife.com"""

    def __init__(self):
        self.br = robobrowser.RoboBrowser(
            history=True, parser='html.parser', user_agent=User_Agent)
        self.br.open('https://fetlife.com/')

        # Set some default values.
        self.country = '14'
        self.state = '160'
        self.location = 'Studio Kink'
        self.address = 'Half way down Caroline lane St Peters 2044 Sydney NSW'

    @property
    def __is_logged_in(self):
        """Check if browser is currently logged in"""
        self.br.open('https://fetlife.com/settings/profile')
        logged_in = self.br.parsed.find(
            string=re.compile("Login to FetLife")) is None

        self.br.back()
        return logged_in

    def log_in(self, username, password):
        # Log in to fetlife.

        if self.__is_logged_in:
            return True, self.br
        else:
            # Go to sign in page.
            self.br.open('https://fetlife.com/users/sign_in')

            # Select the sign in form.
            form = self.br.get_form()

            # Enter the user name and password supplied.
            form['user[login]'] = username
            form['user[password]'] = password
            response = self.br.submit_form(form)
            return self.__is_logged_in, response

    def make_event(self, name, tagline, description, cost, dress_code,
                   s_year, s_month, s_day, s_hour, s_minute,
                   e_year, e_month, e_day, e_hour, e_minute):
        """Assumes fetlife is already logged in"""

        # Go to events.
        self.br.open(
            'https://fetlife.com/events/near_me_in_administrative_area')

        # TODO: Add some error checking code here eg is logged in.

        # Go to create new event.
        self.br.follow_link(link=self.br.get_link(text="Create a New Event"))

        # Select correct form on the new event page.
        form = self.br.get_form(action="/events")

        # Enter event details.

        # Event name.
        form["event[name]"] = name
        # Event tagline.
        form["event[tagline]"] = tagline
        # Event description.
        form["event[description]"] = description
        # Event cost.
        form["event[cost]"] = cost
        # Event dress code.
        form["event[dress_code]"] = dress_code

        # EVENT START DATE/TTME
        # Start year.
        form["event[start_date_time(1i)]"] = str(s_year)
        # Start month as an integer 1 - 12.
        form["event[start_date_time(2i)]"] = str(s_month)
        # Start date as an integer 1 - 31.
        form["event[start_date_time(3i)]"] = str(s_day)
        # Start hour as an integer 01 - 23 (single digit numbers are 0 padded eg 01, 09.
        form["event[start_date_time(4i)]"] = str(s_hour)
        # Start minute as an integer 01 - 59 (single digit numbers are 0 padded eg 01, 09.
        form["event[start_date_time(5i)]"] = str(s_minute)

        # EVENT END DATE/TTME
        # End year.
        form["event[end_date_time(1i)]"] = str(e_year)
        # End month as an integer 1 - 12.
        form["event[end_date_time(2i)]"] = str(e_month)
        # End date as an integer 1 - 31.
        form["event[end_date_time(3i)]"] = str(e_day)
        # End hour as an integer 01 - 23 (single digit numbers are 0 padded eg 01, 09.
        form["event[end_date_time(4i)]"] = str(e_hour)
        # End minute as an integer 01 - 59 (single digit numbers are 0 padded eg 01, 09.
        form["event[end_date_time(5i)]"] = str(e_minute)

        # Name of location.
        form["event[location]"] = self.location

        # Address.
        form["event[address]"] = self.address

        # Set country to Australia.
        form["event[country_id]"] = self.country

        # Sneaky bit to get to state.
        # Submit the form with Australia selected.
        self.br.submit_form(form)

        # On the error page select the administrative area.
        form = self.br.get_form(action="/events")

        # Set to NSW.
        form["event[administrative_area_id]"] = self.state

        # Submit event!!!
        self.br.submit_form(form)

        return self.br.response

    def get_messages(self):
        """Assumes that the automator is already logged in"""

        self.br.open('https://fetlife.com/inbox')
        conversations = self.br.parsed.find_all(
            attrs={"data-conversation": True})
        conversations = list(map(lambda c: c.find(href=re.compile(
            r"\/conversations\/"), class_="silver"), conversations))
        # The conversations list is now a list of tuples of (message: string, conversation_url: string).
        conversations = list(map(lambda c: (c.string, c['href']), conversations))
        return conversations

if __name__ == "__main__":
    automator = FetlifeAutomator()
    automator.log_in(os.environ['FETLIFE_USERNAME'],
                     os.environ['FETLIFE_PASSWORD'])
    automator.make_event('Who knows', '', 'This is a description', 'free', 'N/A',
                         '2019', '1', '1', '07', '00',
                         '2019', '1', '1', '10', '00')
