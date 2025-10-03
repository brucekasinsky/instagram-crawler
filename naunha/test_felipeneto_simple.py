#!/usr/bin/env python3
"""
Script simples para teste rápido do Felipe Neto
"""

from InstaScraperV2 import ScraperController
import json

def quick_test():
    """Teste rápido e direto"""
    print("🚀 Teste Rápido - Felipe Neto")
    print("-" * 40)
    
    # Criar scraper
    scraper = ScraperController()
    
    try:
        # Testar proxy
        print("1. Testando proxy...")
        if scraper.test_proxy_connection():
            print("✅ Proxy OK")
        else:
            print("❌ Proxy falhou")
            return
        
        # Criar sessão
        print("2. Criando sessão...")
        scraper.create_session()
        print("✅ Sessão criada")
        
        # Obter dados do perfil
        print("3. Obtendo dados do perfil...")
        profile = scraper.get_profile_data("felipeneto")
        
        if profile:
            print("✅ Perfil obtido!")
            print(f"   Nome: {profile['full_name']}")
            print(f"   Seguidores: {profile['followers']:,}")
            print(f"   Posts: {profile['uploads']:,}")
            print(f"   Bio: {profile['description'][:50]}...")
            
            # Salvar em JSON
            with open('felipeneto_profile.json', 'w', encoding='utf-8') as f:
                json.dump(profile, f, ensure_ascii=False, indent=2)
            print("💾 Dados salvos em felipeneto_profile.json")
        else:
            print("❌ Falha ao obter perfil")
        
        # Obter posts
        print("4. Obtendo posts...")
        
        # Primeiro, navegar para a página e capturar screenshot
        print("   Navegando para a página do perfil...")
        scraper.browser.get('https://instagram.com/felipeneto/')
        
        # Aguardar um pouco para a página carregar
        import time
        time.sleep(5)
        
        # Capturar screenshot
        print("   Capturando screenshot da página...")
        screenshot_path = "felipeneto_page_screenshot.png"
        scraper.browser.save_screenshot(screenshot_path)
        print(f"   📸 Screenshot salvo em: {screenshot_path}")
        
        # Obter HTML da página para análise
        print("   Salvando HTML da página...")
        html_content = scraper.browser.page_source
        with open("felipeneto_page.html", "w", encoding="utf-8") as f:
            f.write(html_content)
        print("   📄 HTML salvo em: felipeneto_page.html")
        
        # Agora tentar obter os posts
        posts = scraper.get_creator_posts("felipeneto")
        
        if posts:
            print(f"✅ {len(posts)} posts obtidos!")
            
            # Mostrar resumo
            total_likes = sum(p.get('likes', 0) for p in posts)
            print(f"   Total de likes: {total_likes:,}")
            
            # Salvar em JSON
            with open('felipeneto_posts.json', 'w', encoding='utf-8') as f:
                json.dump(posts, f, ensure_ascii=False, indent=2)
            print("💾 Posts salvos em felipeneto_posts.json")
        else:
            print("❌ Falha ao obter posts")
        
        print("\n🎉 Teste concluído!")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    finally:
        scraper.quit_session()

if __name__ == "__main__":
    quick_test()
