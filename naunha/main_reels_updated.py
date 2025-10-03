#!/usr/bin/env python3
"""
Sistema principal para extração de reels do Instagram
Usando automação web com login manual
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'naunha'))

from naunha.InstaScraperV2 import ScraperController
import json
from datetime import datetime

def main():
    """
    Função principal do sistema - Fluxo completo:
    1. Abrir Selenium
    2. Login manual no Instagram
    3. Extrair reels do perfil
    """
    print("🎬 SISTEMA DE EXTRAÇÃO DE REELS DO INSTAGRAM")
    print("=" * 60)
    print("📝 Este sistema irá:")
    print("   1. 🚀 Abrir o navegador Chrome")
    print("   2. 🔐 Permitir login manual no Instagram")
    print("   3. 🎬 Extrair reels do perfil especificado")
    print("=" * 60)
    
    # Criar instância do scraper
    scraper = ScraperController()
    
    try:
        # PASSO 1: ABRIR SELENIUM E FAZER LOGIN
        print("\n🚀 PASSO 1: Abrindo navegador e fazendo login...")
        print("=" * 50)
        
        if not scraper.manual_login_instagram():
            print("❌ Falha no login. Sistema encerrado.")
            return
        
        print("✅ Login realizado com sucesso!")
        
        # PASSO 2: OBTER PERFIL PARA EXTRAIR
        print("\n🎬 PASSO 2: Configurando extração de reels...")
        print("=" * 50)
        
        profile_name = input("📝 Digite o nome do perfil do Instagram: ").strip()
        
        if not profile_name:
            print("❌ Nome do perfil não fornecido")
            return
        
        # Obter número máximo de reels
        try:
            max_reels = int(input("📊 Número máximo de reels (padrão: 10): ") or "10")
        except ValueError:
            max_reels = 10
        
        print(f"\n🎯 Configuração:")
        print(f"   👤 Perfil: @{profile_name}")
        print(f"   📊 Máximo de reels: {max_reels}")
        
        # PASSO 3: EXTRAIR REELS
        print(f"\n🚀 PASSO 3: Extraindo reels de @{profile_name}...")
        print("=" * 50)
        
        # Executar scraper
        result = scraper.scrapper_reels_web(profile_name, max_reels)
        
        # PASSO 4: EXIBIR RESULTADOS
        print(f"\n📊 PASSO 4: Resultados da extração...")
        display_results(result, profile_name)
        
    except KeyboardInterrupt:
        print("\n⚠️ Sistema interrompido pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        # Fechar navegador
        print("\n🔒 Fechando navegador...")
        scraper.quit_session()
        print("✅ Sistema finalizado!")

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
