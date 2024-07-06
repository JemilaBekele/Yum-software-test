import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class TestLogin:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://yum.co.ke/register/?next=/")
        try:
            # Wait for the dropdown element to be clickable and then click it
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div/div[4]/a"))
            ).click()
        except TimeoutException:
            print("Element not found or not clickable")
        yield
        self.driver.quit()

    def test_valid_registration(self):
        # Wait for the input fields to be present and then find them
        try:
            firstname_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='id_first_name']"))
            )
            lastname_field = self.driver.find_element(By.XPATH, "//*[@id='id_last_name']")
            email_field = self.driver.find_element(By.XPATH, "//*[@id='id_email']")
            phone_field = self.driver.find_element(By.XPATH, "//*[@id='id_phone']")
            password_field = self.driver.find_element(By.XPATH, "//*[@id='id_password']")
            confirmpassword_field = self.driver.find_element(By.XPATH, "//*[@id='id_conf_password']")

            firstname_field.send_keys("Jemila")
            lastname_field.send_keys("Bekele")
            email_field.send_keys("bekelehussen48@gmail.com")
            phone_field.send_keys("+254712367651")
            password_field.send_keys("!QAZXsw2#EDC")
            confirmpassword_field.send_keys("!QAZXsw2#EDC")

            # Find the checkbox and click it
            agree_checkboxinput = self.driver.find_element(By.XPATH, "//*[@id='id_agree_to_terms_and_conditions']")
            agree_checkboxinput.click()

            # Wait for the register button to be clickable and then click it
            register_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='wrapper']/div[6]/div/div/div/div/div[1]/div/div[2]/form/button"))
            )
            register_button.click()

            # Wait for the new address input fields to be present
            address_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='user_input_autocomplete_address']"))
            )
            address_field.send_keys("Cavalli @ The Manor, Westlands Road, Nairobi, Kenya")
            WebDriverWait(self.driver, 10)

            streetname_field = self.driver.find_element(By.XPATH, "//*[@id='id_street_name']")
            unit_field = self.driver.find_element(By.XPATH, "//*[@id='id_unit']")

            agree_radioinput = self.driver.find_element(By.XPATH, "//*[@id='id_address_or_landmark_1']")
            agree_radioinput.click()

            streetname_field.send_keys("73")
            unit_field.send_keys("9")

            # Find the submit button on the address form and click it
            address_submit_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='wrapper']/div[6]/div/div/div/div/div[1]/div/div[2]/form/button"))
            )
            address_submit_button.click()

            # Wait for the final page to load after address submission
            WebDriverWait(self.driver, 40).until(EC.url_contains("wp-admin"))

            # Check if the registration was successful by looking for a specific element that appears only upon successful registration
            success_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Welcome')]"))  # Update this XPath based on actual success element
            )

            assert success_element is not None, "Registration failed."
        except TimeoutException:
            print("Element not found within the provided time")
        except NoSuchElementException as e:
            print(f"Error: {e}")

    def test_invalid_password_confirmation(self):
        # Wait for the input fields to be present and then find them
        try:
            firstname_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='id_first_name']"))
            )
            lastname_field = self.driver.find_element(By.XPATH, "//*[@id='id_last_name']")
            email_field = self.driver.find_element(By.XPATH, "//*[@id='id_email']")
            phone_field = self.driver.find_element(By.XPATH, "//*[@id='id_phone']")
            password_field = self.driver.find_element(By.XPATH, "//*[@id='id_password']")
            confirmpassword_field = self.driver.find_element(By.XPATH, "//*[@id='id_conf_password']")

            firstname_field.send_keys("Jemila")
            lastname_field.send_keys("Bekele")
            email_field.send_keys("bekelehussen4@gmail.com")
            phone_field.send_keys("+254712367651")
            password_field.send_keys("!QAZXsw2#EDC")
            confirmpassword_field.send_keys("DifferentPassword123")

            # Find the checkbox and click it
            agree_checkboxinput = self.driver.find_element(By.XPATH, "//*[@id='id_agree_to_terms_and_conditions']")
            agree_checkboxinput.click()

            # Wait for the register button to be clickable and then click it
            register_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='wrapper']/div[6]/div/div/div/div/div[1]/div/div[2]/form/button"))
            )
            register_button.click()

            # Check if an error message is displayed for password mismatch
            error_message = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'alert-danger') and contains(text(), 'password')]"))  # Update this XPath based on actual error message element
            )

            assert error_message is not None, "Password mismatch error message not displayed."
        except TimeoutException:
            print("Element not found within the provided time")
        except NoSuchElementException as e:
            print(f"Error: {e}")

    def test_existing_email(self):
        # Wait for the input fields to be present and then find them
        try:
            firstname_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='id_first_name']"))
            )
            lastname_field = self.driver.find_element(By.XPATH, "//*[@id='id_last_name']")
            email_field = self.driver.find_element(By.XPATH, "//*[@id='id_email']")
            phone_field = self.driver.find_element(By.XPATH, "//*[@id='id_phone']")
            password_field = self.driver.find_element(By.XPATH, "//*[@id='id_password']")
            confirmpassword_field = self.driver.find_element(By.XPATH, "//*[@id='id_conf_password']")

            firstname_field.send_keys("Jemila")
            lastname_field.send_keys("Bekele")
            email_field.send_keys("bekelehussen48@gmail.com")  # Use an email that is known to be already registered
            phone_field.send_keys("+254712367651")
            password_field.send_keys("!QAZXsw2#EDC")
            confirmpassword_field.send_keys("!QAZXsw2#EDC")

            # Find the checkbox and click it
            agree_checkboxinput = self.driver.find_element(By.XPATH, "//*[@id='id_agree_to_terms_and_conditions']")
            agree_checkboxinput.click()

            # Wait for the register button to be clickable and then click it
            register_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='wrapper']/div[6]/div/div/div/div/div[1]/div/div[2]/form/button"))
            )
            register_button.click()

            # Check if an error message is displayed for existing email
            error_message = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'alert-danger') and contains(text(), 'email')]"))  # Update this XPath based on actual error message element
            )

            assert error_message is not None, "Existing email error message not displayed."
        except TimeoutException:
            print("Element not found within the provided time")
        except NoSuchElementException as e:
            print(f"Error: {e}")
