import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class TestLogin:
    @pytest.fixture(autouse=True)
    def setup(self, request):
        self.driver = webdriver.Chrome()
        self.driver.get("https://yum.co.ke/login/")
        yield
        self.driver.quit()

        # Generate the HTML report
        report_file = request.config.getoption("--html")
        if report_file:
            try:
                self.driver.save_screenshot("screenshot.png")
            except Exception as e:
                print(f"Error capturing screenshot: {e}")

    def test_valid_login(self):
        try:
            # Find the username and password input fields
            phone_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='id_email_address']"))
            )
            password_field = self.driver.find_element(By.XPATH, "//*[@id='id_password']")

            # Enter the username and password
            phone_field.send_keys("+254712367651")
            password_field.send_keys("!QAZXsw2#EDC")

            # Find the login button and click it
            login_button = self.driver.find_element(By.XPATH, "//*[@id='submit-id-login']")
            login_button.click()

            # Wait for the page to load after the login
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.url_contains("wp-admin"))

            # Check if the login was successful
            current_url = self.driver.current_url
            assert "wp-admin" in current_url, "Login failed."

        except TimeoutException:
            print("Element not found within the provided time")
        except NoSuchElementException as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def test_invalid_password(self):
        try:
            # Find the username and password input fields
            phone_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='id_email_address']"))
            )
            password_field = self.driver.find_element(By.XPATH, "//*[@id='id_password']")

            # Enter the username and password
            phone_field.send_keys("+254712367651")
            password_field.send_keys("wrongpassword")

            # Find the login button and click it
            login_button = self.driver.find_element(By.XPATH, "//*[@id='submit-id-login']")
            login_button.click()

            # Wait for the page to load after the login
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.url_contains("wp-admin"))

            # Check if the login was successful
            current_url = self.driver.current_url
            assert "wp-admin" in current_url, "Login succeeded with invalid password."

        except TimeoutException:
            print("Element not found within the provided time")
        except NoSuchElementException as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def test_invalid_Email(self):
        try:
            # Find the username and password input fields
            phone_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='id_email_address']"))
            )
            password_field = self.driver.find_element(By.XPATH, "//*[@id='id_password']")

            # Enter the username and password
            phone_field.send_keys("jemillllabebe@gmail.com")
            password_field.send_keys("!QAZXsw2#EDC")

            # Find the login button and click it
            login_button = self.driver.find_element(By.XPATH, "//*[@id='submit-id-login']")
            login_button.click()

            # Wait for the page to load after the login
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.url_contains("wp-admin"))

            # Check if the login was successful
            current_url = self.driver.current_url
            assert "wp-admin" in current_url, "Login succeeded with invalid phone."

        except TimeoutException:
            print("Element not found within the provided time")
        except NoSuchElementException as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def test_empty_username(self):
        try:
            # Find the username and password input fields
            phone_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='id_email_address']"))
            )
            password_field = self.driver.find_element(By.XPATH, "//*[@id='id_password']")

            # Enter the password
            password_field.send_keys("!QAZXsw2#EDC")

            # Find the login button and click it
            login_button = self.driver.find_element(By.XPATH, "//*[@id='submit-id-login']")
            login_button.click()

            # Wait for the page to load after the login
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.url_contains("wp-admin"))

            # Check if the login was successful
            current_url = self.driver.current_url
            assert "wp-admin" in current_url, "Login succeeded with empty username."

        except TimeoutException:
            print("Element not found within the provided time")
        except NoSuchElementException as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def test_empty_password(self):
        try:
            # Find the username and password input fields
            phone_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='id_email_address']"))
            )
            password_field = self.driver.find_element(By.XPATH, "//*[@id='id_password']")

            # Enter the username
            phone_field.send_keys("+254712367651")

            # Find the login button and click it
            login_button = self.driver.find_element(By.XPATH, "//*[@id='submit-id-login']")
            login_button.click()

            # Wait for the page to load after the login
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.url_contains("wp-admin"))

            # Check if the login was successful
            current_url = self.driver.current_url
            assert "wp-admin" in current_url, "Login succeeded with empty password."

        except TimeoutException:
            print("Element not found within the provided time")
        except NoSuchElementException as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    pytest.main(["-v", "--html=loginreport.html"])
