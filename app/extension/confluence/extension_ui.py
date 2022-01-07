import random

from selenium.webdriver.common.by import By

from selenium_ui.base_page import BasePage
from selenium_ui.conftest import print_timing
from selenium_ui.confluence.pages.pages import Login, AllUpdates
from util.conf import CONFLUENCE_SETTINGS


def app_specific_action(webdriver, datasets):
    page = BasePage(webdriver)

    @print_timing("selenium_app_specific_user_login")
    def login_admin_user():
        def app_specific_user_login(username='admin', password='admin'):
            login_page = Login(webdriver)
            login_page.delete_all_cookies()
            login_page.go_to()
            login_page.wait_for_page_loaded()
            login_page.set_credentials(username=username, password=password)
            login_page.click_login_button()
            if login_page.is_first_login():
                login_page.first_user_setup()
            all_updates_page = AllUpdates(webdriver)
            all_updates_page.wait_for_page_loaded()
        app_specific_user_login(username='admin', password='admin')
    login_admin_user()

    @print_timing("iframe for confluence settings")
    def iframe_settings():
        page.go_to_url(f"{CONFLUENCE_SETTINGS.server_url}/admin/plugins/iframed/config.action")
        page.wait_until_visible((By.ID, "add-list"))

        ip_input = page.get_element((By.ID, "list-input"))
        ip_input.send_keys("https://atlasauthority.com")

        add_button = page.get_element((By.ID, "add-list"))
        add_button.click()

        page.wait_until_visible((By.XPATH, "//option[@value='https://atlasauthority.com']"))

        submit_button = page.get_element((By.ID, "submit-button"))
        submit_button.click()
    iframe_settings()
