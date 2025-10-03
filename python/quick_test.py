#!/usr/bin/env python3
"""
Teste rápido com credenciais reais
"""
from instagram_private_api import Client
from config import PROXY_CONFIG, FAKE_USERS

def main():
    username, password = FAKE_USERS[0]
    print(f"🔐 Testando login com: {username}")
    print(f"🌐 Proxy: {PROXY_CONFIG['http'][:50]}...")
    
    try:
        print("⏳ Criando cliente...")
        client = Client(username, password, proxy=PROXY_CONFIG)
        print("✅ Login bem-sucedido!")
        
        # Teste básico
        print("🧪 Testando busca de perfil...")
        profile = client.user_info_by_username("felipeneto")
        print("✅ Busca de perfil OK!")
        
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        print(f"Tipo do erro: {type(e).__name__}")

if __name__ == "__main__":
    main()



