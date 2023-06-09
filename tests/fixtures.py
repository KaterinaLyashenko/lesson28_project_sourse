import pytest

from tests.factories import UserFactory


@pytest.fixture
@pytest.mark.django_db
def access_token(client, django_user_model):
    #test_user = UserFactory.create()
    username = "test"
    password = "qwe123"
    django_user_model.objects.create(username=username, password=password)
    response = client.post("/user/token/", data={"username": username, "password": password})
    print(response)
    return response.data.get("access")

@pytest.fixture
@pytest.mark.django_db
def user_with_access_token(client, django_user_model):
    #test_user = UserFactory.create()
    username = "test"
    password = "qwe123"
    user = django_user_model.objects.create(username=username, password=password)
    response = client.post("/user/token/", data={"username": username, "password": password})
    return user, response.data.get("access")