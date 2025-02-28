
import pynput
import pyautogui
import pyperclip
import time

# Define keyword-to-text mappings
expansions = {
    "addr": """123 Main Street, Cityville, USA""",
    "email": """example@email.com""",
    "sign": """Best regards,\nYour Name""",
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
                    time.sleep(0.1)  # Ensure keyword is fully typed

                    # Delete the keyword
                    for _ in range(len(keyword)):
                        pyautogui.press('backspace')
                        time.sleep(0.01)  

                    time.sleep(0.1)  # Short delay before pasting

                    # Copy the full text to clipboard
                    pyperclip.copy(replacement)
                    pyautogui.hotkey("ctrl", "v")  # Paste instead of typing

                    typed_text = ""  # Reset buffer

    except AttributeError:
        if key == pynput.keyboard.Key.backspace:
            typed_text = typed_text[:-1]  # Handle backspace correctly

# Start listening to keyboard input
with pynput.keyboard.Listener(on_press=on_press) as listener:
    listener.join()
