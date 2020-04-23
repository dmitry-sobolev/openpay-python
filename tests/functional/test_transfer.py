import pytest

import openpay
from tests.functional.conftest import customer
from tests.functional.helpers import generate_order_id

pytestmark = pytest.mark.asyncio


second_customer = customer


@pytest.fixture
async def charge_customer(customer, card):
    await customer.charges.create(
        source_id=card.id, method="card",
        amount=10, description="Test Charge",
        order_id=generate_order_id())


async def test_transfer_create(customer, second_customer, charge_customer):
    transfer = await customer.transfers.create(
        customer_id=second_customer.id, amount=10,
        description="Test transfer", order_id=generate_order_id())
    assert isinstance(transfer, openpay.Transfer)
    assert hasattr(transfer, 'id')


async def test_transfer_list_all(customer):
    transfer_list = await customer.transfers.all()
    assert isinstance(transfer_list, openpay.resource.ListObject)
    assert isinstance(transfer_list.data, list)
    assert transfer_list.count == len(transfer_list.data)


async def test_transfer_retrieve(customer, second_customer, charge_customer):
    transfer = await customer.transfers.create(
        customer_id=second_customer.id, amount=10,
        description="Test transfer", order_id=generate_order_id())

    transfer_list = await customer.transfers.all()
    test_transfer = transfer_list.data[0]

    assert test_transfer.id == transfer.id

    transfer = await customer.transfers.retrieve(test_transfer.id)
    assert isinstance(transfer, openpay.Transfer)


async def test_list_transfers():
    customer = await openpay.Customer.retrieve("amce5ycvwycfzyarjf8l")
    transfers = await customer.transfers.all()
    assert isinstance(transfers.data, list)
    assert isinstance(transfers.data[0], openpay.Transfer)
