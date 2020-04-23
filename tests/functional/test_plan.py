import pytest

import openpay
from tests.functional.helpers import DUMMY_PLAN

pytestmark = pytest.mark.asyncio


async def test_create_plan():
    with pytest.raises(openpay.error.InvalidRequestError):
        await openpay.Plan.create(amount=250)

    p = await openpay.Plan.create(**DUMMY_PLAN)
    assert hasattr(p, 'amount')
    assert hasattr(p, 'id')
    assert DUMMY_PLAN['amount'] == p.amount

    await p.delete()
    assert list(p.keys()) == []


async def test_update_plan():
    p = await openpay.Plan.create(**DUMMY_PLAN)
    name = "New plan name"
    p.name = name

    await p.save()

    assert name == p.name

    await p.delete()


async def test_update_plan_without_retrieving():
    p = await openpay.Plan.create(**DUMMY_PLAN)

    name = 'updated plan name!'
    plan = openpay.Plan(p.id)
    plan.name = name

    # should only have name and id
    assert sorted(['id', 'name']) == sorted(plan.keys())
    await plan.save()

    assert name == plan.name
    # should load all the properties
    assert p.amount == plan.amount

    await p.delete()
