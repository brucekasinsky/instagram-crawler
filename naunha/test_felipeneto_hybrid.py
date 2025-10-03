#!/usr/bin/env python3
"""
Script híbrido para extrair dados do Felipe Neto:
- Instaloader (com proxy) para dados do perfil
- Selenium (sem proxy) para posts usando esquema de divs
"""

import json
import time
from datetime import datetime
from InstaScraperV2 import ScraperController

def save_to_json(data, filename):
    """Salva dados em arquivo JSON com timestamp"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename_with_timestamp = f"{filename}_{timestamp}.json"
    
    with open(filename_with_timestamp, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Dados salvos em: {filename_with_timestamp}")
    return filename_with_timestamp

def test_hybrid_approach():
    """Testa a abordagem híbrida"""
    
    print("🚀 TESTE HÍBRIDO - FELIPE NETO")
    print("=" * 50)
    print("📋 Estratégia:")
    print("   • Instaloader (com proxy) → Dados do perfil")
    print("   • Selenium (sem proxy) → Posts com esquema de divs")
    print("=" * 50)
    
    username = "felipeneto"
    scraper = ScraperController()
    
    try:
        # 1. Testar proxy para Instaloader
        print("\n1️⃣ Testando proxy para Instaloader...")
        if scraper.test_proxy_connection():
            print("✅ Proxy funcionando para Instaloader!")
        else:
            print("❌ Proxy não funcionando")
            return False
        
        # 2. Obter dados do perfil com Instaloader (com proxy)
        print(f"\n2️⃣ Obtendo dados do perfil de @{username} (Instaloader + Proxy)...")
        start_time = time.time()
        
        profile_data = scraper.get_profile_data(username)
        if profile_data:
            print("✅ Dados do perfil obtidos com Instaloader!")
            print(f"   📊 Nome: {profile_data['full_name']}")
            print(f"   📊 Seguidores: {profile_data['followers']:,}")
            print(f"   📊 Seguindo: {profile_data['following']:,}")
            print(f"   📊 Posts: {profile_data['uploads']:,}")
            print(f"   📊 Bio: {profile_data['description'][:100]}...")
            
            # Salvar dados do perfil
            save_to_json(profile_data, f"felipeneto_profile_instaloader")
        else:
            print("❌ Falha ao obter dados do perfil")
            return False
        
        profile_time = time.time() - start_time
        print(f"⏱️ Tempo para dados do perfil: {profile_time:.2f} segundos")
        
        # 3. Obter foto de perfil com Instaloader (com proxy)
        print(f"\n3️⃣ Obtendo foto de perfil de @{username} (Instaloader + Proxy)...")
        start_time = time.time()
        
        profile_photo_url = scraper.get_profile_photo(username, size=640)
        if profile_photo_url:
            print(f"✅ Foto de perfil obtida: {profile_photo_url}")
            photo_data = {
                "username": username,
                "profile_photo_url": profile_photo_url,
                "timestamp": datetime.now().isoformat()
            }
            save_to_json(photo_data, f"felipeneto_photo_instaloader")
        else:
            print("❌ Falha ao obter foto de perfil")
        
        photo_time = time.time() - start_time
        print(f"⏱️ Tempo para foto de perfil: {photo_time:.2f} segundos")
        
        # 4. Criar sessão Selenium (sem proxy)
        print(f"\n4️⃣ Criando sessão Selenium (sem proxy) para posts...")
        start_time = time.time()
        
        scraper.create_session()
        print("✅ Sessão Selenium criada!")
        
        # 5. Navegar para a página e capturar screenshot
        print(f"\n5️⃣ Navegando para @{username} (Selenium sem proxy)...")
        scraper.browser.get(f'https://instagram.com/{username}/')
        
        # Aguardar carregamento
        time.sleep(5)
        
        # Capturar screenshot
        screenshot_path = f"felipeneto_page_selenium_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        scraper.browser.save_screenshot(screenshot_path)
        print(f"📸 Screenshot salvo: {screenshot_path}")
        
        # Salvar HTML
        html_content = scraper.browser.page_source
        html_path = f"felipeneto_page_selenium_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"📄 HTML salvo: {html_path}")
        
        # 6. Tentar extrair posts com Selenium
        print(f"\n6️⃣ Tentando extrair posts com Selenium...")
        start_time = time.time()
        
        posts_data = scraper.get_creator_posts(username)
        if posts_data:
            print(f"✅ {len(posts_data)} posts obtidos com Selenium!")
            
            # Mostrar resumo
            total_likes = sum(post.get('likes', 0) for post in posts_data)
            total_comments = sum(post.get('comments', 0) for post in posts_data)
            posts_with_hashtags = len([post for post in posts_data if post.get('hashtags')])
            posts_with_tags = len([post for post in posts_data if post.get('tags')])
            
            print(f"   📊 Total de likes: {total_likes:,}")
            print(f"   📊 Total de comentários: {total_comments:,}")
            print(f"   📊 Posts com hashtags: {posts_with_hashtags}")
            print(f"   📊 Posts com tags: {posts_with_tags}")
            
            # Mostrar alguns exemplos
            print("\n   📝 Exemplos de posts:")
            for i, post in enumerate(posts_data[:3]):
                print(f"      Post {i+1}:")
                print(f"         URL: {post.get('post_url', 'N/A')}")
                print(f"         Likes: {post.get('likes', 0):,}")
                print(f"         Comentários: {post.get('comments', 0):,}")
                if post.get('hashtags'):
                    print(f"         Hashtags: {', '.join(post['hashtags'][:3])}")
                if post.get('post_text'):
                    text_preview = post['post_text'][:100] + "..." if len(post['post_text']) > 100 else post['post_text']
                    print(f"         Texto: {text_preview}")
                print()
            
            # Salvar posts
            save_to_json(posts_data, f"felipeneto_posts_selenium")
        else:
            print("❌ Falha ao obter posts com Selenium")
            print("💡 Isso é esperado se a página não carregou corretamente")
        
        posts_time = time.time() - start_time
        print(f"⏱️ Tempo para posts: {posts_time:.2f} segundos")
        
        # 7. Resumo final
        print("\n" + "=" * 60)
        print("📋 RESUMO DO TESTE HÍBRIDO")
        print("=" * 60)
        print(f"✅ Proxy para Instaloader: Funcionando")
        print(f"✅ Dados do perfil: Obtidos ({profile_data['followers']:,} seguidores)")
        print(f"✅ Foto de perfil: {'Obtida' if profile_photo_url else 'Falhou'}")
        print(f"✅ Selenium sem proxy: {'Funcionando' if posts_data else 'Problemas'}")
        print(f"✅ Posts extraídos: {'Sim' if posts_data else 'Não'}")
        
        print(f"\n📊 DADOS EXTRAÍDOS:")
        if profile_data:
            print(f"   • Nome: {profile_data['full_name']}")
            print(f"   • Seguidores: {profile_data['followers']:,}")
            print(f"   • Posts: {profile_data['uploads']:,}")
            print(f"   • Bio: {profile_data['description'][:100]}...")
        
        if posts_data:
            print(f"   • Posts extraídos: {len(posts_data)}")
            print(f"   • Total de likes: {sum(post.get('likes', 0) for post in posts_data):,}")
        
        print("\n🎉 TESTE HÍBRIDO CONCLUÍDO!")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERRO durante o teste: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        # Sempre fechar a sessão
        try:
            scraper.quit_session()
            print("\n🔒 Sessão fechada com sucesso!")
        except:
            pass

def main():
    """Função principal"""
    print("🤖 Teste Híbrido - Instagram Scraper")
    print("📅 Data/Hora:", datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    
    # Executar teste
    success = test_hybrid_approach()
    
    if success:
        print("\n✅ Teste híbrido concluído com sucesso!")
        print("📁 Verifique os arquivos gerados:")
        print("   • felipeneto_profile_instaloader_*.json")
        print("   • felipeneto_photo_instaloader_*.json")
        print("   • felipeneto_posts_selenium_*.json")
        print("   • felipeneto_page_selenium_*.png")
        print("   • felipeneto_page_selenium_*.html")
    else:
        print("\n❌ Teste híbrido falhou!")
        print("🔍 Verifique os logs acima para mais detalhes.")

if __name__ == "__main__":
    main()




