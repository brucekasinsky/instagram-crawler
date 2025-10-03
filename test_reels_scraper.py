#!/usr/bin/env python3
"""
Script específico para testar captura de reels
Testa com perfis conhecidos por terem muitos reels
"""

import sys
import os
import json
from datetime import datetime

# Adicionar o diretório do projeto ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from naunha.InstaScraperV2 import ScraperController

def test_reels_extraction(creator_slug, max_reels=10):
    """
    Testa extração de reels para um perfil específico
    """
    print(f"🎬 Testando extração de reels para: @{creator_slug}")
    print("=" * 60)
    
    # Criar instância do scraper
    scraper = ScraperController()
    
    # Testar login primeiro (obrigatório para todos os perfis)
    print("\n🔐 Fazendo login no Instagram (obrigatório)...")
    if not scraper.login_instaloader():
        print("❌ Falha no login")
        print("ℹ️ Lembre-se: Login é obrigatório mesmo para perfis públicos!")
        return None
    
    # Testar captura de dados do perfil
    print(f"\n👤 Capturando dados do perfil @{creator_slug}...")
    profile_data = scraper.get_profile_data(creator_slug)
    
    if not profile_data:
        print(f"❌ Não foi possível acessar o perfil @{creator_slug}")
        return None
    
    print(f"✅ Perfil acessado:")
    print(f"   Seguidores: {profile_data['followers']:,}")
    print(f"   Posts: {profile_data['uploads']:,}")
    print(f"   Privado: {'Sim' if profile_data['is_private'] else 'Não'}")
    
    # Testar captura de reels com Instaloader
    print(f"\n🎬 Capturando reels com Instaloader (máx: {max_reels})...")
    reels_data = scraper.get_creator_reels_instaloader(creator_slug, max_count=max_reels)
    
    if reels_data:
        print(f"✅ {len(reels_data)} reels capturados com Instaloader!")
        
        # Salvar dados em arquivo JSON
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"reels_data_{creator_slug}_{timestamp}.json"
        
        # Preparar dados para salvar
        output_data = {
            'profile': profile_data,
            'reels': reels_data,
            'timestamp': timestamp,
            'total_reels': len(reels_data)
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Dados salvos em: {filename}")
        
        # Mostrar estatísticas
        total_likes = sum(reel['likes'] for reel in reels_data)
        total_comments = sum(reel['comments'] for reel in reels_data)
        total_views = sum(reel['views'] for reel in reels_data)
        
        print(f"\n📊 Estatísticas dos reels:")
        print(f"   Total de likes: {total_likes:,}")
        print(f"   Total de comentários: {total_comments:,}")
        print(f"   Total de visualizações: {total_views:,}")
        print(f"   Média de likes por reel: {total_likes // len(reels_data):,}")
        
        # Mostrar os top 3 reels por likes
        top_reels = sorted(reels_data, key=lambda x: x['likes'], reverse=True)[:3]
        print(f"\n🏆 Top 3 reels por likes:")
        for i, reel in enumerate(top_reels, 1):
            print(f"   {i}. {reel['likes']:,} likes - {reel['comments']:,} comentários")
        
        return reels_data
    else:
        print("❌ Nenhum reel encontrado")
        return None

def main():
    """
    Função principal
    """
    # Perfis conhecidos por terem muitos reels
    test_profiles = [
        "instagram",      # Perfil oficial do Instagram
        "reels",          # Perfil oficial de Reels
        "creators",       # Perfil oficial de Creators
    ]
    
    print("🚀 Teste de Captura de Reels do Instagram")
    print("=" * 60)
    
    for profile in test_profiles:
        try:
            reels_data = test_reels_extraction(profile, max_reels=5)
            if reels_data:
                print(f"✅ Sucesso com @{profile}: {len(reels_data)} reels")
                break  # Parar no primeiro sucesso
            else:
                print(f"⚠️ Nenhum reel encontrado em @{profile}")
        except Exception as e:
            print(f"❌ Erro ao testar @{profile}: {str(e)}")
        
        print("\n" + "-" * 40 + "\n")
    
    print("🎉 Teste concluído!")

if __name__ == "__main__":
    main()
