import datetime
import string
import time
import random


def generate_order_id():
    order_id = 'oid-test-{0}-{1}'.format(
        random.randint(1, 3000), str(time.time())[7:])
    if len(order_id) > 20:
        order_id = order_id[:20]

    return order_id


NOW = datetime.datetime.now()

DUMMY_CARD = {
    'card_number': '4111111111111111',
    'holder_name': 'Juan Lopez',
    'expiration_month': NOW.month,
    'expiration_year': str(NOW.year + 4)[2:],
    "cvv2": "110",
    "address": {
        "line1": "Av. 5 de febrero No. 1080 int Roble 207",
        "line2": "Carrillo puerto",
        "line3": "Zona industrial carrillo puerto",
        "postal_code": "06500",
        "state": "Querétaro",
        "city": "Querétaro",
        "country_code": "MX"
    }
}

DUMMY_CHARGE = {
    'amount': 100,
    'card': DUMMY_CARD,
    'order_id': generate_order_id(),
    'method': 'card',
    'description': 'Dummy Charge',
}

DUMMY_CHARGE_STORE = {
    'amount': 100,
    'method': 'store',
    'description': 'Dummy Charge on Store',
}

DUMMY_PLAN = {
    'amount': 2000,
    'status_after_retry': 'cancelled',
    'name': 'Amazing Gold Plan',
    'retry_times': 2,
    'repeat_unit': 'month',
    'trial_days': 0,
    'repeat_every': 1,
    'id': ('openpay-test-gold-' +
           ''.join(random.choice(string.ascii_lowercase) for x in range(10)))
}

DUMMY_TRANSFER = {
    'amount': 400,
    'customer_id': 'acuqxruyv0hi1wfdwmym',
    'description': 'Dummy Transfer',
    'order_id': 'oid-00099',
}
