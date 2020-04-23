import pytest

import openpay
from tests.resources.helpers import MyResource, MySingleton, MyCreatable, \
    MyUpdateable, MyDeletable


@pytest.mark.asyncio
async def test_retrieve_and_refresh(request_mock):
    mk = request_mock({
        'id': 'foo2',
        'bobble': 'scrobble',
    })

    res = await MyResource.retrieve('foo*', myparam=5)

    url = f'/v1/{openpay.merchant_id}/myresources/foo%2A'

    mk.assert_called_with('get', url, {'myparam': 5})

    assert res.bobble == 'scrobble'
    assert res.id == 'foo2'
    assert res.api_key == 'reskey'

    mk = request_mock({
        'frobble': 5,
    })

    res = await res.refresh()
    url = f'/v1/{openpay.merchant_id}/myresources/foo2'

    mk.assert_called_with('get', url, {'myparam': 5})

    assert res.frobble == 5
    with pytest.raises(AttributeError):
        res.bobble


def test_convert_to_openpay_object():
    sample = {
        'foo': 'bar',
        'adict': {
            'object': 'charge',
            'id': 42,
            'amount': 7,
        },
        'alist': [
            {
                'object': 'customer',
                'name': 'chilango'
            }
        ]
    }

    converted = openpay.resource.convert_to_openpay_object(sample, 'akey')

    # Types
    assert isinstance(converted, openpay.resource.BaseObject)
    assert isinstance(converted.adict, openpay.Charge)
    assert len(converted.alist) == 1
    assert isinstance(converted.alist[0], openpay.Customer)

    # Values
    assert converted.foo == 'bar'
    assert converted.adict.id == 42
    assert converted.alist[0].name == 'chilango'


@pytest.mark.asyncio
async def test_singleton_retrieve(request_mock):
    mk = request_mock({'single': 'ton'})

    res = await MySingleton.retrieve()
    url = f'/v1/{openpay.merchant_id}/mysingleton'
    mk.assert_called_with('get', url, {})

    assert res.single == 'ton'


@pytest.mark.asyncio
async def test_create(request_mock):
    mk = request_mock({
        'object': 'charge',
        'foo': 'bar',
    })

    res = await MyCreatable.create()
    url = '/v1/{0}/mycreatables'.format(openpay.merchant_id)
    mk.assert_called_with('post', url, {})

    assert isinstance(res, openpay.Charge)
    assert res.foo == 'bar'


@pytest.fixture
def update_req_mock(request_mock):
    return request_mock({'thats': 'it'})


@pytest.fixture
async def update_resource():
    return MyUpdateable.construct_from({
        'id': 'myid',
        'foo': 'bar',
        'baz': 'boz',
        'metadata': {
            'size': 'l',
            'score': 4,
            'height': 10
        }
    }, 'mykey')


@pytest.mark.asyncio
async def test_update_save(update_resource, update_req_mock):
    update_resource.baz = 'updated'
    update_resource.other = 'newval'
    update_resource.metadata.size = 'm'
    update_resource.metadata.info = 'a2'
    update_resource.metadata.height = None

    res = await update_resource.save()

    assert res is update_resource
    assert update_resource.thats == 'it'
    with pytest.raises(AttributeError):
        update_resource.baz

    update_req_mock.assert_called_with(
        'put',
        f'/v1/{openpay.merchant_id}/myupdateables/myid',
        MyUpdateable.construct_from({
            'id': 'myid',
            'foo': 'bar',
            'baz': 'updated',
            'other': 'newval',
            'status': None,
            'metadata': {
                'size': 'm',
                'info': 'a2',
                'height': None,
                'score': 4
            }
        }, 'mykey')
    )


@pytest.mark.asyncio
async def test_update_save_replace_metadata(update_resource, update_req_mock):
    update_resource.baz = 'updated'
    update_resource.other = 'newval'
    update_resource.metadata = {
        'size': 'm',
        'info': 'a2',
        'score': 4,
    }

    res = await update_resource.save()

    assert res is update_resource
    assert update_resource.thats == 'it'
    with pytest.raises(AttributeError):
        update_resource.baz

    update_req_mock.assert_called_with(
        'put',
        f'/v1/{openpay.merchant_id}/myupdateables/myid',
        MyUpdateable.construct_from({
            'id': 'myid',
            'foo': 'bar',
            'baz': 'updated',
            'other': 'newval',
            'status': None,
            'metadata': {
                'size': 'm',
                'info': 'a2',
                'height': '',
                'score': 4
            }
        }, 'mykey')
    )


@pytest.mark.asyncio
async def test_delete(request_mock):
    request_mock({
        'id': 'mid',
        'deleted': True,
    })

    obj = MyDeletable.construct_from({
        'id': 'mid'
    }, 'mykey')

    res = await obj.delete()
    assert res is obj

    assert obj.deleted == True
    assert obj.id == 'mid'
