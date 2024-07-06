import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestPerformance:
    @pytest.fixture(autouse=True)
    def setup(self, request):
        self.driver = webdriver.Chrome()
        yield
        self.driver.quit()

        # Generate the HTML report
        report_file = request.config.getoption("--html")
        if report_file:
            try:
                self.driver.save_screenshot("screenshot.png")
            except Exception as e:
                print(f"Error capturing screenshot: {e}")

    def test_load_website(self):
        start_time = time.time()
        self.driver.get("https://yum.co.ke")
        end_time = time.time()
        load_time = end_time - start_time
        print(f"Website load time: {load_time:.2f} seconds")
        assert load_time < 10, "Website load time exceeded 10 seconds."

        start_time = time.time()
        self.driver.get("https://yum.co.ke/login/")
        end_time = time.time()
        load_time = end_time - start_time
        print(f"Login page load time: {load_time:.2f} seconds")
        assert load_time < 15, "Login page load time exceeded 15 seconds."

    def test_search_performance(self):
        self.driver.get("https://yum.co.ke")

        # Find the search input field and enter a search term
        search_field = self.driver.find_element(By.XPATH, "//*[@id='wrapper']/div[3]/nav/div/div[2]/ul/li[4]/span/form/div/div/span/input")
        search_field.send_keys("Grill Shack")
        search_field.submit()

        start_time = time.time()

        # Wait for the search results page to load
        wait = WebDriverWait(self.driver, 60)
        wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='wrapper']/div[3]/nav/div/div[2]/ul/li[4]/span/form/div/div/span/input")))
        end_time = time.time()
        search_time = end_time - start_time
        print(f"Search time: {search_time:.2f} seconds")
        assert search_time < 10, "Search time exceeded 10 seconds."
