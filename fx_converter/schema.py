import graphene

from fx_converter.models import Rate as RateModel
from fx_converter.service import update_db


# class Rate(SQLAlchemyObjectType):
#     class Meta:
#         model = RateModel
#         interfaces = (relay.Node,)
class Rate(graphene.ObjectType):
    date = graphene.Date()
    code = graphene.String()
    value = graphene.Decimal()


class Query(graphene.ObjectType):
    # node = relay.Node.Field()
    # rates = SQLAlchemyConnectionField(Rate)
    # Explain connections better:
    # https://github.com/graphql-python/graphene/issues/592

    rates = graphene.Field(graphene.List(Rate),
                           day=graphene.Date())

    def resolve_rates(self, info, day=None):
        day = update_db(day)

        rates_db = RateModel.query.filter_by(date=day).all()
        return [
            Rate(date=r.date, code=r.code, value=r.value)
            for r in rates_db
        ]

    convert = graphene.Field(graphene.Decimal,
                             input_currency=graphene.String(),
                             input_value=graphene.Decimal(),
                             output_currency=graphene.String(),
                             day=graphene.Date())

    def resolve_convert(self, info,
                        input_currency, input_value, output_currency,
                        day=None):
        day = update_db(day)

        if input_currency == 'EUR':
            input_eur = 1
        else:
            input_eur_db = RateModel.query.filter_by(
                date=day, code=input_currency).first()
            input_eur = input_eur_db.value
        if output_currency == 'EUR':
            output_eur = 1
        else:
            output_eur_db = RateModel.query.filter_by(
                date=day, code=output_currency).first()
            output_eur = output_eur_db.value

        return input_value * output_eur / input_eur

    available_currencies = graphene.List(graphene.String)

    def resolve_available_currencies(self, info):
        return [code[0] for code in
                RateModel.query.with_entities(RateModel.code).distinct()]


schema = graphene.Schema(query=Query)
