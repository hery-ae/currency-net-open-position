from flask import current_app, request, Response
from requests import post
from jwt import decode, encode
from redis import Redis

def auth():
    code = request.values.get('auth-token')
    client_url = current_app.config.get('CLIENT_AUTH_URL')

    client_request = post(client_url, data={'code': code})

    if client_request.status_code == 200:
        client_response = client_request.json()

        payload = decode(client_response.get('access_token'), client_response.get('id_token'), algorithms=['HS256'])

        access_token = encode(
            {
                'sub': payload.get('sub'),
                'user_id': payload.get('user_id')
            },
            current_app.config.get('SECRET_KEY'),
            algorithm='HS256'
        )

        redis = Redis()

        redis.set(('token:{}').format(payload.get('sub')), 'authenticated')
        redis.expire(('token:{}').format(payload.get('sub')), client_response.get('expires_in'))

        return {
            'access_token': access_token,
            'token_type': 'Bearer',
            'expires_in': redis.ttl(('token:{}').format(payload.get('sub')))
        }

    return Response(status=401)
