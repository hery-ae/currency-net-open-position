from flask import request, Response
from sqlalchemy.exc import SQLAlchemyError
from ..auth import authorize
from ..models.sales_deal import SalesDeal as SalesDealModel

class SalesDeal:
    url_prefix = '/sales-deals'

    @authorize
    def get_sales_deal(user=None):
        model = SalesDealModel()
        query = model.query()
        data = model.get(query)

        return data

    @authorize
    def store_sales_deal(user=None):
        if (request.is_json == False):
            return Response(status=400)

        try:
            values = {
                'user_id': user['user_id'],
                'currency_id': request.json['currency_id'],
                'interoffice_rate': request.json['interoffice_rate'],
                'customer_rate': request.json['customer_rate'],
                'base_currency_closing_rate': request.json['base_currency_closing_rate'],
                'amount': request.json['amount'],
            }

            try:
                SalesDealModel(**values).save()

            except SQLAlchemyError:
                return Response(status=500)

        except KeyError:
            return Response(status=400)

        return Response(status=201)

    @authorize
    def update_sales_deal(sales_deal_id, user=None):
        if (request.is_json == False):
            return Response(status=400)

        try:
            values = {
                'id': sales_deal_id,
                'user_id': user['user_id'],
                'currency_id': request.json['currency_id'],
                'interoffice_rate': request.json['interoffice_rate'],
                'customer_rate': request.json['customer_rate'],
                'base_currency_closing_rate': request.json['base_currency_closing_rate'],
                'amount': request.json['amount'],
            }

            try:
                SalesDealModel(**values).save()

            except SQLAlchemyError:
                return Response(status=500)

        except KeyError:
            return Response(status=400)

        return Response(status=200)

    @authorize
    def delete_sales_deal(sales_deal_id, user=None):
        try:
            SalesDealModel(id=sales_deal_id).delete()

        except SQLAlchemyError:
            return Response(status=500)

        return Response(status=202)
