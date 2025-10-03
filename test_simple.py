#!/usr/bin/env python3
"""
Teste simples do sistema de reels
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'naunha'))

try:
    from naunha.InstaScraperV2 import ScraperController
    print("✅ Importação bem-sucedida!")
    
    # Criar instância
    scraper = ScraperController()
    print("✅ Instância criada!")
    
    # Testar proxy
    scraper.test_proxy_connection()
    
except Exception as e:
    print(f"❌ Erro: {str(e)}")
    import traceback
    traceback.print_exc()
