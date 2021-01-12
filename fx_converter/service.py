import requests
from datetime import date, timedelta
import logging

from fx_converter.config import LOGGER_NAME
from fx_converter.models import Rate

logger = logging.getLogger(LOGGER_NAME)


ONEDAY = timedelta(days=1)


def download_history(start_at: date, end_at: date):
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
    for day, code, value in download_history(start_at=date(2020, 12, 1),
                                             end_at=date(2021, 1, 1)):
        Rate.create(date=day, code=code, value=value)


def update_db(till=None):
    if not till:
        till = date.today()
    if not Rate.query.first():
        basic_db_data()

    latest_db = Rate.query.order_by(Rate.date.desc()).first().date
    try:
        for day, code, value in download_history(start_at=latest_db + ONEDAY,
                                                 end_at=till + ONEDAY):
            Rate.create(date=day, code=code, value=value)
    except Exception:
        return latest_db
    return till
