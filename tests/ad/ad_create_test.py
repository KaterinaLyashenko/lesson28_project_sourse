import pytest
from rest_framework import status
from tests.fixtures import access_token
from tests.factories import UserFactory, CategoryFactory


@pytest.mark.django_db
def test_ad_crate(client, access_token):
    user = UserFactory.create()
    category = CategoryFactory.create()

    data = {
        "author": user.username,
        "category": category.name,
        "name": "Длинное название",
        "price": 313
    }

    expected_data = {
        "id": 1,
        "category": category.name,
        "author": user.username,
        "is_published": False,
        "name": "Длинное название",
        "price": 313,
        "description": None,
        "image": None
    }

    response = client.post("/ad/", data=data, HTTP_AUTHORIZATION=f"Bearer {access_token}")
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data == expected_data
