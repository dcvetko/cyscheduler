#!/usr/bin/python3

import json
import argparse
import datetime
from datetime import timedelta
from urllib.request import Request
from urllib.request import urlopen

##########################################################################

class PollData:
    def __init__(self, title, weekdayoptions, weekendoptions, answers=[], multi=True, dupcheck="permissive", captcha=False):
        self.title        = title
        self.weekdayoptions = weekdayoptions
        self.weekendoptions = weekendoptions 
        self.answers      = answers
        self.multi        = multi
        self.dupcheck     = dupcheck
        self.captcha      = captcha

    def add_answer(self, answer):
        self.answers.append(answer)

    def add_daily_answers(self, date_from, repeat):
        date = date_from
        for i in range(0, repeat):
            self.add_options_for_day(date)
            date += timedelta(days=1)

    # Friday, Saturday, Sunday
    def add_weekend_only_answers(self, date_from, repeat):
        date = date_from
        for i in range(0, repeat):
            while date.weekday() < 4:
                date += timedelta(days=1)

            self.add_options_for_day(date)
            date += timedelta(days=1)

    def add_options_for_day(self, date):
        if date.weekday() < 5:
            for weekdayoption in self.weekdayoptions:
                self.add_answer(self.create_answer_string(date, weekdayoption))
        else:
            for weekendoption in self.weekendoptions:
                self.add_answer(self.create_answer_string(date, weekendoption))

    def create_answer_string(self, date, optionstr):
        return date.strftime("%Y-%m-%d (%A)") + " | " + optionstr

    def get_json_representation(self):
        obj = {}
        obj["title"]       = self.title
        obj["options"]     = self.answers
        obj["multi"]       = self.multi
        obj["dupcheck"]    = self.dupcheck
        obj["captcha"]     = self.captcha

        return obj

##########################################################################

class StrawPollCreator:
    def __init__(self):
        self.strawpoll_url    = "https://www.strawpoll.me/api/v2/polls"
        self.created_poll_url = "https://www.strawpoll.me/"

    def create_poll(self, poll_data):
        custom_header = {
            "Content-Type": "application/json"
        }
        req = Request(
            self.strawpoll_url,
            json.dumps(poll_data.get_json_representation(), indent=2).encode("ascii"),
            custom_header
        )

        with urlopen(req) as response:
            poll_response = json.loads(response.read().decode('utf-8'))
            final_url = self.created_poll_url + str(poll_response['id'])
            print("Poll created: " + final_url)


##########################################################################

from_date = datetime.date.today()
from_date += timedelta(days=1)

# Uses some "ugly" defaults for "Among Us" scheduling
# Weekend = Friday, Saturday, Sunday
# Weekendtimes for Saturday, Sunday only
parser = argparse.ArgumentParser(description='Create a new strawpoll meeting')
parser.add_argument("-t", action="store", dest="title", type=str, default="Among Us")
parser.add_argument("--fullweek", action="store_true", default=False)
parser.add_argument("--weekdayoptions", nargs="+", default=["19:30 - 22:00 CEST"])
parser.add_argument("--weekendoptions", nargs="+", default=["14:00 - 17:00 CEST", "19:30 - 22:00 CEST"])
parser.add_argument("--repeat", action="store", dest="repeat", type=int, default=6)

args      = parser.parse_args()
poll_data = PollData(args.title, args.weekdayoptions, args.weekendoptions)

if args.fullweek:
    poll_data.add_daily_answers(from_date, args.repeat)
else:
    poll_data.add_weekend_only_answers(from_date, args.repeat)

strawpoll_creator = StrawPollCreator()
strawpoll_creator.create_poll(poll_data)