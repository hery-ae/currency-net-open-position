from flask import request, Response
from sqlalchemy.exc import SQLAlchemyError
from ..auth import Auth
from ..models.interbank_deal import InterbankDeal as InterbankDealModel

class InterbankDeal:
    url_prefix = '/interbank-deals'

    @Auth.authenticate
    def get_interbank_deal():
        model = InterbankDealModel()
        query = model.query()
        data = model.get(query)

        return data

    @Auth.authenticate
    def store_interbank_deal():
        if (request.is_json == False):
            return Response(status=400)

        try:
            values = {
                'user_id': request.json['user_id'],
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

    @Auth.authenticate
    def update_interbank_deal(interbank_deal_id):
        if (request.is_json == False):
            return Response(status=400)

        try:
            values = {
                'id': interbank_deal_id,
                'user_id': request.json['user_id'],
                'currency_pair_id': request.json['currency_pair_id'],
                'interoffice_rate': request.json['interoffice_rate'],
                'base_currency_closing_rate': request.json['base_currency_closing_rate'],
                'amount': request.json['amount'],
                'tod_tom_spot_forward': request.json['tod_tom_spot_forward'],
            }

            try:
                InterbankDealModel(**values).save()

            except SQLAlchemyError:
                return Response(status=500)

        except KeyError:
            return Response(status=400)

        return Response(status=200)

    @Auth.authenticate
    def delete_interbank_deal(interbank_deal_id):
        try:
            InterbankDealModel(id=interbank_deal_id).delete()

        except SQLAlchemyError:
            return Response(status=500)

        return Response(status=202)
