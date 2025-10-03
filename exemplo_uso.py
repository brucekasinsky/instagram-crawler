#!/usr/bin/env python3
"""
Exemplo de uso do Instagram Scraper com login obrigatório
Demonstra como usar o scraper para capturar dados de perfis e reels
"""

import sys
import os

# Adicionar o diretório do projeto ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from naunha.InstaScraperV2 import ScraperController

def exemplo_basico():
    """
    Exemplo básico de uso do scraper
    """
    print("🚀 Exemplo Básico - Instagram Scraper")
    print("=" * 50)
    
    # 1. Criar instância do scraper
    scraper = ScraperController()
    
    # 2. Login é automático em todas as funções
    # Não precisa chamar login_instaloader() manualmente
    
    # 3. Capturar dados de um perfil
    username = "instagram"  # Perfil público para teste
    print(f"\n📊 Capturando dados do perfil @{username}...")
    
    profile_data = scraper.get_profile_data(username)
    if profile_data:
        print(f"✅ Perfil encontrado:")
        print(f"   Nome: {profile_data['full_name']}")
        print(f"   Seguidores: {profile_data['followers']:,}")
        print(f"   Posts: {profile_data['uploads']:,}")
        print(f"   Privado: {'Sim' if profile_data['is_private'] else 'Não'}")
    
    # 4. Capturar reels
    print(f"\n🎬 Capturando reels de @{username}...")
    reels_data = scraper.get_creator_reels_instaloader(username, max_count=5)
    
    if reels_data:
        print(f"✅ {len(reels_data)} reels encontrados!")
        for i, reel in enumerate(reels_data[:3], 1):  # Mostrar apenas os 3 primeiros
            print(f"   Reel {i}: {reel['likes']:,} likes, {reel['comments']:,} comentários")
    else:
        print("❌ Nenhum reel encontrado")
    
    print("\n🎉 Exemplo concluído!")

def exemplo_avancado():
    """
    Exemplo avançado com tratamento de erros
    """
    print("\n🚀 Exemplo Avançado - Tratamento de Erros")
    print("=" * 50)
    
    scraper = ScraperController()
    
    # Lista de usuários para testar
    usuarios_teste = ["instagram", "reels", "creators"]
    
    for username in usuarios_teste:
        print(f"\n🔍 Testando @{username}...")
        
        try:
            # Testar acesso ao perfil
            profile_data = scraper.get_profile_data(username)
            
            if profile_data:
                print(f"✅ Perfil acessível: {profile_data['followers']:,} seguidores")
                
                # Tentar capturar reels
                reels_data = scraper.get_creator_reels_instaloader(username, max_count=3)
                
                if reels_data:
                    total_likes = sum(reel['likes'] for reel in reels_data)
                    print(f"   🎬 {len(reels_data)} reels: {total_likes:,} likes totais")
                else:
                    print(f"   ⚠️ Nenhum reel encontrado")
            else:
                print(f"❌ Perfil não acessível")
                
        except Exception as e:
            print(f"❌ Erro ao processar @{username}: {str(e)}")
        
        print("-" * 30)

def main():
    """
    Função principal
    """
    print("📱 Instagram Scraper - Exemplos de Uso")
    print("ℹ️ Login é obrigatório para todos os perfis (públicos e privados)")
    print("=" * 60)
    
    try:
        # Exemplo básico
        exemplo_basico()
        
        # Exemplo avançado
        exemplo_avancado()
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Operação cancelada pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro geral: {str(e)}")
    
    print("\n🎉 Todos os exemplos concluídos!")

if __name__ == "__main__":
    main()






