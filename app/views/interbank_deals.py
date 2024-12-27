from flask import request, Response
from sqlalchemy.exc import SQLAlchemyError
from ..auth import authorize
from ..models.interbank_deal import InterbankDeal as InterbankDealModel

class InterbankDeal:
    url_prefix = '/interbank-deals'

    @authorize
    def get_interbank_deal(user=None):
        model = InterbankDealModel()
        query = model.query()
        data = model.get(query)

        return data

    @authorize
    def store_interbank_deal(user=None):
        if (request.is_json == False):
            return Response(status=400)

        try:
            values = {
                'user_id': user['user_id'],
                'currency_id': request.json['currency_id'],
                'interoffice_rate': request.json['interoffice_rate'],
                'base_currency_closing_rate': request.json['base_currency_closing_rate'],
                'amount': request.json['amount'],
            }

            try:
                InterbankDealModel(**values).save()

            except SQLAlchemyError:
                return Response(status=500)

        except KeyError:
            return Response(status=400)

        return Response(status=201)
