#!/usr/bin/env python3
"""
Script de teste para o Instagram Scraper com Instaloader
Testa login e captura de reels
"""

import sys
import os

# Adicionar o diretório do projeto ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from naunha.InstaScraperV2 import ScraperController

def main():
    """
    Função principal para testar o Instagram Scraper
    """
    print("🚀 Iniciando teste do Instagram Scraper com Instaloader")
    print("=" * 60)
    
    # Criar instância do scraper
    scraper = ScraperController()
    
    # Testar conexão e login (obrigatório para todos os perfis)
    print("\n1️⃣ Testando conexão e login (obrigatório)...")
    test_profile = "instagram"  # Perfil público para teste
    connection_success = scraper.test_instagram_connection(test_profile)
    
    if not connection_success:
        print("❌ Falha na conexão. Verifique as credenciais e proxy.")
        print("ℹ️ Lembre-se: Login é obrigatório mesmo para perfis públicos!")
        return
    
    print("\n2️⃣ Testando captura de dados do perfil...")
    profile_data = scraper.get_profile_data(test_profile)
    
    if profile_data:
        print(f"✅ Dados do perfil capturados:")
        print(f"   Username: {profile_data['username']}")
        print(f"   Nome completo: {profile_data['full_name']}")
        print(f"   Seguidores: {profile_data['followers']:,}")
        print(f"   Seguindo: {profile_data['following']:,}")
        print(f"   Posts: {profile_data['uploads']:,}")
        print(f"   Privado: {'Sim' if profile_data['is_private'] else 'Não'}")
        print(f"   Verificado: {'Sim' if profile_data['is_verified'] else 'Não'}")
    else:
        print("❌ Falha ao capturar dados do perfil")
        return
    
    print("\n3️⃣ Testando captura de reels com Instaloader...")
    reels_data = scraper.get_creator_reels_instaloader(test_profile, max_count=5)
    
    if reels_data:
        print(f"✅ Reels capturados: {len(reels_data)}")
        for i, reel in enumerate(reels_data[:3], 1):  # Mostrar apenas os 3 primeiros
            print(f"   Reel {i}:")
            print(f"     ID: {reel['reel_id']}")
            print(f"     Likes: {reel['likes']:,}")
            print(f"     Comentários: {reel['comments']:,}")
            print(f"     Visualizações: {reel['views']:,}")
            print(f"     Duração: {reel['duration']}s")
            if reel['hashtags']:
                print(f"     Hashtags: {', '.join(reel['hashtags'][:3])}...")
    else:
        print("❌ Nenhum reel encontrado")
    
    print("\n4️⃣ Testando funcionalidade completa de reels...")
    test_reels = scraper.test_reels_functionality(test_profile)
    
    if test_reels:
        print(f"✅ Teste completo bem-sucedido! {len(test_reels)} reels capturados")
    else:
        print("❌ Teste completo falhou")
    
    print("\n" + "=" * 60)
    print("🎉 Teste concluído!")

if __name__ == "__main__":
    main()
