
import sys

def test_import(module_name):
    print(f"Testing {module_name}...", end=" ", flush=True)
    try:
        if module_name == "PIL":
            import PIL
        else:
            __import__(module_name)
        print(f"✅")
    except ImportError as e:
        print(f"❌ Failed: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

print("Starting import tests...", flush=True)
test_import("os")
test_import("time")
test_import("datetime")
test_import("pathlib")
test_import("pyautogui")
test_import("google.genai")
test_import("pymongo")

try:
    print("Testing dotenv...", end=" ", flush=True)
    from dotenv import load_dotenv
    print("✅")
except:
    print("❌ Failed")
    
test_import("psutil")
test_import("logging")
test_import("sys")

# Optional dependencies
test_import("win32gui")
test_import("PIL")
print("Done.", flush=True)
