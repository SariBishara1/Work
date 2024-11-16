import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Discord credentials and channel URLs
USER_EMAIL = 'saribish1@gmail.com'
USER_PASSWORD = 'sari123sari'
SOURCE_CHANNEL_URL = 'https://discord.com/channels/94882524378968064/94882524378968064'  # TOS is source
TARGET_CHANNEL_URL = 'https://discord.com/channels/1305451688752054312/1305451689645576214'  # Test is target

# Set up Chrome options and driver with stealth modifications
chrome_options = Options()

# Modification 2: Manual stealth settings
chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Prevent detection of automation
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])  # Remove automation banner
chrome_options.add_experimental_option("useAutomationExtension", False)  # Disable automation extension
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36")  # Custom User-Agent

# Modification 6: Disable images to improve performance
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options.add_experimental_option("prefs", prefs)

# Updated Chrome binary and driver paths for Ubuntu
chrome_options.binary_location = '/usr/bin/google-chrome'  # Correct path for Chrome binary on Ubuntu
driver = webdriver.Chrome(
    service=Service('/usr/local/bin/chromedriver'),  # Correct path for ChromeDriver on Ubuntu
    options=chrome_options
)
wait = WebDriverWait(driver, 10)

def login():
    driver.get('https://discord.com/login')
    wait.until(EC.presence_of_element_located((By.NAME, 'email'))).send_keys(USER_EMAIL)
    driver.find_element(By.NAME, 'password').send_keys(USER_PASSWORD)
    driver.find_element(By.XPATH, '//button[@type="submit"]').click()
    time.sleep(5)
    print("Logged in successfully")

def forward_message(message):
    driver.get(TARGET_CHANNEL_URL)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="textbox"]')))

    try:
        # Locate the message input box and send the message
        message_box = driver.find_element(By.CSS_SELECTOR, 'div[role="textbox"]')
        message_box.click()
        time.sleep(0.5)  # Short pause to ensure focus

        # Clear any existing text and type the message
        message_box.send_keys(Keys.CONTROL + "a")  # Select all text
        message_box.send_keys(Keys.BACKSPACE)  # Clear
        message_box.send_keys(message)  # Type the message

        # Press Enter to send
        message_box.send_keys(Keys.ENTER)
        print("Message sent to target channel:", message)
        time.sleep(2)
    except Exception as e:
        print("Error sending message:", e)

    driver.get(SOURCE_CHANNEL_URL)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[class*="messageContent"]')))
    time.sleep(2)  # Short pause to stabilize

def monitor_and_forward():
    driver.get(SOURCE_CHANNEL_URL)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[class*="messageContent"]')))

    last_message = ""
    while True:
        print("Checking for new messages in the source channel...")

        try:
            messages = driver.find_elements(By.CSS_SELECTOR, '[class*="messageContent"]')
            if messages:
                new_message = messages[-1].text
                if new_message != last_message:
                    last_message = new_message
                    print("New message detected:", new_message)
                    forward_message(new_message)
                else:
                    print("No new messages. Resting...")
                    time.sleep(1)  # Shorter rest interval for responsiveness
            else:
                print("No messages found in the source channel. Sleeping for 1 second...")
                time.sleep(1)
        except Exception as e:
            print("Error in monitoring loop:", e)
            time.sleep(5)  # Pause before retrying

try:
    login()
    monitor_and_forward()
except Exception as e:
    print("An error occurred:", e)
finally:
    driver.quit()

