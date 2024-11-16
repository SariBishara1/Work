from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# Updated ChromeDriver path for Ubuntu EC2 instance
driver = webdriver.Chrome(service=Service("/usr/local/bin/chromedriver"))

# Example usage: Open Google
driver.get("https://www.google.com")

# Example action: Search for a term
search_box = driver.find_element(By.NAME, "q")
search_box.send_keys("Selenium on AWS EC2")
search_box.submit()

# Print page title to verify functionality
print("Page title is:", driver.title)

# Close the browser
driver.quit()
