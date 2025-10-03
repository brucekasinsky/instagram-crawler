"""
Configuration file for Instagram Scraper
"""
import os
from typing import List, Dict

# Proxy Configuration
PROXY_CONFIG = {
    'http': 'http://user-juicyspace69-country-br-city-salvador-sessionduration-60:aCQs0w0Qjbj9l9Umex@gate.smartproxy.com:10001',
    'https': 'https://user-juicyspace69-country-br-city-salvador-sessionduration-60:aCQs0w0Qjbj9l9Umex@gate.smartproxy.com:10001'
}

# Fake Users for Login (same as PHP)
FAKE_USERS = [
    ['brucekasinskybackup', 'Le22fa5ble22fa5b'],
    ['brucekasinskybackup', 'Le22fa5ble22fa5b'],
    ['brucekasinskybackup', 'Le22fa5ble22fa5b']
]

# User Agents (Updated 2024/2025)
USER_AGENTS = [
    # Chrome 136 (latest)
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Linux; Android 14; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2.1 Mobile/15E148 Safari/604.1',
    # Firefox 138 (latest)
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:138.0) Gecko/20100101 Firefox/138.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:138.0) Gecko/20100101 Firefox/138.0',
    # Safari 18.5 (latest)
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.5 Safari/605.1.15',
    # Edge 136 (latest)
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0'
]

# Instagram App User Agent (Latest)
INSTAGRAM_APP_USER_AGENT = 'Instagram 320.0.0.32.90 Android (34/14; 420dpi; 1080x2400; samsung; SM-G998B; o1s; exynos2100; pt_BR; 456789123)'

# Request Settings
REQUEST_SETTINGS = {
    'timeout': 60,
    'connect_timeout': 30,
    'max_retries': 3,
    'retry_delay': (3, 7),  # Random delay between 3-7 seconds
    'request_delay': (2, 5)  # Random delay between requests
}

# Instagram API Settings
INSTAGRAM_SETTINGS = {
    'min_followers': 1000,
    'max_posts_analyze': 20,
    'max_reels_analyze': 10,
    'cache_duration': 3600,  # 1 hour
    'session_duration': 3600  # 1 hour
}

# File Paths
PATHS = {
    'cache_dir': '../cache/instagram',
    'temp_images': '../assets/tempprofileimg',
    'error_logs': '../assets/error_logs',
    'output_dir': '../assets/python_output'
}

# Headers for requests
DEFAULT_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    'Accept-Encoding': 'gzip, deflate',
    'Cache-Control': 'max-age=0',
    'DNT': '1',
    'Sec-GPC': '1',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1'
}

# Instagram-specific headers
INSTAGRAM_HEADERS = {
    'X-IG-App-Locale': 'pt_BR',
    'X-IG-Device-Locale': 'pt_BR',
    'X-IG-Mapped-Locale': 'pt_BR',
    'X-IG-Connection-Type': 'WIFI',
    'X-IG-Capabilities': '3brTvwE=',
    'X-IG-App-ID': '567067343352427',
    'X-IG-Android-ID': 'android-456789123',
    'X-IG-Device-ID': 'android-456789123'
}

# Error handling
ERROR_CONFIG = {
    'max_consecutive_errors': 3,
    'error_cooldown': 300,  # 5 minutes
    'log_level': 'INFO'
}
