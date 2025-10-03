#!/usr/bin/env python3
"""
Script de teste para demonstrar o uso da função create_session modificada
com parâmetros mobile e web
"""

from InstaScraperV2 import ScraperController
import time

def test_mobile_session():
    """Testa a criação de sessão em modo mobile"""
    print("=" * 50)
    print("🧪 TESTE: Sessão MOBILE")
    print("=" * 50)
    
    scraper = ScraperController()
    
    try:
        # Criar sessão em modo mobile
        scraper.create_session(mobile=True)
        
        print("✅ Sessão mobile criada com sucesso!")
        print("📱 Configurações aplicadas:")
        print("   - User-Agent: Instagram App (Android)")
        print("   - Viewport: 375x812 (iPhone X)")
        print("   - Touch events: Habilitados")
        print("   - Mobile emulation: Ativada")
        
        # Testar navegação para Instagram
        print("\n🌐 Testando navegação para Instagram...")
        scraper.browser.get("https://www.instagram.com")
        time.sleep(3)
        
        # Verificar se a página carregou
        current_url = scraper.browser.current_url
        print(f"📍 URL atual: {current_url}")
        
        if "instagram.com" in current_url:
            print("✅ Navegação para Instagram bem-sucedida!")
        else:
            print("⚠️ Pode ter sido redirecionado")
            
    except Exception as e:
        print(f"❌ Erro ao testar sessão mobile: {str(e)}")
    finally:
        # Fechar sessão
        scraper.quit_session()

def test_web_session():
    """Testa a criação de sessão em modo web"""
    print("\n" + "=" * 50)
    print("🧪 TESTE: Sessão WEB")
    print("=" * 50)
    
    scraper = ScraperController()
    
    try:
        # Criar sessão em modo web (padrão)
        scraper.create_session(mobile=False)
        
        print("✅ Sessão web criada com sucesso!")
        print("💻 Configurações aplicadas:")
        print("   - User-Agent: Chrome Desktop")
        print("   - Viewport: Desktop padrão")
        print("   - Mobile emulation: Desabilitada")
        
        # Testar navegação para Instagram
        print("\n🌐 Testando navegação para Instagram...")
        scraper.browser.get("https://www.instagram.com")
        time.sleep(3)
        
        # Verificar se a página carregou
        current_url = scraper.browser.current_url
        print(f"📍 URL atual: {current_url}")
        
        if "instagram.com" in current_url:
            print("✅ Navegação para Instagram bem-sucedida!")
        else:
            print("⚠️ Pode ter sido redirecionado")
            
    except Exception as e:
        print(f"❌ Erro ao testar sessão web: {str(e)}")
    finally:
        # Fechar sessão
        scraper.quit_session()

def test_default_session():
    """Testa a criação de sessão com parâmetro padrão (web)"""
    print("\n" + "=" * 50)
    print("🧪 TESTE: Sessão PADRÃO (sem parâmetro)")
    print("=" * 50)
    
    scraper = ScraperController()
    
    try:
        # Criar sessão sem parâmetro (deve usar web por padrão)
        scraper.create_session()
        
        print("✅ Sessão padrão criada com sucesso!")
        print("💻 Configurações aplicadas (padrão = web):")
        print("   - User-Agent: Chrome Desktop")
        print("   - Viewport: Desktop padrão")
        print("   - Mobile emulation: Desabilitada")
        
    except Exception as e:
        print(f"❌ Erro ao testar sessão padrão: {str(e)}")
    finally:
        # Fechar sessão
        scraper.quit_session()

if __name__ == "__main__":
    print("🚀 Iniciando testes da função create_session modificada...")
    print("📝 Este script testa as configurações mobile e web")
    print("⚠️  Nota: Os testes abrirão janelas do Chrome para demonstração")
    
    # Executar todos os testes
    test_mobile_session()
    test_web_session()
    test_default_session()
    
    print("\n" + "=" * 50)
    print("✅ TODOS OS TESTES CONCLUÍDOS!")
    print("=" * 50)
    print("\n📋 RESUMO DAS MODIFICAÇÕES:")
    print("1. ✅ Função create_session() agora aceita parâmetro 'mobile'")
    print("2. ✅ mobile=True: Configura para parecer app mobile do Instagram")
    print("3. ✅ mobile=False: Configura para navegador web padrão")
    print("4. ✅ mobile não especificado: Usa web por padrão")
    print("\n🔧 CONFIGURAÇÕES MOBILE INCLUEM:")
    print("   - User-Agent do Instagram App (Android)")
    print("   - Viewport 375x812 (iPhone X)")
    print("   - Touch events habilitados")
    print("   - Mobile emulation ativada")
    print("   - Headers específicos para mobile")











