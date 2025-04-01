from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import platform
import argparse
import time
import getpass

parser = argparse.ArgumentParser(description="webreg params")
parser.add_argument("--username", help="login username")
parser.add_argument("--password", default="", help="login password")
parser.add_argument("--name", help="name to register")
parser.add_argument("--number", help="the active details page number")
parser.add_argument("--refresh", action="store_true", help="refresh page continuously", default=False)
parser.add_argument("--dryrun", action="store_true", help="dryrun", default=False)
args = parser.parse_args()

if not args.password:
    args.password = getpass.getpass('Password:')

# URL of the webpage you want to interact with
login_url = "https://anc.ca.apm.activecommunities.com/burnaby/signin"
url = "https://anc.ca.apm.activecommunities.com/burnaby/activity/search/detail/{}".format(args.number)

# Path to your WebDriver (e.g., chromedriver for Chrome)
if platform.system() != "Windows":
    webdriver_path = "./chromedriver"  # Replace with the path to your chromedriver
else:
    webdriver_path = r".\chromedriver.exe"

service = Service(executable_path=webdriver_path)
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(service=service, options=options)

# Open login page
driver.get(login_url)

# need manual login here then reload target page
time.sleep(2)

# login
# find username/email field and send the username itself to the input field
driver.find_element(By.XPATH, '//input[@type="text"]').send_keys(args.username)
# find password input field and insert password as well
driver.find_element(By.XPATH, '//input[@type="password"]').send_keys(args.password)

# need manual click to bypass reCaptcha
time.sleep(20)

# click login button
driver.find_element(By.XPATH, '//button[@type="submit"]').click()
time.sleep(2)

# open wish list page
driver.get(url)

# Define the button's identifier (e.g., CSS selector, XPath, etc.)
button_selector = "button.btn.btn-strong"  # Modify this selector as per your button
delay = 5 # seconds
button_clicked = False

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
                button_clicked = True
                # wait seconds to select participation
                time.sleep(2)
                # registration
                try:
                    driver.find_element(By.CSS_SELECTOR, "div.dropdown__button.input__field").click()  # You can use By.XPATH as well
                    time.sleep(1)
                    driver.find_element(By.XPATH, '//li[@title="{}"]'.format(args.name)).click()
                    time.sleep(1)
                    btn = driver.find_element(By.CSS_SELECTOR, "button.btn.btn-strong.fee-summary__add-to-cart-button")
                    btn.click()
                    time.sleep(2)
                    btn = driver.find_element(By.CSS_SELECTOR, "button.btn.btn-strong.checkout__button")
                    time.sleep(2)
                    if not args.dryrun:
                        btn.click()
                        time.sleep(2)
                    else:
                        print("registration skipped for {} due to dryrun is True.".format(args.name))
                    print("registration complete successfully for {}.".format(args.name))
                except Exception:
                    print("registration failed for {}.".format(args.name))
                break
            else:
                print("Button disabled. retrying.." + time_string)

        except Exception as e:
            print("Button not found, retrying..." + time_string)

        # Wait for a while before searching again
        if args.refresh:
            time.sleep(0.5)  # Adjust this sleep time if needed for efficiency
except KeyboardInterrupt:
    print("Process interrupted by user.")
finally:
    if not button_clicked:
        driver.quit()
