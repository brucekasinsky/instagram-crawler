#!/usr/bin/env python3
"""
Exemplo de uso do Instagram Scraper com LOGIN ÚNICO
Demonstra como capturar todos os dados em uma única sessão
"""

import sys
import os
import json
from datetime import datetime

# Adicionar o diretório do projeto ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from naunha.InstaScraperV2 import ScraperController

def exemplo_sessao_unica():
    """
    Exemplo de captura de dados em sessão única
    """
    print("🚀 Exemplo - Login Único e Captura Completa")
    print("=" * 60)
    
    # 1. Criar instância do scraper
    scraper = ScraperController()
    
    # 2. Capturar dados completos em uma única sessão
    username = "instagram"  # Perfil para teste
    print(f"\n📱 Capturando dados completos de @{username}...")
    print("🔐 Login será feito apenas UMA vez!")
    
    complete_data = scraper.get_creator_complete_data(username, max_reels=5)
    
    if complete_data:
        print(f"\n✅ Dados capturados com sucesso!")
        
        # Mostrar resumo
        profile = complete_data['profile_data']
        reels = complete_data['reels_data']
        
        print(f"\n📊 RESUMO:")
        print(f"   👤 Username: {profile['username'] if profile else 'N/A'}")
        print(f"   👥 Seguidores: {profile['followers']:,}" if profile else "   👥 Seguidores: N/A")
        print(f"   📸 Posts: {profile['uploads']:,}" if profile else "   📸 Posts: N/A")
        print(f"   🎬 Reels: {len(reels) if reels else 0}")
        
        if reels and complete_data.get('statistics'):
            stats = complete_data['statistics']
            print(f"   ❤️ Total Likes: {stats['total_likes']:,}")
            print(f"   💬 Total Comentários: {stats['total_comments']:,}")
            print(f"   👀 Total Visualizações: {stats['total_views']:,}")
        
        # Salvar dados em arquivo JSON
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"dados_completos_{username}_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(complete_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Dados salvos em: {filename}")
        
        # Mostrar alguns reels
        if reels:
            print(f"\n🎬 PRIMEIROS 3 REELS:")
            for i, reel in enumerate(reels[:3], 1):
                print(f"   {i}. {reel['likes']:,} likes, {reel['comments']:,} comentários")
                if reel['hashtags']:
                    print(f"      Hashtags: {', '.join(reel['hashtags'][:3])}")
        
    else:
        print("❌ Falha na captura de dados")
    
    # 3. Finalizar sessão
    print(f"\n🔒 Finalizando sessão...")
    scraper.quit_session()
    
    print("\n🎉 Exemplo concluído!")

def exemplo_multiplos_usuarios():
    """
    Exemplo de captura de múltiplos usuários em uma única sessão
    """
    print("\n🚀 Exemplo - Múltiplos Usuários em Sessão Única")
    print("=" * 60)
    
    scraper = ScraperController()
    
    # Lista de usuários para testar
    usuarios = ["instagram", "reels"]
    
    # Login único para todos
    print("🔐 Fazendo login único para todos os usuários...")
    if not scraper.ensure_logged_in():
        print("❌ Falha no login")
        return
    
    print("🔒 Sessão ativa - processando múltiplos usuários...")
    
    resultados = {}
    
    for username in usuarios:
        print(f"\n👤 Processando @{username}...")
        
        try:
            # Usar sessão ativa (sem novo login)
            complete_data = scraper.get_creator_complete_data(username, max_reels=3)
            resultados[username] = complete_data
            
            if complete_data:
                profile = complete_data['profile_data']
                reels_count = complete_data['total_reels']
                print(f"   ✅ Sucesso: {profile['followers']:,} seguidores, {reels_count} reels")
            else:
                print(f"   ❌ Falha")
                
        except Exception as e:
            print(f"   ❌ Erro: {str(e)}")
            resultados[username] = None
    
    # Salvar resultados consolidados
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"multiplos_usuarios_{timestamp}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(resultados, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Resultados salvos em: {filename}")
    
    # Resumo final
    sucessos = sum(1 for data in resultados.values() if data)
    print(f"\n📊 RESUMO FINAL:")
    print(f"   ✅ Sucessos: {sucessos}/{len(usuarios)}")
    print(f"   🔒 Login realizado: 1 vez apenas")
    print(f"   ⏱️ Tempo economizado: ~{len(usuarios) * 10} segundos")
    
    # Finalizar sessão
    scraper.quit_session()

def main():
    """
    Função principal
    """
    print("📱 Instagram Scraper - Exemplo de Sessão Única")
    print("🔐 Login realizado apenas UMA vez para todas as operações")
    print("=" * 70)
    
    try:
        # Exemplo 1: Usuário único
        exemplo_sessao_unica()
        
        # Exemplo 2: Múltiplos usuários
        exemplo_multiplos_usuarios()
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Operação cancelada pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro geral: {str(e)}")
    
    print("\n🎉 Todos os exemplos concluídos!")

if __name__ == "__main__":
    main()






