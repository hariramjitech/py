import sys
import time
import pyautogui
import pyperclip
import subprocess
import threading
from pynput import keyboard

# Global variables
generated_text = ""
is_paused = False  # Toggle for pausing auto-typing


def run_ollama():
    """Fetch text from clipboard, process it through Ollama, and store the output."""
    global generated_text
    copied_text = pyperclip.paste().strip()

    if not copied_text:
        print("[❌ ERROR] No text found in the clipboard.")
        return

    try:
        print("[✅ INFO] Running Ollama with input:", copied_text)

        process = subprocess.Popen(
            ["ollama", "run", "deepseek-r1:1.5b"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        output, error = process.communicate(input=copied_text)

        if process.returncode != 0:
            print(f"[❌ ERROR] Ollama execution failed! Exit code: {process.returncode}")
            print(f"[💡 DEBUG] STDERR: {error.strip()}")
            generated_text = "[⚠️ ERROR] Ollama failed to generate output."
            return

        if not output.strip():
            print("[⚠️ WARNING] No output received from Ollama.")
            generated_text = "[⚠️ ERROR] Ollama returned an empty response."
            return

        generated_text = output.strip()
        print("[✅ SUCCESS] Generated Output:", generated_text)
        pyperclip.copy(generated_text)  # Copy to clipboard

    except FileNotFoundError:
        print("[❌ ERROR] Ollama is not installed or not found in PATH.")
    except subprocess.SubprocessError as e:
        print(f"[❌ ERROR] Subprocess error occurred: {e}")
    except Exception as e:
        print(f"[❌ ERROR] Unexpected error in run_ollama(): {e}")
        generated_text = "[⚠️ ERROR] Unexpected error."


def type_generated_text():
    """Autotypes the generated text asynchronously."""
    global generated_text, is_paused
    if not generated_text:
        print("[❌ ERROR] No generated text to type.")
        return

    # Detect if the text is code
    is_code = generated_text.startswith("```") and generated_text.endswith("```")
    if is_code:
        generated_text = "\n".join(generated_text.split("\n")[1:-1])  # Remove ``` markers

    def typer():
        try:
            for char in generated_text:
                if is_paused:
                    print("[⏸️ PAUSED] Typing paused...")
                    while is_paused:
                        time.sleep(0.1)
                    print("[▶️ RESUMED] Typing resumed...")

                pyautogui.typewrite(char)
                time.sleep(0.005)
            print("[✅ SUCCESS] Successfully typed generated text.")
        except pyautogui.FailSafeException as e:
            print("[❌ ERROR] Typing stopped due to PyAutoGUI fail-safe trigger.")
        except Exception as e:
            print(f"[❌ ERROR] Unexpected error in typer(): {e}")

    # Run typing in a new thread
    threading.Thread(target=typer, daemon=True).start()


def toggle_pause():
    """Toggles the pause state for autotyping."""
    global is_paused
    is_paused = not is_paused
    print("[⏸️ PAUSED]" if is_paused else "[▶️ RESUMED]")


def exit_program():
    """Exits the program safely."""
    print("[🛑 EXIT] Exiting...")
    sys.exit()


# Hotkeys: Ctrl+Alt+C to copy and send to Ollama, F8 to type output, F9 to pause/resume
the_listener = keyboard.GlobalHotKeys({
    '<ctrl>+<alt>+c': lambda: threading.Thread(target=run_ollama, daemon=True).start(),
    '<f8>': type_generated_text,
    '<f9>': toggle_pause,
    '<delete>': exit_program
})

# Start keyboard listener in a thread
try:
    print("[🎧 LISTENING] Hotkeys enabled. Use Ctrl+Alt+C, F8, F9, or Delete.")
    the_listener.start()
    the_listener.join()
except KeyboardInterrupt:
    print("[🛑 EXIT] Program interrupted by user.")
except Exception as e:
    print(f"[❌ ERROR] Unexpected error in main thread: {e}")

