    def test_proxy_connection(self):
        """
        Testa a conectividade do proxy fazendo uma requisição simples
        """
        try:
            print("🌐 Testando conectividade do proxy...")
            
            # Tentar primeiro com HTTP
            try:
                response = requests.get('http://httpbin.org/ip', 
                                      proxies={'http': self.PROXY_CONFIG['http']}, 
                                      timeout=10)
                if response.status_code == 200:
                    ip_info = response.json()
                    print(f"✅ Proxy funcionando! IP detectado: {ip_info.get('origin', 'N/A')}")
                    return True
            except Exception as e1:
                print(f"⚠️ Erro com HTTP: {str(e1)}")
                
                # Tentar com HTTPS
                try:
                    response = requests.get('https://httpbin.org/ip', 
                                          proxies=self.PROXY_CONFIG, 
                                          timeout=10, 
                                          verify=False)
                    if response.status_code == 200:
                        ip_info = response.json()
                        print(f"✅ Proxy funcionando! IP detectado: {ip_info.get('origin', 'N/A')}")
                        return True
                except Exception as e2:
                    print(f"⚠️ Erro com HTTPS: {str(e2)}")
            
            print("❌ Proxy não está funcionando com nenhum protocolo")
            return False
                
        except Exception as e:
            print(f"❌ Erro geral ao testar proxy: {str(e)}")
            return False

    def ensure_logged_in(self):
