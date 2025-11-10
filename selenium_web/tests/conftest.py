import os
import pytest
from selenium_web.utils.driver_factory import create_driver
from selenium_web.utils.settings import CONFIG

@pytest.fixture
def driver(request):
    # CLI flag overrides env; else use settings
    opt = request.config.getoption("--headless")
    headless = CONFIG["headless"] if opt in (None, "",) else str(opt).lower() == "true"
    d = create_driver(headless=headless)
    yield d
    d.quit()

@pytest.fixture
def base_url():
    return CONFIG["base_url"]
