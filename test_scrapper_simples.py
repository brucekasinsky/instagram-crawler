#!/usr/bin/env python3
"""
Teste da função scrapper_simples - versão mais robusta e sem loops infinitos
"""

import sys
import os
import json
from datetime import datetime

# Adicionar o diretório do projeto ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from naunha.InstaScraperV2 import ScraperController

def test_scrapper_simples():
    """
    Testa a versão simplificada do scraper
    """
    print("🚀 Teste do Scrapper Simples (Sem Loops Infinitos)")
    print("=" * 60)
    
    # Criar instância do scraper
    scraper = ScraperController()
    
    # Testar com perfil público
    profile_name = "instagram"  # Perfil público para teste
    
    print(f"🔍 Testando scraper simples com @{profile_name}...")
    print("📋 Versão robusta sem loops infinitos...")
    
    # Chamar a função scrapper_simples
    result = scraper.scrapper_simples(profile_name)
    
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
        
        # Salvar dados em arquivo JSON
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"scrapper_simples_result_{profile_name}_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Dados salvos em: {filename}")
        
    else:
        print(f"   ❌ Falha: {result['message']}")
    
    # Finalizar sessão
    print(f"\n🔒 Finalizando sessão...")
    scraper.quit_session()
    
    print("\n🎉 Teste concluído!")
    return result

def test_multiplos_perfis():
    """
    Testa com múltiplos perfis usando a versão simples
    """
    print("\n🚀 Teste com Múltiplos Perfis (Versão Simples)")
    print("=" * 60)
    
    scraper = ScraperController()
    
    # Lista de perfis para testar
    profiles = ["instagram", "reels"]
    
    results = {}
    
    for profile in profiles:
        print(f"\n👤 Testando @{profile}...")
        result = scraper.scrapper_simples(profile)
        results[profile] = result
        
        if result['success'] == 1:
            followers = result['data']['instagram']['followers']
            print(f"   ✅ Sucesso: {followers:,} seguidores")
        else:
            print(f"   ❌ Falha: {result['message']}")
    
    # Salvar resultados consolidados
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"scrapper_simples_multiple_{timestamp}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Resultados salvos em: {filename}")
    
    # Resumo
    sucessos = sum(1 for r in results.values() if r['success'] == 1)
    print(f"\n📊 RESUMO:")
    print(f"   ✅ Sucessos: {sucessos}/{len(profiles)}")
    print(f"   🔒 Login realizado: 1 vez apenas")
    print(f"   ⏱️ Sem loops infinitos")
    
    scraper.quit_session()

def main():
    """
    Função principal
    """
    print("📱 Instagram Scraper - Teste da Versão Simples")
    print("🔍 Versão robusta sem loops infinitos")
    print("=" * 70)
    
    try:
        # Teste 1: Perfil único
        test_scrapper_simples()
        
        # Teste 2: Múltiplos perfis
        test_multiplos_perfis()
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Operação cancelada pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro geral: {str(e)}")
    
    print("\n🎉 Todos os testes concluídos!")

if __name__ == "__main__":
    main()






