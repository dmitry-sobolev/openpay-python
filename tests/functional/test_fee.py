import pytest

import openpay
from tests.functional.helpers import generate_order_id

pytestmark = pytest.mark.asyncio


async def test_fee_create(customer, card):
    await customer.charges.create(
        source_id=card.id, method="card",
        amount=10, description="Test Charge",
        order_id=generate_order_id())
    
    fee = await openpay.Fee.create(
        customer_id=customer.id, amount=5,
        description="Test Fee", order_id=generate_order_id())
    assert isinstance(fee, openpay.Fee)
    assert hasattr(fee, 'id')


async def test_fee_list_all():
    fee_list = await openpay.Fee.all()
    assert isinstance(fee_list, openpay.resource.ListObject)
    assert isinstance(fee_list.data, list)
    assert fee_list.count == len(fee_list.data)

