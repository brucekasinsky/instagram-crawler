#!/usr/bin/env python3
"""
Teste simples do Selenium para verificar se está funcionando
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def test_selenium():
    print("🧪 Testando Selenium...")
    
    try:
        # Configurações básicas do Chrome
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1280,720")
        
        print("📦 Instalando ChromeDriver...")
        service = Service(ChromeDriverManager().install())
        
        print("🚀 Criando WebDriver...")
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        print("✅ WebDriver criado com sucesso!")
        
        print("🌐 Navegando para Google...")
        driver.get("https://www.google.com")
        
        print(f"📄 Título da página: {driver.title}")
        
        print("⏳ Aguardando 3 segundos...")
        time.sleep(3)
        
        print("🔒 Fechando navegador...")
        driver.quit()
        
        print("✅ Teste concluído com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_selenium()
    if success:
        print("🎉 Selenium está funcionando!")
    else:
        print("💥 Selenium não está funcionando!")
