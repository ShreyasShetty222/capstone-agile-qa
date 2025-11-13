import os
import pytest

def pytest_addoption(parser):
    \"\"\"Register CLI options used by local runs and CI.\"\"\"
    parser.addoption(
        \"--browser\",
        action=\"store\",
        default=None,
        help=\"Browser name (chrome or firefox). Can also be set via BROWSER env var.\"
    )
    parser.addoption(
        \"--headless\",
        action=\"store_true\",
        default=False,
        help=\"Run browsers in headless mode (useful for CI). Can also be set via HEADLESS env var (true/1/yes).\"
    )

@pytest.fixture(scope=\"session\")
def browser_name(request):
    # priority: CLI option --browser > BROWSER env var > default 'chrome'
    opt = request.config.getoption(\"--browser\")
    return opt or os.environ.get(\"BROWSER\", \"chrome\")

@pytest.fixture(scope=\"session")
def headless(request):
    # CLI option --headless has highest priority; otherwise read HEADLESS env var
    opt = request.config.getoption(\"--headless\")
    if opt:
        return True
    return os.environ.get(\"HEADLESS\", \"false\").lower() in (\"1\", \"true\", \"yes\")