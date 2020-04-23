import pytest

import openpay
from tests.functional.helpers import DUMMY_CARD

pytestmark = pytest.mark.asyncio


async def test_dns_failure(mocker):
    mocker.patch(
        'openpay.get_api_base',
        lambda: 'https://my-invalid-domain.ireallywontresolve/v1'
    )

    with pytest.raises(openpay.error.APIConnectionError):
        await openpay.Customer.create()


async def test_invalid_credentials(change_api_key):
    change_api_key('invalid')
    with pytest.raises(openpay.error.AuthenticationError) as e:
        await openpay.Customer.create()

    assert e.value.http_status == 401
    assert isinstance(e.value.http_body, str)
    assert isinstance(e.value.json_body, dict)


async def test_create_invalid():
    with pytest.raises(openpay.error.InvalidRequestError) as e:
        await openpay.Charge.create()

    assert e.value.http_status == 400


async def test_retrieve_non_existent():
    with pytest.raises(openpay.error.InvalidRequestError) as e:
        await openpay.Charge.retrieve('invalid', customer_id='123')

    assert e.value.http_status == 404
    assert isinstance(e.value.http_body, str)
    assert isinstance(e.value.json_body, dict)


async def test_raise():
    EXPIRED_CARD = DUMMY_CARD.copy()
    EXPIRED_CARD['expiration_month'] = '01'
    EXPIRED_CARD['expiration_year'] = '19'

    with pytest.raises(openpay.error.InvalidRequestError) as e:
        await openpay.Charge.create(
            amount=100, method='card', description="Test Order",
            order_id="oid-00080", card=EXPIRED_CARD
        )

    assert e.value.http_status == 400
    assert isinstance(e.value.http_body, str)
    assert isinstance(e.value.json_body, dict)


async def test_unicode():
    # Make sure unicode requests can be sent
    with pytest.raises(openpay.error.InvalidRequestError):
        await openpay.Charge.retrieve_as_merchant(id='☃')


async def test_missing_id():
    customer = openpay.Customer()
    with pytest.raises(openpay.error.InvalidRequestError):
        await customer.refresh()

