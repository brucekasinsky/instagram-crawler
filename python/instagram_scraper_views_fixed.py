#!/usr/bin/env python3
"""
Instagram Scraper - Versão com Views Corrigidos
Usa instaloader com configurações específicas para perfis públicos
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

class InstagramScraperViewsFixed:
    """
    Instagram Scraper com configurações específicas para views corretos
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
        
        # Initialize loader with specific configurations
        self._initialize_loader_optimized()
    
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
            'proxy_config': self.proxies,
            'consecutive_errors': self.consecutive_errors
        }
        
        with open(error_file, 'w', encoding='utf-8') as f:
            json.dump(error_data, f, indent=2, ensure_ascii=False)
        
        logger.error(f"Error saved to: {error_file}")
    
    def _initialize_loader_optimized(self):
        """Initialize instaloader with optimized configurations for public profiles"""
        try:
            print("🔧 Inicializando instaloader com configurações otimizadas...")
            
            # Create loader with specific settings
            self.loader = instaloader.Instaloader(
                download_pictures=False,
                download_videos=False,
                download_video_thumbnails=False,
                download_geotags=False,
                download_comments=False,
                save_metadata=False,
                compress_json=False,
                max_connection_attempts=3,
                request_timeout=30
            )
            
            # Configure proxy
            if self.proxies:
                print("🌐 Configurando proxy...")
                session = requests.Session()
                session.proxies = self.proxies
                self.loader.context._session = session
            
            # Configure headers for better data access
            self.loader.context._session.headers.update({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            })
            
            print("✅ Instaloader configurado com sucesso!")
            logger.info("Instaloader initialized with optimized settings")
            
        except Exception as e:
            print(f"❌ Erro ao inicializar instaloader: {str(e)}")
            logger.error(f"Failed to initialize instaloader: {str(e)}")
            raise e
    
    def _get_enhanced_views(self, post):
        """
        Tenta obter views de diferentes campos e retorna o maior valor
        """
        view_fields = [
            'video_view_count',
            'view_count',
            'views',
            'play_count',
            'video_play_count'
        ]
        
        max_views = 0
        best_field = None
        
        for field in view_fields:
            try:
                value = getattr(post, field, 0) or 0
                if value > max_views:
                    max_views = value
                    best_field = field
            except:
                continue
        
        return max_views, best_field
    
    def _collect_posts_optimized(self, profile, target_posts: int) -> List:
        """Coleta posts de forma otimizada"""
        posts = []
        consecutive_data_errors = 0
        max_data_errors = 2
        
        try:
            print(f"📊 Coletando posts (objetivo: {target_posts})...")
            posts_generator = profile.get_posts()
            
            while len(posts) < target_posts:
                try:
                    post = next(posts_generator)
                    posts.append(post)
                    consecutive_data_errors = 0
                    
                    # Log progress
                    if len(posts) % 10 == 0:
                        print(f"   Coletados {len(posts)} posts...")
                        
                except StopIteration:
                    print("✅ Fim dos posts disponíveis")
                    break
                except Exception as post_error:
                    error_msg = str(post_error)
                    if "'data'" in error_msg:
                        consecutive_data_errors += 1
                        print(f"⚠️ Erro 'data' {consecutive_data_errors}/2 - Parando coleta de posts")
                        
                        if consecutive_data_errors >= max_data_errors:
                            print("🛑 Parando coleta de posts - foco nos reels")
                            break
                    else:
                        print(f"⚠️ Erro no post {len(posts) + 1}: {error_msg}")
                        consecutive_data_errors = 0
                        
        except Exception as e:
            print(f"⚠️ Erro geral na coleta de posts: {str(e)}")
        
        return posts
    
    def _collect_reels_with_enhanced_views(self, profile, min_reels: int = 12) -> List:
        """Coleta reels com views aprimorados"""
        reels_data = []
        consecutive_data_errors = 0
        max_data_errors = 10
        post_count = 0
        max_posts_to_check = 500
        
        try:
            print(f"📹 Coletando reels com views aprimorados (objetivo: {min_reels})...")
            posts_generator = profile.get_posts()
            
            while len(reels_data) < min_reels and post_count < max_posts_to_check:
                try:
                    post = next(posts_generator)
                    post_count += 1
                    
                    # Verificar se é reel (GraphVideo)
                    if getattr(post, 'typename', '') == 'GraphVideo':
                        # Coletar dados básicos
                        likes = getattr(post, 'likes', 0) or 0
                        comments = getattr(post, 'comments', 0) or 0
                        date = getattr(post, 'date_utc', None)
                        shortcode = getattr(post, 'shortcode', '')
                        caption = getattr(post, 'caption', '') or ''
                        
                        # Tentar obter views aprimorados
                        enhanced_views, best_field = self._get_enhanced_views(post)
                        
                        reel_data = {
                            'shortcode': shortcode,
                            'likes': likes,
                            'comments': comments,
                            'views': enhanced_views,
                            'views_field': best_field,
                            'date': date,
                            'caption': caption
                        }
                        
                        reels_data.append(reel_data)
                        
                        # Formatar para exibição
                        def format_number(num):
                            if num >= 1000000:
                                return f"{num/1000000:.1f}M"
                            elif num >= 1000:
                                return f"{num/1000:.1f}K"
                            else:
                                return str(num)
                        
                        print(f"   📹 Reel {len(reels_data)}: {format_number(likes)} likes, {format_number(enhanced_views)} views, {format_number(comments)} comments")
                        print(f"       Campo usado para views: {best_field}")
                        print(f"       Shortcode: {shortcode}")
                        
                        consecutive_data_errors = 0
                        
                        # Log de progresso a cada 5 reels
                        if len(reels_data) % 5 == 0:
                            print(f"   🎯 Progresso: {len(reels_data)}/{min_reels} reels coletados")
                    
                except StopIteration:
                    print("✅ Fim dos posts disponíveis para reels")
                    break
                except Exception as post_error:
                    error_msg = str(post_error)
                    if "'data'" in error_msg:
                        consecutive_data_errors += 1
                        print(f"⚠️ Erro 'data' {consecutive_data_errors}/10 na coleta de reels")
                        
                        if consecutive_data_errors >= max_data_errors:
                            print("🛑 Muitos erros 'data' consecutivos, parando coleta de reels")
                            break
                    else:
                        print(f"⚠️ Erro no post {post_count + 1}: {error_msg}")
                        consecutive_data_errors = 0
                        
        except Exception as e:
            print(f"⚠️ Erro geral na coleta de reels: {str(e)}")
        
        return reels_data
    
    def get_profile_data(self, username: str) -> Optional[Dict]:
        """
        Get profile data for a given username (public profiles only)
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
            
            # Coletar posts (3x mais)
            target_posts = INSTAGRAM_SETTINGS['max_posts_analyze'] * 3
            posts = self._collect_posts_optimized(profile, target_posts)
            print(f"✅ Coletados {len(posts)} posts (objetivo: {target_posts})")
            
            # Coletar dados de reels (mínimo 12) - FOCO PRINCIPAL
            min_reels = 12
            reels_data = self._collect_reels_with_enhanced_views(profile, min_reels)
            print(f"✅ Coletados {len(reels_data)} reels (objetivo: {min_reels})")
            
            # Se não temos reels suficientes, tentar mais uma vez
            if len(reels_data) < min_reels:
                print(f"⚠️ Apenas {len(reels_data)} reels encontrados, tentando mais uma vez...")
                additional_reels = self._collect_reels_with_enhanced_views(profile, min_reels - len(reels_data))
                reels_data.extend(additional_reels)
                print(f"✅ Total de reels coletados: {len(reels_data)}")
            
            # Process profile data
            profile_data = self._process_profile_data(profile, posts, reels_data)
            
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
    
    def _process_profile_data(self, profile, posts: List, reels_data: List) -> Dict:
        """
        Process profile data and calculate metrics
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
        
        # Process reels data (apenas dados essenciais)
        reels_metrics = self._calculate_reels_metrics_from_data(reels_data, profile_data['followers'])
        
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
    
    def _calculate_media_metrics(self, posts: List, followers: int) -> Dict:
        """Calculate metrics for regular media posts"""
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
    
    def _calculate_reels_metrics_from_data(self, reels_data: List, followers: int) -> Dict:
        """Calculate metrics for reels from collected data only"""
        likes_array = []
        comments_array = []
        views_array = []
        engagement_rate_array = []
        
        # Skip first 3 reels (as in PHP version)
        for reel_data in reels_data[3:]:
            likes = reel_data['likes']
            comments = reel_data['comments']
            views = reel_data['views']
            
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
        """
        print(f"🚀 Iniciando scraping com views aprimorados: {username}")
        logger.info(f"Starting enhanced views scrape for user: {username}")
        
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
            
            self._save_error_log(e, {'username': username})
            
            return {
                'success': 0,
                'message': f'Error: {error_msg}',
                'data': []
            }


def main():
    """Main function for testing"""
    print("🎯 Instagram Scraper - Views Aprimorados - Iniciando...")
    print("=" * 60)
    
    scraper = InstagramScraperViewsFixed()
    
    # Test with felipeneto
    print("📋 Testando com usuário: felipeneto")
    result = scraper.scrape_user("felipeneto")
    
    print("\n" + "=" * 60)
    print("📊 RESULTADO FINAL:")
    print("=" * 60)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()



