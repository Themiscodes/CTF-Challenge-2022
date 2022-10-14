import random

DEGREE = 2
MODULUS = 0x73eda753299d7d483339d80809a1d80553bda402fffe5bfeffffffff00000001
SEED = 1 # XXX censored

def evaluate_poly(poly, x):
    result = 0
    for i, coeff in enumerate(poly):
        result += coeff * (x**i)
    return result % MODULUS

secret =1 # XXX censored

secret_int = int.from_bytes(secret, byteorder="big")
assert secret_int < MODULUS

test = secret_int.to_bytes(30, byteorder="big")
assert test == secret

poly = [secret_int]
random.seed(SEED)
for i in range(DEGREE):
    coeff = random.randint(0, MODULUS)
    poly.append(coeff)

assert evaluate_poly(poly, 0) == secret_int

shares = []
shares.append(evaluate_poly(poly, 1))
shares.append(evaluate_poly(poly, 2))
shares.append(evaluate_poly(poly, 3))

print("shares: ", shares)
