#!/usr/bin/python

# import datetime
from ansible.errors import AnsibleError
from ansible.module_utils.basic import AnsibleModule
# from cryptography.hazmat.primitives.asymmetric import rsa

HAVE_PYJWT = False
try:
    import jwt
    #from jwt.algorithms import RSAAlgorithm
    HAVE_PYJWT = True
except ImportError:
    pass

DOCUMENTATION = r'''
---
module: jwt_hash_decode

short_description: decode a JWT hash

description: This module decodes a JWT hash

options:
    secret:
        description: JTW secret
        required: true
        type: str
    encoded_hash:
        description: JTW Claims
        required: true
        type: str
    algorithm:
        description: JWT algorithm defaulted to HS256
        required: false
        type: str

author:
    - Hugues Granger (@huguesgr)
    - Fabio Isgrò (@drgogeta86)
'''

EXAMPLES = r'''
- name: Decode hashed JWT Token
    hyperhcp.jwt_token.jwt_hash_decode:
    secret: "{{ secret }}"
    algorithm: "HS256"
    encoded_hash: "{{jwt_hash_token.jwt}}"
'''

RETURN = r'''
# jwks:
#     description: JWKS
#     type: str
#     returned: always
#     sample: '{"keys":[{"kty": "RSA", "key_ops": ["verify"], "n": "u8iLUp71u3y59jAWsBHLPwcnXY9Dugu-7YtBb9LXYHnYa6FcLiY7asQC7i8eOkXK4x2I-P5Wh-05NnRxVbJMR_VF0oMtGKpbeqoHmNdfrcAF87Y5xMTX4s9YA9Ii_6XMvdHvrX03XWWTrKvY_RD9YYjMCUIC309TmunZxFqh_EXW6sBAgmkpzgcFLiw_rzwQ0diqE9uQZlDqnV3jcBd0wOQqV9D-A59sen8tkR1GM-5VtxlNWv_9ztQQvOg-tdjLYaEh8ST6qi15MkNGea2HidYqDpKOzYbwUGBbIofq1lShhssZQ_3hOU84ANg6OjNrg7bB3mfDJtudGyGVXmSiCQ", "e": "AQAB"}]}'
jwt:
    description: JTW decoded claims
    type: dict
    returned: always
'''

def jwt_hash_decode(secret: str, encoded_hash: str, algorithm: str, ) -> dict:

    res = {}
    res["jwt"] = jwt.decode(encoded_hash, secret, algorithms=algorithm )

    return res


def run_module():
    module = AnsibleModule(
        argument_spec=dict(
            secret=dict(type="str", required=True),
            encoded_hash=dict(type="str", required=True),
            algorithm=dict(type="str", required=False, default="HS256"),
        )
    )

    result = dict(
        changed=True,
        # jwks="",
        jwt="",
    )

    if not HAVE_PYJWT:
        raise AnsibleError("Library PyJWT is not installed")

    if module.check_mode:
        module.exit_json(**result)

    secret = module.params["secret"]
    encoded_hash = module.params["encoded_hash"]
    algorithm = module.params["algorithm"]
    result = jwt_hash_decode(secret, encoded_hash, algorithm)

    module.exit_json(**result)


def main() -> None:
    run_module()


if __name__ == "__main__":
    main()
