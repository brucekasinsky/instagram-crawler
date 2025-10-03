#!/usr/bin/env python3
"""
Exemplo simples de uso da função scrapper que replica o PHP
"""

import sys
import os
import json

# Adicionar o diretório do projeto ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from naunha.InstaScraperV2 import ScraperController

def exemplo_simples():
    """
    Exemplo simples de uso
    """
    print("🚀 Exemplo Simples - Função Scrapper (PHP)")
    print("=" * 50)
    
    # 1. Criar instância
    scraper = ScraperController()
    
    # 2. Usar a função scrapper (igual ao PHP)
    profile_name = "instagram"  # Perfil para teste
    
    print(f"🔍 Capturando dados de @{profile_name}...")
    result = scraper.scrapper(profile_name)
    
    # 3. Verificar resultado
    if result['success'] == 1:
        print("✅ Sucesso!")
        
        # Dados do Instagram
        instagram = result['data']['instagram']
        details = result['data']['details']
        
        print(f"\n📊 RESUMO:")
        print(f"   👤 @{instagram['username']}")
        print(f"   👥 {instagram['followers']:,} seguidores")
        print(f"   📸 {instagram['uploads']:,} posts")
        print(f"   ❤️ {details['total_likes']:,} likes totais")
        print(f"   🎬 {details['reels_total_likes']:,} likes em reels")
        print(f"   📈 {instagram['average_engagement_rate']}% engagement")
        
        # Salvar resultado
        with open(f"resultado_{profile_name}.json", 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Dados salvos em: resultado_{profile_name}.json")
        
    else:
        print(f"❌ Erro: {result['message']}")
    
    # 4. Finalizar
    scraper.quit_session()
    print("\n🎉 Concluído!")

def exemplo_com_credenciais():
    """
    Exemplo usando credenciais customizadas
    """
    print("\n🚀 Exemplo com Credenciais Customizadas")
    print("=" * 50)
    
    scraper = ScraperController()
    
    # Usar credenciais customizadas
    profile_name = "instagram"
    custom_login = "coralvelado2309"  # Ou suas credenciais
    custom_senha = "4&bfa&Eh8QFw"
    
    print(f"🔐 Usando credenciais customizadas...")
    result = scraper.scrapper(profile_name, custom_login, custom_senha)
    
    if result['success'] == 1:
        print("✅ Sucesso com credenciais customizadas!")
    else:
        print(f"❌ Erro: {result['message']}")
    
    scraper.quit_session()

if __name__ == "__main__":
    try:
        exemplo_simples()
        exemplo_com_credenciais()
    except Exception as e:
        print(f"❌ Erro: {str(e)}")







