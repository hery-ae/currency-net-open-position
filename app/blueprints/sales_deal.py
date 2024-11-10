from flask import Flask, Blueprint, request, Response
from sqlalchemy import select, insert, exc
from ..auth import Auth
from ..database import engine
from ..models.sales_deal import SalesDeal as SalesDealModel

class SalesDeal:
    url_prefix = '/sales-deals'

    @Auth.authenticate
    def get_sales_deal():
        model = SalesDealModel()
        query = model.query()
        data = model.get(query)

        return data

    @Auth.authenticate
    def store_sales_deal():
        if (request.is_json == False):
            return Response(status=400)

        try:
            values = {
                'user_id': request.json['user_id'],
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

    @Auth.authenticate
    def update_sales_deal(sales_deal_id):
        pass

    @Auth.authenticate
    def delete_sales_deal(sales_deal_id):
        pass
