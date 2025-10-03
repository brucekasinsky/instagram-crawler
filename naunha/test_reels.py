#!/usr/bin/env python3
"""
Teste de funcionalidade de extração de Reels do Instagram
"""

import sys
import os
import time

# Adicionar o diretório atual ao path
sys.path.append(os.path.dirname(__file__))

from InstaScraperV2 import ScraperController

def test_reels_functionality():
    """
    Testa a funcionalidade de extração de reels
    """
    print("=== TESTE DE FUNCIONALIDADE DE REELS ===")
    
    # Criar instância do scraper
    scraper = ScraperController()
    
    try:
        # Criar sessão do browser em modo mobile (app Instagram)
        print("Criando sessão do browser em modo MOBILE (app Instagram)...")
        scraper.create_session(mobile=True)
        
        # Aguardar um pouco para a sessão estabilizar
        time.sleep(5)
        
        # Testar com um perfil público
        test_username = "felipeneto"  # Perfil público do Instagram
        
        print(f"Testando extração de reels para: {test_username}")
        
        # Navegar para a página do perfil primeiro
        print(f"Navegando para a página do perfil: {test_username}")
        scraper.browser.get(f'https://instagram.com/{test_username}/')
        time.sleep(5)  # Aguardar carregamento da página
        
        # Aguardar 60 segundos para dar tempo de inserir credenciais do proxy
        print("⏳ Aguardando 60 segundos para inserir credenciais do proxy...")
        print("📝 Insira as credenciais no modal do Chrome:")
        print("   Usuário: juicyspace69")
        print("   Senha: aCQs0w0Qjbj9l9Umex")
        time.sleep(60)
        
        # Aguardar até que a página carregue completamente
        print("🔍 Aguardando página carregar...")
        try:
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            from selenium.webdriver.common.by import By
            
            WebDriverWait(scraper.browser, 60).until(
                EC.presence_of_element_located((By.TAG_NAME, 'main'))
            )
            print("✅ Página carregada com sucesso!")
        except Exception as e:
            print(f"⚠️ Timeout aguardando página carregar: {str(e)}")
            print("🔄 Continuando mesmo assim...")
        
        # Testar funcionalidade de reels
        reels_data = scraper.test_reels_functionality(test_username)
        
        if reels_data:
            print(f"\n✅ Sucesso! {len(reels_data)} reels processados")
            
            # Verificar se os screenshots foram salvos
            screenshots_folder = os.path.join(os.path.dirname(__file__), "screenshots")
            if os.path.exists(screenshots_folder):
                screenshot_files = [f for f in os.listdir(screenshots_folder) if f.endswith('.png')]
                print(f"📸 Screenshots salvos: {len(screenshot_files)}")
                
                for i, reel in enumerate(reels_data[:3]):  # Mostrar apenas os primeiros 3
                    print(f"\nReel {i+1}:")
                    print(f"  - URL: {reel.get('reel_url', 'N/A')}")
                    print(f"  - ID: {reel.get('reel_id', 'N/A')}")
                    print(f"  - Likes: {reel.get('likes', 0)}")
                    print(f"  - Comments: {reel.get('comments', 0)}")
                    print(f"  - Screenshot: {reel.get('screenshot_path', 'N/A')}")
            else:
                print("❌ Pasta de screenshots não encontrada")
        else:
            print("❌ Falha ao extrair reels")
            
    except Exception as e:
        print(f"❌ Erro durante o teste: {str(e)}")
        
    finally:
        # Fechar sessão
        try:
            scraper.quit_session()
            print("\n✅ Sessão fechada com sucesso")
        except:
            pass

if __name__ == "__main__":
    test_reels_functionality()
