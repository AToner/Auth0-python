"""Python Flask API Auth0 integration example
"""

from functools import wraps
import json
from os import environ as env, path
import urllib
import requests

from dotenv import load_dotenv
from flask import Flask, request, jsonify, _app_ctx_stack
from flask_cors import cross_origin
from jose import jwt

load_dotenv(path.splitext(__file__)[0] + ".env")
AUTH0_DOMAIN = env["AUTH0_DOMAIN"]
API_AUDIENCE = env["API_ID"]
CLIENT_ID = env["CLIENT_ID"]

#
# This needs to be called application for beanstalk
# Can you believe it?
# http://stackoverflow.com/questions/28048342/how-do-i-configure-the-name-of-my-wsgi-application-on-aws-elastic-beanstalk
application = Flask(__name__)


# Format error response and append status code.
def handle_error(error, status_code):
    """Handles the errors
    """
    resp = jsonify(error)
    resp.status_code = status_code
    return resp


def get_token_auth_header():
    """Obtains the access token from the Authorization Header
    """
    auth = request.headers.get("Authorization", None)
    if not auth:
        return handle_error({"code": "authorization_header_missing",
                             "description":
                                 "Authorization header is expected"}, 401)

    parts = auth.split()

    if parts[0].lower() != "bearer":
        return handle_error({"code": "invalid_header",
                             "description":
                                 "Authorization header must start with"
                                 "Bearer"}, 401)
    elif len(parts) == 1:
        return handle_error({"code": "invalid_header",
                             "description": "Token not found"}, 401)
    elif len(parts) > 2:
        return handle_error({"code": "invalid_header",
                             "description": "Authorization header must be"
                                            "Bearer token"}, 401)

    token = parts[1]
    return token


def requires_scope(required_scope):
    """Determines if the required scope is present in the access token
    Args:
        required_scope (str): The scope required to access the resource
    """
    token = get_token_auth_header()
    unverified_claims = jwt.get_unverified_claims(token)
    token_scopes = unverified_claims["scope"].split()
    for token_scope in token_scopes:
        if token_scope == required_scope:
            return True
    return False


def requires_auth(f):
    """Determines if the access token is valid
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = get_token_auth_header()
        jsonurl = urllib.urlopen("https://"+AUTH0_DOMAIN+"/.well-known/jwks.json")
        jwks = json.loads(jsonurl.read())

        try:
            unverified_header = jwt.get_unverified_header(token)
        except jwt.JWTError:
            return "", 401, {'Content-Type': 'text/plain'}
        except Exception:
            return "", 500

        rsa_key = {}
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"]
                }
        if rsa_key:
            try:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=unverified_header["alg"],
                    audience=API_AUDIENCE,
                    issuer="https://"+AUTH0_DOMAIN+"/"
                )
            except jwt.ExpiredSignatureError:
                return handle_error({"code": "token_expired",
                                     "description": "token is expired"}, 401)
            except jwt.JWTClaimsError:
                return handle_error({"code": "invalid_claims",
                                     "description": "incorrect claims,"
                                                    "please check the audience and issuer"}, 401)
            except Exception:
                return handle_error({"code": "invalid_header",
                                     "description": "Unable to parse authentication"
                                                    "token."}, 400)

            _app_ctx_stack.top.current_user = payload
            return f(*args, **kwargs)
        return handle_error({"code": "invalid_header",
                             "description": "Unable to find appropriate key"}, 400)
    return decorated


@application.errorhandler(404)
def page_not_found(e):
    return "", 404


@application.errorhandler(500)
def server_error(e):
    return "", 500


# Controllers API
@application.route("/ping")
@cross_origin(headers=["Content-Type", "Authorization"])
def ping():
    """No access token required to access this route
    """
    return 'Ping', 200, {'Content-Type': 'text/plain'}


@application.route("/secure")
@cross_origin(headers=["Content-Type", "Authorization"])
@cross_origin(headers=["Access-Control-Allow-Origin", "*"])
@requires_auth
def secured_ping():
    """A valid access token is required to access this route
    """
    return 'SECURE!', 200, {'Content-Type': 'text/plain'}


@application.route("/gettoken")
@cross_origin(headers=["Content-Type", "Authorization"])
def get_token():
    username = request.args.get('username')
    password = request.args.get('password')

    payload = {
        "client_id": CLIENT_ID,
        "username": username,
        "password": password,
        "audience": API_AUDIENCE,
        "connection": "Username-Password-Authentication",
        "grant_type": "password"
    }

    url = "https://"+AUTH0_DOMAIN+"/oauth/token"
    response = requests.post(url,data=payload)
    if response.status_code != 200:
        return "", response.status_code
    data = response.json()
    return data["access_token"], 200, {'Content-Type': 'text/plain'}


# @APP.route("/secured/private/ping")
# @cross_origin(headers=["Content-Type", "Authorization"])
# @cross_origin(headers=["Access-Control-Allow-Origin", "*"])
# @requires_auth
# def secured_private_ping():
#     """A valid access token and an appropriate scope are required to access this route
#     """
#     if requires_scope("read:agenda"):
#         return "All good. You're authenticated and the access token has the appropriate scope"
#     return "You don't have access to this resource"


if __name__ == "__main__":
    application.run(host="0.0.0.0", port=env.get("PORT", 8080))
