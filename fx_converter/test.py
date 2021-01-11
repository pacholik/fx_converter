from graphene.test import Client
import warnings
warnings.filterwarnings('ignore')

from fx_converter.app import app
from fx_converter.schema import schema


def test_schema():
    client = Client(schema)
    print(client)


with app.app_context():
    print(
        schema.execute('''
            query {
                convert(inputCurrency: "CZK",
                        inputValue: "123",
                        outputCurrency: "EUR",
                        day: "2020-12-31")
            }''')
    )

    # print(
    #     schema.execute('''
    #         query {
    #             availableCurrencies
    #         }''')
    # )

    print(
        schema.execute('''
            query {
                rates(last: 10) {
                    edges {
                        node {
                            date
                            code
                            value
                        }
                    }
                }
            }''')
    )
