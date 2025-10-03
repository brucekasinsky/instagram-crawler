#!/usr/bin/env python3
"""
Script de teste para verificar se o proxy está funcionando corretamente
"""

from InstaScraperV2 import ScraperController

def main():
    print("=== TESTE DE PROXY ===")
    
    # Criar instância do scraper
    scraper = ScraperController()
    
    # Testar conectividade do proxy
    print("\n1. Testando conectividade do proxy...")
    proxy_working = scraper.test_proxy_connection()
    
    if proxy_working:
        print("✅ Proxy está funcionando!")
        
        # Testar criação de sessão com proxy
        print("\n2. Testando criação de sessão com proxy...")
        try:
            scraper.create_session()
            print("✅ Sessão criada com sucesso usando proxy!")
            
            # Testar acesso a uma página
            print("\n3. Testando acesso a uma página...")
            scraper.browser.get('https://httpbin.org/ip')
            print("✅ Acesso à página realizado com sucesso!")
            
            # Fechar sessão
            scraper.quit_session()
            
        except Exception as e:
            print(f"❌ Erro ao criar sessão: {str(e)}")
    else:
        print("❌ Proxy não está funcionando!")
    
    print("\n=== FIM DO TESTE ===")

if __name__ == "__main__":
    main()
