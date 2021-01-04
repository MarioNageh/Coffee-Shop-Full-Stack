import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen

AUTH0_DOMAIN = 'coffeshopapp.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'drinks'

## AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


## Auth Header

'''
@TODO implement get_token_auth_header() method
    it should attempt to get the header from the request
        it should raise an AuthError if no header is present
    it should attempt to split bearer and the token
        it should raise an AuthError if the header is malformed
    return the token part of the header
'''


def get_token_auth_header():
    # First We Will Check if Request Have Auth Header
    auth_header = request.headers.get("Authorization", None)
    if not auth_header:
        raise AuthError("Not Authroized", 401)

    # Try To Get Data After Barre
    # Bearer  The Length -> 7
    return auth_header[7:]


'''
@TODO implement check_permissions(permission, payload) method
    @INPUTS
        permission: string permission (i.e. 'post:drink')
        payload: decoded jwt payload

    it should raise an AuthError if permissions are not included in the payload
        !!NOTE check your RBAC settings in Auth0
    it should raise an AuthError if the requested permission string is not in the payload permissions array
    return true otherwise
'''


def check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise AuthError('Bad Request',400)

    counter=0
    for x in payload['permissions']:
        print(x)
        if x==permission:
            counter=1

    if counter==0:
        raise AuthError('Forbidden',403)
'''
@TODO implement verify_decode_jwt(token) method
    @INPUTS
        token: a json web token (string)

    it should be an Auth0 token with key id (kid)
    it should verify the token using Auth0 /.well-known/jwks.json
    it should decode the payload from the token
    it should validate the claims
    return the decoded payload

    !!NOTE urlopen has a common certificate error described here: https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org
'''


def verify_decode_jwt(token):
    # RSASHA256(
    #  base64UrlEncode(header) + "." +
    #  base64UrlEncode(payload),Public Key)
    # Here We Need To Get Public Key From Auth0 List

    jwtKeys = json.loads(urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json').read())
    header_data = jwt.get_unverified_header(token)

    if 'kid' not in header_data:
        raise AuthError("Invalid Header", 401)

    compose_rsaKey = {}
    for x in jwtKeys["keys"]:
        if header_data["kid"] == x["kid"]:
            compose_rsaKey  = {
            'kty': x['kty'],
            'kid': x['kid'],
            'use': x['use'],
            'n': x['n'],
            'e': x['e']
        }
        break
    print(compose_rsaKey)
    if compose_rsaKey:
        try:
            payload = jwt.decode(token,
                                 compose_rsaKey,
                                 algorithms=ALGORITHMS,
                                 audience=API_AUDIENCE,
                                 issuer=f'https://{AUTH0_DOMAIN}/')
            return payload
        except:
            raise AuthError("Not Authraized", 401)

    raise AuthError('Valid Key', 401)


'''
@TODO implement @requires_auth(permission) decorator method
    @INPUTS
        permission: string permission (i.e. 'post:drink')

    it should use the get_token_auth_header method to get the token
    it should use the verify_decode_jwt method to decode the jwt
    it should use the check_permissions method validate claims and check the requested permission
    return the decorator which passes the decoded payload to the decorated method
'''


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper

    return requires_auth_decorator
