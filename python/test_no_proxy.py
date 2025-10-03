#!/usr/bin/env python3
"""
Teste sem proxy para verificar se o problema é o proxy
"""
from instagram_private_api import Client
from config import FAKE_USERS

def main():
    username, password = FAKE_USERS[0]
    print(f"🔐 Testando login SEM proxy: {username}")
    
    try:
        print("⏳ Criando cliente sem proxy...")
        client = Client(username, password)  # Sem proxy
        print("✅ Login sem proxy bem-sucedido!")
        
        # Teste básico
        print("🧪 Testando busca de perfil...")
        profile = client.user_info_by_username("felipeneto")
        print("✅ Busca de perfil OK!")
        
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        print(f"Tipo do erro: {type(e).__name__}")
        
        # Se for erro de login, pode ser credenciais inválidas
        if "login" in str(e).lower() or "password" in str(e).lower():
            print("💡 Possível problema: Credenciais inválidas")
        elif "challenge" in str(e).lower():
            print("💡 Instagram solicitando verificação (challenge)")
        elif "rate" in str(e).lower():
            print("💡 Rate limiting - muitas tentativas")

if __name__ == "__main__":
    main()



