import pyautogui
from time import sleep

def post_review_visually(comment_text):
    """Uses OS-level mouse and keyboard control with your exact measured coordinates
       and types the dynamic comment pulled from comments.csv.
    """
    try:
        # Give a brief pause for the modal to fully render on screen
        sleep(3)

        # 1. Click the 4th star using your coordinate (1025, 440)
        pyautogui.moveTo(1025, 440, duration=0.4)
        pyautogui.click()
        sleep(1)

        # 2. Click inside the comment text area box (approx center of textarea: 960, 560)
        pyautogui.moveTo(960, 560, duration=0.3)
        pyautogui.click()
        sleep(0.5)

        # 3. Type the comment from comments.csv dynamically via OS keyboard buffer
        pyautogui.write(comment_text, interval=0.01)
        sleep(1.5)

        # 4. Scroll down the modal to bring the Post button into view
        pyautogui.scroll(-600)
        sleep(1)

        # 5. Click the Post button using your coordinate (1255, 855)
        pyautogui.moveTo(1255, 855, duration=0.4)
        pyautogui.click()
        
        print("Visual agent successfully posted the review!")
        sleep(3)
        return True

    except Exception as e:
        print(f"Visual poster error: {e}")
        return False