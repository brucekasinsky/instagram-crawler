#!/usr/bin/env python3
"""
Teste específico para posts e reels
"""
import instaloader
from config import PROXY_CONFIG

def main():
    print("🧪 Testando acesso a posts e reels")
    
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
        
        print("📊 Testando acesso aos posts...")
        
        # Teste 1: Iterar posts um por um
        print("1️⃣ Testando iteração de posts...")
        post_count = 0
        for post in profile.get_posts():
            post_count += 1
            print(f"   Post {post_count}: {post.shortcode}")
            print(f"   Tipo: {post.typename}")
            print(f"   Likes: {post.likes}")
            print(f"   Comentários: {post.comments}")
            print(f"   Data: {post.date}")
            
            if post.typename == 'GraphVideo':  # Reel
                print(f"   📹 REEL - Views: {getattr(post, 'video_view_count', 'N/A')}")
            else:
                print(f"   📸 POST - Caption: {post.caption[:50] if post.caption else 'Sem legenda'}...")
            
            if post_count >= 5:  # Limitar a 5 posts para teste
                break
        
        print(f"✅ Total de posts processados: {post_count}")
        
        # Teste 2: Converter para lista
        print("\n2️⃣ Testando conversão para lista...")
        try:
            posts_list = list(profile.get_posts())
            print(f"✅ Lista criada com {len(posts_list)} posts")
        except Exception as e:
            print(f"❌ Erro ao criar lista: {str(e)}")
        
        # Teste 3: Acessar posts específicos
        print("\n3️⃣ Testando acesso a posts específicos...")
        try:
            posts_generator = profile.get_posts()
            first_post = next(posts_generator)
            print(f"✅ Primeiro post: {first_post.shortcode}")
            print(f"   Dados disponíveis: {dir(first_post)}")
        except Exception as e:
            print(f"❌ Erro ao acessar primeiro post: {str(e)}")
        
    except Exception as e:
        print(f"❌ Erro geral: {str(e)}")
        print(f"Tipo: {type(e).__name__}")

if __name__ == "__main__":
    main()



