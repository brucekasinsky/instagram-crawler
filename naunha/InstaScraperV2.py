#!/usr/bin/env python3
"""
Scraper do Instagram usando automação web com Selenium
Versão 2.0 - Focado em reels com login manual
"""

import time
import requests
import os
import random
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

class ScraperController:
    """
    Controlador principal para scraping do Instagram
    """
    
    def __init__(self):
        """
        Inicializa o scraper com configurações padrão
        """
        # Configurações de proxy (desabilitadas para evitar problemas)
        self.PROXY_CONFIG = {
            'http': None,
            'https': None
        }
        
        # Credenciais do Instagram
        self.instagram_credentials = {
            'username': '',
            'password': ''
        }
        
        # Controle de sessão - login único
        self._is_logged_in = False
        self._login_attempted = False
        self.browser = None

    def manual_login_instagram(self, username=None, password=None):
        """
        Faz login manual no Instagram através da interface web
        Permite ao usuário inserir credenciais manualmente
        """
        try:
            print("🌐 Iniciando login manual no Instagram...")
            print("🔧 Preparando navegador para abrir...")
            
            # Usar credenciais fornecidas ou padrão
            if username and password:
                self.instagram_credentials['username'] = username
                self.instagram_credentials['password'] = password
            
            # Criar sessão do navegador se não existir
            if not hasattr(self, 'browser') or self.browser is None:
                print("🚀 Iniciando navegador Chrome...")
                print("⏳ Aguarde, o navegador está abrindo...")
                self.create_session(mobile=False)
                print("✅ Navegador iniciado com sucesso!")
            
            # Navegar para página de login
            print("📱 Navegando para página de login do Instagram...")
            print("🌐 URL: https://www.instagram.com/accounts/login/")
            self.browser.get('https://www.instagram.com/accounts/login/')
            time.sleep(5)  # Mais tempo para carregar
            
            print("\n" + "="*70)
            print("🔐 LOGIN MANUAL NO INSTAGRAM")
            print("="*70)
            print("📝 O navegador Chrome está aberto na página de login do Instagram.")
            print("👆 Por favor, faça login manualmente:")
            print("   1. Digite seu username do Instagram")
            print("   2. Digite sua senha")
            print("   3. Clique no botão 'Entrar'")
            print("   4. Complete qualquer verificação (2FA, captcha, etc.)")
            print("   5. Aguarde até estar logado no Instagram")
            print("   6. Navegue para qualquer página do Instagram")
            print("\n⏳ Aguardando você fazer login manual...")
            print("💡 Pressione ENTER quando estiver logado com sucesso...")
            print("="*70)
            
            # Aguardar input do usuário
            input("👆 Pressione ENTER após fazer login no navegador...")
            
            # Verificar se login foi bem-sucedido
            current_url = self.browser.current_url
            print(f"🔍 URL atual do navegador: {current_url}")
            
            if "instagram.com" in current_url and "login" not in current_url:
                print("✅ Login realizado com sucesso!")
                print("🎉 Você está logado no Instagram!")
                self._is_logged_in = True
                return True
            else:
                print("❌ Login não detectado automaticamente.")
                print("💡 Se você fez login, podemos continuar mesmo assim.")
                resposta = input("🤔 Deseja continuar? (s/n): ").lower()
                if resposta in ['s', 'sim', 'y', 'yes']:
                    print("✅ Continuando com o processo...")
                    self._is_logged_in = True
                    return True
                else:
                    print("❌ Login cancelado.")
                    return False
                
        except Exception as e:
            print(f"❌ Erro no login manual: {str(e)}")
            if "EOF" in str(e):
                print("⚠️ Input cancelado pelo usuário")
                return False
            elif "session deleted" in str(e) or "disconnected" in str(e) or "session not created" in str(e):
                print("⚠️ Sessão do navegador foi perdida")
                return False
            else:
                print("❌ Erro inesperado - não tentando reiniciar para evitar loop")
                return False

    def ensure_logged_in(self):
        """
        Garante que está logado (login único)
        """
        if not self._is_logged_in:
            return self.manual_login_instagram()
        return True

    def create_session(self, mobile=False):
        """
        Cria uma sessão do Selenium com configurações específicas para mobile ou web
        """
        print(f"Creating Session - Mode: {'Mobile' if mobile else 'Web'}")
        
        # Configurando opções do Chrome
        chrome_options = Options()
        
        # GARANTIR QUE O NAVEGADOR ABRA VISÍVEL
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--remote-debugging-port=9230")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Configurações para melhor visualização
        chrome_options.add_argument("--window-size=1280,720")
        chrome_options.add_argument("--start-maximized")
        
        # Configurações para garantir que o navegador funcione
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--ignore-ssl-errors')
        chrome_options.add_argument('--disable-web-security')
        chrome_options.add_argument('--allow-running-insecure-content')
        
        # Configurações para melhor compatibilidade
        chrome_options.add_argument('--disable-features=VizDisplayCompositor')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-plugins')
        
        print("🔧 Configurações do navegador aplicadas para visualização")
        
        # Configurações específicas para Mobile vs Web
        if mobile:
            print("📱 Configurando para modo MOBILE - Instagram App")
            mobile_emulation = {
                "deviceMetrics": {"width": 375, "height": 812, "pixelRatio": 3.0},
                "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"
            }
            chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
        else:
            print("💻 Configurando para modo WEB - Navegador Desktop")
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        
        print("Selenium configurado SEM proxy")
        
        try:
            # Instalar ChromeDriver automaticamente
            print("📦 Instalando ChromeDriver...")
            service = Service(ChromeDriverManager().install())
            print(f"ChromeDriver instalado em: {service.path}")
            
            # Criar driver
            print("🚀 Criando WebDriver...")
            self.browser = webdriver.Chrome(service=service, options=chrome_options)
            print("✅ WebDriver criado com sucesso!")
            
            # Configurar timeouts
            self.browser.set_page_load_timeout(30)
            self.browser.implicitly_wait(10)
            
            print("✅ Sessão do Selenium criada com sucesso!")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao criar sessão do Selenium: {str(e)}")
            return False

    def get_profile_reels_web(self, creator_slug, max_reels=20):
        """
        Extrai reels de um perfil usando automação web (baseado na estratégia de get_creator_posts)
        """
        # Imports já disponíveis globalmente
        
        try:
            print(f"🎬 Iniciando extração de reels para @{creator_slug}")
            
            # Garantir que está logado
            if not self.ensure_logged_in():
                print("❌ Não foi possível fazer login")
                return []
            
            # Tentar diferentes URLs para evitar detecção (igual ao get_creator_posts)
            urls_to_try = [
                f'https://instagram.com/{creator_slug}/',
                f'https://www.instagram.com/{creator_slug}/',
                f'https://instagram.com/{creator_slug}/?hl=pt',
                f'https://www.instagram.com/{creator_slug}/?hl=pt'
            ]
            
            success = False
            for url in urls_to_try:
                try:
                    print(f"Tentando URL: {url}")
                    self.browser.get(url)
                    time.sleep(3)
                    
                    # Verificar se não foi redirecionado para login
                    if "login" not in self.browser.current_url.lower():
                        print(f"✅ Sucesso com URL: {url}")
                        success = True
                        break
                    else:
                        print(f"❌ Redirecionado para login com: {url}")
                        
                except Exception as e:
                    print(f"❌ Erro com URL {url}: {str(e)}")
                    continue
            
            if not success:
                print("❌ Todas as URLs falharam - Instagram pode estar bloqueando")
                return []
            
            # Aguardar página carregar completamente
            print("🔍 Aguardando página carregar...")
            try:
                WebDriverWait(self.browser, 60).until(
                    EC.presence_of_element_located((By.TAG_NAME, 'main'))
                )
                print("✅ Página carregada com sucesso!")
            except Exception as e:
                print(f"⚠️ Timeout aguardando página carregar: {str(e)}")
                print("🔄 Continuando mesmo assim...")
            
            # Aguardar um pouco mais para garantir que os elementos carreguem
            delay = random.uniform(3, 7)
            print(f"Aguardando {delay:.1f}s para carregamento...")
            time.sleep(delay)
            
            # Procurar pela aba de reels e clicar
            print("🔍 Procurando pela aba de reels...")
            reels_clicked = False
            
            # Tentar diferentes seletores para encontrar a aba de reels
            reels_selectors = [
                "a[href*='/reels/']",
                "a[href*='/reel/']",
                "[data-testid='reels-tab']",
                "a[aria-label*='Reels']",
                "a[aria-label*='Reel']"
            ]
            
            for selector in reels_selectors:
                try:
                    reels_elements = self.browser.find_elements(By.CSS_SELECTOR, selector)
                    if reels_elements:
                        print(f"✅ Encontrou aba de reels com seletor: {selector}")
                        reels_elements[0].click()
                        reels_clicked = True
                        time.sleep(3)
                        break
                except Exception as e:
                    print(f"⚠️ Erro ao tentar clicar em reels com seletor {selector}: {str(e)}")
                    continue
            
            if not reels_clicked:
                print("⚠️ Não encontrou aba específica de reels, tentando scroll na página principal...")
            
            # Fazer scroll para carregar mais reels
            print("📜 Fazendo scroll para carregar reels...")
            for i in range(5):  # Mais scrolls para reels
                self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(random.uniform(2, 4))
            
            # Scroll de volta para o topo
            self.browser.execute_script("window.scrollTo(0, 0);")
            time.sleep(2)
            
            # Procurar por elementos de reels (usando a mesma estratégia de posts)
            print("🔍 Procurando por elementos de reels...")
            
            # Tentar diferentes seletores para encontrar reels
            reel_selectors = [
                'article div.x1lliihq',  # Mesmo seletor que funciona para posts
                'div[data-testid="reel-item"]',
                'article a[href*="/reel/"]',
                'div a[href*="/reel/"]',
                'article div[role="link"]',
                'div[data-testid="video-reel"]'
            ]
            
            reels_elements = []
            for selector in reel_selectors:
                try:
                    elements = self.browser.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        print(f"✅ Encontrados {len(elements)} elementos com seletor: {selector}")
                        reels_elements = elements
                        break
                except Exception as e:
                    print(f"⚠️ Erro com seletor {selector}: {str(e)}")
                    continue
            
            if len(reels_elements) == 0:
                # Se não encontrou reels, salvar screenshot para debug
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                screenshot_path = f"screenshots/no_reels_found_{creator_slug}_{timestamp}.png"
                os.makedirs("screenshots", exist_ok=True)
                self.browser.save_screenshot(screenshot_path)
                print(f"📸 Screenshot salvo: {screenshot_path}")
                print("🔍 Não foram encontrados elementos de reels. Verifique o screenshot.")
                return []
            
            print(f"📊 Encontrados {len(reels_elements)} elementos de reels")
            
            reels_data = []
            
            for i, reel_element in enumerate(reels_elements):
                if i >= max_reels:
                    break
                    
                try:
                    print(f"🎬 Processando reel {i+1}/{min(len(reels_elements), max_reels)}")
                    
                    # Dados básicos do reel
                    reel_data = {
                        'reel_id': '',
                        'reel_url': '',
                        'likes': 0,
                        'comments': 0,
                        'views': 0,
                        'thumbnail_url': '',
                        'caption': '',
                        'type': 'reel',
                        'screenshot_path': ''
                    }
                    
                    # 1. Pegar URL do reel
                    try:
                        # Procurar por link dentro do elemento
                        link_element = reel_element.find_element(By.TAG_NAME, 'a')
                        reel_data['reel_url'] = link_element.get_attribute('href')
                        
                        # Extrair ID do reel da URL
                        if '/reel/' in reel_data['reel_url']:
                            reel_data['reel_id'] = reel_data['reel_url'].split('/reel/')[-1].rstrip('/')
                        elif '/p/' in reel_data['reel_url']:
                            reel_data['reel_id'] = reel_data['reel_url'].split('/p/')[-1].rstrip('/')
                            
                    except Exception as e:
                        print(f"⚠️ Não foi possível obter URL do reel {i+1}: {str(e)}")
                    
                    # 2. Pegar thumbnail (imagem do reel)
                    try:
                        img_element = reel_element.find_element(By.TAG_NAME, 'img')
                        reel_data['thumbnail_url'] = img_element.get_attribute('src')
                        reel_data['caption'] = img_element.get_attribute('alt')
                        
                    except Exception as e:
                        print(f"⚠️ Não foi possível obter thumbnail do reel {i+1}: {str(e)}")
                    
                    # 3. Hover no reel para mostrar likes e comments (igual ao get_creator_posts)
                    try:
                        # Fazer hover no reel
                        self.browser.execute_script("arguments[0].scrollIntoView(true);", reel_element)
                        time.sleep(0.5)
                        
                        # Simular hover
                        from selenium.webdriver.common.action_chains import ActionChains
                        actions = ActionChains(self.browser)
                        actions.move_to_element(reel_element).perform()
                        time.sleep(1)
                        
                        # Capturar screenshot do reel em hover
                        screenshot_path = self._take_screenshot(reel_element, creator_slug, i, 'reel')
                        if screenshot_path:
                            reel_data['screenshot_path'] = screenshot_path
                        
                        # Procurar pelos spans com métricas (mesma estratégia de posts)
                        try:
                            # Aguardar um pouco para o hover effect aparecer
                            time.sleep(0.5)
                            
                            # Tentar múltiplos seletores para capturar likes e comentários
                            hover_elements = []
                            
                            # Seletor 1: Baseado na estrutura real do HTML
                            selector1 = 'ul.x6s0dn4 li span.html-span'
                            elements1 = self.browser.find_elements(By.CSS_SELECTOR, selector1)
                            if elements1:
                                hover_elements = elements1
                                print(f"Found {len(elements1)} elements with selector1")
                            
                            # Seletor 2: Seletor mais genérico como fallback
                            if not hover_elements:
                                selector2 = 'ul li span[class*="html-span"]'
                                elements2 = self.browser.find_elements(By.CSS_SELECTOR, selector2)
                                if elements2:
                                    hover_elements = elements2
                                    print(f"Found {len(elements2)} elements with selector2")
                            
                            # Seletor 3: Seletor original como último recurso
                            if not hover_elements:
                                selector3 = 'ul li span.htmlspan'
                                elements3 = self.browser.find_elements(By.CSS_SELECTOR, selector3)
                                if elements3:
                                    hover_elements = elements3
                                    print(f"Found {len(elements3)} elements with selector3")
                            
                            # Seletor 4: Procurar por spans com texto numérico dentro de ul
                            if not hover_elements:
                                selector4 = 'ul li span'
                                all_spans = self.browser.find_elements(By.CSS_SELECTOR, selector4)
                                hover_elements = [span for span in all_spans if span.text.strip().isdigit()]
                                print(f"Found {len(hover_elements)} numeric spans with selector4")
                            
                            if len(hover_elements) >= 2:
                                # Primeiro span = likes, segundo span = comments
                                likes_text = hover_elements[0].text.strip()
                                comments_text = hover_elements[1].text.strip()
                                
                                print(f"Raw text - Likes: '{likes_text}', Comments: '{comments_text}'")
                                
                                # Converter texto para número
                                reel_data['likes'] = self._parse_count(likes_text)
                                reel_data['comments'] = self._parse_count(comments_text)
                                
                                print(f"✅ Reel {i+1}: {reel_data['likes']} likes, {reel_data['comments']} comments")
                            else:
                                print(f"⚠️ Could not find likes/comments for reel {i+1}. Found {len(hover_elements)} elements")
                                # Debug: imprimir todos os elementos encontrados
                                for idx, elem in enumerate(hover_elements):
                                    print(f"Element {idx}: text='{elem.text}', tag='{elem.tag_name}', classes='{elem.get_attribute('class')}'")
                                
                        except Exception as e:
                            print(f"⚠️ Error getting likes/comments for reel {i+1}: {str(e)}")
                    
                    except Exception as e:
                        print(f"⚠️ Error hovering on reel {i+1}: {str(e)}")
                    
                    reels_data.append(reel_data)
                    
                    # Delay aleatório entre reels para parecer mais humano
                    if i < len(reels_elements) - 1:  # Não esperar após o último reel
                        delay = random.uniform(1, 3)
                        print(f"Aguardando {delay:.1f}s antes do próximo reel...")
                        time.sleep(delay)
                    
                except Exception as e:
                    print(f"❌ Error processing reel {i+1}: {str(e)}")
                    continue
            
            print(f"🎉 Successfully extracted data from {len(reels_data)} reels")
            return reels_data
            
        except Exception as e:
            print(f"❌ Error getting creator reels: {str(e)}")
            return []

    def _take_screenshot(self, element, creator_slug, index, type_name='post'):
        """
        Captura screenshot de um elemento específico
        """
        try:
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"screenshots/{type_name}_{creator_slug}_{index}_{timestamp}.png"
            
            os.makedirs("screenshots", exist_ok=True)
            
            # Capturar screenshot do elemento
            element.screenshot(screenshot_path)
            print(f"📸 Screenshot salvo: {screenshot_path}")
            
            return screenshot_path
            
        except Exception as e:
            print(f"⚠️ Erro ao capturar screenshot: {str(e)}")
            return None

    def _parse_count(self, count_text):
        """
        Converte texto de contagem (ex: '1.2K', '500') para número
        """
        try:
            count_text = count_text.replace(',', '').replace('.', '')
            if 'K' in count_text.upper():
                return int(float(count_text.upper().replace('K', '')) * 1000)
            elif 'M' in count_text.upper():
                return int(float(count_text.upper().replace('M', '')) * 1000000)
            else:
                return int(count_text)
        except:
            return 0

    def scrapper_reels_web(self, profile_name, max_reels=20):
        """
        Scraper simplificado para reels usando automação web
        """
        try:
            print(f"🎬 Iniciando scraper de reels para @{profile_name}")
            
            # Extrair reels
            reels_data = self.get_profile_reels_web(profile_name, max_reels)
            
            if not reels_data:
                return {
                    'success': 0,
                    'message': 'Nenhum reel encontrado ou erro na extração',
                    'data': {
                        'profile': profile_name,
                        'total_reels': 0,
                        'reels': [],
                        'statistics': {
                            'total_likes': 0,
                            'total_comments': 0,
                            'average_likes': 0,
                            'average_comments': 0
                        }
                    }
                }
            
            # Calcular estatísticas
            total_likes = sum(reel.get('likes', 0) for reel in reels_data)
            total_comments = sum(reel.get('comments', 0) for reel in reels_data)
            total_reels = len(reels_data)
            
            statistics = {
                'total_likes': total_likes,
                'total_comments': total_comments,
                'average_likes': total_likes // total_reels if total_reels > 0 else 0,
                'average_comments': total_comments // total_reels if total_reels > 0 else 0
            }
            
            return {
                'success': 1,
                'message': f'Reels extraídos com sucesso para @{profile_name}',
                'data': {
                    'profile': profile_name,
                    'total_reels': total_reels,
                    'reels': reels_data,
                    'statistics': statistics
                }
            }
            
        except Exception as e:
            return {
                'success': 0,
                'message': f'Erro na extração: {str(e)}',
                'data': {
                    'profile': profile_name,
                    'total_reels': 0,
                    'reels': [],
                    'statistics': {
                        'total_likes': 0,
                        'total_comments': 0,
                        'average_likes': 0,
                        'average_comments': 0
                    }
                }
            }

    def test_proxy_connection(self):
        """
        Testa a conectividade do proxy fazendo uma requisição simples
        """
        try:
            print("🌐 Testando conectividade do proxy...")
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

    def quit_session(self):
        """
        Fecha a sessão do navegador
        """
        try:
            if hasattr(self, 'browser') and self.browser:
                print("🔒 Fechando navegador...")
                self.browser.quit()
                print("✅ Browser fechado com sucesso.")
                self.browser = None
            else:
                print("ℹ️ Browser não foi inicializado ou já foi fechado.")
        except Exception as e:
            print(f"⚠️ Erro ao fechar browser: {str(e)}")
        
        print("🔒 Sessão de login finalizada.")

    def get_profile_photo_web(self, creator_slug):
        """
        Obtém a foto de perfil do usuário usando automação web
        
        Args:
            creator_slug (str): Nome de usuário do Instagram
        
        Returns:
            str: URL da foto de perfil ou None se não encontrada
        """
        try:
            print(f"📸 Obtendo foto de perfil para @{creator_slug}...")
            
            # Garantir que está logado
            if not self.ensure_logged_in():
                print("❌ Falha no login")
                return None
            
            # Navegar para o perfil
            profile_url = f"https://www.instagram.com/{creator_slug}/"
            self.browser.get(profile_url)
            time.sleep(3)
            
            # Procurar pela foto de perfil
            try:
                profile_img = self.browser.find_element(By.CSS_SELECTOR, 'header img[alt*="@' + creator_slug + '"]')
                profile_pic_url = profile_img.get_attribute('src')
                print(f"✅ Foto de perfil encontrada: {profile_pic_url}")
                return profile_pic_url
            except:
                print("⚠️ Foto de perfil não encontrada")
                return None
                
        except Exception as e:
            print(f"❌ Erro ao obter foto de perfil: {str(e)}")
            return None
    
    def download_profile_photo(self, creator_slug, save_path="./", size=350):
        """
        Baixa a foto de perfil do usuário
        
        Args:
            creator_slug (str): Nome de usuário do Instagram
            save_path (str): Caminho para salvar a imagem
            size (int): Tamanho desejado da imagem
        
        Returns:
            str: Caminho do arquivo salvo ou None se falhou
        """
        try:
            print(f"Downloading profile photo for {creator_slug}...")
            
            # Garantir que está logado (sessão única)
            if not self.ensure_logged_in():
                print("❌ Falha no login, não é possível acessar perfil")
                return None
            
            # Função desabilitada - usando automação web
            print("⚠️ Função de download com instaloader desabilitada")
            print("💡 Use get_profile_photo_web() para obter URL da foto")
            return None
            
            # O Instaloader salva na pasta com o nome do usuário
            profile_folder = os.path.join(save_path, creator_slug)
            if os.path.exists(profile_folder):
                # Procurar pelo arquivo da foto de perfil
                for file in os.listdir(profile_folder):
                    if file.endswith('.jpg') and 'profile_pic' in file:
                        file_path = os.path.join(profile_folder, file)
                        print(f"Profile photo saved to: {file_path}")
                        return file_path
            
            print("Profile photo download completed")
            return None
            
        except Exception as e:
            print(f"Error downloading profile photo: {str(e)}")
            return None

    def get_profile_data_web(self, creator_slug):
        """
        Extrai dados básicos do perfil usando automação web
        
        Args:
            creator_slug (str): Nome de usuário do Instagram
        
        Returns:
            dict: Dados básicos do perfil ou None se falhou
        """
        try:
            print(f"📊 Obtendo dados do perfil @{creator_slug}...")
            
            # Garantir que está logado
            if not self.ensure_logged_in():
                print("❌ Falha no login")
                return None
            
            # Navegar para o perfil
            profile_url = f"https://www.instagram.com/{creator_slug}/"
            self.browser.get(profile_url)
            time.sleep(5)
            
            # Verificar se o perfil existe
            if "Page Not Found" in self.browser.page_source:
                print(f"❌ Perfil @{creator_slug} não encontrado")
                return None
            
            # Extrair dados básicos do perfil
            profile_data = {
                'username': creator_slug,
                'full_name': '',
                'description': '',
                'website': '',
                'followers': 0,
                'following': 0,
                'uploads': 0,
                'profile_picture_url': '',
                'is_private': 0,
                'is_verified': 0
            }
            
            try:
                # Nome completo
                full_name_elem = self.browser.find_element(By.CSS_SELECTOR, 'header h2')
                profile_data['full_name'] = full_name_elem.text
            except:
                pass
            
            try:
                # Descrição/bio
                bio_elem = self.browser.find_element(By.CSS_SELECTOR, 'header div[data-testid="user-bio"]')
                profile_data['description'] = bio_elem.text
            except:
                pass
            
            try:
                # Contadores de seguidores, seguindo, posts
                counters = self.browser.find_elements(By.CSS_SELECTOR, 'header section ul li')
                if len(counters) >= 3:
                    profile_data['uploads'] = self._parse_count(counters[0].text)
                    profile_data['followers'] = self._parse_count(counters[1].text)
                    profile_data['following'] = self._parse_count(counters[2].text)
            except:
                pass
            
            print(f"✅ Dados do perfil extraídos: {profile_data['followers']} seguidores, {profile_data['uploads']} posts")
            
            return profile_data
            
        except Exception as e:
            print(f"❌ Erro ao obter dados do perfil: {str(e)}")
            return None

    def get_creator_posts(self, creator_slug):
        """
        Extrai dados dos posts do Instagram usando Selenium
        
        Args:
            creator_slug (str): Nome de usuário do Instagram
        
        Returns:
            list: Lista de dicionários com dados dos posts ou None se falhou
        """
        print("Loading Creator's Page...")
        
        import time
        import random
        
        # Tentar diferentes URLs para evitar detecção
        urls_to_try = [
            f'https://instagram.com/{creator_slug}/',
            f'https://www.instagram.com/{creator_slug}/',
            f'https://instagram.com/{creator_slug}/?hl=pt',
            f'https://www.instagram.com/{creator_slug}/?hl=pt'
        ]
        
        success = False
        for url in urls_to_try:
            try:
                print(f"Tentando URL: {url}")
                self.browser.get(url)
                time.sleep(3)
                
                # Verificar se não foi redirecionado para login
                if "login" not in self.browser.current_url.lower():
                    print(f"✅ Sucesso com URL: {url}")
                    success = True
                    break
                else:
                    print(f"❌ Redirecionado para login com: {url}")
                    
            except Exception as e:
                print(f"❌ Erro com URL {url}: {str(e)}")
                continue
        
        if not success:
            print("❌ Todas as URLs falharam - Instagram pode estar bloqueando")
            return []
            
        print('Getting posts...')
        
        try:
            # Aguardar 60 segundos para dar tempo de inserir credenciais do proxy
            print("⏳ Aguardando 60 segundos para inserir credenciais do proxy...")
            print("📝 Insira as credenciais no modal do Chrome:")
            print("   Usuário: juicyspace69")
            print("   Senha: aCQs0w0Qjbj9l9Umex")
            time.sleep(60)
            
            # Aguardar até que a página carregue completamente
            print("🔍 Aguardando página carregar...")
            try:
                WebDriverWait(self.browser, 60).until(
                    EC.presence_of_element_located((By.TAG_NAME, 'main'))
                )
                print("✅ Página carregada com sucesso!")
            except Exception as e:
                print(f"⚠️ Timeout aguardando página carregar: {str(e)}")
                print("🔄 Continuando mesmo assim...")
            
            # Aguardar um pouco mais para garantir que os posts carreguem
            # Delay aleatório entre 3-7 segundos para parecer mais humano
            delay = random.uniform(3, 7)
            print(f"Aguardando {delay:.1f}s para carregamento...")
            time.sleep(delay)
            
            # Fazer scroll suave para carregar mais posts
            print("Fazendo scroll para carregar posts...")
            for i in range(3):
                self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(random.uniform(2, 4))
            
            # Scroll de volta para o topo
            self.browser.execute_script("window.scrollTo(0, 0);")
            time.sleep(2)
            
            # Encontrar todos os posts (divs com classe x1lliihq)
            posts = self.browser.find_elements(By.CSS_SELECTOR, 'article div.x1lliihq')
            print(f"Found {len(posts)} posts")
            
            # Se não encontrou posts, salvar screenshot para debug
            if len(posts) == 0:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                screenshot_path = f"screenshots/no_posts_found_{creator_slug}_{timestamp}.png"
                os.makedirs("screenshots", exist_ok=True)
                self.browser.save_screenshot(screenshot_path)
                print(f"📸 Screenshot salvo: {screenshot_path}")
            
            posts_data = []
            
            for i, post in enumerate(posts):
                try:
                    print(f"Processing post {i+1}/{len(posts)}")
                    
                    # Dados básicos do post
                    post_data = {
                        'post_url': '',
                        'image_src': '',
                        'image_alt': '',
                        'post_text': '',
                        'likes': 0,
                        'comments': 0,
                        'tags': [],
                        'hashtags': [],
                        'image_description': '',
                        'screenshot_path': ''
                    }
                    
                    # 1. Pegar URL do post (href do link 'a')
                    try:
                        link_element = post.find_element(By.TAG_NAME, 'a')
                        post_data['post_url'] = link_element.get_attribute('href')
                    except:
                        print(f"Could not find post URL for post {i+1}")
                    
                    # 2. Pegar imagem (src e alt do img) e extrair tags/hashtags
                    try:
                        img_element = post.find_element(By.TAG_NAME, 'img')
                        post_data['image_src'] = img_element.get_attribute('src')
                        post_data['image_alt'] = img_element.get_attribute('alt')
                        
                        # Extrair tags e hashtags do alt text
                        alt_parsed = self._parse_alt_text(post_data['image_alt'])
                        post_data['tags'] = alt_parsed['tags']
                        post_data['hashtags'] = alt_parsed['hashtags']
                        post_data['image_description'] = alt_parsed['description']
                        
                        if post_data['tags'] or post_data['hashtags']:
                            print(f"Post {i+1}: Found {len(post_data['tags'])} tags and {len(post_data['hashtags'])} hashtags")
                            
                    except:
                        print(f"Could not find image for post {i+1}")
                    
                    # 3. Pegar texto do post (h2->span)
                    try:
                        h2_element = post.find_element(By.TAG_NAME, 'h2')
                        span_element = h2_element.find_element(By.TAG_NAME, 'span')
                        post_data['post_text'] = span_element.text
                    except:
                        print(f"Could not find post text for post {i+1}")
                    
                    # 4. Hover no post para mostrar likes e comments e capturar screenshot
                    try:
                        # Fazer hover no post
                        self.browser.execute_script("arguments[0].scrollIntoView(true);", post)
                        time.sleep(0.5)
                        
                        # Simular hover
                        from selenium.webdriver.common.action_chains import ActionChains
                        actions = ActionChains(self.browser)
                        actions.move_to_element(post).perform()
                        time.sleep(1)
                        
                        # Capturar screenshot do post em hover
                        screenshot_path = self._take_screenshot(post, creator_slug, i)
                        if screenshot_path:
                            post_data['screenshot_path'] = screenshot_path
                        
                        # Procurar pelos spans com classe 'htmlspan' dentro de ul->li
                        try:
                            # Aguardar um pouco para o hover effect aparecer
                            time.sleep(0.5)
                            
                            # Tentar múltiplos seletores para capturar likes e comentários
                            hover_elements = []
                            
                            # Seletor 1: Baseado na estrutura real do HTML fornecido
                            selector1 = 'ul.x6s0dn4 li span.html-span'
                            elements1 = self.browser.find_elements(By.CSS_SELECTOR, selector1)
                            if elements1:
                                hover_elements = elements1
                                print(f"Found {len(elements1)} elements with selector1")
                            
                            # Seletor 2: Seletor mais genérico como fallback
                            if not hover_elements:
                                selector2 = 'ul li span[class*="html-span"]'
                                elements2 = self.browser.find_elements(By.CSS_SELECTOR, selector2)
                                if elements2:
                                    hover_elements = elements2
                                    print(f"Found {len(elements2)} elements with selector2")
                            
                            # Seletor 3: Seletor original como último recurso
                            if not hover_elements:
                                selector3 = 'ul li span.htmlspan'
                                elements3 = self.browser.find_elements(By.CSS_SELECTOR, selector3)
                                if elements3:
                                    hover_elements = elements3
                                    print(f"Found {len(elements3)} elements with selector3")
                            
                            # Seletor 4: Procurar por spans com texto numérico dentro de ul
                            if not hover_elements:
                                selector4 = 'ul li span'
                                all_spans = self.browser.find_elements(By.CSS_SELECTOR, selector4)
                                hover_elements = [span for span in all_spans if span.text.strip().isdigit()]
                                print(f"Found {len(hover_elements)} numeric spans with selector4")
                            
                            if len(hover_elements) >= 2:
                                # Primeiro span = likes, segundo span = comments
                                likes_text = hover_elements[0].text.strip()
                                comments_text = hover_elements[1].text.strip()
                                
                                print(f"Raw text - Likes: '{likes_text}', Comments: '{comments_text}'")
                                
                                # Converter texto para número
                                post_data['likes'] = self._parse_count(likes_text)
                                post_data['comments'] = self._parse_count(comments_text)
                                
                                print(f"Post {i+1}: {post_data['likes']} likes, {post_data['comments']} comments")
                            else:
                                print(f"Could not find likes/comments for post {i+1}. Found {len(hover_elements)} elements")
                                # Debug: imprimir todos os elementos encontrados
                                for idx, elem in enumerate(hover_elements):
                                    print(f"Element {idx}: text='{elem.text}', tag='{elem.tag_name}', classes='{elem.get_attribute('class')}'")
                                
                        except Exception as e:
                            print(f"Error getting likes/comments for post {i+1}: {str(e)}")
                    
                    except Exception as e:
                        print(f"Error hovering on post {i+1}: {str(e)}")
                    
                    posts_data.append(post_data)
                    
                    # Delay aleatório entre posts para parecer mais humano
                    if i < len(posts) - 1:  # Não esperar após o último post
                        delay = random.uniform(1, 3)
                        print(f"Aguardando {delay:.1f}s antes do próximo post...")
                        time.sleep(delay)
                    
                except Exception as e:
                    print(f"Error processing post {i+1}: {str(e)}")
                    continue
            
            print(f"Successfully extracted data from {len(posts_data)} posts")
            return posts_data
            
        except Exception as e:
            print(f"Error getting creator posts: {str(e)}")
            return None