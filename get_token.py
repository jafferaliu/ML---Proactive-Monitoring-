import time, jwt, json
import sys

sa = json.load(open("service-account.json","r"))

iat = time.time()
exp = iat + 3600
payload = {
    "iss": sa["client_email"],
    "sub": sa["client_email"],
    "aud": "https://pubsub.googleapis.com/",
    "iat": iat,
    "exp": exp
}
additional_headers = { "kid": sa["private_key_id"] }

signed_jwt = jwt.encode(payload, sa["private_key"], 
    headers=additional_headers, algorithm="RS256")

file1 = open("access_token.txt", "w")
file1.write(signed_jwt)
file1.close()
