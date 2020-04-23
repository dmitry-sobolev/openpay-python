import pytest

import openpay
from tests.resources.helpers import MyListable


@pytest.fixture
def list_req_mock(request_mock):
    return request_mock([{'foo': 'bar', }])


@pytest.fixture
def list_resource():
    return openpay.resource.ListObject.construct_from({
        'id': 'me',
        'url': '/my/path',
        'item_type': 'charge'
    }, 'mykey')


@pytest.mark.asyncio
@pytest.mark.parametrize('method,http_method,oid,params', [
    ('all', 'get', None, {'myparam': 'you'}),
    ('create', 'post', None, {'myparam': 'eter'}),
    ('retrieve', 'get', 'myid', {'myparam': 'cow'})
])
async def test_list_methods(
        method, http_method, oid, params, list_resource, list_req_mock
):
    method_call = getattr(list_resource, method)

    args = (oid, ) if oid is not None else ()

    res = await method_call(*args, **params)

    url = '/my/path'
    if oid:
        url += f'/{oid}'

    list_req_mock.assert_called_with(http_method, url, params)

    assert isinstance(res.data[0], openpay.Charge)
    assert res.data[0].foo == 'bar'


@pytest.mark.asyncio
async def test_listable_all(request_mock):
    mk = request_mock([
        {
            'object': 'charge',
            'name': 'jose',
        },
        {
            'object': 'charge',
            'name': 'curly',
        }
    ])

    res = await MyListable.all()
    url = f'/v1/{openpay.merchant_id}/mylistables'
    mk.assert_called_with('get', url, {})

    assert len(res.data) == 2
    assert (all(isinstance(obj, openpay.Charge) for obj in res.data))

    assert res.data[0].name == 'jose'
    assert res.data[1].name == 'curly'
