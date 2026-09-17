import pyautogui
from time import sleep

def post_review_visually():
    """Uses OS-level mouse and keyboard control with your exact measured coordinates.
    """
    try:
        # Give a brief pause for the modal to fully render on screen
        sleep(3)

        # 1. Click the 4th star using your exact coordinate (1025, 440)
        pyautogui.moveTo(1025, 440, duration=0.4)
        pyautogui.click()
        sleep(1)

        # 2. Click the Post button using your exact coordinate (1255, 855)
        # Note: We click Post directly since the comment is already injected safely via the main script
        pyautogui.moveTo(1255, 855, duration=0.4)
        pyautogui.click()
        
        print("Visual agent successfully clicked the star and posted the review!")
        sleep(3)
        return True

    except Exception as e:
        print(f"Visual poster error: {e}")
        return False