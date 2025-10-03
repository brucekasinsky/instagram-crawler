#!/usr/bin/env python3
"""
Script para corrigir problemas com o ChromeDriver
"""

import os
import shutil
import subprocess
from webdriver_manager.chrome import ChromeDriverManager

def clean_webdriver_cache():
    """Limpa o cache do WebDriver Manager"""
    print("🧹 Limpando cache do WebDriver Manager...")
    
    # Caminho do cache do WebDriver Manager
    cache_path = os.path.expanduser("~/.wdm")
    
    if os.path.exists(cache_path):
        try:
            shutil.rmtree(cache_path)
            print(f"✅ Cache removido: {cache_path}")
        except Exception as e:
            print(f"⚠️ Erro ao remover cache: {str(e)}")
    else:
        print("ℹ️ Cache não encontrado")

def install_chromedriver():
    """Instala o ChromeDriver corretamente"""
    print("📥 Instalando ChromeDriver...")
    
    try:
        # Limpar cache primeiro
        clean_webdriver_cache()
        
        # Instalar ChromeDriver
        driver_path = ChromeDriverManager().install()
        print(f"✅ ChromeDriver instalado em: {driver_path}")
        
        # Verificar se o arquivo é executável
        if os.path.exists(driver_path):
            # Tornar executável
            os.chmod(driver_path, 0o755)
            print("✅ Permissões de execução configuradas")
            
            # Testar se é executável
            try:
                result = subprocess.run([driver_path, '--version'], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    print(f"✅ ChromeDriver funcionando: {result.stdout.strip()}")
                    return True
                else:
                    print(f"❌ ChromeDriver não funcionando: {result.stderr}")
                    return False
            except Exception as e:
                print(f"❌ Erro ao testar ChromeDriver: {str(e)}")
                return False
        else:
            print(f"❌ Arquivo não encontrado: {driver_path}")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao instalar ChromeDriver: {str(e)}")
        return False

def check_chrome_installation():
    """Verifica se o Chrome está instalado"""
    print("🔍 Verificando instalação do Chrome...")
    
    try:
        # Tentar diferentes comandos para encontrar o Chrome
        chrome_commands = ['google-chrome', 'chrome', 'chromium-browser', 'chromium']
        
        for cmd in chrome_commands:
            try:
                result = subprocess.run([cmd, '--version'], 
                                      capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    print(f"✅ Chrome encontrado: {result.stdout.strip()}")
                    return True
            except:
                continue
        
        print("❌ Chrome não encontrado no sistema")
        print("💡 Instale o Chrome ou Chromium:")
        print("   sudo apt update")
        print("   sudo apt install google-chrome-stable")
        print("   # ou")
        print("   sudo apt install chromium-browser")
        return False
        
    except Exception as e:
        print(f"❌ Erro ao verificar Chrome: {str(e)}")
        return False

def main():
    """Função principal"""
    print("🔧 CORRETOR DE CHROMEDRIVER")
    print("=" * 40)
    
    # 1. Verificar Chrome
    if not check_chrome_installation():
        print("\n❌ Chrome não está instalado. Instale primeiro.")
        return False
    
    # 2. Limpar cache
    clean_webdriver_cache()
    
    # 3. Instalar ChromeDriver
    if install_chromedriver():
        print("\n🎉 ChromeDriver configurado com sucesso!")
        print("✅ Agora você pode executar os testes.")
        return True
    else:
        print("\n❌ Falha ao configurar ChromeDriver")
        print("💡 Tente instalar manualmente:")
        print("   wget https://chromedriver.storage.googleapis.com/LATEST_RELEASE")
        print("   # Depois baixe a versão correspondente")
        return False

if __name__ == "__main__":
    main()




