#!/usr/bin/env python
# encoding: utf-8
import datetime
import time


class Card:
    def __init__(self):
        self.factor = 0
        self.ivl = 0  # 复习间隔
        self.reps = 0  # 重复次数
        self.due = 0  # 应该复习的时间，相对于第一次复习时间
        self.reviewTime = None
        self.lapses = 0

    def get_review_time(self):
        d = datetime.datetime.fromtimestamp(self.reviewTime)
        d -= datetime.timedelta(hours=4)
        d = datetime.datetime(d.year, d.month, d.day)
        d += datetime.timedelta(hours=4)
        return int(time.mktime(d.timetuple()))
