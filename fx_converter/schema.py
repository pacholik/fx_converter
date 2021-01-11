import graphene

from fx_converter.models import Rate as RateModel


# class Rate(SQLAlchemyObjectType):
#     class Meta:
#         model = RateModel
#         interfaces = (relay.Node,)


class Rate(graphene.ObjectType):
    input_currency = graphene.String()
    input_value = graphene.Decimal()
    output_currency = graphene.String()
    day = graphene.Date()
    output_value = graphene.Decimal()


class Query(graphene.ObjectType):
    # node = relay.Node.Field()
    # all_items = SQLAlchemyConnectionField(Rate)

    # rates = graphene.List(Rate)
    rate = graphene.Field(Rate,
                          input_currency=graphene.String(),
                          input_value=graphene.Decimal(),
                          output_currency=graphene.String(),
                          day=graphene.Date())

    def resolve_rate(self, info,
                     input_currency, input_value, output_currency, day):
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

        return Rate(input_currency=input_currency,
                    output_currency=output_currency,
                    day=day,
                    output_value=input_value * output_eur / input_eur)


schema = graphene.Schema(query=Query)
