from flask import request, Response
from sqlalchemy.exc import SQLAlchemyError
from ..auth import authorize
from ..models.adjustment import Adjustment as AdjustmentModel

class Adjustment:
    url_prefix = '/adjustments'

    @authorize
    def get_adjustment(user=None):
        model = AdjustmentModel()
        query = model.query()
        data = model.get(query)

        return data

    @authorize
    def store_adjustment(user=None):
        if (request.is_json == False):
            return Response(status=400)

        try:
            values = {
                'user_id': user['user_id'],
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

    @authorize
    def update_adjustment(adjustment_id, user=None):
        if (request.is_json == False):
            return Response(status=400)

        try:
            values = {
                'id': adjustment_id,
                'user_id': user['user_id'],
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

        return Response(status=200)

    @authorize
    def delete_adjustment(adjustment_id, user=None):
        try:
            AdjustmentModel(id=adjustment_id).delete()

        except SQLAlchemyError:
            return Response(status=500)

        return Response(status=202)
