import random


def purchase_gateway(price: int):
    print('=-' * 20)
    print("The payment was made successfully")
    print(f"Amount paid: {price} IRR")
    print('=-' * 20)
    return random.randint(10000, 99999)
