#!/usr/bin/env python3
"""
Teste sem login - apenas perfis públicos
"""
import instaloader
from config import PROXY_CONFIG

def main():
    print("🔍 Testando acesso a perfis públicos (sem login)")
    
    try:
        # Criar loader sem login
        loader = instaloader.Instaloader()
        
        # Configurar proxy se disponível
        if PROXY_CONFIG:
            print("🌐 Configurando proxy...")
            import requests
            session = requests.Session()
            session.proxies = PROXY_CONFIG
            loader.context._session = session
        
        print("🧪 Testando busca de perfil público...")
        profile = instaloader.Profile.from_username(loader.context, "felipeneto")
        
        print(f"✅ Perfil encontrado: {profile.username}")
        print(f"   Nome: {profile.full_name}")
        print(f"   Seguidores: {profile.followers}")
        print(f"   Seguindo: {profile.followees}")
        print(f"   Posts: {profile.mediacount}")
        print(f"   Privado: {profile.is_private}")
        print(f"   Verificado: {profile.is_verified}")
        print(f"   Bio: {profile.biography[:100]}...")
        
        # Testar download de algumas imagens
        print("\n📸 Testando download de posts...")
        posts = list(profile.get_posts())[:3]  # Primeiros 3 posts
        
        for i, post in enumerate(posts, 1):
            print(f"   Post {i}: {post.caption[:50] if post.caption else 'Sem legenda'}...")
            print(f"   Likes: {post.likes}, Comentários: {post.comments}")
        
        print("\n✅ Teste de perfil público bem-sucedido!")
        
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        print(f"Tipo do erro: {type(e).__name__}")

if __name__ == "__main__":
    main()



