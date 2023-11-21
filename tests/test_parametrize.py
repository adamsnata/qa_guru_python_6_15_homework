import pytest
from selene import browser, have


@pytest.fixture(params=[(1920, 1080), (1600, 900), (1440, 900), (1366, 768), (375, 667), (414, 896), (360, 780),
                        (360, 720)],
                scope='function',
                autouse=True)
def browser_manager(request):
    browser.config.base_url = 'https://github.com'
    browser.config.window_width = request.param[0]
    browser.config.window_height = request.param[1]
    yield
    browser.quit()


desktop = pytest.mark.parametrize('browser_manager', [(1920, 1080), (1600, 900), (1440, 900), (1366, 768)],
                                  indirect=True)
mobile = pytest.mark.parametrize('browser_manager', [(375, 667), (414, 896), (780, 844), (360, 720)], indirect=True)


@desktop
def test_github_desktop(browser_manager):
    browser.open('/')
    browser.element("a[href='/login']").click()
    browser.element('.auth-form-header').should(have.exact_text('Sign in to GitHub'))


@mobile
def test_github_mobile(browser_manager):
    browser.open('/')
    browser.element('.flex-1 button').click()
    browser.element("a[href='/login']").click()
    browser.element('.auth-form-header').should(have.exact_text('Sign in to GitHub'))
