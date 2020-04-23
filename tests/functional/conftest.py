import pytest

import openpay


@pytest.fixture(scope='module', autouse=True)
def set_openpay_params():
    old_api_key = openpay.api_key
    openpay.api_key = 'sk_10d37cc4da8e4ffd902cdf62e37abd1b'

    old_merchant_id = openpay.merchant_id
    openpay.merchant_id = 'mynvbjhtzxdyfewlzmdo'

    old_verify_ssl = openpay.verify_ssl_certs
    openpay.verify_ssl_certs = False

    yield

    openpay.api_key = old_api_key
    openpay.merchant_id = old_merchant_id
    openpay.verify_ssl_certs = old_verify_ssl


@pytest.fixture
def change_api_key():
    def _change(tmp_api_key):
        openpay.api_key = tmp_api_key

    old_key = openpay.api_key

    yield _change

    openpay.api_key = old_key


@pytest.fixture
async def customer():
    return await openpay.Customer.create(
        name="John", last_name="Doe", description="Test User",
        email="johndoe@example.com"
    )

@pytest.fixture
async def card(customer):
    card = await customer.cards.create(
        card_number="4111111111111111",
        holder_name="Juan Perez",
        expiration_year="20",
        expiration_month="12",
        cvv2="110",
        address={
            "city": "Querétaro",
            "country_code": "MX",
            "postal_code": "76900",
            "line1": "Av 5 de Febrero",
            "line2": "Roble 207",
            "line3": "col carrillo",
            "state": "Querétaro"
        }
    )

    return card
