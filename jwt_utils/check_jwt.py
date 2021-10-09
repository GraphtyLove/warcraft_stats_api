import jwt
from jwt import PyJWKClient
import os


def check_jwt(token: str):

    try:
        jwt_algo = os.environ["JWT_ALGO"]
        jwt_client_id = os.environ["JWT_CLIENT_ID"]
        jwks_uri = os.environ["JWKS_URI"]
    except KeyError:
        return {"error": "Server error, missing env variables."}

    jwks_client = PyJWKClient(jwks_uri)
    signing_key = jwks_client.get_signing_key_from_jwt(token)
    try:
        data = jwt.decode(
            token,
            signing_key.key,
            algorithms=[jwt_algo],
            audience=jwt_client_id,
            options={"verify_exp": True},
        )
    except jwt.exceptions.ExpiredSignatureError:
        return False

    return True if data else False
