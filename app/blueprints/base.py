from datetime import datetime
from requests import post
from flask import current_app, request, Response
from redis import Redis
from ..auth import Auth
from ..models import InterbankDealModel, SalesDealModel, AdjustmentModel

@Auth.authenticate
def index():
    date_to = datetime.now()

    if 'date-to' in request.args:
        try:
            date_to = datetime.fromisoformat(request.args.get('date-to')).replace(hour=23, minute=59, second=59)

        except ValueError:
            return Response(status=400)

    data = []

    interbank_deal = InterbankDealModel()

    query = interbank_deal.query().where(
        InterbankDealModel.created_at <= date_to
    )

    interbank_deals = interbank_deal.get(query)

    sales_deal = SalesDealModel()

    query = sales_deal.query().where(
        SalesDealModel.created_at <= date_to
    )

    sales_deals = sales_deal.get(query)

    adjustment = AdjustmentModel()

    query = adjustment.query().where(
        AdjustmentModel.created_at <= date_to
    )

    adjustments = adjustment.get(query)

    if len(interbank_deals):
        data = data + interbank_deals

    if len(sales_deals):
        data = data + sales_deals

    if len(adjustments):
        data = data + adjustments

    data.sort(key=lambda value: value['created_at'])

    if len(data):
        date_to = data[len(data) - 1]['created_at']

    nop = []

    for deal in data:
        nop_key = None

        if not any(deal['currency_id'] == value['currency_id'] for value in nop):
            nop.append({
                'currency_id': deal['currency_id'],
                'opening_adjustment': 0,
                'current_adjustment': 0,
                'opening_nop': 0,
                'current_nop': 0,
                'counter_amount': 0
            })

            nop_key = len(nop) - 1

        else:
            for value in nop:
                if value['currency_id'] == deal['currency_id']:
                    nop_key = nop.index(value)
                    break

        if deal['created_at'].date() == date_to.date():
            nop[nop_key]['opening_rate'] = deal['base_currency_closing_rate']

        if 'interoffice_rate' in deal:
            nop[nop_key]['counter_amount'] += deal['interoffice_rate'] * deal['amount']

            if deal['created_at'].date() < date_to.date():
                nop[nop_key]['opening_nop'] += deal['amount']

            if deal['created_at'].date() == date_to.date():
                nop[nop_key]['current_nop'] += deal['amount']

        else:
            if deal['created_at'].date() < date_to.date():
                nop[nop_key]['opening_adjustment'] += deal['amount']

            if deal['created_at'].date() == date_to.date():
                nop[nop_key]['current_adjustment'] += deal['amount']

    for value in nop:
        if 'opening_rate' in value and value['current_nop']:
            value['average_rate'] = value['opening_adjustment'] * value['opening_rate']
            value['average_rate'] += value['current_adjustment'] * value['opening_rate']
            value['average_rate'] += value['counter_amount']
            value['average_rate'] /= value['opening_nop'] + value['opening_adjustment'] + value['current_nop'] + value['current_adjustment']

        value['current_adjustment'] += value['opening_adjustment']
        value['opening_nop'] += value['opening_adjustment']
        value['current_nop'] += value['current_adjustment'] + value['opening_nop']

    return nop

def authorize():
    code = request.values.get('auth-token')
    client_url = current_app.config.get('CLIENT_URL')

    client_request = post(('{}token.json').format(client_url), data={'code': code})

    if client_request.status_code == 200:
        client_response = client_request.json()

        redis = Redis()
        session = len(redis.keys())

        redis.hset(f'user-session:{session}', mapping=client_response)

        return {
            'access_token': redis.hget(f'user-session:{session}', 'access_token'),
            'token_type': 'Bearer'
        }

    return Response(status=401)
