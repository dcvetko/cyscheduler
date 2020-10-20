#!/usr/bin/python3

import json
import argparse
import datetime
from datetime import timedelta

# https://strawpoll.com/api-docs/polls/create

##########################################################################

class PollData:
    def __init__(self):
        self.title       = None
        self.description = None
        self.answers     = []
        self.ma          = True
        self.mip         = True
        self.weekdaytimes = []
        self.weekendtimes = []

    def add_answer(self, answer):
        self.answers.append(answer)

    def add_daily_answers(self, date_from, repeat):
        date = date_from
        for i in range(0, repeat):
            if date.weekday() < 5:
                for weekdaytime in self.weekdaytimes:
                    self.add_answer(self.get_date_str(date, weekdaytime))
            else:
                for weekendtime in self.weekendtimes:
                    self.add_answer(self.get_date_str(date, weekendtime))
            date += timedelta(days=1)

    # Friday, Saturday, Sunday
    def add_weekend_only_answers(self, date_from, repeat):
        date = date_from
        for i in range(0, repeat):
            while date.weekday() < 4:
                date += timedelta(days=1)

            if date.weekday() < 5:
                for weekdaytime in self.weekdaytimes:
                    self.add_answer(self.get_date_str(date, weekdaytime))
            else:
                for weekendtime in self.weekendtimes:
                    self.add_answer(self.get_date_str(date, weekendtime))

            date += timedelta(days=1)

    def get_date_str(self, date, timestr):
        return date.strftime("%Y-%m-%d (%A)") + " | " + timestr

    def get_json_representation(self):
        obj = {}
        obj["title"]       = self.title
        obj["description"] = self.description
        obj["answers"]     = self.answers
        obj["ma"]          = self.ma
        obj["mip"]         = self.mip

        return json.dumps(obj)

##########################################################################

class Poller:
    def __init__(self, api_key, poll_data):
        self.strawpoll_url  = "https://strawpoll.com/api/poll"
        self.api_key_header = "API-KEY: " + api_key
        self.poll_data      = poll_data

    # TODO send request and also copy to clipboard
    def create_poll(self):
        pass

##########################################################################

# Uses some "ugly" defaults for "Among Us" scheduling
# Weekend = Friday, Saturday, Sunday
# Weekendtimes for Saturday, Sunday only
parser = argparse.ArgumentParser(description='Create a new strawpoll meeting')
parser.add_argument("-t", action="store", dest="title", type=str, default="Among Us")
parser.add_argument("-d", action="store", dest="description", type=str, default="Imposters not welcome")
parser.add_argument("--fullweek", action="store_true", default=False)
parser.add_argument("--weekdaytimes", nargs="+", default=["19:30 - 22:00 CEST"])
parser.add_argument("--weekendtimes", nargs="+", default=["14:00 - 17:00 CEST", "19:30 - 22:00 CEST"])
parser.add_argument("--repeat", action="store", dest="repeat", type=int, default=6)

args = parser.parse_args()
poll_data = PollData()
poll_data.title        = args.title
poll_data.description  = args.description
poll_data.weekdaytimes = args.weekdaytimes
poll_data.weekendtimes = args.weekendtimes

from_date = datetime.date.today()
from_date += timedelta(days=1)

if args.fullweek:
    poll_data.add_daily_answers(from_date, args.repeat)
else:
    poll_data.add_weekend_only_answers(from_date, args.repeat)

print(poll_data.get_json_representation()) 