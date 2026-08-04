from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_donation_updates_donor_count():
    driver = webdriver.Chrome()  # Or Firefox, etc.
    wait = WebDriverWait(driver, 10)

    try:
        # Open homepage
        driver.get("http://127.0.0.1:8000/")

        # Wait and get initial donors count (e.g. the element that has the count)
        donors_count_elem = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(text(), 'Donors')]/preceding-sibling::div[contains(text(), '+')]")))
        initial_count_text = donors_count_elem.text
        print(f"Initial donors count text: {initial_count_text}")

        # Click "See all" button under Latest Project (green box)
        see_all_latest_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Latest Project')]/following-sibling::button[contains(text(), 'See all')]")))
        see_all_latest_btn.click()

        # Wait for project list page or modal to load
        # Assuming project links have a class 'project-link'
        project_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Donate Supplies")))  # Change project name if needed
        project_link.click()

        # Wait for project details page to load
        donate_button = wait.until(EC.element_to_be_clickable((By.ID, "donateBtn")))  # Assuming your donate button ID is donateBtn
        donate_button.click()

        # Fill donation form (if any)
        # Assuming donation input has id='donationAmount' and a submit button id='submitDonation'
        donation_amount_input = wait.until(EC.visibility_of_element_located((By.ID, "donationAmount")))
        donation_amount_input.clear()
        donation_amount_input.send_keys("10")  # example donation amount

        submit_btn = driver.find_element(By.ID, "submitDonation")
        submit_btn.click()

        # Wait for donation modal to close or confirmation message
        wait.until(EC.invisibility_of_element_located((By.ID, "donationModal")))

        # Go back to homepage or reload
        driver.get("http://127.0.0.1:8000/")

        # Wait for donors count element again
        donors_count_elem_after = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(text(), 'Donors')]/preceding-sibling::div[contains(text(), '+')]")))
        updated_count_text = donors_count_elem_after.text
        print(f"Updated donors count text: {updated_count_text}")

        # Simple assertion that updated count is different (you can do more specific checks if you parse numbers)
        assert updated_count_text != initial_count_text, "Donors count did not update after donation"

        print("Donation test passed. Donors count updated.")

    except Exception as e:
        print(f"Test failed: {e}")

    finally:
        driver.quit()

