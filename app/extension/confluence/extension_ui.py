import random

from selenium.webdriver.common.by import By

from selenium_ui.base_page import BasePage
from selenium_ui.conftest import print_timing
from selenium_ui.confluence.pages.pages import Login, AllUpdates
from util.conf import CONFLUENCE_SETTINGS


def app_specific_action(webdriver, datasets):
    page = BasePage(webdriver)

    # To run action as specific user uncomment code bellow.
    # NOTE: If app_specific_action is running as specific user, make sure that app_specific_action is running
    # just before test_2_selenium_z_log_out
    # @print_timing("selenium_app_specific_user_login")
    # def measure():
    #     def app_specific_user_login(username='admin', password='admin'):
    #         login_page = Login(webdriver)
    #         login_page.delete_all_cookies()
    #         login_page.go_to()
    #         login_page.wait_for_page_loaded()
    #         login_page.set_credentials(username=username, password=password)
    #         login_page.click_login_button()
    #         if login_page.is_first_login():
    #             login_page.first_user_setup()
    #         all_updates_page = AllUpdates(webdriver)
    #         all_updates_page.wait_for_page_loaded()
    #     app_specific_user_login(username='admin', password='admin')
    # measure()

    @print_timing("iframe for confluence")
    def view_edit_iframe():
        page.go_to_url(f"{CONFLUENCE_SETTINGS.server_url}/display/DC/Test+iframe")

        page.wait_until_visible((By.XPATH, "//a[@href='/display/DC/Test+iframe']"))
        page.wait_until_visible((By.XPATH, f"//iframe[@src='{CONFLUENCE_SETTINGS.server_url}/display/DC/Embedded']"))
        
        iframe = page.get_element((By.XPATH, f"//iframe[@src='{CONFLUENCE_SETTINGS.server_url}/display/DC/Embedded']"))
        webdriver.switch_to.frame(iframe)
        page.wait_until_visible((By.XPATH, "//a[@href='/display/DC/Embedded']"))

        webdriver.switch_to.default_content()
        webdriver.execute_script("arguments[0].setAttribute('src',arguments[1])", iframe, f"{CONFLUENCE_SETTINGS.server_url}/display/DC/Embedded+2")
        iframe2 = page.get_element((By.XPATH, f"//iframe[@src='{CONFLUENCE_SETTINGS.server_url}/display/DC/Embedded+2']"))
        webdriver.switch_to.frame(iframe2)
        page.wait_until_visible((By.XPATH, "//a[@href='/display/DC/Embedded+2']"))
        
    view_edit_iframe()
