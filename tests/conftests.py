from pytest_factoryboy import register

from tests.factories import *

pytest_plugin = "tests.fixtures"

register(UserFactory)
register(CategoryFactory)
register(AdFactory)