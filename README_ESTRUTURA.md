# 📁 Estrutura do Projeto Instagram Crawler

## 🗂️ Organização dos Arquivos

### 📂 Pasta `naunha/` (Pasta Principal)
Todos os arquivos principais do sistema estão organizados na pasta `naunha/`:

#### 🔧 Arquivos Principais
- **`InstaScraperV2.py`** - Classe principal do scraper com automação web
- **`main.py`** - Servidor Flask para scraping de artistas do Spotify (versão original)
- **`main_reels.py`** - Sistema principal para extração de reels do Instagram
- **`test_reels_web.py`** - Teste do sistema de reels

#### 📋 Outros Arquivos na Pasta `naunha/`
- `requirements.txt` - Dependências do projeto
- `user_manager.py` - Gerenciador de usuários
- `fix_chromedriver.py` - Utilitário para ChromeDriver
- `proxy_auth_extension.zip` - Extensão para autenticação de proxy
- `screenshots/` - Pasta com screenshots de debug
- Vários arquivos de teste e debug

### 📂 Pasta Raiz
- **`main.py`** - Execução principal para reels (chama o sistema da pasta naunha)
- **`test_reels_web.py`** - Teste do sistema (chama o sistema da pasta naunha)
- **`README_REELS_WEB.md`** - Documentação do sistema de reels
- **`README_ESTRUTURA.md`** - Este arquivo

## 🚀 Como Executar

### 1. Execução Principal (Reels)
```bash
# Na pasta raiz
python main.py
```

### 2. Execução com Menu Interativo
```bash
# Na pasta naunha
cd naunha
python main_reels.py
```

### 3. Teste do Sistema
```bash
# Na pasta raiz
python test_reels_web.py

# OU na pasta naunha
cd naunha
python test_reels_web.py
```

### 4. Servidor Flask (Spotify)
```bash
# Na pasta naunha
cd naunha
python main.py
```

## 📋 Sistemas Disponíveis

### 🎬 Sistema de Reels (Instagram)
- **Arquivo Principal**: `naunha/main_reels.py`
- **Classe**: `naunha/InstaScraperV2.py`
- **Funcionalidade**: Extração de reels usando automação web com login manual
- **Uso**: `python main.py` (pasta raiz) ou `python naunha/main_reels.py`

### 🎵 Sistema de Artistas (Spotify)
- **Arquivo Principal**: `naunha/main.py`
- **Classe**: `naunha/InstaScraperV2.py`
- **Funcionalidade**: Servidor Flask para scraping de artistas do Spotify
- **Uso**: `python naunha/main.py`

## 🔧 Configuração

### Dependências
```bash
# Instalar dependências
pip install -r naunha/requirements.txt
```

### Variáveis de Ambiente (Opcional)
```bash
export INSTAGRAM_USERNAME="seu_username"
export INSTAGRAM_PASSWORD="sua_senha"
```

## 📊 Fluxo de Execução

### Para Reels (Instagram):
1. Executa `main.py` na pasta raiz
2. Importa `naunha.InstaScraperV2`
3. Cria instância do `ScraperController`
4. Faz login manual no Instagram
5. Extrai reels do perfil especificado
6. Salva resultados em JSON

### Para Artistas (Spotify):
1. Executa `naunha/main.py`
2. Inicia servidor Flask na porta 8080
3. Endpoint `/scrape_artist` para requisições POST
4. Retorna dados do artista em JSON

## 🎯 Vantagens da Organização

✅ **Separação Clara**: Reels e Spotify em sistemas distintos
✅ **Reutilização**: Mesma classe `ScraperController` para ambos
✅ **Flexibilidade**: Execução de qualquer pasta
✅ **Manutenção**: Fácil de encontrar e modificar arquivos
✅ **Compatibilidade**: Mantém versão original do Spotify

## 📝 Notas Importantes

- O sistema de **reels** é o foco principal da implementação atual
- O sistema de **Spotify** mantém a funcionalidade original
- Ambos usam a mesma classe `ScraperController` mas com métodos diferentes
- A pasta `naunha/` contém todos os arquivos principais do projeto

