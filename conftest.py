import os
import pytest

def pytest_addoption(parser):
    """
    Register the --browser option so pytest will accept it anywhere (CI or local).
    If CI sets env BROWSER, tests will use that when --browser is not provided.
    """
    parser.addoption(
        "--browser",
        action="store",
        default=None,
        help="Browser name (chrome or firefox). Can also be set via BROWSER env var."
    )

@pytest.fixture(scope="session")
def browser_name(request):
    # priority: CLI option --browser > BROWSER env var > default 'chrome'
    opt = request.config.getoption("--browser")
    return opt or os.environ.get("BROWSER", "chrome")