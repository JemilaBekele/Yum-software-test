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

    def test_valid_sortfood(self):
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

            # Find and click the sortfood button
            sortfood_field_xpath = "//*[@id='menu']/div[2]/div[1]/aside/div/div/ul/li[15]/a/span"
            sortfood_button = WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.XPATH, sortfood_field_xpath))
            )
            sortfood_button.click()

            # Verify that clicking the sortfood button redirects to the expected page
            expected_url = "https://yum.co.ke/menu/grilll-shack#cat947"  # Replace with the actual expected URL
            wait.until(EC.url_to_be(expected_url))
            assert self.driver.current_url == expected_url, "Redirection to expected page failed."
            
        except TimeoutException:
            print("Element not found within the provided time")
        except NoSuchElementException as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    
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

            # Find and click the remove from cart button
            removefromcart_field_xpath = "//*[@id='wrapper']/div[6]/div[2]/div/div/div[1]/div[2]/div[2]/aside/div[1]/div/div[2]/div/ul/li[1]/div/div/span[1]/a[2]/span/i[2]"
            removefromcart_button = WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.XPATH, removefromcart_field_xpath))
            )
            removefromcart_button.click()

            # Verify that clicking the remove from cart button redirects to the expected page
            expected_url = "https://yum.co.ke/menu/grilll-shack#cat947"  # Replace with the actual expected URL
            wait.until(EC.url_to_be(expected_url))
            assert self.driver.current_url == expected_url, "Redirection to expected page failed."
            
        except TimeoutException:
            print("Element not found within the provided time")
        except NoSuchElementException as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def test_valid_cuisine(self):
        try:
            # Perform login
            self.perform_login()
            
            # Find the cuisine filter button and click it
            cuisine_field_xpath = "//*[@id='wrapper']/div[7]/div/div/div/div[2]/div[1]/aside/div/div/div[1]/label"
            cuisine_button = WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.XPATH, cuisine_field_xpath))
            )
            cuisine_button.click()

            # Verify that clicking the cuisine button redirects to the expected page
            expected_url = "https://yum.co.ke/neighborhood/kilimani-east/"  # Replace with the actual expected URL
            wait = WebDriverWait(self.driver, 60)
            wait.until(EC.url_to_be(expected_url))
            assert self.driver.current_url == expected_url, "Redirection to expected page failed."
            
        except TimeoutException:
            print("Element not found within the provided time")
        except NoSuchElementException as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
