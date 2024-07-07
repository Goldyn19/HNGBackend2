import random

def generate_org_id():
    cart_id = ''
    characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
    cart_id_lenght = 10
    for y in range(cart_id_lenght):
        cart_id += characters[random.randint(0, len(characters)-1)]
    return cart_id