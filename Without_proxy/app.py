from flask import Flask, render_template, jsonify
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import pymongo
import socket
import uuid
from datetime import datetime

app = Flask(__name__)

# MongoDB setup
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["selenium_trends"]
collection = db["trends_data"]

# Path to geckodriver
geckodriver_path = r".\geckodriver-v0.35.0-win32\geckodriver.exe"

def run_selenium_script():
    options = Options()
   # options.add_argument("--headless")
    service = Service(executable_path=geckodriver_path)
    driver = webdriver.Firefox(service=service, options=options)

    try:
        driver.get("https://www.x.com")
       # print("Opened Twitter (X.com) in Firefox browser.")

        # Wait for the "Sign In" button to be present and click it
        try:
            sign_in_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[text()='Sign in']"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", sign_in_button)
            time.sleep(1)
            sign_in_button.click()
          #  print("Clicked on the 'Sign In' button.")
        except TimeoutException:
            print("Sign In button not found or not clickable.")
            return {"error": "Sign In button not found or not clickable."}

        try:
            username_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "text"))
            )
            username_field.send_keys("Your_username")         # Enter your username
          #  print("Entered the username.")
            username_field.send_keys(Keys.RETURN)
        except TimeoutException:
            print("Username field not found.")
            return {"error": "Username field not found."}

        try:
            email_field = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.NAME, "text"))
            )
            email_field.send_keys("your_email_address")      # Enter you email
          #  print("Entered the email address.")
            email_field.send_keys(Keys.RETURN)
        except TimeoutException:
            print("No email field found, proceeding to password field.")

        try:
            password_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "password"))
            )
            password_field.send_keys("your_password")             # Enter your twitter password
            print("Entered the password.")
            password_field.send_keys(Keys.RETURN)
        except TimeoutException:
            print("Password field not found.")
            return {"error": "Password field not found."}

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
      #  print("Logged in successfully and navigated to the home page.")
        
        time.sleep(5)

        explore_url = "https://x.com/explore/tabs/for-you"
        driver.get(explore_url)
       # print("Navigated to the Explore tab.")

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        print("Explore tab loaded successfully.")

        try:
            explore_elements = WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[data-testid="cellInnerDiv"]'))
            )
            print(f"Found {len(explore_elements)} elements in the Explore tab.")

            hashtags = []
            for element in explore_elements:
                span_elements = element.find_elements(By.CLASS_NAME, "css-1jxf684.r-bcqeeo.r-1ttztb7.r-qvutc0.r-poiln3")
                for span in span_elements:
                    if span.text.startswith("#") and len(hashtags) < 5:
                        hashtags.append(span.text)
                    if len(hashtags) == 5:
                        break
                if len(hashtags) == 5:
                    break

            print("Top 5 Hashtags:")
            for hashtag in hashtags:
                print(hashtag)
            
            ip_address = socket.gethostbyname(socket.gethostname())
            print(f"IP Address: {ip_address}")

            trend_data = {
                "_id": str(uuid.uuid4()),
                "name_of_trend1": hashtags[0] if len(hashtags) > 0 else None,
                "name_of_trend2": hashtags[1] if len(hashtags) > 1 else None,
                "name_of_trend3": hashtags[2] if len(hashtags) > 2 else None,
                "name_of_trend4": hashtags[3] if len(hashtags) > 3 else None,
                "name_of_trend5": hashtags[4] if len(hashtags) > 4 else None,
                "date_and_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "ip_address": ip_address
            }

            collection.insert_one(trend_data)
            print(f"Data stored in MongoDB: {trend_data}")

            return trend_data

        except TimeoutException:
            print("Timeout while waiting for Explore tab elements. Dumping page source for debugging...")
            print(driver.page_source)
            return {"error": "Timeout while waiting for Explore tab elements."}

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return {"error": str(e)}
    finally:
        driver.quit()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/run_script', methods=['POST'])
def run_script():
    data = run_selenium_script()
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
