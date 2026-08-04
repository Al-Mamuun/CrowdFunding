import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

# Screenshot utility
def take_screenshot(driver, name):
    path = os.path.join(os.getcwd(), f"{name}.png")
    driver.save_screenshot(path)
    print(f"📸 Screenshot saved: {path}")

@pytest.fixture(scope="module")
def driver():
    # Setup WebDriver
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    # Teardown WebDriver
    driver.quit()

def test_sign_up_page(driver):
    # Generate unique test data
    timestamp = str(int(time.time()))
    test_data = {
        "username": f"testuser_{timestamp}",
        "first_name": "Test",
        "last_name": "User",
        "email": f"test_{timestamp}@example.com",
        "password": "Test@1234",
        "phone": "01845196403"
    }

    driver.get("http://127.0.0.1:8000/sign-up/")
    wait = WebDriverWait(driver, 15)

    # Fill the form
    try:
        driver.find_element(By.NAME, "username").send_keys(test_data["username"])
        driver.find_element(By.NAME, "first_name").send_keys(test_data["first_name"])
        driver.find_element(By.NAME, "last_name").send_keys(test_data["last_name"])
        driver.find_element(By.NAME, "email").send_keys(test_data["email"])
        driver.find_element(By.NAME, "password1").send_keys(test_data["password"])
        driver.find_element(By.NAME, "password2").send_keys(test_data["password"])
        driver.find_element(By.NAME, "phn_number").send_keys(test_data["phone"])
    except Exception as e:
        take_screenshot(driver, "form_fill_error")
        pytest.fail(f"Form fill error: {e}")

    # Submit form
    try:
        submit_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(., 'REGISTER')]")))
        submit_button.click()
        
        # Wait for either success or error
        WebDriverWait(driver, 10).until(
            lambda d: "profile" in d.current_url.lower() or 
                    "dashboard" in d.current_url.lower() or
                    "error" in d.current_url.lower() or
                    len(d.find_elements(By.CLASS_NAME, "alert-info")) > 0
        )
        
        # Check for error messages
        error_messages = driver.find_elements(By.CLASS_NAME, "alert-info")
        if error_messages:
            errors = "\n".join([msg.text for msg in error_messages if msg.text])
            pytest.fail(f"Registration errors:\n{errors}")
            
        # Verify successful registration
        assert "profile" in driver.current_url.lower() or "dashboard" in driver.current_url.lower(), \
            f"Expected profile/dashboard URL, got {driver.current_url}"
            
    except Exception as e:
        take_screenshot(driver, "submission_error")
        pytest.fail(f"Form submission error: {e}")

    # Verify user is logged in
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), '{test_data['username']}')]"))
        )
    except Exception as e:
        take_screenshot(driver, "profile_verification_error")
        pytest.fail(f"Profile verification failed: {e}")