import os
import sys
from unittest.mock import patch
import pytest

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import places_search


class FakeResponse:
    def __init__(self, data, status=200):
        self._data = data
        self.status = status

    async def json(self):
        return self._data

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        pass


@pytest.mark.asyncio
async def test_buscar_lugares_async_parsing():
    data_nearby = {
        "results": [
            {"name": "Store A", "vicinity": "Addr", "place_id": "1"}
        ]
    }
    data_details = {
        "status": "OK",
        "result": {"formatted_phone_number": "123", "types": ["hardware_store"]}
    }

    async def fake_get(url, params=None):
        if "nearbysearch" in url:
            return FakeResponse(data_nearby)
        return FakeResponse(data_details)

    with patch("aiohttp.ClientSession.get", side_effect=fake_get):
        results = await places_search.buscar_lugares_async("key", 0, 0, 100, "kw", True)
        assert results[0]["telefono"] == "123"
        assert results[0]["categoria"] == "Hardware Store"

