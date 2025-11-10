import pytest
from conftest import CONFIG
from selenium_web.pages.login_page import LoginPage

@pytest.mark.smoke
def test_login_valid(driver, base_url):
    page = LoginPage(driver, base_url)
    page.open()
    page.login(CONFIG["user"], CONFIG["password"])
    msg = page.flash_text()
    assert "You logged into a secure area!" in msg

def test_login_invalid(driver, base_url):
    page = LoginPage(driver, base_url)
    page.open()
    page.login("wrong", "wrong")
    msg = page.flash_text()
    assert "Your username is invalid!" in msg or "Your password is invalid!" in msg
