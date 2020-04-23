import pytest

import openpay
from tests.functional.helpers import generate_order_id

pytestmark = pytest.mark.asyncio


@pytest.fixture
async def bank_account(customer):
    return await customer.bank_accounts.create(
        clabe="646180109490002822",
        alias="Cuenta principal",
        holder_name="John Doe")


async def test_create_payout_with_bank_account(customer, bank_account):
    payout = await customer.payouts.create(
        method='bank_account',
        destination_id=bank_account.id,
        amount="10",
        description="First payout",
        order_id=generate_order_id())

    assert hasattr(payout, 'id')
    assert isinstance(payout, openpay.Payout)


async def test_list_all_payout(customer):
    payout_list = await customer.payouts.all()
    assert isinstance(payout_list.data, list)
    assert len(payout_list.data) == payout_list.count
