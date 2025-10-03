#!/usr/bin/env python3
"""
Teste da função scrapper que replica o comportamento do script PHP
"""

import sys
import os
import json
from datetime import datetime

# Adicionar o diretório do projeto ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from naunha.InstaScraperV2 import ScraperController

def test_scrapper_php():
    """
    Testa a função scrapper que replica o PHP
    """
    print("🚀 Teste da Função Scrapper (Replica PHP)")
    print("=" * 60)
    
    # Criar instância do scraper
    scraper = ScraperController()
    
    # Testar com perfil público
    profile_name = "instagram"  # Perfil público para teste
    
    print(f"🔍 Testando scraper com @{profile_name}...")
    print("📋 Replicando exatamente o comportamento do PHP...")
    
    # Chamar a função scrapper
    result = scraper.scrapper(profile_name)
    
    # Mostrar resultado
    print(f"\n📊 RESULTADO:")
    print(f"   Success: {result['success']}")
    print(f"   Message: {result['message']}")
    
    if result['success'] == 1:
        print(f"   ✅ Dados capturados com sucesso!")
        
        # Mostrar dados do Instagram
        instagram_data = result['data']['instagram']
        print(f"\n👤 DADOS DO PERFIL:")
        print(f"   Username: {instagram_data['username']}")
        print(f"   Nome: {instagram_data['full_name']}")
        print(f"   Seguidores: {instagram_data['followers']:,}")
        print(f"   Seguindo: {instagram_data['following']:,}")
        print(f"   Posts: {instagram_data['uploads']:,}")
        print(f"   Privado: {'Sim' if instagram_data['is_private'] else 'Não'}")
        print(f"   Verificado: {'Sim' if instagram_data['is_verified'] else 'Não'}")
        print(f"   Engagement Rate: {instagram_data['average_engagement_rate']}%")
        
        # Mostrar detalhes/estatísticas
        details = result['data']['details']
        print(f"\n📈 ESTATÍSTICAS DOS POSTS:")
        print(f"   Total Likes: {details['total_likes']:,}")
        print(f"   Total Comentários: {details['total_comments']:,}")
        print(f"   Média Likes: {details['average_likes']:.1f}")
        print(f"   Média Comentários: {details['average_comments']:.1f}")
        
        print(f"\n🎬 ESTATÍSTICAS DOS REELS:")
        print(f"   Total Likes: {details['reels_total_likes']:,}")
        print(f"   Total Comentários: {details['reels_total_comments']:,}")
        print(f"   Total Visualizações: {details['reels_total_video_views']:,}")
        print(f"   Média Likes: {details['reels_average_likes']:.1f}")
        print(f"   Média Comentários: {details['reels_average_comments']:.1f}")
        print(f"   Média Visualizações: {details['reels_average_video_views']:.1f}")
        print(f"   Engagement Rate: {details['reels_average_engagement_rate']}%")
        
        # Mostrar top hashtags
        if details['top_hashtags']:
            print(f"\n🏷️ TOP HASHTAGS:")
            for hashtag, count in list(details['top_hashtags'].items())[:5]:
                print(f"   #{hashtag}: {count} vezes")
        
        # Mostrar top mentions
        if details['top_mentions']:
            print(f"\n👥 TOP MENTIONS:")
            for mention, count in list(details['top_mentions'].items())[:5]:
                print(f"   @{mention}: {count} vezes")
        
        # Mostrar top posts
        if details['top_posts']:
            print(f"\n🔥 TOP POSTS (por engagement):")
            for post_id, engagement in list(details['top_posts'].items())[:3]:
                print(f"   {post_id}: {engagement}% engagement")
        
        # Salvar dados em arquivo JSON
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"scrapper_result_{profile_name}_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Dados salvos em: {filename}")
        
        # Mostrar URL da imagem
        print(f"\n🖼️ IMAGEM:")
        print(f"   URL: {result['data']['image']}")
        
    else:
        print(f"   ❌ Falha: {result['message']}")
    
    # Finalizar sessão
    print(f"\n🔒 Finalizando sessão...")
    scraper.quit_session()
    
    print("\n🎉 Teste concluído!")
    return result

def test_scrapper_multiple():
    """
    Testa o scraper com múltiplos perfis
    """
    print("\n🚀 Teste com Múltiplos Perfis")
    print("=" * 60)
    
    scraper = ScraperController()
    
    # Lista de perfis para testar
    profiles = ["instagram", "reels"]
    
    results = {}
    
    for profile in profiles:
        print(f"\n👤 Testando @{profile}...")
        result = scraper.scrapper(profile)
        results[profile] = result
        
        if result['success'] == 1:
            followers = result['data']['instagram']['followers']
            print(f"   ✅ Sucesso: {followers:,} seguidores")
        else:
            print(f"   ❌ Falha: {result['message']}")
    
    # Salvar resultados consolidados
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"scrapper_multiple_{timestamp}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Resultados salvos em: {filename}")
    
    # Resumo
    sucessos = sum(1 for r in results.values() if r['success'] == 1)
    print(f"\n📊 RESUMO:")
    print(f"   ✅ Sucessos: {sucessos}/{len(profiles)}")
    print(f"   🔒 Login realizado: 1 vez apenas")
    
    scraper.quit_session()

def main():
    """
    Função principal
    """
    print("📱 Instagram Scraper - Teste da Função PHP")
    print("🔍 Replicando exatamente o comportamento do script PHP")
    print("=" * 70)
    
    try:
        # Teste 1: Perfil único
        test_scrapper_php()
        
        # Teste 2: Múltiplos perfis
        test_scrapper_multiple()
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Operação cancelada pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro geral: {str(e)}")
    
    print("\n🎉 Todos os testes concluídos!")

if __name__ == "__main__":
    main()







