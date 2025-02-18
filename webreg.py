from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import platform
import argparse
import time

parser = argparse.ArgumentParser(description="webreg params")
parser.add_argument("--refresh", action="store_true", help="refresh page continuously", default=False)
args = parser.parse_args()

# URL of the webpage you want to interact with
login_url = "https://anc.ca.apm.activecommunities.com/burnaby/signin"
url = "https://anc.ca.apm.activecommunities.com/burnaby/wishlist"  # Replace with the actual URL

# Path to your WebDriver (e.g., chromedriver for Chrome)
if platform.system() == "Windows":
    webdriver_path = "./chromedriver"  # Replace with the path to your chromedriver
else:
    webdriver_path = r".\chromedriver.exe"

service = Service(executable_path=webdriver_path)
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

# Open login page
driver.get(login_url)

# need manual login here then reload target page
time.sleep(10)

# open wish list page
driver.get(url)

# Define the button's identifier (e.g., CSS selector, XPath, etc.)
button_selector = "button.btn.btn-strong"  # Modify this selector as per your button
delay = 5 # seconds

# Loop to continuously search and click the button if found
try:
    while True:
        time_string = time.strftime("%m/%d/%Y-%H:%M:%S", time.localtime())
        try:
            if args.refresh:
                driver.get(driver.current_url)
                myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, button_selector)))
                print("Page is ready! " + time_string)
                #time.sleep(delay)

            # Find the button (adjust the selector as needed)
            button = driver.find_element(By.CSS_SELECTOR, button_selector)  # You can use By.XPATH as well
            isDisabled = button.get_attribute("disabled")
            if not isDisabled:
                # If the button is found, click it
                button.click()
                print("Button clicked! " + time_string)
                # wait seconds to select participation
                time.sleep(10)
            else:
                print("Button disabled. retrying.." + time_string)

        except Exception as e:
            print("Button not found, retrying..." + time_string)

        # Wait for a while before searching again
        time.sleep(0.5)  # Adjust this sleep time if needed for efficiency
except KeyboardInterrupt:
    print("Process interrupted by user.")
finally:
    driver.quit()
