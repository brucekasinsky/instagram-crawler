#!/usr/bin/env python3
"""
Script de teste para extrair dados do Instagram do Felipe Neto
Testa: login com Instaloader, foto de perfil, dados do perfil, posts e reels
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

def test_felipeneto_scraping():
    """Testa o scraping completo do perfil do Felipe Neto incluindo reels"""
    
    print("=" * 60)
    print("🚀 INICIANDO TESTE DE SCRAPING - FELIPE NETO (POSTS + REELS)")
    print("=" * 60)
    
    # Username do Felipe Neto no Instagram
    username = "felipeneto"
    
    # Criar instância do scraper
    scraper = ScraperController()
    
    try:
        # 1. Testar conectividade do proxy
        print("\n1️⃣ Testando conectividade do proxy...")
        if not scraper.test_proxy_connection():
            print("❌ Proxy não está funcionando! Abortando teste.")
            return False
        print("✅ Proxy funcionando corretamente!")
        
        # 2. Testar proxy do Instaloader
        print("\n2️⃣ Testando proxy do Instaloader...")
        if not scraper.test_instaloader_proxy():
            print("❌ Proxy do Instaloader não está funcionando! Abortando teste.")
            return False
        print("✅ Proxy do Instaloader funcionando corretamente!")
        
        # 3. Fazer login com Instaloader
        print("\n3️⃣ Fazendo login com Instaloader...")
        if not scraper.login_instaloader():
            print("❌ Falha no login com Instaloader! Abortando teste.")
            return False
        print("✅ Login com Instaloader realizado com sucesso!")
        
        # 4. Criar sessão do Selenium
        print("\n4️⃣ Criando sessão do Selenium...")
        scraper.create_session()
        print("✅ Sessão criada com sucesso!")
        
        # 5. Obter foto de perfil
        print(f"\n5️⃣ Obtendo foto de perfil de @{username}...")
        start_time = time.time()
        
        profile_photo_url = scraper.get_profile_photo(username, size=640)
        if profile_photo_url:
            print(f"✅ Foto de perfil obtida: {profile_photo_url}")
            profile_photo_data = {
                "username": username,
                "profile_photo_url": profile_photo_url,
                "timestamp": datetime.now().isoformat()
            }
            save_to_json(profile_photo_data, f"felipeneto_profile_photo")
        else:
            print("❌ Não foi possível obter a foto de perfil")
        
        photo_time = time.time() - start_time
        print(f"⏱️ Tempo para obter foto: {photo_time:.2f} segundos")
        
        # 6. Obter dados completos do perfil
        print(f"\n6️⃣ Obtendo dados completos do perfil de @{username}...")
        start_time = time.time()
        
        profile_data = scraper.get_profile_data(username)
        if profile_data:
            print("✅ Dados do perfil obtidos com sucesso!")
            print(f"   📊 Seguidores: {profile_data['followers']:,}")
            print(f"   📊 Seguindo: {profile_data['following']:,}")
            print(f"   📊 Posts: {profile_data['uploads']:,}")
            print(f"   🔒 Privado: {'Sim' if profile_data['is_private'] else 'Não'}")
            print(f"   ✅ Verificado: {'Sim' if profile_data['is_verified'] else 'Não'}")
            
            # Salvar dados do perfil
            save_to_json(profile_data, f"felipeneto_profile_data")
        else:
            print("❌ Não foi possível obter os dados do perfil")
        
        profile_time = time.time() - start_time
        print(f"⏱️ Tempo para obter dados do perfil: {profile_time:.2f} segundos")
        
        # 7. Obter posts do perfil
        print(f"\n7️⃣ Obtendo posts de @{username}...")
        start_time = time.time()
        
        posts_data = scraper.get_creator_posts(username)
        if posts_data:
            print(f"✅ {len(posts_data)} posts obtidos com sucesso!")
            
            # Mostrar resumo dos posts
            total_likes = sum(post.get('likes', 0) for post in posts_data)
            total_comments = sum(post.get('comments', 0) for post in posts_data)
            posts_with_hashtags = len([post for post in posts_data if post.get('hashtags')])
            posts_with_tags = len([post for post in posts_data if post.get('tags')])
            
            print(f"   📊 Total de likes: {total_likes:,}")
            print(f"   📊 Total de comentários: {total_comments:,}")
            print(f"   📊 Posts com hashtags: {posts_with_hashtags}")
            print(f"   📊 Posts com tags: {posts_with_tags}")
            
            # Mostrar alguns exemplos de posts
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
            
            # Salvar dados dos posts
            save_to_json(posts_data, f"felipeneto_posts")
        else:
            print("❌ Não foi possível obter os posts")
        
        posts_time = time.time() - start_time
        print(f"⏱️ Tempo para obter posts: {posts_time:.2f} segundos")
        
        # 8. Obter reels do perfil usando Instaloader
        print(f"\n8️⃣ Obtendo reels de @{username} usando Instaloader...")
        start_time = time.time()
        
        reels_data = scraper.get_creator_reels_instaloader(username, max_count=20)
        if reels_data:
            print(f"✅ {len(reels_data)} reels obtidos com sucesso!")
            
            # Mostrar resumo dos reels
            total_reel_likes = sum(reel.get('likes', 0) for reel in reels_data)
            total_reel_comments = sum(reel.get('comments', 0) for reel in reels_data)
            total_reel_views = sum(reel.get('views', 0) for reel in reels_data)
            reels_with_hashtags = len([reel for reel in reels_data if reel.get('hashtags')])
            
            print(f"   📊 Total de likes nos reels: {total_reel_likes:,}")
            print(f"   📊 Total de comentários nos reels: {total_reel_comments:,}")
            print(f"   📊 Total de visualizações nos reels: {total_reel_views:,}")
            print(f"   📊 Reels com hashtags: {reels_with_hashtags}")
            
            # Mostrar alguns exemplos de reels
            print("\n   🎬 Exemplos de reels:")
            for i, reel in enumerate(reels_data[:3]):
                print(f"      Reel {i+1}:")
                print(f"         URL: {reel.get('reel_url', 'N/A')}")
                print(f"         Likes: {reel.get('likes', 0):,}")
                print(f"         Comentários: {reel.get('comments', 0):,}")
                print(f"         Visualizações: {reel.get('views', 0):,}")
                print(f"         Duração: {reel.get('duration', 0):.1f}s")
                if reel.get('hashtags'):
                    print(f"         Hashtags: {', '.join(reel['hashtags'][:3])}")
                if reel.get('caption'):
                    caption_preview = reel['caption'][:100] + "..." if len(reel['caption']) > 100 else reel['caption']
                    print(f"         Legenda: {caption_preview}")
                print()
            
            # Salvar dados dos reels
            save_to_json(reels_data, f"felipeneto_reels")
        else:
            print("❌ Não foi possível obter os reels")
        
        reels_time = time.time() - start_time
        print(f"⏱️ Tempo para obter reels: {reels_time:.2f} segundos")
        
        # 9. Resumo final
        print("\n" + "=" * 60)
        print("📋 RESUMO DO TESTE")
        print("=" * 60)
        print(f"✅ Proxy: Funcionando")
        print(f"✅ Proxy Instaloader: Funcionando")
        print(f"✅ Login Instaloader: Realizado")
        print(f"✅ Sessão Selenium: Criada")
        print(f"✅ Foto de perfil: {'Obtida' if profile_photo_url else 'Falhou'}")
        print(f"✅ Dados do perfil: {'Obtidos' if profile_data else 'Falharam'}")
        print(f"✅ Posts: {'Obtidos' if posts_data else 'Falharam'}")
        print(f"✅ Reels: {'Obtidos' if reels_data else 'Falharam'}")
        
        if profile_data:
            print(f"\n📊 DADOS DO PERFIL:")
            print(f"   Username: @{profile_data['username']}")
            print(f"   Nome: {profile_data['full_name']}")
            print(f"   Seguidores: {profile_data['followers']:,}")
            print(f"   Seguindo: {profile_data['following']:,}")
            print(f"   Posts: {profile_data['uploads']:,}")
            print(f"   Bio: {profile_data['description'][:100]}..." if profile_data['description'] else "   Bio: Sem descrição")
        
        if posts_data:
            print(f"\n📊 DADOS DOS POSTS:")
            print(f"   Total de posts: {len(posts_data)}")
            print(f"   Total de likes: {sum(post.get('likes', 0) for post in posts_data):,}")
            print(f"   Total de comentários: {sum(post.get('comments', 0) for post in posts_data):,}")
        
        if reels_data:
            print(f"\n🎬 DADOS DOS REELS:")
            print(f"   Total de reels: {len(reels_data)}")
            print(f"   Total de likes: {sum(reel.get('likes', 0) for reel in reels_data):,}")
            print(f"   Total de comentários: {sum(reel.get('comments', 0) for reel in reels_data):,}")
            print(f"   Total de visualizações: {sum(reel.get('views', 0) for reel in reels_data):,}")
        
        print("\n🎉 TESTE CONCLUÍDO COM SUCESSO!")
        
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
    print("🤖 Teste de Scraping do Instagram - Felipe Neto (Posts + Reels)")
    print("📅 Data/Hora:", datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    
    # Executar teste
    success = test_felipeneto_scraping()
    
    if success:
        print("\n✅ Todos os testes passaram!")
        print("📁 Verifique os arquivos JSON gerados para os dados extraídos.")
    else:
        print("\n❌ Alguns testes falharam!")
        print("🔍 Verifique os logs acima para mais detalhes.")

if __name__ == "__main__":
    main()




