import os
from flask import Flask
from .views.index import nop
from .views.auth import auth
from .views.interbank_deals import InterbankDeal
from .views.sales_deals import SalesDeal
from .views.adjustments import Adjustment
from .database import init_db

app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(8).hex()

app.config.from_prefixed_env()

app.config['CLIENT_AUTH_URL'] = app.config.get('CLIENT_AUTH_URL') or 'http://localhost:8080/nop/token.json'

with app.app_context():
    init_db()

@app.after_request
def afterrequest(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, PATCH, DELETE'

    return response

app.add_url_rule(
    '/',
    view_func=nop,
    methods=['GET']
)

app.add_url_rule(
    '/auth',
    view_func=auth,
    methods=['POST']
)

app.add_url_rule(
    ('{}/').format(InterbankDeal.url_prefix),
    view_func=InterbankDeal.get_interbank_deal,
    methods=['GET']
)

app.add_url_rule(
    ('{}/').format(InterbankDeal.url_prefix),
    view_func=InterbankDeal.store_interbank_deal,
    methods=['PUT']
)

app.add_url_rule(
    ('{}/').format(SalesDeal.url_prefix),
    view_func=SalesDeal.get_sales_deal,
    methods=['GET']
)

app.add_url_rule(
    ('{}/').format(SalesDeal.url_prefix),
    view_func=SalesDeal.store_sales_deal,
    methods=['PUT']
)

app.add_url_rule(
    ('{}/<int:sales_deal_id>').format(SalesDeal.url_prefix),
    view_func=SalesDeal.update_sales_deal,
    methods=['PATCH']
)

app.add_url_rule(
    ('{}/<int:sales_deal_id>').format(SalesDeal.url_prefix),
    view_func=SalesDeal.delete_sales_deal,
    methods=['DELETE']
)

app.add_url_rule(
    ('{}/').format(Adjustment.url_prefix),
    view_func=Adjustment.get_adjustment,
    methods=['GET']
)

app.add_url_rule(
    ('{}/').format(Adjustment.url_prefix),
    view_func=Adjustment.store_adjustment,
    methods=['PUT']
)

app.add_url_rule(
    ('{}/<int:adjustment_id>').format(Adjustment.url_prefix),
    view_func=Adjustment.update_adjustment,
    methods=['PATCH']
)

app.add_url_rule(
    ('{}/<int:adjustment_id>').format(Adjustment.url_prefix),
    view_func=Adjustment.delete_adjustment,
    methods=['DELETE']
)
