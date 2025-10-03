#!/usr/bin/env python3
"""
Sistema principal para extração de reels do Instagram
Usando automação web com login manual
"""

from InstaScraperV2 import ScraperController
import json
from datetime import datetime

def main():
    """
    Função principal do sistema de extração de reels
    """
    print("🎬 SISTEMA DE EXTRAÇÃO DE REELS DO INSTAGRAM")
    print("=" * 50)
    print("📝 Este sistema usa automação web com login manual")
    print("🔐 Você fará login manualmente no navegador")
    print("🎯 Foco em extrair reels de perfis públicos")
    print("=" * 50)
    
    # Criar instância do scraper
    scraper = ScraperController()
    
    try:
        # Menu principal
        while True:
            print("\n📋 MENU PRINCIPAL:")
            print("1. 🎬 Extrair reels de um perfil")
            print("2. 🌐 Testar conectividade do proxy")
            print("3. 🔐 Fazer login manual")
            print("4. ❌ Sair")
            
            choice = input("\n👉 Escolha uma opção (1-4): ").strip()
            
            if choice == "1":
                extract_reels_menu(scraper)
            elif choice == "2":
                test_proxy_menu(scraper)
            elif choice == "3":
                login_menu(scraper)
            elif choice == "4":
                print("👋 Saindo do sistema...")
                break
            else:
                print("❌ Opção inválida. Tente novamente.")
    
    except KeyboardInterrupt:
        print("\n⚠️ Sistema interrompido pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {str(e)}")
    finally:
        # Fechar navegador
        print("\n🔒 Fechando navegador...")
        scraper.quit_session()
        print("✅ Sistema finalizado!")

def extract_reels_menu(scraper):
    """
    Menu para extração de reels
    """
    print("\n🎬 EXTRAÇÃO DE REELS")
    print("-" * 30)
    
    # Obter nome do perfil
    profile_name = input("📝 Nome do perfil do Instagram: ").strip()
    
    if not profile_name:
        print("❌ Nome do perfil não fornecido")
        return
    
    # Obter número máximo de reels
    try:
        max_reels = int(input("📊 Número máximo de reels (padrão: 10): ") or "10")
    except ValueError:
        max_reels = 10
    
    print(f"\n🚀 Iniciando extração de reels de @{profile_name}...")
    print(f"📊 Máximo de reels: {max_reels}")
    
    # Executar scraper
    result = scraper.scrapper_reels_web(profile_name, max_reels)
    
    # Exibir resultados
    display_results(result, profile_name)

def test_proxy_menu(scraper):
    """
    Menu para teste de proxy
    """
    print("\n🌐 TESTE DE PROXY")
    print("-" * 20)
    
    if scraper.test_proxy_connection():
        print("✅ Proxy está funcionando corretamente!")
    else:
        print("❌ Proxy não está funcionando")

def login_menu(scraper):
    """
    Menu para login manual
    """
    print("\n🔐 LOGIN MANUAL")
    print("-" * 20)
    
    username = input("👤 Username (opcional): ").strip()
    password = input("🔑 Senha (opcional): ").strip()
    
    if scraper.manual_login_instagram(username or None, password or None):
        print("✅ Login realizado com sucesso!")
    else:
        print("❌ Falha no login")

def display_results(result, profile_name):
    """
    Exibe os resultados da extração
    """
    print("\n" + "="*60)
    print("📊 RESULTADOS DA EXTRAÇÃO")
    print("="*60)
    
    if result['success'] == 1:
        data = result['data']
        print(f"✅ Status: {result['message']}")
        print(f"👤 Perfil: @{data['profile']}")
        print(f"🎬 Total de reels: {data['total_reels']}")
        
        if data['statistics']:
            stats = data['statistics']
            print(f"❤️ Total de likes: {stats['total_likes']:,}")
            print(f"💬 Total de comentários: {stats['total_comments']:,}")
            print(f"📈 Média de likes: {stats['average_likes']:,}")
            print(f"📈 Média de comentários: {stats['average_comments']:,}")
        
        # Salvar resultados
        save_results(result, profile_name)
        
        # Exibir alguns reels como exemplo
        if data['reels']:
            print(f"\n🎬 PRIMEIROS {min(3, len(data['reels']))} REELS:")
            for i, reel in enumerate(data['reels'][:3]):
                print(f"\n  Reel {i+1}:")
                print(f"    ID: {reel.get('reel_id', 'N/A')}")
                print(f"    URL: {reel.get('reel_url', 'N/A')}")
                print(f"    Likes: {reel.get('likes', 0):,}")
                print(f"    Comentários: {reel.get('comments', 0):,}")
                if reel.get('thumbnail_url'):
                    print(f"    Thumbnail: {reel['thumbnail_url'][:50]}...")
    
    else:
        print(f"❌ Erro: {result['message']}")

def save_results(result, profile_name):
    """
    Salva os resultados em arquivo JSON
    """
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"reels_{profile_name}_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Resultados salvos em: {filename}")
        
    except Exception as e:
        print(f"⚠️ Erro ao salvar resultados: {str(e)}")

if __name__ == "__main__":
    main()
