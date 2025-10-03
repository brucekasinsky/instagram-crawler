#!/usr/bin/env python3
"""
Teste robusto para posts com tratamento de erro detalhado
"""
import instaloader
from config import PROXY_CONFIG
import traceback

def main():
    print("🧪 Teste robusto de posts")
    
    try:
        # Criar loader
        loader = instaloader.Instaloader()
        
        # Configurar proxy
        if PROXY_CONFIG:
            print("🌐 Configurando proxy...")
            import requests
            session = requests.Session()
            session.proxies = PROXY_CONFIG
            loader.context._session = session
        
        print("🔍 Carregando perfil...")
        profile = instaloader.Profile.from_username(loader.context, "felipeneto")
        print(f"✅ Perfil carregado: {profile.username}")
        
        print("📊 Testando coleta de posts com tratamento de erro...")
        
        posts = []
        post_count = 0
        max_posts = 10
        
        try:
            posts_generator = profile.get_posts()
            print("✅ Generator criado com sucesso")
            
            while post_count < max_posts:
                try:
                    post = next(posts_generator)
                    posts.append(post)
                    post_count += 1
                    
                    print(f"   Post {post_count}: {post.shortcode}")
                    print(f"   Tipo: {post.typename}")
                    print(f"   Likes: {post.likes}")
                    print(f"   Comentários: {post.comments}")
                    
                    if post.typename == 'GraphVideo':
                        views = getattr(post, 'video_view_count', 0)
                        print(f"   📹 REEL - Views: {views}")
                    else:
                        caption = getattr(post, 'caption', '') or ''
                        print(f"   📸 POST - Caption: {caption[:50]}...")
                    
                except StopIteration:
                    print("✅ Fim dos posts")
                    break
                except Exception as post_error:
                    print(f"❌ Erro no post {post_count + 1}: {str(post_error)}")
                    print(f"Tipo: {type(post_error).__name__}")
                    traceback.print_exc()
                    break
                    
        except Exception as generator_error:
            print(f"❌ Erro ao criar generator: {str(generator_error)}")
            print(f"Tipo: {type(generator_error).__name__}")
            traceback.print_exc()
        
        print(f"\n✅ Total de posts coletados: {len(posts)}")
        
        # Teste de processamento
        if posts:
            print("\n📊 Testando processamento dos posts...")
            for i, post in enumerate(posts[:3]):
                try:
                    likes = getattr(post, 'likes', 0) or 0
                    comments = getattr(post, 'comments', 0) or 0
                    caption = getattr(post, 'caption', '') or ''
                    
                    print(f"Post {i+1}: {likes} likes, {comments} comments")
                    if caption:
                        print(f"  Caption: {caption[:100]}...")
                        
                except Exception as process_error:
                    print(f"❌ Erro ao processar post {i+1}: {str(process_error)}")
        
    except Exception as e:
        print(f"❌ Erro geral: {str(e)}")
        print(f"Tipo: {type(e).__name__}")
        traceback.print_exc()

if __name__ == "__main__":
    main()



