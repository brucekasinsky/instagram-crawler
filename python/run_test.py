"""
Test script for Instagram Scraper
Quick test to verify everything is working
"""
import json
import sys
from instagram_scraper import InstagramScraper

def test_scraper():
    """Test the Instagram scraper with felipeneto"""
    print("🚀 Testing Instagram Scraper...")
    print("=" * 50)
    
    try:
        # Initialize scraper
        print("📱 Initializing scraper...")
        scraper = InstagramScraper()
        
        # Test with felipeneto (same as PHP version)
        print("🔍 Scraping user: felipeneto")
        result = scraper.scrape_user("felipeneto")
        
        # Display results
        print("\n📊 Results:")
        print("=" * 30)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
        # Check if successful
        if result.get('success') == 1:
            print("\n✅ SUCCESS: Scraper is working correctly!")
            
            # Parse the data to show some details
            try:
                instagram_data = json.loads(result['data']['instagram'])
                print(f"\n📈 Profile Data:")
                print(f"   Username: {instagram_data.get('username')}")
                print(f"   Followers: {instagram_data.get('followers'):,}")
                print(f"   Following: {instagram_data.get('following'):,}")
                print(f"   Posts: {instagram_data.get('uploads'):,}")
                print(f"   Verified: {'Yes' if instagram_data.get('is_verified') else 'No'}")
                
                details_data = json.loads(result['data']['details'])
                print(f"\n📊 Engagement Data:")
                print(f"   Average Engagement Rate: {details_data.get('reels_average_engagement_rate', 0)}%")
                print(f"   Total Likes: {details_data.get('total_likes', 0):,}")
                print(f"   Total Comments: {details_data.get('total_comments', 0):,}")
                
            except Exception as e:
                print(f"⚠️  Could not parse detailed data: {e}")
                
        else:
            print(f"\n❌ FAILED: {result.get('message', 'Unknown error')}")
            
    except Exception as e:
        print(f"\n💥 ERROR: {str(e)}")
        print("Check the logs for more details.")
        return False
    
    return True

def test_configuration():
    """Test configuration loading"""
    print("⚙️  Testing configuration...")
    
    try:
        from config import PROXY_CONFIG, FAKE_USERS, USER_AGENTS
        print(f"✅ Proxy configured: {bool(PROXY_CONFIG.get('http'))}")
        print(f"✅ Fake users loaded: {len(FAKE_USERS)}")
        print(f"✅ User agents loaded: {len(USER_AGENTS)}")
        return True
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 Instagram Scraper Test Suite")
    print("=" * 50)
    
    # Test 1: Configuration
    config_ok = test_configuration()
    print()
    
    if not config_ok:
        print("❌ Configuration test failed. Please check config.py")
        return
    
    # Test 2: Scraper functionality
    scraper_ok = test_scraper()
    
    print("\n" + "=" * 50)
    if config_ok and scraper_ok:
        print("🎉 ALL TESTS PASSED! The scraper is ready to use.")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")

if __name__ == "__main__":
    main()
