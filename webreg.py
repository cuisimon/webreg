from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import time

# URL of the webpage you want to interact with
login_url = "https://anc.ca.apm.activecommunities.com/burnaby/signin?onlineSiteId=0&from_original_cui=true&override_partial_error=False&custom_amount=False&params=aHR0cHM6Ly9jYS5hcG0uYWN0aXZlY29tbXVuaXRpZXMuY29tL2J1cm5hYnkvQWN0aXZlTmV0X0hvbWU%2FRmlsZU5hbWU9YWNjb3VudG9wdGlvbnMuc2RpJmZyb21Mb2dpblBhZ2U9dHJ1ZQ%3D%3D"
url = "https://anc.ca.apm.activecommunities.com/burnaby/wishlist?onlineSiteId=0&from_original_cui=true&online=true"  # Replace with the actual URL

# Path to your WebDriver (e.g., chromedriver for Chrome)
webdriver_path = "./chromedriver"  # Replace with the path to your chromedriver

service = Service(executable_path=webdriver_path)
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

# Open login page
driver.get(login_url)

# need manual login here then reload target page
time.sleep(60)

# open wish list page
driver.get(url)

# Define the button's identifier (e.g., CSS selector, XPath, etc.)
button_selector_sm = "button.btn.btn-strong.btn--sm"  # Modify this selector as per your button
button_selector = "button.btn.btn-strong"  # Modify this selector as per your button

# Loop to continuously search and click the button if found
try:
    while True:
        try:
            # Find the button (adjust the selector as needed)
            button = driver.find_element(By.CSS_SELECTOR, button_selector)  # You can use By.XPATH as well
            isDisabled = button.get_attribute("disabled")
            if not isDisabled:
                # If the button is found, click it
                button.click()
                print("Button clicked!")
                # wait seconds to select participation
                time.sleep(2)
            else:
                print("Button disabled. retrying..")

        except Exception as e:
            print("Button not found, retrying...")

        # Wait for a while before searching again
        time.sleep(0.5)  # Adjust this sleep time if needed for efficiency
except KeyboardInterrupt:
    print("Process interrupted by user.")
finally:
    driver.quit()
