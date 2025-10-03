#!/usr/bin/env python3
"""
Script para abrir Selenium e manter a janela aberta até o usuário fechar
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def abrir_selenium():
    print("🚀 Abrindo navegador Selenium...")
    
    try:
        # Configurações básicas do Chrome
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1280,720")
        chrome_options.add_argument("--start-maximized")
        
        print("📦 Instalando ChromeDriver...")
        service = Service(ChromeDriverManager().install())
        
        print("🌐 Criando WebDriver...")
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        print("✅ Navegador aberto com sucesso!")
        
        print("🌐 Navegando para Instagram...")
        driver.get("https://www.instagram.com/")
        
        print("📄 Título da página:", driver.title)
        
        print("\n" + "="*60)
        print("🎉 NAVEGADOR ABERTO!")
        print("="*60)
        print("📱 O navegador está aberto no Instagram")
        print("👆 Você pode fazer login manualmente")
        print("⏳ A janela ficará aberta até você fechar")
        print("🔒 Para fechar, feche a janela do navegador ou pressione Ctrl+C")
        print("="*60)
        
        # Manter o navegador aberto
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🔒 Fechando navegador...")
            driver.quit()
            print("✅ Navegador fechado!")
        
    except Exception as e:
        print(f"❌ Erro: {str(e)}")

if __name__ == "__main__":
    abrir_selenium()
