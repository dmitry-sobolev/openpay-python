from unittest.mock import AsyncMock

import pytest


@pytest.fixture
def request_mock(mocker):
    def _mock_builder(return_val):
        mock = mocker.patch(
            'openpay.api.APIClient.request',
            return_value=(return_val, 'reskey')
        )

        return mock

    return _mock_builder
