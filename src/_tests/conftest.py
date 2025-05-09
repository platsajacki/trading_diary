import pytest

from _tests import FixtureFactory


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


pytest_plugins = [
    '_tests.fixtures.clients',
    '_tests.fixtures.finances',
]


@pytest.fixture
def factory() -> FixtureFactory:
    return FixtureFactory()
