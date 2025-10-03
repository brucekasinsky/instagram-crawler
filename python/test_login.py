#!/usr/bin/env python3
"""
Script para testar diferentes abordagens de login
"""
import time
import signal
from config import PROXY_CONFIG, FAKE_USERS

def test_login_with_timeout(username, password, timeout=15):
    """Testa login com timeout"""
    print(f"🔐 Testando login: {username}")
    
    def timeout_handler(signum, frame):
        raise TimeoutError("Login timeout")
    
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(timeout)
    
    try:
        from instagram_private_api import Client
        
        print("⏳ Criando cliente...")
        client = Client(
            username=username,
            password=password,
            proxy=PROXY_CONFIG
        )
        
        signal.alarm(0)
        print("✅ Login bem-sucedido!")
        return True
        
    except TimeoutError:
        signal.alarm(0)
        print(f"⏰ Timeout após {timeout}s")
        return False
    except Exception as e:
        signal.alarm(0)
        print(f"❌ Erro: {str(e)}")
        return False

def test_without_proxy(username, password):
    """Testa login sem proxy"""
    print(f"🌐 Testando sem proxy: {username}")
    
    try:
        from instagram_private_api import Client
        
        client = Client(
            username=username,
            password=password
        )
        
        print("✅ Login sem proxy OK!")
        return True
        
    except Exception as e:
        print(f"❌ Erro sem proxy: {str(e)}")
        return False

def main():
    print("🧪 TESTE DE LOGIN INSTAGRAM")
    print("=" * 50)
    
    # Teste com credenciais do config
    username, password = FAKE_USERS[0]
    
    print("1️⃣ Teste com proxy (15s timeout)")
    result1 = test_login_with_timeout(username, password, 15)
    print()
    
    if not result1:
        print("2️⃣ Teste sem proxy")
        result2 = test_without_proxy(username, password)
        print()
        
        if not result2:
            print("3️⃣ Teste com timeout maior (30s)")
            result3 = test_login_with_timeout(username, password, 30)
            print()
    
    print("=" * 50)
    print("📊 RESULTADO:")
    if result1:
        print("✅ Login funcionando com proxy")
    else:
        print("❌ Problema com login")
        print("💡 Possíveis soluções:")
        print("   - Verificar credenciais")
        print("   - Instagram pode estar bloqueando")
        print("   - Tentar sem proxy")
        print("   - Aguardar e tentar novamente")

if __name__ == "__main__":
    main()



