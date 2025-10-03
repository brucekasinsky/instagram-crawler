#!/usr/bin/env python3
"""
Teste usando instaloader como alternativa
"""
import instaloader
from config import PROXY_CONFIG, FAKE_USERS

def main():
    username, password = FAKE_USERS[0]
    print(f"🔐 Testando com instaloader: {username}")
    
    try:
        # Criar loader
        loader = instaloader.Instaloader()
        
        # Configurar proxy se disponível
        if PROXY_CONFIG:
            print("🌐 Configurando proxy...")
            # instaloader usa requests, então podemos configurar via requests
            import requests
            session = requests.Session()
            session.proxies = PROXY_CONFIG
            loader.context._session = session
        
        print("⏳ Fazendo login...")
        loader.login(username, password)
        print("✅ Login bem-sucedido!")
        
        # Teste básico
        print("🧪 Testando busca de perfil...")
        profile = instaloader.Profile.from_username(loader.context, "felipeneto")
        print(f"✅ Perfil encontrado: {profile.username}")
        print(f"   Seguidores: {profile.followers}")
        print(f"   Seguindo: {profile.followees}")
        print(f"   Posts: {profile.mediacount}")
        
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        print(f"Tipo do erro: {type(e).__name__}")

if __name__ == "__main__":
    main()



