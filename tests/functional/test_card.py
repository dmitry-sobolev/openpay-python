import pytest

import openpay

pytestmark = pytest.mark.asyncio


async def test_card_created(card):
    assert isinstance(card, openpay.Card)


async def test_card_list_all(customer, card):
    card_list = await customer.cards.all()
    assert card_list.count == 1
    assert len(card_list.data) == card_list.count
    assert isinstance(card_list, openpay.resource.ListObject)
    assert card_list.data[0].id == card.id


async def test_card_retrieve(customer, card):
    retrieved_card = await customer.cards.retrieve(card.id)

    assert card.id == retrieved_card.id


async def test_card_delete(card):
    await card.delete()
    assert list(card.keys()) == []
