"""
Test privacy filter functionality
"""
from collector import is_sensitive_content

def test_privacy_filter():
    print("🧪 Testing Privacy Filter...")
    print()
    
    test_cases = [
        # (window_title, should_block, description)
        ("Chrome - Sign in to Google", True, "Login page"),
        ("1Password - Vault", True, "Password manager"),
        ("Incognito - New Tab", True, "Private browsing"),
        ("Chrome - PayPal - Send Money", True, "Payment service"),
        ("Bitwarden - Unlock Vault", True, "Password manager unlock"),
        ("Enter Password - Windows Security", True, "Password prompt"),
        ("VS Code - main.py", False, "Code editor"),
        ("Spotify - Playlist", False, "Music app"),
        ("Chrome - YouTube - Home", False, "Video streaming"),
        ("Discord - General Chat", False, "Chat app"),
        ("Notion - Project Notes", False, "Note-taking"),
        ("Figma - Design System", False, "Design tool"),
        ("Terminal - bash", False, "Command line"),
        ("Chrome - GitHub - Repository", False, "Code hosting"),
        ("Slack - #engineering", False, "Team chat"),
    ]
    
    passed = 0
    failed = 0
    
    print(f"{'Window Title':<45} {'Expected':<10} {'Result':<10} {'Keyword':<20} {'Status'}")
    print("=" * 100)
    
    for window_title, should_block, description in test_cases:
        is_blocked, keyword = is_sensitive_content(window_title)
        
        # Check if result matches expectation
        is_correct = is_blocked == should_block
        status = "✅ PASS" if is_correct else "❌ FAIL"
        
        if is_correct:
            passed += 1
        else:
            failed += 1
        
        expected_str = "BLOCK" if should_block else "ALLOW"
        result_str = "BLOCK" if is_blocked else "ALLOW"
        keyword_str = keyword if keyword else "N/A"
        
        print(f"{window_title[:44]:<45} {expected_str:<10} {result_str:<10} {keyword_str:<20} {status}")
    
    print("=" * 100)
    print()
    print(f"📊 Test Results:")
    print(f"   ✅ Passed: {passed}/{len(test_cases)}")
    print(f"   ❌ Failed: {failed}/{len(test_cases)}")
    print()
    
    if failed == 0:
        print("✅ All privacy filter tests PASSED")
        return True
    else:
        print(f"❌ {failed} test(s) FAILED")
        return False

if __name__ == "__main__":
    test_privacy_filter()
