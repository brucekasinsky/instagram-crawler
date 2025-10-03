#!/usr/bin/env python3
"""
Script de teste para verificar a funcionalidade de screenshot
"""

import sys
import os

# Adicionar o diretório atual ao path
sys.path.append(os.path.dirname(__file__))

from InstaScraperV2 import ScraperController

def test_screenshot_functionality():
    """
    Testa a funcionalidade de screenshot
    """
    print("=== TESTE DE FUNCIONALIDADE DE SCREENSHOT ===")
    
    # Criar instância do scraper
    scraper = ScraperController()
    
    try:
        # Criar sessão do browser
        print("Criando sessão do browser...")
        scraper.create_session()
        
        # Testar com um perfil público (exemplo: instagram)
        test_username = "felipeneto"  # Perfil público do Instagram
        
        print(f"Testando extração de posts com screenshot para: {test_username}")
        
        # Extrair posts com screenshots
        posts_data = scraper.get_creator_posts(test_username)
        
        if posts_data:
            print(f"\n✅ Sucesso! {len(posts_data)} posts processados")
            
            # Verificar se os screenshots foram salvos
            screenshots_folder = os.path.join(os.path.dirname(__file__), "screenshots")
            if os.path.exists(screenshots_folder):
                screenshot_files = [f for f in os.listdir(screenshots_folder) if f.endswith('.png')]
                print(f"📸 Screenshots salvos: {len(screenshot_files)}")
                
                for i, post in enumerate(posts_data[:3]):  # Mostrar apenas os primeiros 3
                    print(f"\nPost {i+1}:")
                    print(f"  - URL: {post.get('post_url', 'N/A')}")
                    print(f"  - Likes: {post.get('likes', 0)}")
                    print(f"  - Comments: {post.get('comments', 0)}")
                    print(f"  - Screenshot: {post.get('screenshot_path', 'N/A')}")
            else:
                print("❌ Pasta de screenshots não encontrada")
        else:
            print("❌ Falha ao extrair posts")
            
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
    test_screenshot_functionality()
