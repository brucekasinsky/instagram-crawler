#!/usr/bin/env python3
"""
Teste do sistema de extração de reels usando automação web
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'naunha'))

from naunha.InstaScraperV2 import ScraperController
import json
from datetime import datetime

def main():
    """
    Função principal para testar o scraper de reels
    """
    print("🚀 Iniciando teste do scraper de reels com automação web...")
    
    # Criar instância do scraper
    scraper = ScraperController()
    
    try:
        # Testar proxy primeiro
        print("\n🌐 Testando conectividade do proxy...")
        if not scraper.test_proxy_connection():
            print("❌ Proxy não está funcionando. Continuando sem proxy...")
        
        # Definir perfil para testar
        profile_name = input("\n📝 Digite o nome do perfil do Instagram para extrair reels: ").strip()
        
        if not profile_name:
            print("❌ Nome do perfil não fornecido")
            return
        
        # Definir número máximo de reels
        try:
            max_reels = int(input("📊 Número máximo de reels para extrair (padrão: 10): ") or "10")
        except ValueError:
            max_reels = 10
        
        print(f"\n🎬 Iniciando extração de reels de @{profile_name}...")
        print(f"📊 Máximo de reels: {max_reels}")
        
        # Executar scraper
        result = scraper.scrapper_reels_web(profile_name, max_reels)
        
        # Exibir resultados
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
            
            # Salvar resultados em arquivo JSON
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"reels_{profile_name}_{timestamp}.json"
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            
            print(f"\n💾 Resultados salvos em: {filename}")
            
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
        
    except KeyboardInterrupt:
        print("\n⚠️ Operação cancelada pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {str(e)}")
    finally:
        # Fechar navegador
        print("\n🔒 Fechando navegador...")
        scraper.quit_session()
        print("✅ Teste finalizado!")

if __name__ == "__main__":
    main()
