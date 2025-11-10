def pytest_addoption(parser):
    parser.addoption("--headless", action="store", default=None)
