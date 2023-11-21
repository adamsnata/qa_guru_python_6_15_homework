import pytest
from selene import browser, have


@pytest.fixture(params=[(1920, 1080), (1600, 900), (1440, 900), (1366, 768), (375, 667), (360, 780), (414, 896),
                        (360, 720)],
                scope='function',
                autouse=True)
def browser_manager(request):
    browser.config.base_url = 'https://github.com'
    browser.config.window_width = request.param[0]
    browser.config.window_height = request.param[1]
    yield
    browser.quit()


def mobile_window(width, height):
    return width < height


def test_github_desktop(browser_manager):
    if mobile_window(browser.config.window_width, browser.config.window_height):
        pytest.skip('Этот тест только для ПК версии сайта')
    browser.open('/')
    browser.element('[class~="HeaderMenu-link--sign-in"]').click()
    browser.element('[class="auth-form-header p-0"]').should(have.text('Sign in to GitHub'))


def test_github_mobile(browser_manager):
    if not mobile_window(browser.config.window_width, browser.config.window_height):
        pytest.skip('Этот тест только для мобильной версии сайта')
    browser.open('/')
    browser.element('[class="flex-1 flex-order-2 text-right"] .Button-content').click()
    browser.element('[class~="HeaderMenu-link--sign-in"]').click()
    browser.element('[class="auth-form-header p-0"]').should(have.text('Sign in to GitHub'))
