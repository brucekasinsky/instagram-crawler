#!/usr/bin/env python3
"""
Teste específico para login manual no Instagram
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'naunha'))

from naunha.InstaScraperV2 import ScraperController

def main():
    """
    Teste do login manual
    """
    print("🔐 TESTE DE LOGIN MANUAL NO INSTAGRAM")
    print("=" * 50)
    
    # Criar instância do scraper
    scraper = ScraperController()
    
    try:
        print("🚀 Iniciando teste de login manual...")
        
        # Testar login manual
        if scraper.manual_login_instagram():
            print("✅ Login manual realizado com sucesso!")
            
            # Testar navegação para um perfil
            print("\n🎬 Testando navegação para perfil...")
            test_profile = input("Digite um perfil para testar (ex: instagram): ").strip() or "instagram"
            
            print(f"📱 Navegando para @{test_profile}...")
            scraper.browser.get(f"https://www.instagram.com/{test_profile}/")
            
            print("✅ Navegação testada com sucesso!")
            print("💡 O navegador está funcionando corretamente!")
            
        else:
            print("❌ Falha no login manual")
        
    except KeyboardInterrupt:
        print("\n⚠️ Teste cancelado pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro no teste: {str(e)}")
    finally:
        # Fechar navegador
        print("\n🔒 Fechando navegador...")
        scraper.quit_session()
        print("✅ Teste finalizado!")

if __name__ == "__main__":
    main()

