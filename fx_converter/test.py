from graphene.test import Client

from fx_converter.app import app
from fx_converter.schema import schema


def test_schema():
    client = Client(schema)
    print(client)


with app.app_context():
    print(
        schema.execute('''
            query {
                rate(inputCurrency: "CZK",
                     inputValue: "123",
                     outputCurrency: "EUR",
                     day: "2020-12-31") {
                    inputCurrency
                    outputCurrency
                    day
                    outputValue
                }
            }''')
    )
