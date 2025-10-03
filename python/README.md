# Instagram Scraper - Python Version

Este projeto é uma versão Python do `indexdados.php`, desenvolvida para fazer scraping de dados do Instagram usando as melhores práticas de 2025.

## 🚀 Funcionalidades

- ✅ **Scraping de Perfis**: Coleta dados completos de perfis do Instagram
- ✅ **Análise de Métricas**: Calcula engagement rate, likes, comentários, etc.
- ✅ **Suporte a Reels**: Analisa métricas de reels e vídeos
- ✅ **Rotação de Proxies**: Suporte a proxies para evitar bloqueios
- ✅ **User-Agent Rotation**: Rotação de User-Agents atualizados (2024/2025)
- ✅ **Sistema de Retry**: Múltiplas tentativas com diferentes usuários
- ✅ **Logging Avançado**: Sistema completo de logs e tratamento de erros
- ✅ **Download de Imagens**: Download automático de fotos de perfil

## 📋 Pré-requisitos

- Python 3.8+
- pip (gerenciador de pacotes Python)

## 🛠️ Instalação

1. **Clone ou baixe o projeto**
2. **Navegue até a pasta python**:
   ```bash
   cd python
   ```

3. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

## ⚙️ Configuração

### 1. Configurar Proxies
Edite o arquivo `config.py` e atualize as configurações de proxy:

```python
PROXY_CONFIG = {
    'http': 'http://seu-usuario:senha@proxy-server:porta',
    'https': 'https://seu-usuario:senha@proxy-server:porta'
}
```

### 2. Configurar Usuários Fake
Atualize a lista de usuários fake no `config.py`:

```python
FAKE_USERS = [
    ['usuario1', 'senha1'],
    ['usuario2', 'senha2'],
    ['usuario3', 'senha3']
]
```

### 3. Configurar Diretórios
Verifique se os diretórios estão corretos no `config.py`:

```python
PATHS = {
    'cache_dir': '../cache/instagram',
    'temp_images': '../assets/tempprofileimg',
    'error_logs': '../assets/error_logs',
    'output_dir': '../assets/python_output'
}
```

## 🎯 Como Usar

### 1. Execução Básica
```bash
python main.py
```

### 2. Execução com Usuário Específico
Edite o arquivo `main.py` e altere:
```python
json_input = '{"instagramuser":"nome_do_usuario"}'
```

### 3. Execução Programática
```python
from instagram_scraper import InstagramScraper

scraper = InstagramScraper()
result = scraper.scrape_user("felipeneto")
print(json.dumps(result, indent=2))
```

## 📊 Estrutura de Dados Retornados

```json
{
  "success": 1,
  "message": "dados recebidos com sucesso",
  "data": {
    "instagram": "{\"username\":\"felipeneto\",\"followers\":1000000,...}",
    "details": "{\"total_likes\":50000,\"average_engagement_rate\":3.5,...}",
    "image": "assets/tempprofileimg/Juicy_felipeneto.jpg"
  }
}
```

## 🔧 Configurações Avançadas

### User-Agents Atualizados (2024/2025)
- Chrome 136.0.0.0
- Firefox 138.0
- Safari 18.5
- Edge 136.0.0.0
- Instagram App 320.0.0.32.90

### Configurações de Request
```python
REQUEST_SETTINGS = {
    'timeout': 60,
    'connect_timeout': 30,
    'max_retries': 3,
    'retry_delay': (3, 7),  # 3-7 segundos
    'request_delay': (2, 5)  # 2-5 segundos
}
```

### Configurações do Instagram
```python
INSTAGRAM_SETTINGS = {
    'min_followers': 1000,
    'max_posts_analyze': 20,
    'max_reels_analyze': 10,
    'cache_duration': 3600,  # 1 hora
    'session_duration': 3600  # 1 hora
}
```

## 📁 Estrutura de Arquivos

```
python/
├── config.py              # Configurações
├── instagram_scraper.py   # Classe principal do scraper
├── main.py               # Ponto de entrada principal
├── requirements.txt      # Dependências Python
└── README.md            # Este arquivo
```

## 🚨 Tratamento de Erros

O sistema inclui tratamento robusto de erros:

- **Rate Limiting**: Detecção e retry automático
- **Login Errors**: Rotação automática de usuários
- **Proxy Errors**: Logs detalhados de problemas de proxy
- **Network Errors**: Retry com delays aleatórios

## 📝 Logs

Os logs são salvos em:
- `../assets/error_logs/instagram_scraper_YYYY-MM-DD.log`
- `../assets/error_logs/instagram_error_YYYY-MM-DD_HH-MM-SS.json`

## ⚠️ Considerações Legais

- Respeite os Termos de Serviço do Instagram
- Use delays apropriados entre requests
- Implemente rate limiting
- Considere usar proxies de qualidade
- Monitore o uso para evitar bloqueios

## 🔄 Diferenças do PHP

### Melhorias Implementadas:
- ✅ **Melhor tratamento de erros**
- ✅ **Logging mais detalhado**
- ✅ **User-Agents mais recentes**
- ✅ **Sistema de retry mais robusto**
- ✅ **Configuração mais flexível**
- ✅ **Código mais modular e reutilizável**

### Funcionalidades Mantidas:
- ✅ **Mesma estrutura de dados de saída**
- ✅ **Mesma lógica de análise de métricas**
- ✅ **Mesmo sistema de usuários fake**
- ✅ **Mesma configuração de proxy**
- ✅ **Mesma validação de perfis**

## 🆘 Troubleshooting

### Erro de Login
- Verifique se os usuários fake estão corretos
- Confirme se o proxy está funcionando
- Verifique se não há 2FA ativado

### Erro de Proxy
- Teste a conectividade do proxy
- Verifique as credenciais
- Confirme se o proxy suporta HTTPS

### Rate Limiting
- Aumente os delays entre requests
- Use proxies de melhor qualidade
- Reduza a frequência de requests

## 📞 Suporte

Para problemas ou dúvidas:
1. Verifique os logs de erro
2. Confirme as configurações
3. Teste com um usuário diferente
4. Verifique a conectividade de rede
