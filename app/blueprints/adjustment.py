from flask import request, Response
from sqlalchemy.exc import SQLAlchemyError
from ..auth import Auth
from ..models.adjustment import Adjustment as AdjustmentModel

class Adjustment:
    url_prefix = '/adjustments'

    @Auth.authenticate
    def get_adjustment():
        model = AdjustmentModel()
        query = model.query()
        data = model.get(query)

        return data

    @Auth.authenticate
    def store_adjustment():
        if (request.is_json == False):
            return Response(status=400)

        try:
            values = {
                'user_id': request.json['user_id'],
                'currency_id': request.json['currency_id'],
                'amount': request.json['amount'],
                'base_currency_closing_rate': request.json['base_currency_closing_rate'],
            }

            try:
                AdjustmentModel(**values).save()

            except SQLAlchemyError:
                return Response(status=500)

        except KeyError:
            return Response(status=400)

        return Response(status=201)

    @Auth.authenticate
    def update_adjustment(adjustment_id):
        pass

    @Auth.authenticate
    def delete_adjustment(adjustment_id):
        pass
