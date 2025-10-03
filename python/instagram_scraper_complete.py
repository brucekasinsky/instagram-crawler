#!/usr/bin/env python3
"""
Instagram Scraper - Versão Completa para Perfis Públicos
Implementa todas as funcionalidades do instagram_scraper.py original
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

# Instagram Public API
import instaloader

# Configuration
from config import (
    PROXY_CONFIG, USER_AGENTS, INSTAGRAM_APP_USER_AGENT,
    REQUEST_SETTINGS, INSTAGRAM_SETTINGS, PATHS, DEFAULT_HEADERS,
    INSTAGRAM_HEADERS, ERROR_CONFIG
)

# Logging
from loguru import logger

class InstagramScraperComplete:
    """
    Instagram Scraper completo para perfis públicos
    Implementa todas as funcionalidades do arquivo original
    """
    
    def __init__(self):
        self.loader = None
        self.consecutive_errors = 0
        self.last_error_time = None
        
        # Setup logging
        self._setup_logging()
        
        # Create directories
        self._create_directories()
        
        # Setup proxy
        self._setup_proxy()
        
        # Initialize loader
        self._initialize_loader()
    
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
    
    def _initialize_loader(self):
        """Initialize instaloader with proxy"""
        try:
            print("🔧 Inicializando instaloader...")
            self.loader = instaloader.Instaloader()
            
            if self.proxies:
                print("🌐 Configurando proxy...")
                session = requests.Session()
                session.proxies = self.proxies
                self.loader.context._session = session
            
            print("✅ Instaloader configurado com sucesso!")
            logger.info("Instaloader initialized successfully")
            
        except Exception as e:
            print(f"❌ Erro ao inicializar instaloader: {str(e)}")
            logger.error(f"Failed to initialize instaloader: {str(e)}")
            raise e
    
    def get_profile_data(self, username: str) -> Optional[Dict]:
        """
        Get profile data for a given username (public profiles only)
        Replicates the scrapper function from indexdados.php
        """
        try:
            print(f"🔍 Buscando dados do perfil público: {username}")
            logger.info(f"Fetching public profile data for: {username}")
            
            # Get profile information
            print("⏳ Obtendo informações do perfil...")
            profile = instaloader.Profile.from_username(self.loader.context, username)
            
            if not profile:
                print(f"❌ Perfil não encontrado: {username}")
                logger.error(f"Profile not found: {username}")
                return None
            
            # Check minimum followers
            if profile.followers < INSTAGRAM_SETTINGS['min_followers']:
                print(f"⚠️ Usuário {username} tem menos de {INSTAGRAM_SETTINGS['min_followers']} seguidores")
                logger.warning(f"User {username} has less than {INSTAGRAM_SETTINGS['min_followers']} followers")
                return {
                    'success': 0,
                    'message': 'O usuário não tem o mínimo de followers',
                    'data': []
                }
            
            # Check if profile is private
            if profile.is_private:
                print(f"⚠️ Perfil {username} é privado")
                logger.warning(f"Profile {username} is private")
                return {
                    'success': 0,
                    'message': 'O perfil é privado',
                    'data': []
                }
            
            print("📊 Coletando posts (3x mais)...")
            # Get user's posts using next() method (more reliable)
            posts = []
            try:
                post_count = 0
                max_posts = INSTAGRAM_SETTINGS['max_posts_analyze'] * 3  # 3x mais posts
                
                posts_generator = profile.get_posts()
                
                while post_count < max_posts:
                    try:
                        post = next(posts_generator)
                        posts.append(post)
                        post_count += 1
                        
                        # Log progress
                        if post_count % 10 == 0:
                            print(f"   Coletados {post_count} posts...")
                            
                    except StopIteration:
                        print("✅ Fim dos posts disponíveis")
                        break
                    except Exception as post_error:
                        print(f"⚠️ Erro no post {post_count + 1}: {str(post_error)}")
                        break
                
                print(f"✅ Coletados {len(posts)} posts")
                
            except Exception as posts_error:
                print(f"⚠️ Erro ao coletar posts: {str(posts_error)}")
                posts = []  # Continue without posts
            
            # Get user's reels (separate collection - mínimo 12)
            print("📹 Coletando reels (mínimo 12)...")
            reels = []
            try:
                reel_count = 0
                min_reels = 12  # Mínimo 12 reels
                max_reels = max(min_reels, INSTAGRAM_SETTINGS['max_reels_analyze'])
                
                # Filter reels from posts
                for post in posts:
                    if getattr(post, 'typename', '') == 'GraphVideo':
                        reels.append(post)
                        reel_count += 1
                        print(f"   📹 Reel {reel_count}: {getattr(post, 'likes', 0)} likes, {getattr(post, 'video_view_count', 0)} views")
                        
                        if reel_count >= max_reels:
                            break
                
                # Se não temos reels suficientes, buscar mais posts
                if len(reels) < min_reels:
                    print(f"⚠️ Apenas {len(reels)} reels encontrados, buscando mais posts...")
                    
                    # Continuar buscando posts até ter reels suficientes
                    posts_generator = profile.get_posts()
                    additional_posts = 0
                    
                    while len(reels) < min_reels and additional_posts < 50:  # Limite de segurança
                        try:
                            post = next(posts_generator)
                            additional_posts += 1
                            
                            if getattr(post, 'typename', '') == 'GraphVideo':
                                reels.append(post)
                                reel_count += 1
                                print(f"   📹 Reel adicional {reel_count}: {getattr(post, 'likes', 0)} likes, {getattr(post, 'video_view_count', 0)} views")
                                
                        except StopIteration:
                            print("✅ Fim dos posts disponíveis para reels")
                            break
                        except Exception as reel_error:
                            print(f"⚠️ Erro ao buscar reel adicional: {str(reel_error)}")
                            break
                
                print(f"✅ Coletados {len(reels)} reels (mínimo: {min_reels})")
                
            except Exception as reels_error:
                print(f"⚠️ Erro ao coletar reels: {str(reels_error)}")
                reels = []
            
            # Process profile data
            profile_data = self._process_profile_data(profile, posts, reels)
            
            print(f"✅ Perfil processado com sucesso: {username}")
            logger.info(f"Successfully processed profile: {username}")
            return profile_data
            
        except Exception as e:
            error_msg = str(e)
            print(f"❌ Erro ao buscar perfil {username}: {error_msg}")
            logger.error(f"Error fetching profile {username}: {error_msg}")
            self._save_error_log(e, {'username': username})
            self.consecutive_errors += 1
            return None
    
    def _process_profile_data(self, profile, posts: List, reels: List) -> Dict:
        """
        Process profile data and calculate metrics
        Replicates the data processing logic from indexdados.php
        """
        # Basic profile information
        profile_data = {
            'instagram_id': str(profile.userid),
            'username': profile.username,
            'full_name': profile.full_name or profile.username,
            'description': profile.biography or '',
            'website': profile.external_url or '',
            'followers': profile.followers,
            'following': profile.followees,
            'uploads': profile.mediacount,
            'profile_picture_url': profile.profile_pic_url,
            'is_private': 1 if profile.is_private else 0,
            'is_verified': 1 if profile.is_verified else 0
        }
        
        # Process media data (posts)
        media_metrics = self._calculate_media_metrics(posts, profile_data['followers'])
        
        # Process reels data
        reels_metrics = self._calculate_reels_metrics(reels, profile_data['followers'])
        
        # Calculate engagement rates
        profile_data['average_engagement_rate'] = media_metrics['average_engagement_rate']
        
        # Download profile picture
        profile_pic_path = self._download_profile_picture(profile_data['profile_picture_url'], profile_data['username'])
        if profile_pic_path:
            profile_data['profile_picture_url'] = profile_pic_path
        
        # Prepare details (same structure as original)
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
    
    def _calculate_media_metrics(self, posts: List, followers: int) -> Dict:
        """Calculate metrics for regular media posts (same as original)"""
        likes_array = []
        comments_array = []
        engagement_rate_array = []
        hashtags_array = {}
        mentions_array = {}
        
        # Skip first 3 posts (as in PHP version)
        for post in posts[3:]:
            # Get likes and comments
            likes = getattr(post, 'likes', 0) or 0
            comments = getattr(post, 'comments', 0) or 0
            
            likes_array.append(likes)
            comments_array.append(comments)
            
            # Calculate engagement rate
            total_engagement = likes + comments
            if followers > 0:
                engagement_rate = (total_engagement / followers) * 100
                engagement_rate_array.append(engagement_rate)
            
            # Extract hashtags and mentions from caption
            caption = getattr(post, 'caption', '') or ''
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
    
    def _calculate_reels_metrics(self, reels: List, followers: int) -> Dict:
        """Calculate metrics for reels (same as original)"""
        likes_array = []
        comments_array = []
        views_array = []
        engagement_rate_array = []
        
        # Skip first 3 reels (as in PHP version)
        for reel in reels[3:]:
            likes = getattr(reel, 'likes', 0) or 0
            comments = getattr(reel, 'comments', 0) or 0
            views = getattr(reel, 'video_view_count', 0) or 0
            
            likes_array.append(likes)
            comments_array.append(comments)
            views_array.append(views)
            
            # Calculate engagement rate
            total_engagement = likes + comments
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
    print("🎯 Instagram Scraper Completo - Iniciando...")
    print("=" * 50)
    
    scraper = InstagramScraperComplete()
    
    # Test with felipeneto (same as PHP version)
    print("📋 Testando com usuário: felipeneto")
    result = scraper.scrape_user("felipeneto")
    
    print("\n" + "=" * 50)
    print("📊 RESULTADO FINAL:")
    print("=" * 50)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
