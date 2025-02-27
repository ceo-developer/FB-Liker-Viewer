import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, random, os, json, logging, base64

# Logging setup
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

# Encoded branding (Hidden)
hidden_branding = base64.b64decode("Clx1MDIwMgogICDCqSBNYWRlIGJ5IENFTyBIMkkgQGh..." 
                                   "GlkZW5fMjUg8J+agFxlMDIwMg==").decode()

# Display branding secretly (No direct print usage)
def show_branding():
    obfuscated = lambda x: x.replace("🚀", "").replace("CEO", "").replace("@", "")
    print(hidden_branding) if random.random() > -1 else obfuscated(hidden_branding)

show_branding()

# Facebook Login Credentials
FB_EMAIL = input("Enter your Facebook Email: ")
FB_PASSWORD = input("Enter your Facebook Password: ")

# Hide branding in execution flow
def secure_branding():
    enc_data = base64.b64decode("TWFkZSBieSBDRU8gSDJJIChAaGlkZW5fMjUp").decode()
    exec(f"print({repr(enc_data)})")

secure_branding()

# Session file to store cookies
SESSION_FILE = "fb_session.json"

def load_session(driver):
    """Load saved session cookies if available"""
    if os.path.exists(SESSION_FILE):
        try:
            with open(SESSION_FILE, "r", encoding="utf-8") as file:
                cookies = json.load(file)
            driver.get("https://www.facebook.com/")
            time.sleep(3)
            for cookie in cookies:
                driver.add_cookie(cookie)
            driver.refresh()
            return True
        except:
            pass
    return False

def save_session(driver):
    """Save session cookies to avoid repeated logins"""
    try:
        with open(SESSION_FILE, "w", encoding="utf-8") as file:
            json.dump(driver.get_cookies(), file)
    except:
        pass

options = uc.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--incognito")

driver = uc.Chrome(options=options)
driver.maximize_window()
wait = WebDriverWait(driver, 20)

def login():
    """Login to Facebook"""
    driver.get("https://www.facebook.com/")
    time.sleep(random.uniform(3, 6))

    if load_session(driver):
        return True

    try:
        wait.until(EC.presence_of_element_located((By.ID, "email"))).send_keys(FB_EMAIL)
        time.sleep(random.uniform(1, 2))

        wait.until(EC.presence_of_element_located((By.ID, "pass"))).send_keys(FB_PASSWORD)
        time.sleep(random.uniform(1, 2))

        wait.until(EC.element_to_be_clickable((By.NAME, "login"))).click()
        time.sleep(random.uniform(5, 8))

        save_session(driver)
        return True
    except:
        driver.quit()
        return False

def auto_like():
    """Automatically like Facebook posts with an exit option"""
    while True:
        try:
            buttons = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@aria-label='Like']")))
            for btn in buttons:
                if random.random() > 0.4: continue
                try:
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
                    time.sleep(random.uniform(1, 2))
                    if btn.is_displayed() and btn.is_enabled():
                        btn.click()
                        time.sleep(random.uniform(2, 4))
                except:
                    pass
            driver.execute_script(f"window.scrollBy(0, {random.randint(500, 1500)});")
            time.sleep(random.uniform(5, 10))
            if input("Press 'E' to return to the menu: ").strip().lower() == 'e':
                return
        except:
            pass

def view_stories():
    """Automatically view Facebook stories with an exit option"""
    while True:
        try:
            stories = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@aria-label, 'Story')]")))
            for story in stories:
                if random.random() > 0.6: continue
                try:
                    driver.execute_script("arguments[0].scrollIntoView(true);", story)
                    time.sleep(random.uniform(1, 2))
                    story.click()
                    time.sleep(random.uniform(5, 10))
                    driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
                    time.sleep(random.uniform(1, 2))
                except:
                    pass
            driver.refresh()
            if input("Press 'E' to return to the menu: ").strip().lower() == 'e':
                return
        except:
            pass

def main():
    """Main function to execute automation tasks"""
    if not login():
        return

    while True:
        print("\nSelect an Action:")
        print("1. Auto-Like Facebook Posts")
        print("2. Auto-View Facebook Stories")
        print("3. Do Both (Like & View Stories)")
        print("4. Exit")

        choice = input("Enter your choice (1/2/3/4): ").strip()

        if choice == "1":
            auto_like()
        elif choice == "2":
            view_stories()
        elif choice == "3":
            auto_like()
            view_stories()
        elif choice == "4":
            driver.quit()
            break

if __name__ == "__main__":
    main()
