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
module: jwt_hash_encode

short_description: Generate a JWKS along with a valid JWT

description: This module generates a JWKS containing a single JWK, along with a signed JWT which never expires

options:
    secret:
        description: JTW secret
        required: true
        type: str
    claims:
        description: JWT Cliams
        required: false
        type: dict
    algorithm:
        description: JWT algorithm defaulted to HS256
        required: false
        type: str

author:
    - Hugues Granger (@huguesgr)
    - Fabio Isgrò (@drgogeta86)
'''

EXAMPLES = r'''
- name: Hash a JWT Token
    hyperhcp.jwt_token.jwt_hash_encode:
    secret: "{{ secret }}"
    algorithm: "HS256"
    claims:
        exp: "300"
        iat: "{{ (ansible_date_time.epoch | int )  }}"
        user: "{{ user | lower }}"
        secret: "mysecret"
        email: "mailme@mailmenot.to"
        sub: "mailme@mailmenot.to/user"
    register: jwt_hash_token
'''

RETURN = r'''
# jwks:
#     description: JWKS
#     type: str
#     returned: always
#     sample: '{"keys":[{"kty": "RSA", "key_ops": ["verify"], "n": "u8iLUp71u3y59jAWsBHLPwcnXY9Dugu-7YtBb9LXYHnYa6FcLiY7asQC7i8eOkXK4x2I-P5Wh-05NnRxVbJMR_VF0oMtGKpbeqoHmNdfrcAF87Y5xMTX4s9YA9Ii_6XMvdHvrX03XWWTrKvY_RD9YYjMCUIC309TmunZxFqh_EXW6sBAgmkpzgcFLiw_rzwQ0diqE9uQZlDqnV3jcBd0wOQqV9D-A59sen8tkR1GM-5VtxlNWv_9ztQQvOg-tdjLYaEh8ST6qi15MkNGea2HidYqDpKOzYbwUGBbIofq1lShhssZQ_3hOU84ANg6OjNrg7bB3mfDJtudGyGVXmSiCQ", "e": "AQAB"}]}'
jwt:
    description: JWT Hasjed as string
    type: str
    returned: always
    sample: 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJobGFiIiwic3ViIjoiaGxhYiJ9.PT2VfFyLCWLICdRwbAk0riCxAvz5F7uWHQin7mlwJgJhQ9RhfAvK9awJi3H3PCS-9QD_v2RbQ0QobuOyOxtku7-FU72FLVjL9XVIhHS_dWT0gaiqm2IQbLJmXrqGKzY6SEAe0zqOUFG5TBeyObYjyfo8XOnFmNsDMldsERlcP95bDbuaEtlPLPtkagnoiIeZtlq-p4qEFg55NVSsEE1CARy1BGvHetHYUpYhHWLFtFioqkr88BU8SOqB7LkaLn0tHZbWJXcHjjvNFMogUgye_0RD7MSGPSo0_jNp6RTE_zm0N81SbUmuz0ly_nM8EQ8bYjWI0h4AgTWw1YBH3Qkvrg'
'''

def generate(secret: str, claims: dict, algorithm: str, ) -> dict:

    res = {}
    res["jwt"] = jwt.encode(claims, secret, algorithm=algorithm )

    return res


def run_module():
    module = AnsibleModule(
        argument_spec=dict(
            secret=dict(type="str", required=True),
            claims=dict(type="dict", required=True),
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
    claims = module.params["claims"]
    algorithm = module.params["algorithm"]
    result = generate(secret, claims, algorithm)

    module.exit_json(**result)


def main() -> None:
    run_module()


if __name__ == "__main__":
    main()