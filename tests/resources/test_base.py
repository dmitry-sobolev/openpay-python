import pytest

import openpay


def test_initialize_w_parameters():
    obj = openpay.resource.BaseObject(
        'foo', 'bar', myparam=5, yourparam='boo')

    assert obj.id == 'foo'
    assert obj.api_key == 'bar'


def test_get_resource_data():
    obj = openpay.resource.BaseObject.construct_from(
        {'id': 'myid', 'myattr': 5}, 'mykey'
    )

    assert obj.get('notattr', 'def') == 'def'
    assert obj.get('notattr') is None

    assert obj.setdefault('myattr', 'sdef') == 5
    assert obj.myattr == 5
    assert obj['myattr'] == 5
    assert obj.get('myattr') == 5


def test_set_resource_data():
    obj = openpay.resource.BaseObject('myid', 'mykey', myparam=5)

    # Setters
    obj.myattr = 'myval'
    obj['myitem'] = 'itval'

    assert obj.setdefault('mydef', 'sdef') == 'sdef'

    # Getters
    assert obj.myattr == 'myval'

    assert dict(**obj) == {
        'id': 'myid', 'myattr': 'myval', 'mydef': 'sdef', 'myitem': 'itval'
    }


def test_illegal_operations():
    obj = openpay.resource.BaseObject('myid', 'mykey', myparam=5)

    # Empty
    with pytest.raises(AttributeError):
        obj.myattr

    with pytest.raises(KeyError):
        obj['myattr']

    with pytest.raises(ValueError):
        obj.foo = ''

    with pytest.raises(TypeError):
        del obj['myattr']


def test_refresh_from():
    obj = openpay.resource.BaseObject.construct_from({
        'foo': 'bar',
        'trans': 'me',
    }, 'mykey')

    assert obj.api_key == 'mykey'
    assert obj.foo == 'bar'
    assert obj['trans'] == 'me'

    obj.refresh_from({
        'foo': 'baz',
        'johnny': 5,
    }, 'key2')

    assert obj.api_key == 'key2'
    assert obj.johnny == 5
    assert obj.foo == 'baz'

    with pytest.raises(KeyError):
        obj['trans']

    obj.refresh_from({
        'trans': 4,
        'metadata': {'amount': 42}
    }, 'key2', True)

    assert obj.foo == 'baz'
    assert obj.trans == 4
    assert obj._previous_metadata == {'amount': 42}
