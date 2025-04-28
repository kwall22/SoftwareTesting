from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

def before_all(context):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--remote-debugging-port=9222")

    context.browser = webdriver.Chrome(options=chrome_options)
    context.browser.implicitly_wait(35)

def after_all(context):
    context.browser.quit()

def after_step(context, step):
    if step.status == "failed":
        filename = f"screenshot_{step.name}_{int(time.time())}.png"
        context.browser.save_screenshot(filename)

def wait_for_element(context, locator):
    try:
        element = WebDriverWait(context.browser, 35).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, locator))
        )
        return element
    except TimeoutException:
        print(f"Timeout waiting for element with locator: {locator}")
        return None