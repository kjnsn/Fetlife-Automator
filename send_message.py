import os

from automator import FetlifeAutomator

if __name__ == "__main__":
    automator = FetlifeAutomator()
    automator.log_in(os.environ['FETLIFE_USERNAME'],
                     os.environ['FETLIFE_PASSWORD'])
    print(automator.get_messages())
