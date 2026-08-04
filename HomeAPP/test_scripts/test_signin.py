import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
import os

# Define the pytest fixture for driver setup
@pytest.fixture
def driver():

    chrome_options = Options()
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("--disable-logging")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
    service = Service(log_path=os.devnull)

    # Initialize the WebDriver
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.maximize_window()
    yield driver  # This will allow the tests to use the same driver instance
    driver.quit()  # Quit the driver after all tests are done

def test_admin_sign_in(driver):
    wait = WebDriverWait(driver, 15)

    # Step 1: Navigate to home page
    driver.get("http://127.0.0.1:8000/")
    print("✅ Home page loaded")

    # Step 2: Open sign-in dropdown and click on 'Admin'
    sign_in_button = wait.until(EC.element_to_be_clickable((By.ID, "signinDropdownButton")))
    driver.execute_script("arguments[0].scrollIntoView();", sign_in_button)
    time.sleep(2)
    sign_in_button.click()
    print("✅ Sign In dropdown opened")

    admin_option = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Admin")))
    admin_option.click()
    wait.until(EC.url_contains("/admin_signin/"))
    print("✅ Redirected to Admin Sign In page")

    # Step 3: Fill in the login form for Admin
    username_field = wait.until(EC.presence_of_element_located((By.NAME, "username")))
    password_field = wait.until(EC.presence_of_element_located((By.NAME, "password")))
    submit_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))

    # Use valid admin credentials
    username_field.send_keys("admin_user")
    password_field.send_keys("admin_pass")
    submit_button.click()

    # Step 4: Verify successful login for Admin
    try:
        wait.until(EC.url_contains("/admin/"))
        print("✅ Admin Sign In Successful 🎉")
    except Exception as e:
        print("❌ Admin Login failed or redirect not working.")
        print(f"🔍 Current page URL: {driver.current_url}")
        raise e

    # Step 5: After Admin login, return to the home page
    driver.get("http://127.0.0.1:8000/")  # Navigate back to the homepage
    print("✅ Redirected to Home page after Admin login")

def test_user_sign_in(driver):
    wait = WebDriverWait(driver, 15)

    # Step 1: Navigate to home page (after admin login redirection)
    driver.get("http://127.0.0.1:8000/")  # Ensure we're on the home page
    print("✅ Home page loaded")

    # Step 2: Re-locate the sign-in button and click on 'User'
    sign_in_button = wait.until(EC.element_to_be_clickable((By.ID, "signinDropdownButton")))
    driver.execute_script("arguments[0].scrollIntoView();", sign_in_button)
    time.sleep(2)
    sign_in_button.click()  # Click the button again after re-locating it
    print("✅ Sign In dropdown opened")

    user_option = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "User")))
    user_option.click()
    wait.until(EC.url_contains("/user_signin/"))
    print("✅ Redirected to User Sign In page")

    # Step 3: Fill in the login form for User
    username_field = wait.until(EC.presence_of_element_located((By.NAME, "username")))
    password_field = wait.until(EC.presence_of_element_located((By.NAME, "password")))
    submit_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))

    # Use valid user credentials
    username_field.send_keys("test_user")
    password_field.send_keys("user_pass")  # Replace with actual test user credentials
    submit_button.click()

    # Step 4: Verify successful login for User
    try:
        wait.until(EC.url_contains("/profile/"))  # Check if redirected to the profile page
        print("✅ User Sign In Successful 🎉")
    except Exception as e:
        print("❌ Login failed or redirect not working.")
        print(f"🔍 Current page URL: {driver.current_url}")
        raise e
