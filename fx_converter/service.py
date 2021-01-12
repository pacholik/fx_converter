import sqlalchemy.exc
import requests
from datetime import date
import logging

from fx_converter.config import LOGGER_NAME
from fx_converter.models import Rate

logger = logging.getLogger(LOGGER_NAME)


def download_history(start_at: date = date(2000, 1, 1),
                     end_at: date = date(2021, 1, 1)):
    response = requests.get('https://api.exchangeratesapi.io/history',
                            params={
                                'start_at': start_at.isoformat(),
                                'end_at': end_at.isoformat(),
                            })
    if response.ok:
        json = response.json()

        for day, rates in sorted(json['rates'].items()):
            # print(day, sorted(rates.keys()))
            for code, value in sorted(rates.items()):
                yield date.fromisoformat(day), code, value


def basic_db_data():
    for day, code, value in download_history():
        rate = Rate.create(date=day, code=code, value=value)


def latest_available_day():
    print(Rate.query.order_by(Rate.date.desc()).first().date)
