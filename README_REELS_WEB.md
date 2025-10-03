# 🎬 Sistema de Extração de Reels - Automação Web

Este sistema permite extrair reels do Instagram usando automação web com Selenium, fazendo login manual através da interface web.

## 🚀 Características

- ✅ **Login Manual**: Faça login manualmente no Instagram através do navegador
- ✅ **Automação Web**: Usa Selenium para navegar e extrair dados
- ✅ **Foco em Reels**: Especializado em extrair reels de perfis públicos
- ✅ **Dados Completos**: Extrai URLs, likes, comentários, thumbnails
- ✅ **Proxy Support**: Suporte a proxy configurado
- ✅ **Interface Amigável**: Sistema interativo e fácil de usar

## 📋 Pré-requisitos

### Instalação de Dependências

```bash
pip install -r requirements.txt
```

### Dependências Principais

- `selenium==4.15.0`
- `webdriver-manager==4.0.1`
- `requests`
- `beautifulsoup4`

### Chrome/Chromium

O sistema precisa do Chrome ou Chromium instalado. O WebDriver Manager baixa automaticamente o ChromeDriver.

## 🎯 Como Usar

### 1. Execução Simples

```bash
python main.py
```

### 2. Execução com Menu Interativo

```bash
python main_reels.py
```

### 3. Teste do Sistema

```bash
python test_reels_web.py
```

## 📝 Fluxo de Uso

### Passo 1: Login Manual
1. O sistema abre o navegador na página de login do Instagram
2. **Você faz login manualmente**:
   - Digite seu username
   - Digite sua senha
   - Complete qualquer verificação (2FA, etc.)
   - Pressione ENTER quando estiver logado

### Passo 2: Extração de Reels
1. Digite o nome do perfil do Instagram
2. Defina o número máximo de reels para extrair
3. O sistema navega para o perfil e clica na aba "Reels"
4. Extrai dados dos reels (URLs, likes, comentários, etc.)

### Passo 3: Resultados
1. Os dados são exibidos no terminal
2. Um arquivo JSON é salvo com todos os dados
3. O navegador é fechado automaticamente

## 📊 Dados Extraídos

Para cada reel, o sistema extrai:

- **ID do Reel**: Identificador único
- **URL**: Link direto para o reel
- **Likes**: Número de curtidas
- **Comentários**: Número de comentários
- **Thumbnail**: URL da imagem de preview
- **Timestamp**: Data/hora da extração

## 📁 Estrutura de Arquivos

```
instagram-crawler/
├── main.py                 # Execução principal simples
├── main_reels.py           # Execução com menu interativo
├── test_reels_web.py       # Arquivo de teste
├── naunha/
│   └── InstaScraperV2.py  # Classe principal do scraper
├── requirements.txt        # Dependências
└── README_REELS_WEB.md    # Este arquivo
```

## 🔧 Configuração

### Proxy (Opcional)

O sistema já vem configurado com proxy. Para desabilitar ou alterar, modifique a variável `PROXY_CONFIG` em `InstaScraperV2.py`.

### Credenciais (Opcional)

Você pode definir credenciais padrão através de variáveis de ambiente:

```bash
export INSTAGRAM_USERNAME="seu_username"
export INSTAGRAM_PASSWORD="sua_senha"
```

## 📋 Exemplo de Uso

```python
from naunha.InstaScraperV2 import ScraperController

# Criar instância
scraper = ScraperController()

# Fazer login manual
if scraper.manual_login_instagram():
    # Extrair reels
    result = scraper.scrapper_reels_web("nome_do_perfil", max_reels=20)
    
    if result['success'] == 1:
        print(f"Extraídos {result['data']['total_reels']} reels!")
        print(f"Total de likes: {result['data']['statistics']['total_likes']}")
    
    # Fechar navegador
    scraper.quit_session()
```

## 📊 Exemplo de Saída

```json
{
  "success": 1,
  "message": "Reels extraídos com sucesso",
  "data": {
    "profile": "nome_do_perfil",
    "total_reels": 15,
    "reels": [
      {
        "reel_id": "ABC123",
        "reel_url": "https://www.instagram.com/reel/ABC123/",
        "likes": 1250,
        "comments": 45,
        "views": 0,
        "thumbnail_url": "https://...",
        "caption": "",
        "type": "reel"
      }
    ],
    "statistics": {
      "total_likes": 18750,
      "total_comments": 675,
      "average_likes": 1250,
      "average_comments": 45
    },
    "extraction_timestamp": "2024-01-15T10:30:00"
  }
}
```

## ⚠️ Limitações

- **Perfis Privados**: Não funciona com perfis privados
- **Rate Limiting**: Instagram pode limitar requisições excessivas
- **Login Manual**: Requer intervenção manual para login
- **Navegador Visível**: O navegador fica visível durante a execução

## 🛠️ Solução de Problemas

### Chrome não encontrado
```bash
# Ubuntu/Debian
sudo apt-get install chromium-browser

# macOS
brew install chromium
```

### Erro de WebDriver
```bash
# Limpar cache do WebDriver Manager
rm -rf ~/.wdm
```

### Proxy não funcionando
- Verifique as credenciais do proxy
- Teste a conectividade: `python -c "from naunha.InstaScraperV2 import ScraperController; ScraperController().test_proxy_connection()"`

## 📞 Suporte

Para problemas ou dúvidas:
1. Verifique os logs de erro no terminal
2. Teste a conectividade do proxy
3. Verifique se o Chrome está instalado
4. Certifique-se de que está fazendo login corretamente

## 🔄 Atualizações

- **v1.0**: Sistema inicial com automação web
- **v1.1**: Adicionado suporte a proxy
- **v1.2**: Melhorada interface e tratamento de erros

