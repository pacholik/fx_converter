"""FIXME: THIS IS AN EXAMPLARY SCHEMA!!!

Source: https://github.com/timfeirg/flask-graphene-boilerplate/blob/master/graphene_boilerplate/schema.py
"""

import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField

from fx_converter.database import db
from fx_converter.models import Rate as RateModel


# class Rate(SQLAlchemyObjectType):
#     class Meta:
#         model = RateModel
#         interfaces = (relay.Node,)


class Rate(graphene.ObjectType):
    from_ = graphene.String()
    to_ = graphene.String()
    day = graphene.Date()


class Query(graphene.ObjectType):
    # node = relay.Node.Field()
    # all_items = SQLAlchemyConnectionField(Rate)

    # rates = graphene.List(Rate)
    rate = graphene.Field(Rate,
                          from_=graphene.String(),
                          to_=graphene.String(),
                          day=graphene.Date())

    def resolve_rates(self, info, from_, to_, day):
        print(self)
        print(info)
        print(from_)
        print(to_)
        print(day)


schema = graphene.Schema(query=Query)


if __name__ == '__main__':
    print(
        schema.execute('''
            query {
                rate(from_: "CZK", to_: "EUR", day: "today") {
                    from_
                    to_
                    day
                }
            }''')
    )
