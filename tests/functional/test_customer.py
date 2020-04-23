import datetime
import time

import pytest

import openpay
from tests.functional.helpers import generate_order_id, DUMMY_CARD, DUMMY_PLAN

pytestmark = pytest.mark.asyncio


@pytest.fixture
async def customers_plan():
    plan = await openpay.Plan.create(**DUMMY_PLAN)

    yield plan

    await plan.delete()


async def test_list_customers():
    customers = await openpay.Customer.all()
    assert isinstance(customers.data, list)


async def test_list_charges():
    customer = await openpay.Customer.create(
        name="Miguel Lopez",
        email="mlopez@example.com",
        description="foo bar")

    await customer.charges.create(
        amount=100, method="card",
        description="Customer test charge",
        order_id=generate_order_id(),
        card=DUMMY_CARD
    )

    charges = await customer.charges.all()

    assert len(charges.data) == 1


async def test_create_customer(customers_plan):
    with pytest.raises(openpay.error.InvalidRequestError):
        await openpay.Customer.create(plan=DUMMY_PLAN['id'])

    customer = await openpay.Customer.create(
        name="Miguel", last_name="Lopez", email="mlopez@example.com")

    subscription = await customer.subscriptions.create(
        plan_id=customers_plan.id, trial_days="0", card=DUMMY_CARD)

    assert isinstance(subscription, openpay.Subscription)

    await subscription.delete()
    await customer.delete()

    assert not hasattr(customer, 'subscription')
    assert not hasattr(customer, 'plan')


async def test_update_and_cancel_subscription(customers_plan):
    customer = await openpay.Customer.create(
        name="Miguel", last_name="Lopez", email="mlopez@example.com")

    sub = await customer.subscriptions.create(
        plan_id=customers_plan.id, card=DUMMY_CARD)

    sub.cancel_at_period_end = True
    await sub.save()
    assert sub.status == 'active'
    assert sub.cancel_at_period_end

    await sub.delete()


async def test_datetime_trial_end(customers_plan):
    trial_end = datetime.datetime.now() + datetime.timedelta(days=15)
    customer = await openpay.Customer.create(
        name="Miguel", last_name="Lopez", email="mlopez@example.com")
    subscription = await customer.subscriptions.create(
        plan_id=customers_plan.id, card=DUMMY_CARD,
        trial_end=trial_end.strftime('Y-m-d'))
    assert bool(subscription.id)


async def test_integer_trial_end(customers_plan):
    trial_end_dttm = datetime.datetime.now() + datetime.timedelta(days=15)
    trial_end_int = int(time.mktime(trial_end_dttm.timetuple()))
    customer = await openpay.Customer.create(name="Miguel",
                                             last_name="Lopez",
                                             email="mlopez@example.com")
    subscription = await customer.subscriptions.create(
        plan_id=customers_plan.id, card=DUMMY_CARD,
        trial_end=trial_end_int)

    assert bool(subscription.id)
