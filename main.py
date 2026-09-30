# main.py
import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def send_notification(task_result):
    
    topic = "goniogas2667" 
    ntfy_url = f"https://ntfy.sh/{topic}"
    message = f"🔔 Goniogas Check\n\n{task_result}"
    requests.post(ntfy_url, data=message.encode('utf-8'))
    print(message)

# 1. Configure Chrome for GitHub Actions (Linux environment)
options = Options()
options.add_argument('--headless=new')       # Run without opening a visible window
options.add_argument('--no-sandbox')         # Bypass OS security model
options.add_argument('--disable-dev-shm-usage') # Overcome limited resource problems
# options.add_argument('--disable-gpu')
# options.add_argument('--window-size=1920,1080')

driver = webdriver.Chrome(options=options)
driver.set_page_load_timeout(60)

url = 'https://goniogas.com/producto/cilindro-de-gas-de-10kg/'

task_result = "Failed to run"

success=False

while not success:
    print('eeeeeeo!!!')
    try:

        driver.get(url)
        time.sleep(5) # Wait for JavaScript to render

        # --- 2. YOUR SCRAPING LOGIC HERE ---
        # Example: Try to extract the price. 
        # (You might need to right-click the price on the site -> Inspect -> find the exact CSS class)
        try:
            # This is a generic example selector. Change it if it fails to find the price.
            # available= driver.
            not_available_element = driver.find_element(By.CSS_SELECTOR, ".woocommerce .out-of-stock, .usb_preview .out-of-stock, .w-grid .out-of-stock")
            existences_element = driver.find_element(By.CSS_SELECTOR, ".woocommerce-notices-wrapper")
            existences_exist = existences_element.value_of_css_property("display") != 'none'
            existences= existences_element.text
            not_available = not_available_element.text
            success=True


        except Exception as scrape_error:
            # If the selector is wrong, it will still tell you the page loaded successfully
            page_title = driver.title
            task_result = f"⚠️ Page loaded ({page_title}), but couldn't extract elements. Error: {str(scrape_error)}"
            send_notification(task_result)

    except Exception as e:
        task_result = f"❌ Script crashed! Error: {str(e)}"
        send_notification(task_result)
        time.sleep(60)
    
if 'driver' in locals():
    driver.quit()

# --- 3. SEND NOTIFICATION TO PHONE ---
# We use ntfy.sh because it requires ZERO API keys or GitHub Secrets!
# IMPORTANT: Change "my_goniogas_task_8f7a9b" to a random, unique string so no one else gets your notifications.

if existences_exist:
    task_result= existences + ' disponibles'
else:
    task_result = not_available
    
send_notification(task_result)
        