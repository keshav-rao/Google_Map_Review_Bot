import random
from pathlib import Path
from time import sleep

import pandas as pd
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from visual_poster import post_review_visually


class GoogleReviewBot:

    def __init__(self, mailaddress, password, comment):
        self.mailaddress = mailaddress
        self.password = password
        self.comment = comment
        self.completedAccountsPath = Path(__file__).resolve().parent / "data" / "completedAccounts.csv"
        self.completedAccountsPath.parent.mkdir(exist_ok=True, parents=True)
        self.waitDuration = [3, 4, 5]
        
        options = uc.ChromeOptions()
        options.add_argument("--start-maximized")
        self.driver = uc.Chrome(options=options, version_main=153)
        self.initialize()

    def initialize(self):
        self.i = 0
        PlaceURL = "https://www.google.com/maps/place/Srinivasa+Medicals+%2B/@11.0290809,76.9043137,21z/data=!4m6!3m5!1s0x3ba85f1111afd1b7:0x278e36b7534cbe8!8m2!3d11.02906!16s%2Fg%2F11tr5b9n2f?authuser=0&entry=ttu&g_ep=EgoyMDI2MDkxNC4wIKXMDSoASAFQAw%3D%3D"
        self.driver.delete_all_cookies()
        self.urls = [
            "https://accounts.google.com/signin/v2/identifier?hl=en&passive=true&continue=https%3A%2F%2Fwww.google.com%2Fsearch%3Fq%3Dgoogle%26oq%3Dgoogle%26aqs%3Dchrome.0.69i59l3j0i271l2j69i60j69i65j69i60.706j0j1&ec=GAZAAQ&flowName=GlifWebSignIn&flowEntry=ServiceLogin",
            PlaceURL,
        ]
        self.driver.get(self.urls[self.i])
        WebDriverWait(self.driver, 15).until(
            lambda d: "accounts.google.com" in d.current_url or "google.com" in d.current_url
        )

    @staticmethod
    def _find_any(driver, locators, timeout=20):
        deadline = __import__("time").time() + timeout
        last_error = None
        while __import__("time").time() < deadline:
            for by, value in locators:
                try:
                    element = driver.find_element(by, value)
                    if element and element.is_displayed():
                        return element
                except Exception as exc:
                    last_error = exc
            sleep(0.5)
        if last_error:
            raise last_error
        raise TimeoutError(f"Could not find any of: {locators}")

    def _hardware_click(self, element):
        """Generates a raw OS-level mouse click via Chrome DevTools Protocol."""
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", element)
        sleep(0.5)
        
        rect = self.driver.execute_script("return arguments[0].getBoundingClientRect();", element)
        x = int(rect['left'] + (rect['width'] / 2))
        y = int(rect['top'] + (rect['height'] / 2))
        
        self.driver.execute_cdp_cmd('Input.dispatchMouseEvent', {'type': 'mouseMoved', 'x': x, 'y': y})
        sleep(0.1)
        self.driver.execute_cdp_cmd('Input.dispatchMouseEvent', {'type': 'mousePressed', 'x': x, 'y': y, 'button': 'left', 'clickCount': 1})
        sleep(0.1)
        self.driver.execute_cdp_cmd('Input.dispatchMouseEvent', {'type': 'mouseReleased', 'x': x, 'y': y, 'button': 'left', 'clickCount': 1})

    def _login(self):
        try:
            email_field = self._find_any(self.driver, [(By.ID, "identifierId"), (By.CSS_SELECTOR, "input[type='email']")], timeout=20)
            email_field.clear()
            email_field.send_keys(self.mailaddress)

            identifier_next = self._find_any(self.driver, [(By.ID, "identifierNext"), (By.XPATH, "//button[.//*[normalize-space()='Next']]")], timeout=20)
            self._hardware_click(identifier_next)

            password_field = self._find_any(self.driver, [(By.NAME, "Passwd"), (By.CSS_SELECTOR, "input[type='password']"), (By.ID, "password")], timeout=25)
            password_field.clear()
            password_field.send_keys(self.password)

            password_next = self._find_any(self.driver, [(By.ID, "passwordNext"), (By.XPATH, "//button[.//*[normalize-space()='Next']]")], timeout=20)
            self._hardware_click(password_next)
            
            sleep(random.choice(self.waitDuration))
            
        except Exception as exc:
            print("There is a problem 1 during login.")
            print(f"Login detail: {exc}")
            raise exc

    def _comment(self):
        try:
            self.i += 1
            self.driver.get(self.urls[self.i])
            sleep(5)

            # Step 1: Open the review modal
            review_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Write a review') or contains(@aria-label, 'Rate this place')]"))
            )
            self._hardware_click(review_button)
            sleep(3)

            # Step 2: Inject your exact comment text safely via DOM/JS
            target_comment = "Good overall experience with clear communication and efficient support. Everything was reasonably well organized, and the team made the process easy to understand and complete."
            
            self.driver.execute_script("""
                let commentText = arguments[0];
                let ta = document.querySelector('textarea');
                if (ta) {
                    ta.focus();
                    let nativeSetter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, "value").set;
                    if (nativeSetter) {
                        nativeSetter.call(ta, commentText);
                    } else {
                        ta.value = commentText;
                    }
                    ta.dispatchEvent(new Event('input', { bubbles: true }));
                    ta.dispatchEvent(new Event('change', { bubbles: true }));
                }
            """, target_comment)
            sleep(1.5)

            # Step 3: Trigger your custom coordinate visual agent for the star and post button
            success = post_review_visually()
            if not success:
                print("Warning: Visual poster encountered an issue.")
            
            sleep(random.choice(self.waitDuration))
            
            # Save completed account credentials
            with open(self.completedAccountsPath, "a", encoding="utf-8") as completedAccounts:
                completedAccounts.write(self.mailaddress + "-" + self.password + "\n")
                
        except Exception as exc:
            print("There is a problem in Comment.")
            print(f"Comment detail: {exc}")
        finally:
            if self.driver:
                try:
                    self.driver.quit()
                except Exception:
                    pass

    @staticmethod
    def _read_single_column_csv(file_path):
        rows = []
        with open(file_path, "r", encoding="utf-8-sig", errors="replace") as csv_file:
            for raw_line in csv_file:
                value = raw_line.strip().strip('"')
                if not value:
                    continue
                if value.lower() in {"mailaddress", "password", "comment"}:
                    continue
                rows.append(value)
        return rows

    @staticmethod
    def GetUserInfo(mailaddressFile, passwordsFile, commentsFile):
        mail_addresses = GoogleReviewBot._read_single_column_csv(mailaddressFile)
        passwords = GoogleReviewBot._read_single_column_csv(passwordsFile)
        comments = GoogleReviewBot._read_single_column_csv(commentsFile)

        num = min(len(mail_addresses), len(passwords), len(comments))
        if num <= 0:
            raise ValueError("CSV files do not contain any usable rows.")

        UserInfo = pd.DataFrame({
            "mailaddress": mail_addresses[:num],
            "password": passwords[:num],
            "comment": comments[:num],
        })
        UserInfo = UserInfo.sample(frac=1, random_state=0).reset_index(drop=True)
        return UserInfo
    
    
if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parent
    mailaddressFile = base_dir / "data" / "mailaddresses.csv"
    passwordsFile = base_dir / "data" / "passwords.csv"
    commentsFile = base_dir / "data" / "comments.csv"

    UserInfoDF = GoogleReviewBot.GetUserInfo(str(mailaddressFile), str(passwordsFile), str(commentsFile))
    for num in range(len(UserInfoDF)):
        UserInfoSeries = UserInfoDF.loc[num]
        try:
            GRB = GoogleReviewBot(UserInfoSeries["mailaddress"], UserInfoSeries["password"], UserInfoSeries["comment"])
            GRB._login()
            GRB._comment()
        except Exception as exc:
            print(f"There is a problem during account processing: {exc}")
            pass