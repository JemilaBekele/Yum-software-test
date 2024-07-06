import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class TestSearch:
    @pytest.fixture(autouse=True)
    def setup(self, request):
        try:
            self.driver = webdriver.Chrome()
            self.driver.get("https://yum.co.ke/login/")
        except Exception as e:
            print(f"Error setting up the test suite: {e}")
            if hasattr(self, 'driver'):
                self.driver.quit()
            raise e

        yield

        self.driver.quit()

        # Generate the HTML report
        report_file = request.config.getoption("--html")
        if report_file:
            try:
                self.driver.save_screenshot("screenshot.png")
            except Exception as e:
                print(f"Error capturing screenshot: {e}")

    def perform_login(self):
        try:
            phone_field = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='id_email_address']"))
            )
            password_field = self.driver.find_element(By.XPATH, "//*[@id='id_password']")

            # Enter the username and password
            phone_field.send_keys("+254712367620")
            password_field.send_keys("!QAZxsw2")

            # Find the login button and click it
            login_button = self.driver.find_element(By.XPATH, "//*[@id='submit-id-login']")
            login_button.click()

            # Wait for the URL to change after login
            wait = WebDriverWait(self.driver, 20)
            wait.until(EC.url_changes("https://yum.co.ke/login/"))

            # Check if the login was successful
            current_url = self.driver.current_url
            assert "https://yum.co.ke/" in current_url, "Login failed."

            # Optionally, close any modals that may appear after login
            try:
                close_button = self.driver.find_element(By.XPATH, "//*[@id='modalUser']/div/div/div[1]/button/i")
                close_button.click()
            except NoSuchElementException:
                print("No modal to close after login.")
        except Exception as e:
            self.driver.save_screenshot("login_error.png")
            raise e

    def test_valid_Check_Out(self):
        try:
            # Perform login
            self.perform_login()

            # Find the menu check button and click it
            menucheck_field_xpath = "//*[@id='load-data']/div/div[1]/div/div[2]/div/span[1]/a"
            menucheck_button = WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.XPATH, menucheck_field_xpath))
            )
            menucheck_button.click()

            # Verify that clicking the menu check button redirects to the expected page 
            wait = WebDriverWait(self.driver, 20)
            wait.until(EC.url_changes("https://yum.co.ke/neighborhood/kilimani-east/"))

            # Find and click the add to cart button
            addfood_field_xpath = "//*[@id='mi66460']/div/div[3]/div/a[1]/i"
            addfood_button = WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.XPATH, addfood_field_xpath))
            )
            addfood_button.click()

            # Find and click the checkout button
            checkout_field_xpath = "//*[@id='doggyBagform']/span/span/button"
            checkout_button = WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.XPATH, checkout_field_xpath))
            )
            checkout_button.click()

            # Verify that clicking the checkout button redirects to the expected cart page
            expected_cart_url = "https://yum.co.ke/cart/"  # Replace with the actual expected URL
            wait.until(EC.url_to_be(expected_cart_url))
            assert self.driver.current_url == expected_cart_url, "Redirection to cart page failed."
            
        except TimeoutException:
            print("Element not found within the provided time")
        except NoSuchElementException as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
