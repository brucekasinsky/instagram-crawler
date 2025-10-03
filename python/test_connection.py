#!/usr/bin/env python3
"""
Script de teste para diagnosticar problemas de conexão
"""
import requests
import time
from config import PROXY_CONFIG

def test_proxy():
    """Testa a conectividade do proxy"""
    print("🌐 Testando proxy...")
    try:
        response = requests.get(
            'https://httpbin.org/ip', 
            proxies=PROXY_CONFIG, 
            timeout=10
        )
        print(f"✅ Proxy OK - IP: {response.json().get('origin', 'N/A')}")
        return True
    except Exception as e:
        print(f"❌ Proxy falhou: {str(e)}")
        return False

def test_instagram_access():
    """Testa acesso ao Instagram"""
    print("📱 Testando acesso ao Instagram...")
    try:
        response = requests.get(
            'https://www.instagram.com/', 
            proxies=PROXY_CONFIG, 
            timeout=15
        )
        print(f"✅ Instagram acessível - Status: {response.status_code}")
        print(f"📄 Tamanho da resposta: {len(response.text)} chars")
        return True
    except Exception as e:
        print(f"❌ Instagram inacessível: {str(e)}")
        return False

def test_instagram_api():
    """Testa a biblioteca instagram-private-api"""
    print("🔧 Testando instagram-private-api...")
    try:
        from instagram_private_api import Client
        print("✅ Biblioteca importada com sucesso")
        
        # Teste básico sem login
        print("🧪 Testando criação de cliente (sem login)...")
        client = Client()
        print("✅ Cliente criado com sucesso")
        return True
    except Exception as e:
        print(f"❌ Erro na biblioteca: {str(e)}")
        return False

def main():
    print("🔍 DIAGNÓSTICO DE CONECTIVIDADE")
    print("=" * 50)
    
    # Teste 1: Proxy
    proxy_ok = test_proxy()
    print()
    
    # Teste 2: Instagram
    instagram_ok = test_instagram_access()
    print()
    
    # Teste 3: Biblioteca
    api_ok = test_instagram_api()
    print()
    
    print("=" * 50)
    print("📊 RESUMO:")
    print(f"Proxy: {'✅' if proxy_ok else '❌'}")
    print(f"Instagram: {'✅' if instagram_ok else '❌'}")
    print(f"API Library: {'✅' if api_ok else '❌'}")
    
    if not proxy_ok:
        print("\n💡 SOLUÇÃO: Verifique as credenciais do proxy")
    elif not instagram_ok:
        print("\n💡 SOLUÇÃO: Instagram pode estar bloqueando o proxy")
    elif not api_ok:
        print("\n💡 SOLUÇÃO: Problema com a biblioteca instagram-private-api")

if __name__ == "__main__":
    main()



