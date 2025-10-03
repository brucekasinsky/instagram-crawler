#!/usr/bin/env python3
"""
Quick Debug - Verificar campos de views rapidamente
"""
import instaloader
from config import PROXY_CONFIG

print("🔍 Quick Debug - Campos de Views")
print("=" * 40)

# Initialize instaloader
L = instaloader.Instaloader()

# Configure proxy
session = L.context._session
session.proxies = {'http': PROXY_CONFIG['http'], 'https': PROXY_CONFIG['https']}

# Load profile
profile = instaloader.Profile.from_username(L.context, "felipeneto")
print(f"✅ Perfil: {profile.username}")

# Get first reel
posts_generator = profile.get_posts()
for post in posts_generator:
    if getattr(post, 'typename', '') == 'GraphVideo':
        print(f"\n📹 REEL: {getattr(post, 'shortcode', 'N/A')}")
        print(f"   Likes: {getattr(post, 'likes', 0)}")
        print(f"   Comments: {getattr(post, 'comments', 0)}")
        print(f"   video_view_count: {getattr(post, 'video_view_count', 0)}")
        print(f"   view_count: {getattr(post, 'view_count', 'N/A')}")
        print(f"   views: {getattr(post, 'views', 'N/A')}")
        print(f"   play_count: {getattr(post, 'play_count', 'N/A')}")
        break

print("\n✅ Debug concluído!")



