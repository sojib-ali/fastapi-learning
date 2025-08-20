import os
import httpx
import pytest



def pytest_configure(config):
    """
    Allows plugins and conftest files to perform initial configuration.
    This hook is called for every plugin and initial conftest file
    after command line options have been parsed.
    """
    os.environ["DATABASE_URL"] = "mongodb://172.17.240.1:27017/testdb"
    os.environ["SECRET_KEY"] = "a_very_secret_key_for_testing"


@pytest.fixture(scope="session")
async def default_client():
    """
    Yield an httpx client for testing the API.
    Handles app lifespan and database cleanup.
    """
    # Import the app and models here, inside the fixture.
    # By the time this fixture is called, pytest_configure has already
    # run and set the necessary environment variables.
    from main import app
    from models.events import Event
    from models.users import User

    async with httpx.AsyncClient(app=app, base_url="http://app") as client:
        yield client
        # Teardown: clean up the test database after the session
        await Event.delete_all()
        await User.delete_all()