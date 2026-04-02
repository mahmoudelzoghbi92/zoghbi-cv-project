import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, patch


@pytest.fixture
def mock_collection():
    collection = AsyncMock()
    collection.find_one.return_value = {"_id": "counts", "likes": 0, "dislikes": 0}
    collection.insert_one.return_value = None
    collection.update_one.return_value = None
    return collection


@pytest.mark.asyncio
async def test_health(mock_collection):
    with patch("app.main.collection", mock_collection):
        from app.main import app
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.get("/health")
            assert response.status_code == 200
            assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_get_counts(mock_collection):
    with patch("app.main.collection", mock_collection):
        from app.main import app
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.get("/api/counts")
            assert response.status_code == 200
            data = response.json()
            assert "likes" in data
            assert "dislikes" in data


@pytest.mark.asyncio
async def test_like(mock_collection):
    mock_collection.find_one.return_value = {"_id": "counts", "likes": 1, "dislikes": 0}
    with patch("app.main.collection", mock_collection):
        from app.main import app
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.post("/api/like")
            assert response.status_code == 200
            assert response.json()["likes"] == 1


@pytest.mark.asyncio
async def test_dislike(mock_collection):
    mock_collection.find_one.return_value = {"_id": "counts", "likes": 0, "dislikes": 1}
    with patch("app.main.collection", mock_collection):
        from app.main import app
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.post("/api/dislike")
            assert response.status_code == 200
            assert response.json()["dislikes"] == 1