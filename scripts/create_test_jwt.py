from jwt import encode

encoded_jwt = encode({"some": "payload"}, "secret", algorithm="HS256")