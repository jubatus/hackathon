# -*- coding: utf-8 -*-

import datetime


def parse_date(date):
    return datetime.datetime.strptime(date, '%Y年%m月%d日 %H:%M')
