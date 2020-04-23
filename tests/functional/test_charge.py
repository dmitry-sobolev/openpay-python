import pytest

import openpay
from tests.functional.helpers import NOW, DUMMY_CHARGE, generate_order_id, \
    DUMMY_CHARGE_STORE

pytestmark = pytest.mark.asyncio


async def test_charge_list_all():
    charge_list = await openpay.Charge.all(
        creation={'lte': NOW.strftime("%Y-%m-%d")}
    )
    list_result = await charge_list.all(
        creation={'lte': NOW.strftime("%Y-%m-%d")}
    )

    assert charge_list.data == list_result.data

    # for expected, actual in zip(charge_list.data,
    #                             list_result.data):
    #     self.assertEqual(expected.id, actual.id)


async def test_charge_list_create():
    params = DUMMY_CHARGE.copy()

    charge_list = await openpay.Charge.all()
    params['order_id'] = generate_order_id()
    charge = await charge_list.create(**params)

    assert isinstance(charge, openpay.Charge)
    assert params['amount'] == charge.amount


async def test_charge_list_retrieve():
    charge_list = await openpay.Charge.all()
    charge = await charge_list.retrieve(charge_list.data[0].id)
    assert isinstance(charge, openpay.Charge)


async def test_charge_capture():
    params = DUMMY_CHARGE.copy()
    params['capture'] = False

    charge = await openpay.Charge.create(**params)

    assert not hasattr(charge, 'captured')

    cap_res = await charge.capture(merchant=True)
    assert charge is cap_res

    charge_merchant = await openpay.Charge.retrieve_as_merchant(charge.id)
    assert charge_merchant.status == 'completed'


async def test_charge_store_as_customer():
    customer = await openpay.Customer.create(
        name="Miguel Lopez", email="mlopez@example.com")
    charge = await customer.charges.create(**DUMMY_CHARGE_STORE)
    assert hasattr(charge, 'payment_method')
    assert hasattr(charge.payment_method, 'reference')
    assert hasattr(charge.payment_method, 'barcode_url')

    charge_res = await customer.charges.retrieve(charge.id)
    assert charge_res.status == 'in_progress'


async def test_charge_store_as_merchant():
    charge = await openpay.Charge.create(**DUMMY_CHARGE_STORE)

    assert isinstance(charge, openpay.Charge)
    assert hasattr(charge, 'payment_method')
    assert hasattr(charge.payment_method, 'reference')
    assert hasattr(charge.payment_method, 'barcode_url')
    assert charge.payment_method.type == "store"

    charge_res = await openpay.Charge.retrieve_as_merchant(charge.id)
    assert charge_res.status == 'in_progress'
