from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import random
import string
import logging

class ProfileUpdateTest:
    def __init__(self, url, email, password):
        self.url = url
        self.email = email
        self.password = password
        self.driver = None
        self.setup_logging()

    def setup_logging(self):
        logging.basicConfig(level=logging.INFO,
                          format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)

    def generate_random_username(self, length=8):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    def wait_and_click(self, by, value, timeout=10):
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((by, value))
            )
            element.click()
            return True
        except TimeoutException:
            self.logger.error(f"Element {value} not clickable after {timeout} seconds")
            return False

    def wait_for_element(self, by, value, timeout=10):
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((by, value))
            )
        except TimeoutException:
            self.logger.error(f"Element {value} not visible after {timeout} seconds")
            return None

    def handle_subscription_popup(self):
        try:
            self.logger.info("Handling subscription popup")
            later_button = self.wait_for_element(By.XPATH, "//button[contains(text(), 'Later')]")
            if later_button:
                later_button.click()
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error handling subscription popup: {str(e)}")
            return False

    def select_random_avatar(self):
        try:
            avatars = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "img[alt='Avatar Image ']"))
            )
            
            if not avatars:
                self.logger.error("No avatar images found")
                return False
            
            random_avatar = random.choice(avatars)
            self.logger.info(f"Selecting avatar with src: {random_avatar.get_attribute('src')}")
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(random_avatar)
            ).click()
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error selecting avatar: {str(e)}")
            return False 

    def click_apply_button(self):
        try:
            self.logger.info("Waiting before clicking Apply button")
            time.sleep(3)  # Wait for 3 seconds
            apply_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'button__content') and text()='Apply']"))
            )
            parent_button = apply_button.find_element(By.XPATH, "./..")
            parent_button.click()
            
            return True
        except Exception as e:
            self.logger.error(f"Error clicking Apply button: {str(e)}")
            return False

    def setup(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        
    def run_test(self):
        try:
            self.setup()
            
            #Open URL
            self.logger.info("Opening URL")
            self.driver.get(self.url)
            
            # Click the Login button first
            self.logger.info("Clicking login button")
            self.wait_and_click(By.CSS_SELECTOR, "[data-testid='lobby-login-btn']")  # Update selector as needed
            
            #Enter login credentials
            self.logger.info("Entering credentials")
            email_field = self.wait_for_element(By.NAME, "email")
            password_field = self.wait_for_element(By.NAME, "password")
            
            if email_field and password_field:
                email_field.send_keys(self.email)
                password_field.send_keys(self.password)
                self.wait_and_click(By.CSS_SELECTOR, "button[type='submit']")


        
            if not self.handle_subscription_popup():
                self.logger.error("Failed to handle subscription popup")
                return False

            #Click Menu button
            self.logger.info("Clicking menu button")
            self.wait_and_click(By.CSS_SELECTOR, "[data-testid='menuButton']")
            
            #Click My Account
            self.logger.info("Navigating to My Account")
            self.wait_and_click(By.CLASS_NAME, "side-menu__action")
            
            #Click Edit button
            self.logger.info("Clicking Edit button")
            self.wait_and_click(By.CSS_SELECTOR, "[data-testid='editAvatar']")
            
            #Update username
            new_username = self.generate_random_username()
            self.logger.info(f"Updating username to: {new_username}")
            username_field = self.wait_for_element(By.CSS_SELECTOR, "[data-testid='nicknameInput']")
            if username_field:
                username_field.clear()
                username_field.send_keys(new_username)
            
            #Choose random avatar
            self.logger.info("Selecting random avatar")
            if not self.select_random_avatar():
                self.logger.error("Failed to select avatar")
                return False
            
            #Click Apply
            self.logger.info("Saving changes")
            self.logger.info("Clicking Apply button")
            if not self.click_apply_button():
                self.logger.error("Failed to click Apply button")
                return False
            
            #Validate username change
            self.logger.info("Validating username change")
            time.sleep(3)
            displayed_username = self.wait_for_element(By.CSS_SELECTOR, "[data-testid='nicknameDisplay']")
            
            if displayed_username:
                assert displayed_username.text == new_username, "Username validation failed"
                self.logger.info("Username validation successful")
            
            # Return to lobby
            self.logger.info("Returning to lobby")
            self.wait_and_click(By.CSS_SELECTOR, "[data-testid='closeButton']")
            
            #Print both coin amounts
            self.logger.info("Getting Yellow coin amounts")
            coin_elements = self.driver.find_elements(By.CSS_SELECTOR, "[data-testid='lobby-balance-bar']")
            for coin in coin_elements:
                self.logger.info(f"Coin amount: {coin.text}")
            
            self.logger.info("Switching to Green coins")
            self.wait_and_click(By.CSS_SELECTOR, "[data-testid='coin-switcher']")
            time.sleep(5)

            self.logger.info("Getting Green coin amounts")
            coin_elements = self.driver.find_elements(By.CSS_SELECTOR, "[data-testid='lobby-balance-bar']")
            for coin in coin_elements:
                self.logger.info(f"Coin amount: {coin.text}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Test failed: {str(e)}")
            return False
            
        finally:
            if self.driver:
                self.driver.quit()

if __name__ == "__main__":
    TEST_URL = "Enter URL here"
    TEST_EMAIL = "Enter email here"
    TEST_PASSWORD = "Enter password here"
    
    test = ProfileUpdateTest(TEST_URL, TEST_EMAIL, TEST_PASSWORD)
    test.run_test()
