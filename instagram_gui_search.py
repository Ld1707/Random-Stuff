import sys
import time
import random
import pyautogui
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QDateEdit
from PyQt5.QtCore import QDate

class InstagramSearchApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Instagram Keyword Search")
        self.setGeometry(100, 100, 500, 400)

        layout = QVBoxLayout()

        # Login Fields
        self.username_label = QLabel("Instagram Username:")
        self.username_input = QLineEdit(self)
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)

        self.password_label = QLabel("Instagram Password:")
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)  # Hide password input
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)

        # Search Fields
        self.target_label = QLabel("Instagram Account to Search:")
        self.target_input = QLineEdit(self)
        layout.addWidget(self.target_label)
        layout.addWidget(self.target_input)

        self.keyword_label = QLabel("Keyword to Search:")
        self.keyword_input = QLineEdit(self)
        layout.addWidget(self.keyword_label)
        layout.addWidget(self.keyword_input)

        # Date Picker
        self.date_label = QLabel("Search Posts From (YYYY-MM-DD) Until Today:")
        self.date_picker = QDateEdit(self)
        self.date_picker.setCalendarPopup(True)
        self.date_picker.setDate(QDate.currentDate().addDays(-30))  # Default to last 30 days
        layout.addWidget(self.date_label)
        layout.addWidget(self.date_picker)

        # Search Button
        self.search_button = QPushButton("Search", self)
        self.search_button.clicked.connect(self.search_instagram)
        layout.addWidget(self.search_button)

        # Results Display
        self.results_text = QTextEdit(self)
        self.results_text.setReadOnly(True)
        layout.addWidget(self.results_text)

        self.setLayout(layout)

    def search_instagram(self):
        insta_username = self.username_input.text().strip()
        insta_password = self.password_input.text().strip()
        target_username = self.target_input.text().strip()
        keyword = self.keyword_input.text().strip().lower()
        start_date = self.date_picker.date().toString("yyyy-MM-dd")

        if not all([insta_username, insta_password, target_username, keyword, start_date]):
            self.results_text.setText("⚠️ Please fill in all fields!")
            return

        self.results_text.setText("🔍 Logging into Instagram...")
        QApplication.processEvents()

        options = Options()
        options.add_argument("--disable-blink-features=AutomationControlled")  # Avoid detection
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.maximize_window()

        try:
            driver.get("https://www.instagram.com/accounts/login/")
            time.sleep(5)

            username_input = driver.find_element(By.NAME, "username")
            password_input = driver.find_element(By.NAME, "password")

            for char in insta_username:
                username_input.send_keys(char)
                time.sleep(random.uniform(0.1, 0.3))

            for char in insta_password:
                password_input.send_keys(char)
                time.sleep(random.uniform(0.1, 0.3))
            time.sleep(1)
            password_input.send_keys(Keys.RETURN)
            time.sleep(7)
            
            # Check for additional login redirects
            while any(x in driver.current_url for x in ["accounts/login", "challenge", "/login", "relogin"]):
                time.sleep(3)
                try:
                    username_input = driver.find_element(By.NAME, "username")
                    password_input = driver.find_element(By.NAME, "password")
                    username_input.clear()
                    password_input.clear()
                    for char in insta_username:
                        username_input.send_keys(char)
                        time.sleep(random.uniform(0.1, 0.3))
                    for char in insta_password:
                        password_input.send_keys(char)
                        time.sleep(random.uniform(0.1, 0.3))
                    password_input.send_keys(Keys.RETURN)
                    time.sleep(7)
                except:
                    try:
                        login_button = driver.find_element(By.XPATH, "//button[contains(text(),'Log in')]" )
                        login_button.click()
                        time.sleep(5)
                    except:
                        pass
                try:
                    time.sleep(3)
                    username_input = driver.find_element(By.NAME, "username")
                    password_input = driver.find_element(By.NAME, "password")
                    username_input.clear()
                    password_input.clear()
                    for char in insta_username:
                        username_input.send_keys(char)
                        time.sleep(random.uniform(0.1, 0.3))
                    for char in insta_password:
                        password_input.send_keys(char)
                        time.sleep(random.uniform(0.1, 0.3))
                    time.sleep(1)
                    password_input.send_keys(Keys.RETURN)
                except:
                    pass
                time.sleep(5)
                if "incorrect" in driver.page_source or "doesn't belong to an account" in driver.page_source:
                    self.results_text.setText("❌ Incorrect username or password. Please try again.")
                    driver.quit()
                    return
                time.sleep(5)
                password_input.send_keys(Keys.RETURN)
                time.sleep(5)


            self.results_text.setText("✅ Logged in. Searching for account...")
            QApplication.processEvents()
            
            time.sleep(10)
            
            screen_width, screen_height = pyautogui.size()
            
            search_x = int(screen_width * 0.047)
            search_y = int(screen_height * 0.241)
            webdriver.ActionChains(driver).move_by_offset(search_x, search_y).click().perform()
            time.sleep(3)

            
            time.sleep(2)
            for char in target_username:
                pyautogui.write(char, interval=random.uniform(0.1, 0.3))
            time.sleep(1)
            pyautogui.write(Keys.RETURN)
            time.sleep(1)
            pyautogui.write(Keys.RETURN)
            time.sleep(5)

            self.results_text.setText("✅ Account found. Searching for posts...")
            QApplication.processEvents()
            
            posts = driver.find_elements(By.XPATH, "//article//a")
            post_links = [post.get_attribute("href") for post in posts]

            matching_posts = []
            for link in post_links:
                driver.get(link)
                time.sleep(3)
                try:
                    caption_element = driver.find_element(By.XPATH, "//span")
                    caption = caption_element.text.lower()
                    if keyword in caption:
                        matching_posts.append(link)
                except:
                    continue

            if matching_posts:
                self.results_text.setText("\n".join(matching_posts))
            else:
                self.results_text.setText("❌ No posts found containing the keyword.")

        except Exception as e:
            self.results_text.setText(f"❌ Error: {str(e)}")
        finally:
            driver.quit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = InstagramSearchApp()
    window.show()
    sys.exit(app.exec_())
