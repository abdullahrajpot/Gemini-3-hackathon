"""
Test Gemini Vision API with image analysis
"""
from google import genai
from dotenv import load_dotenv
import os
from pathlib import Path

def test_gemini_vision():
    print("🧪 Testing Gemini Vision API...")
    print()
    
    # Load environment
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print("❌ GEMINI_API_KEY not found in .env file")
        return False
    
    print(f"✅ API Key loaded: {api_key[:10]}...{api_key[-4:]}")
    
    # Initialize client
    try:
        client = genai.Client(api_key=api_key)
        print("✅ Gemini client initialized")
    except Exception as e:
        print(f"❌ Failed to initialize client: {e}")
        return False
    
    # Check for test image
    test_image = Path("./storage/test_capture.jpg")
    if not test_image.exists():
        print(f"❌ Test image not found: {test_image}")
        print("   Run test_screenshot.py first to create a test image")
        return False
    
    print(f"✅ Test image found: {test_image}")
    
    # Upload image
    try:
        print()
        print("📤 Uploading image to Gemini...")
        uploaded = client.files.upload(file=str(test_image))
        print(f"✅ Image uploaded successfully!")
        print(f"   URI: {uploaded.uri}")
        print(f"   Name: {uploaded.name}")
    except Exception as e:
        print(f"❌ Upload failed: {e}")
        return False
    
    # Analyze image
    try:
        print()
        print("🤖 Analyzing image with Gemini...")
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=["Describe this screen in detail. What apps are open? What is the user doing?", uploaded]
        )
        
        print(f"✅ Analysis complete!")
        print()
        print("=" * 60)
        print("GEMINI ANALYSIS:")
        print("=" * 60)
        print(response.text)
        print("=" * 60)
        print()
        print("✅ Gemini Vision test PASSED")
        return True
        
    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
            print("   ⚠️  API quota limit reached. Wait 60 seconds and try again.")
        return False

if __name__ == "__main__":
    test_gemini_vision()
