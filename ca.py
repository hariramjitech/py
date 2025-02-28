import pynput
import pyautogui
import time

# Define keyword-to-text mappings
expansions = {
    "pass": """23cs068""",
    "email": """727723eucs074@skcet.ac.in""",
    "url": """https://placement.skcet.ac.in""",
    "code": """def hello_world():
    print("Hello, World!")
    for i in range(5):
    hello_world()""",
}

typed_text = ""  # Buffer to store typed characters

def on_press(key):
    global typed_text

    try:
        if hasattr(key, 'char') and key.char:
            typed_text += key.char  # Add to buffer

            for keyword, replacement in expansions.items():
                if typed_text.endswith(keyword):
                    time.sleep(0.1)  # Short delay for stability

                    # Delete the typed keyword
                    for _ in range(len(keyword)):
                        pyautogui.press('backspace')
                        time.sleep(0.01)  # Small delay to avoid key misses

                    # Type the full expansion text
                    pyautogui.write(replacement, interval=0.02)

                    typed_text = ""  # Reset buffer after expansion

    except AttributeError:
        if key == pynput.keyboard.Key.backspace:
            typed_text = typed_text[:-1]  # Handle backspace correctly

# Start listening to keyboard input
with pynput.keyboard.Listener(on_press=on_press) as listener:
    listener.join()

