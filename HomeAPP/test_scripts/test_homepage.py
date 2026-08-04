import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

# 📸 Screenshot helper
def take_screenshot(driver, name):
    path = os.path.join(os.getcwd(), f"{name}.png")
    driver.save_screenshot(path)
    print(f"📸 Screenshot saved: {path}")

# ✅ Navbar elements test
@pytest.mark.django_db
def test_navbar_elements(live_server):
    service = Service("drivers/chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    wait = WebDriverWait(driver, 10)

    try:
        driver.get(live_server.url)
        driver.maximize_window()

        # Navbar visible
        try:
            navbar = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "navbar")))
            assert navbar.is_displayed()
        except Exception:
            take_screenshot(driver, "navbar_not_found")
            pytest.fail("❌ Navbar not visible")

        # Brand name
        assert "Crowdfunding" in driver.page_source

        # Categories dropdown
        try:
            categories_button = wait.until(EC.presence_of_element_located((By.ID, "dropdownMenuButton")))
            categories_button.click()
            for cat in ["Education", "Medical", "Business", "Natural Disaster"]:
                assert cat in driver.page_source
        except Exception:
            take_screenshot(driver, "categories_error")
            pytest.fail("❌ Categories dropdown not working")

        # Search form
        try:
            search_input = driver.find_element(By.NAME, "query")
            assert search_input.get_attribute("placeholder") == "Searching..."
            driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        except Exception:
            take_screenshot(driver, "search_error")
            pytest.fail("❌ Search form not found")

        # Auth links
        try:
            assert "Sign In" in driver.page_source
            assert "Sign Up" in driver.page_source
        except Exception:
            take_screenshot(driver, "auth_links_error")
            pytest.fail("❌ Auth links missing for guest")

    finally:
        driver.quit()
    print("✅ Navbar elements test passed")

# ✅ Full homepage test
@pytest.mark.django_db
def test_full_homepage(live_server):
    service = Service("drivers/chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    wait = WebDriverWait(driver, 10)

    try:
        driver.get(live_server.url)
        driver.maximize_window()

        # Hero title
        assert wait.until(EC.presence_of_element_located((By.XPATH, "//h1[text()='Flood in Bangladesh']")))

        # Donate modal
        donate_btn = driver.find_element(By.ID, "donateBtn")
        donate_btn.click()
        assert wait.until(EC.visibility_of_element_located((By.ID, "donationModal")))
        driver.find_element(By.CLASS_NAME, "close").click()

        # Stats section
        for stat in ["Donors", "Projects", "Success Rating"]:
            assert wait.until(EC.presence_of_element_located((By.XPATH, f"//p[text()='{stat}']")))

        # Project navigation buttons
        project_links = {
            "See all": "//a[text()='See all']",
            "Create your own Project": "//a[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'create your own project')]"
        }
        for name, xpath in project_links.items():
            btn = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            current_url = driver.current_url

            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
            time.sleep(0.5)
            driver.execute_script("arguments[0].click();", btn)

            WebDriverWait(driver, 5).until(EC.url_changes(current_url))
            driver.back()
            WebDriverWait(driver, 5).until(EC.url_to_be(current_url))

        # Team members
        for member in ["Abdullah Al-Mamun", "Anika Nawer Nabila", "Kayes Ahammed Biplob"]:
            assert wait.until(EC.presence_of_element_located((By.XPATH, f"//h2[text()='{member}']")))

        # Footer
        footer = wait.until(EC.presence_of_element_located((By.TAG_NAME, "footer")))
        assert "Crowdfunding Platform" in footer.text

    finally:
        driver.quit()
    print("✅ Full homepage test passed")
