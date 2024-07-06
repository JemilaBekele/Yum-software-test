import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class TestSearch:
    @pytest.fixture(autouse=True)
    def setup(self, request):
        try:
            self.driver = webdriver.Chrome()
            self.driver.get("https://yum.co.ke/login/")
        except Exception as e:
            print(f"Error setting up the test suite: {e}")
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
            wait = WebDriverWait(self.driver, 60)
            try:
                close_button = self.driver.find_element(By.XPATH, "//*[@id='modalUser']/div/div/div[1]/button/i")
                close_button = WebDriverWait(self.driver, 100).until(
                EC.presence_of_element_located((By.XPATH, close_button))
            )
                close_button.click()
            except NoSuchElementException:
                print("No modal to close after login.")
        except Exception as e:
            self.driver.save_screenshot("login_error.png")
            raise e

    def test_valid_Restaurant(self):
        try:
            # Perform login
            self.perform_login()

            # Find the search input field and enter a valid search term
            search_field_xpath = "//*[@id='wrapper']/div[3]/nav/div/div[2]/ul/li[3]/span/form/div/div/span/input"
            search_field = WebDriverWait(self.driver, 100).until(
                EC.presence_of_element_located((By.XPATH, search_field_xpath))
            )
            search_field.send_keys("Grilll Shack")
            search_field.send_keys(Keys.RETURN)  # Simulate pressing Enter key

            # Verify that the expected page is loaded
            search_term = "Grilll Shack"
            assert search_term.lower() in self.driver.page_source.lower(), f"Failed to navigate to search: {search_term}"

        except TimeoutException:
            print("Element not found within the provided time")
        except NoSuchElementException as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def test_invalid_search(self):
        try:
            # Perform login
            self.perform_login()

            # Find the search input field and enter an invalid search term
            search_field_xpath = "//*[@id='wrapper']/div[3]/nav/div/div[2]/ul/li[3]/span/form/div/div/span/input"
            search_field = WebDriverWait(self.driver, 100).until(
                EC.presence_of_element_located((By.XPATH, search_field_xpath))
            )
            search_field.send_keys("InvalidSearchTerm12345")
            search_field.send_keys(Keys.RETURN)  # Simulate pressing Enter key

            # Wait for the URL to contain "wp-admin"
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.url_contains("wp-admin"))

            # Check if the URL contains "wp-admin"
            current_url = self.driver.current_url
            assert "wp-admin" in current_url, "Element 'wp-admin' not found in URL"

        except TimeoutException:
            print("Element 'wp-admin' not found within the provided time")
        except NoSuchElementException as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


    def test_valid_Cuisines(self):
        try:
            # Perform login
            self.perform_login()

            # Find the search input field and enter a valid search term
            search_field_xpath = "//*[@id='wrapper']/div[3]/nav/div/div[2]/ul/li[3]/span/form/div/div/span/input"
            search_field = WebDriverWait(self.driver, 100).until(
                EC.presence_of_element_located((By.XPATH, search_field_xpath))
            )
            search_field.send_keys("Ethiopian")
            search_field.send_keys(Keys.RETURN)  # Simulate pressing Enter key

            # Verify that the expected page is loaded
            search_term = "Ethiopian"
            assert search_term.lower() in self.driver.page_source.lower(), f"Failed to navigate to search: {search_term}"

        except TimeoutException:
            print("Element not found within the provided time")
        except NoSuchElementException as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")