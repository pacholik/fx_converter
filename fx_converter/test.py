from graphene.test import Client
import warnings
warnings.filterwarnings('ignore')

from fx_converter.app import app
from fx_converter.models import Rate
from fx_converter.schema import schema
from fx_converter.service import basic_db_data


def test_schema():
    client = Client(schema)
    print(client)


def test_convert():
    with app.app_context():
        Rate.query.delete()

        res = schema.execute('''
            query {
                convert(inputCurrency: "CZK",
                        inputValue: "123",
                        outputCurrency: "EUR",
                        day: "2020-12-31")
            }''')
        first_result = res.data['convert']
        assert 4.68 < float(first_result) < 4.69    # avoiding FP errors

        # now without “day” – update shoud occur
        res = schema.execute('''
            query {
                convert(inputCurrency: "CZK",
                        inputValue: "123",
                        outputCurrency: "EUR")
            }''')
        second_result = res.data['convert']

        assert first_result != second_result   # coincidence is highly unlikely


def test_available_currencies():
    with app.app_context():
        res = schema.execute('''
            query {
                availableCurrencies
            }''')
        assert res.data['availableCurrencies'] == [
            'AUD', 'BGN', 'BRL', 'CAD', 'CHF', 'CNY', 'CZK', 'DKK',
            'GBP', 'HKD', 'HRK', 'HUF', 'IDR', 'ILS', 'INR', 'ISK',
            'JPY', 'KRW', 'MXN', 'MYR', 'NOK', 'NZD', 'PHP', 'PLN',
            'RON', 'RUB', 'SEK', 'SGD', 'THB', 'TRY', 'USD', 'ZAR',
        ]


def test_rates():
    with app.app_context():
        Rate.query.delete()
        basic_db_data()

        res = schema.execute('''
            query {
                rates(day: "2020-12-18") {
                    code
                    value
                }
            }''')
        rates = res.data['rates']
        assert len(rates) == 32

        res = schema.execute('''
            query {
                rates {
                    date
                    code
                    value
                }
            }''')
        rates = res.data['rates']
        assert len(rates) == 32


if __name__ == '__main__':
    # test_convert()
    # test_available_currencies()
    test_rates()
