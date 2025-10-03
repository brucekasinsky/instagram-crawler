"""
Instagram Scraper - Python Version
Based on indexdados.php functionality
"""
import json
import time
import random
import os
import sys
import requests
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path

# Instagram Private API
from instagram_private_api import Client, ClientError, ClientLoginError
# Remove problematic imports - these classes don't exist in version 1.6.0
# from instagram_private_api.errors import (
#     ChallengeRequiredError,
#     CheckpointRequiredError,
#     LoginRequiredError,
#     RateLimitError
# )

# Configuration
from config import (
    PROXY_CONFIG, FAKE_USERS, USER_AGENTS, INSTAGRAM_APP_USER_AGENT,
    REQUEST_SETTINGS, INSTAGRAM_SETTINGS, PATHS, DEFAULT_HEADERS,
    INSTAGRAM_HEADERS, ERROR_CONFIG
)

# Logging
from loguru import logger

class InstagramScraper:
    """
    Instagram Scraper class that replicates the functionality of indexdados.php
    """
    
    def __init__(self):
        self.client = None
        self.current_user_index = 0
        self.consecutive_errors = 0
        self.last_error_time = None
        
        # Setup logging
        self._setup_logging()
        
        # Create directories
        self._create_directories()
        
        # Setup proxy
        self._setup_proxy()
    
    def _setup_logging(self):
        """Setup logging configuration"""
        log_file = Path(PATHS['error_logs']) / f"instagram_scraper_{datetime.now().strftime('%Y-%m-%d')}.log"
        logger.add(
            log_file,
            rotation="1 day",
            retention="30 days",
            level=ERROR_CONFIG['log_level'],
            format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
        )
    
    def _create_directories(self):
        """Create necessary directories"""
        for path in PATHS.values():
            Path(path).mkdir(parents=True, exist_ok=True)
    
    def _setup_proxy(self):
        """Setup proxy configuration"""
        self.proxies = PROXY_CONFIG
        logger.info(f"Proxy configured: {self.proxies['http']}")
    
    def _get_random_user_agent(self) -> str:
        """Get a random user agent from the list"""
        return random.choice(USER_AGENTS)
    
    def _get_random_delay(self, delay_range: tuple = REQUEST_SETTINGS['request_delay']) -> float:
        """Get random delay between requests"""
        return random.uniform(delay_range[0], delay_range[1])
    
    def _save_error_log(self, error: Exception, context: Dict = None):
        """Save error details to JSON log file"""
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        error_file = Path(PATHS['error_logs']) / f"instagram_error_{timestamp}.json"
        
        error_data = {
            'timestamp': timestamp,
            'error_type': type(error).__name__,
            'error_message': str(error),
            'context': context or {},
            'user_agent': self._get_random_user_agent(),
            'proxy_config': self.proxies,
            'consecutive_errors': self.consecutive_errors
        }
        
        with open(error_file, 'w', encoding='utf-8') as f:
            json.dump(error_data, f, indent=2, ensure_ascii=False)
        
        logger.error(f"Error saved to: {error_file}")
    
    def _log_detailed_error(self, error: Exception, username: str, attempt: int):
        """Log detailed error information including response content"""
        try:
            # Get error details
            error_type = type(error).__name__
            error_message = str(error)
            
            # Try to extract response content if available
            response_content = None
            status_code = None
            
            if hasattr(error, 'response'):
                response = error.response
                if hasattr(response, 'text'):
                    response_content = response.text
                if hasattr(response, 'status_code'):
                    status_code = response.status_code
            
            # Log to file
            timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            detailed_log_file = Path(PATHS['error_logs']) / f"detailed_error_{timestamp}.json"
            
            detailed_error_data = {
                'timestamp': timestamp,
                'error_type': error_type,
                'error_message': error_message,
                'username': username,
                'attempt': attempt,
                'status_code': status_code,
                'response_content': response_content,
                'proxy_config': self.proxies,
                'user_agent': self._get_random_user_agent()
            }
            
            with open(detailed_log_file, 'w', encoding='utf-8') as f:
                json.dump(detailed_error_data, f, indent=2, ensure_ascii=False)
            
            logger.error(f"Detailed error logged to: {detailed_log_file}")
            
            # Print summary to console
            print(f"📋 Detalhes do erro:")
            print(f"   Tipo: {error_type}")
            print(f"   Mensagem: {error_message}")
            if status_code:
                print(f"   Status HTTP: {status_code}")
            if response_content:
                print(f"   Resposta HTML (primeiros 200 chars): {response_content[:200]}...")
                print(f"   📁 Resposta completa salva em: {detailed_log_file}")
            
        except Exception as log_error:
            logger.error(f"Failed to log detailed error: {str(log_error)}")
            print(f"❌ Erro ao salvar detalhes: {str(log_error)}")
    
    def _login_with_retry(self) -> bool:
        """
        Login with retry mechanism using different fake users
        """
        max_attempts = len(FAKE_USERS)
        
        for attempt in range(max_attempts):
            try:
                if self.current_user_index >= len(FAKE_USERS):
                    self.current_user_index = 0
                
                username, password = FAKE_USERS[self.current_user_index]
                logger.info(f"🔄 Attempting login with user: {username} (attempt {attempt + 1}/{max_attempts})")
                print(f"🔄 Tentando login com usuário: {username} (tentativa {attempt + 1}/{max_attempts})")
                
                # Log proxy configuration
                logger.info(f"🌐 Using proxy: {self.proxies['http']}")
                print(f"🌐 Usando proxy: {self.proxies['http'][:50]}...")
                
                # Log user agent
                user_agent = self._get_random_user_agent()
                logger.info(f"📱 User Agent: {user_agent}")
                print(f"📱 User Agent: {user_agent[:50]}...")
                
                print("⏳ Criando cliente Instagram...")
                logger.info("Creating Instagram client instance...")
                
                # Create new client instance for each attempt with timeout
                import signal
                
                def timeout_handler(signum, frame):
                    raise TimeoutError("Client creation timeout")
                
                # Set timeout for client creation (30 seconds)
                signal.signal(signal.SIGALRM, timeout_handler)
                signal.alarm(30)
                
                try:
                    print("🔧 Configurando parâmetros do cliente...")
                    client_settings = {
                        'user_agent': user_agent,
                        'device_settings': {
                            'app_version': '320.0.0.32.90',
                            'android_version': 34,
                            'android_release': '14',
                            'manufacturer': 'samsung',
                            'model': 'SM-G998B',
                            'cpu': 'exynos2100',
                            'locale': 'pt_BR'
                        }
                    }
                    
                print("🔐 Iniciando autenticação...")
                logger.info(f"Client settings: {client_settings}")
                
                # Test proxy connectivity first
                print("🌐 Testando conectividade do proxy...")
                try:
                    test_response = requests.get(
                        'https://httpbin.org/ip', 
                        proxies=self.proxies, 
                        timeout=10
                    )
                    print(f"✅ Proxy funcionando - IP: {test_response.json().get('origin', 'N/A')}")
                except Exception as proxy_error:
                    print(f"⚠️ Aviso: Problema com proxy: {str(proxy_error)}")
                    logger.warning(f"Proxy connectivity issue: {str(proxy_error)}")
                
                print("🔑 Tentando autenticar no Instagram...")
                self.client = Client(
                    username=username,
                    password=password,
                    proxy=self.proxies,
                    user_agent=user_agent,
                    settings=client_settings
                )
                
                # Cancel timeout
                signal.alarm(0)
                
                except TimeoutError:
                    signal.alarm(0)
                    raise Exception("Timeout na criação do cliente Instagram (30s)")
                except Exception as e:
                    signal.alarm(0)
                    raise e
                
                print("✅ Cliente criado com sucesso!")
                logger.info("Instagram client created successfully")
                
                # Add delay after login
                delay = self._get_random_delay()
                print(f"⏳ Aguardando {delay:.1f}s após login...")
                time.sleep(delay)
                
                print(f"✅ Login realizado com sucesso para: {username}")
                logger.info(f"Successfully logged in with user: {username}")
                self.consecutive_errors = 0
                return True
                
            except (ClientLoginError, ClientError) as e:
                error_msg = str(e)
                logger.warning(f"❌ Login failed for user {username}: {error_msg}")
                print(f"❌ Falha no login para {username}: {error_msg}")
                
                # Log detailed error information
                self._log_detailed_error(e, username, attempt + 1)
                
                self.current_user_index += 1
                self._save_error_log(e, {'username': username, 'attempt': attempt + 1})
                
                if attempt < max_attempts - 1:
                    delay = self._get_random_delay((5, 10))
                    print(f"⏳ Aguardando {delay:.1f}s antes da próxima tentativa...")
                    logger.info(f"Waiting {delay:.1f}s before next login attempt...")
                    time.sleep(delay)
                
            except Exception as e:
                error_msg = str(e)
                logger.error(f"💥 Unexpected error during login: {error_msg}")
                print(f"💥 Erro inesperado durante login: {error_msg}")
                
                # Log detailed error information
                self._log_detailed_error(e, username, attempt + 1)
                
                self._save_error_log(e, {'username': username, 'attempt': attempt + 1})
                self.current_user_index += 1
                
                if attempt < max_attempts - 1:
                    delay = self._get_random_delay((5, 10))
                    print(f"⏳ Aguardando {delay:.1f}s antes da próxima tentativa...")
                    time.sleep(delay)
        
        print("❌ Todas as tentativas de login falharam")
        logger.error("All login attempts failed")
        return False
    
    def get_profile_data(self, username: str) -> Optional[Dict]:
        """
        Get profile data for a given username
        Replicates the scrapper function from indexdados.php
        """
        try:
            if not self.client:
                print("🔐 Cliente não autenticado, tentando login...")
                if not self._login_with_retry():
                    print("❌ Falha na autenticação")
                    return None
            
            print(f"🔍 Buscando dados do perfil: {username}")
            logger.info(f"Fetching profile data for: {username}")
            
            # Get profile information
            print("⏳ Obtendo informações do perfil...")
            profile = self.client.user_info_by_username(username)
            
            if not profile:
                logger.error(f"Profile not found: {username}")
                return None
            
            # Check minimum followers
            if profile['user']['follower_count'] < INSTAGRAM_SETTINGS['min_followers']:
                logger.warning(f"User {username} has less than {INSTAGRAM_SETTINGS['min_followers']} followers")
                return {
                    'success': 0,
                    'message': 'O usuário não tem o mínimo de followers',
                    'data': []
                }
            
            # Check if profile is private
            if profile['user']['is_private']:
                logger.warning(f"Profile {username} is private")
                return {
                    'success': 0,
                    'message': 'O perfil é privado',
                    'data': []
                }
            
            # Get user's media
            time.sleep(self._get_random_delay())
            user_media = self.client.user_feed(profile['user']['pk'], count=INSTAGRAM_SETTINGS['max_posts_analyze'])
            
            # Get user's reels (if available)
            time.sleep(self._get_random_delay())
            try:
                user_reels = self.client.user_reel_media(profile['user']['pk'], count=INSTAGRAM_SETTINGS['max_reels_analyze'])
            except Exception as e:
                logger.warning(f"Could not fetch reels for {username}: {str(e)}")
                user_reels = {'items': []}
            
            # Process profile data
            profile_data = self._process_profile_data(profile, user_media, user_reels)
            
            logger.info(f"Successfully processed profile: {username}")
            return profile_data
            
        except (ClientError, ClientLoginError) as e:
            logger.error(f"Rate limit or login required: {str(e)}")
            self._save_error_log(e, {'username': username})
            self.client = None  # Force re-login
            return None
            
        except Exception as e:
            logger.error(f"Error fetching profile {username}: {str(e)}")
            self._save_error_log(e, {'username': username})
            self.consecutive_errors += 1
            return None
    
    def _process_profile_data(self, profile: Dict, user_media: Dict, user_reels: Dict) -> Dict:
        """
        Process profile data and calculate metrics
        Replicates the data processing logic from indexdados.php
        """
        user = profile['user']
        
        # Basic profile information
        profile_data = {
            'instagram_id': str(user['pk']),
            'username': user['username'],
            'full_name': user['full_name'] or user['username'],
            'description': user['biography'] or '',
            'website': user['external_url'] or '',
            'followers': user['follower_count'],
            'following': user['following_count'],
            'uploads': user['media_count'],
            'profile_picture_url': user['profile_pic_url'],
            'is_private': 1 if user['is_private'] else 0,
            'is_verified': 1 if user['is_verified'] else 0
        }
        
        # Process media data
        media_metrics = self._calculate_media_metrics(user_media.get('items', []), profile_data['followers'])
        reels_metrics = self._calculate_reels_metrics(user_reels.get('items', []), profile_data['followers'])
        
        # Calculate engagement rates
        profile_data['average_engagement_rate'] = media_metrics['average_engagement_rate']
        
        # Download profile picture
        profile_pic_path = self._download_profile_picture(profile_data['profile_picture_url'], profile_data['username'])
        if profile_pic_path:
            profile_data['profile_picture_url'] = profile_pic_path
        
        # Prepare details
        details = {
            'total_likes': media_metrics['total_likes'],
            'total_comments': media_metrics['total_comments'],
            'average_comments': media_metrics['average_comments'],
            'average_likes': media_metrics['average_likes'],
            'top_hashtags': media_metrics['top_hashtags'],
            'top_mentions': media_metrics['top_mentions'],
            'top_posts': media_metrics['top_posts'],
            # Reels data
            'reels_total_likes': reels_metrics['total_likes'],
            'reels_total_comments': reels_metrics['total_comments'],
            'reels_total_video_views': reels_metrics['total_views'],
            'reels_average_comments': reels_metrics['average_comments'],
            'reels_average_likes': reels_metrics['average_likes'],
            'reels_average_video_views': reels_metrics['average_views'],
            'reels_average_engagement_rate': reels_metrics['average_engagement_rate']
        }
        
        return {
            'success': 1,
            'message': 'dados recebidos com sucesso',
            'data': {
                'instagram': json.dumps(profile_data, ensure_ascii=False),
                'details': json.dumps(details, ensure_ascii=False),
                'image': profile_pic_path
            }
        }
    
    def _calculate_media_metrics(self, media_items: List[Dict], followers: int) -> Dict:
        """Calculate metrics for regular media posts"""
        likes_array = []
        comments_array = []
        engagement_rate_array = []
        hashtags_array = {}
        mentions_array = {}
        
        # Skip first 3 posts (as in PHP version)
        for media in media_items[3:]:
            if media.get('like_count'):
                likes_array.append(media['like_count'])
            if media.get('comment_count'):
                comments_array.append(media['comment_count'])
            
            # Calculate engagement rate
            total_engagement = media.get('like_count', 0) + media.get('comment_count', 0)
            if followers > 0:
                engagement_rate = (total_engagement / followers) * 100
                engagement_rate_array.append(engagement_rate)
            
            # Extract hashtags and mentions from caption
            caption = media.get('caption', {}).get('text', '') if media.get('caption') else ''
            if caption:
                hashtags = self._extract_hashtags(caption)
                mentions = self._extract_mentions(caption)
                
                for hashtag in hashtags:
                    hashtags_array[hashtag] = hashtags_array.get(hashtag, 0) + 1
                
                for mention in mentions:
                    mentions_array[mention] = mentions_array.get(mention, 0) + 1
        
        # Calculate averages
        total_likes = sum(likes_array) if likes_array else 0
        total_comments = sum(comments_array) if comments_array else 0
        average_likes = total_likes / len(likes_array) if likes_array else 0
        average_comments = total_comments / len(comments_array) if comments_array else 0
        average_engagement_rate = sum(engagement_rate_array) / len(engagement_rate_array) if engagement_rate_array else 0
        
        # Get top items
        top_hashtags = dict(sorted(hashtags_array.items(), key=lambda x: x[1], reverse=True)[:15])
        top_mentions = dict(sorted(mentions_array.items(), key=lambda x: x[1], reverse=True)[:15])
        top_posts = dict(sorted(zip(range(len(engagement_rate_array)), engagement_rate_array), 
                            key=lambda x: x[1], reverse=True)[:4])
        
        return {
            'total_likes': total_likes,
            'total_comments': total_comments,
            'average_likes': round(average_likes, 2),
            'average_comments': round(average_comments, 2),
            'average_engagement_rate': round(average_engagement_rate, 2),
            'top_hashtags': top_hashtags,
            'top_mentions': top_mentions,
            'top_posts': top_posts
        }
    
    def _calculate_reels_metrics(self, reels_items: List[Dict], followers: int) -> Dict:
        """Calculate metrics for reels"""
        likes_array = []
        comments_array = []
        views_array = []
        engagement_rate_array = []
        
        # Skip first 3 reels (as in PHP version)
        for reel in reels_items[3:]:
            if reel.get('like_count'):
                likes_array.append(reel['like_count'])
            if reel.get('comment_count'):
                comments_array.append(reel['comment_count'])
            if reel.get('play_count'):
                views_array.append(reel['play_count'])
            
            # Calculate engagement rate
            total_engagement = reel.get('like_count', 0) + reel.get('comment_count', 0)
            if followers > 0:
                engagement_rate = (total_engagement / followers) * 100
                engagement_rate_array.append(engagement_rate)
        
        # Calculate averages
        total_likes = sum(likes_array) if likes_array else 0
        total_comments = sum(comments_array) if comments_array else 0
        total_views = sum(views_array) if views_array else 0
        average_likes = total_likes / len(likes_array) if likes_array else 0
        average_comments = total_comments / len(comments_array) if comments_array else 0
        average_views = total_views / len(views_array) if views_array else 0
        average_engagement_rate = sum(engagement_rate_array) / len(engagement_rate_array) if engagement_rate_array else 0
        
        return {
            'total_likes': total_likes,
            'total_comments': total_comments,
            'total_views': total_views,
            'average_likes': round(average_likes, 2),
            'average_comments': round(average_comments, 2),
            'average_views': round(average_views, 2),
            'average_engagement_rate': round(average_engagement_rate, 2)
        }
    
    def _extract_hashtags(self, text: str) -> List[str]:
        """Extract hashtags from text"""
        import re
        return re.findall(r'#\w+', text)
    
    def _extract_mentions(self, text: str) -> List[str]:
        """Extract mentions from text"""
        import re
        return re.findall(r'@\w+', text)
    
    def _download_profile_picture(self, url: str, username: str) -> Optional[str]:
        """Download profile picture and return local path"""
        try:
            response = requests.get(url, proxies=self.proxies, timeout=30)
            response.raise_for_status()
            
            filename = f"Juicy_{username}.jpg"
            filepath = Path(PATHS['temp_images']) / filename
            
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            # Return URL path
            return f"assets/tempprofileimg/{filename}"
            
        except Exception as e:
            logger.error(f"Error downloading profile picture for {username}: {str(e)}")
            return None
    
    def scrape_user(self, username: str) -> Dict:
        """
        Main method to scrape user data
        Replicates the main functionality from indexdados.php
        """
        print(f"🚀 Iniciando scraping para usuário: {username}")
        logger.info(f"Starting scrape for user: {username}")
        
        try:
            result = self.get_profile_data(username)
            if result:
                print(f"✅ Scraping concluído com sucesso para: {username}")
                logger.info(f"Successfully scraped user: {username}")
                return result
            else:
                print(f"❌ Falha no scraping para: {username}")
                logger.error(f"Failed to scrape user: {username}")
                return {
                    'success': 0,
                    'message': 'Failed to scrape user data',
                    'data': []
                }
                
        except Exception as e:
            error_msg = str(e)
            print(f"💥 Erro inesperado no scraping de {username}: {error_msg}")
            logger.error(f"Unexpected error scraping {username}: {error_msg}")
            
            # Log detailed error
            self._log_detailed_error(e, username, 0)
            self._save_error_log(e, {'username': username})
            
            return {
                'success': 0,
                'message': f'Error: {error_msg}',
                'data': []
            }


def main():
    """Main function for testing"""
    print("🎯 Instagram Scraper - Iniciando...")
    print("=" * 50)
    
    scraper = InstagramScraper()
    
    # Test with felipeneto (same as PHP version)
    print("📋 Testando com usuário: felipeneto")
    result = scraper.scrape_user("felipeneto")
    
    print("\n" + "=" * 50)
    print("📊 RESULTADO FINAL:")
    print("=" * 50)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
