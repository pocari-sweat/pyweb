from flask import url_for
import os
from datetime import date, datetime, timedelta
from helloflask import app

def make_date(dt, fmt):
    if not isinstance(dt, date):
        return datetime.strptime(dt, fmt)
    else:
        return dt
