# Google Map Review Bot ![License](https://img.shields.io/badge/License-MIT-red.svg)

An advanced, multi-account Python automation pipeline designed to programmatically submit customized Google Maps reviews. This project uses a hybrid architecture combining stealth browser automation with OS-level visual emulation to successfully bypass modern browser security layers, DOM restrictions, and React's `isTrusted` bot-detection mechanisms.

---

## Key Features

* **Hybrid Automation Engine:** Integrates `undetected-chromedriver` and Chrome DevTools Protocol (CDP) for secure login management, paired with **PyAutoGUI** for robust OS-level visual mouse and keyboard interactions.
* **`isTrusted` Bypass:** Overcomes React's synthetic event blocking by dispatching true hardware-level interrupts at the operating system kernel level.
* **Sequential Multi-Account Pipeline:** Handles end-to-end session lifecycles—signing in, navigating, reviewing, and cleanly closing sessions sequentially across multiple accounts.
* **Dynamic CSV Integration:** Automatically pulls credentials and customized review comments from structured datasets (`mailaddresses.csv`, `passwords.csv`, `comments.csv`).
* **Visual Coordinate Mapping:** Employs precise screen resolution scaling and coordinate-based clicking to seamlessly interact with dynamic modals where traditional DOM element selection fails.

---

## Project Structure

```text
bot-main/
│
├── data/
│   ├── comments.csv
│   ├── completedAccounts.csv
│   ├── mailaddresses.csv
│   └── passwords.csv
│
├── GoogleReviewBot.py
├── visual_poster.py
├── LICENSE
├── README.md
└── requirements.txt

Setup & Installation
Clone the Repository:

Bash
git clone [https://github.com/keshav-rao/Google_Map_Review_Bot.git](https://github.com/keshav-rao/Google_Map_Review_Bot.git)
cd Google_Map_Review_Bot
Install Dependencies:
Ensure you have Python installed, then install the required automation libraries:

Bash
pip install -r requirements.txt
(Required packages: undetected-chromedriver, pandas, pyautogui)

Configure Your Data Files:
Navigate into the data/ folder and populate your records:

mailaddresses.csv: List of Google account emails (one per line).

passwords.csv: Corresponding account passwords (one per line).

comments.csv: Customized review comments (one per line).

Note: The total number of rows across all three CSV files must match.

Set Your Target URL:
Open GoogleReviewBot.py and update the PlaceURL variable with the Google Maps link of the location you wish to review.

Usage
Ensure your monitor is set to a maximized or full-screen window environment so the visual agent coordinates align accurately.

Run the automation pipeline from your terminal:

Bash
python GoogleReviewBot.py
Important Note: While the visual agent (pyautogui) is actively executing clicks and typing reviews, avoid moving your physical mouse or typing on your keyboard to ensure smooth execution.

License
Distributed under the MIT License. See LICENSE for more information.