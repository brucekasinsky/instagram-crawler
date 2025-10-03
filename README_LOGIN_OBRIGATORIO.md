# Instagram Scraper - Login Único e Obrigatório

## ⚠️ IMPORTANTE: Login Único e Obrigatório

**A partir de agora, o Instagram exige login para acessar QUALQUER perfil, incluindo perfis públicos.**

**🔒 NOVIDADE: Sistema de Login Único implementado para evitar bloqueios!**

### 🔐 Mudanças Implementadas

1. **Login Único**: Faz login apenas UMA vez e reutiliza a sessão
2. **Sessão Persistente**: Evita múltiplos logins que causam bloqueios
3. **Captura Completa**: Nova função para capturar todos os dados em uma sessão
4. **Controle de Estado**: Sistema inteligente de controle de sessão
5. **Tratamento de Erros**: Melhor tratamento para perfis privados e erros de conexão

### 📝 Credenciais Configuradas

As seguintes credenciais estão configuradas no código:
- **Username**: `coralvelado2309`
- **Password**: `4&bfa&Eh8QFw`
- **Email**: `92qiez5o6d@temp-mail.org`

### 🚀 Como Usar

#### Exemplo Básico (Login Único)

```python
from naunha.InstaScraperV2 import ScraperController

# Criar instância
scraper = ScraperController()

# Capturar dados completos em uma sessão única
complete_data = scraper.get_creator_complete_data("username", max_reels=20)

# Finalizar sessão
scraper.quit_session()
```

#### Exemplo Completo (Múltiplas Operações)

```python
# 1. Criar scraper
scraper = ScraperController()

# 2. Login único (automático)
scraper.ensure_logged_in()

# 3. Capturar dados do perfil (reutiliza sessão)
profile = scraper.get_profile_data("instagram")

# 4. Capturar reels (reutiliza sessão)
reels = scraper.get_creator_reels_instaloader("instagram", max_count=10)

# 5. Capturar foto (reutiliza sessão)
photo_url = scraper.get_profile_photo("instagram")

# 6. Finalizar sessão
scraper.quit_session()
```

#### Exemplo Avançado (Múltiplos Usuários)

```python
scraper = ScraperController()

# Login único para todos
scraper.ensure_logged_in()

usuarios = ["instagram", "reels", "creators"]
for username in usuarios:
    # Cada operação reutiliza a mesma sessão
    complete_data = scraper.get_creator_complete_data(username, max_reels=5)
    print(f"@{username}: {complete_data['total_reels']} reels")

scraper.quit_session()
```

### 🔧 Funções Principais

#### `get_creator_complete_data(username, max_reels=20)` ⭐ **RECOMENDADA**
- **Login**: Único e automático
- **Retorna**: Dados completos (perfil + foto + reels + estatísticas)
- **Funciona**: Perfis públicos e privados (se você seguir)
- **Vantagem**: Captura tudo em uma sessão única

#### `get_profile_data(username)`
- **Login**: Reutiliza sessão ativa
- **Retorna**: Dados completos do perfil
- **Funciona**: Perfis públicos e privados (se você seguir)

#### `get_creator_reels_instaloader(username, max_count=50)`
- **Login**: Reutiliza sessão ativa
- **Retorna**: Lista de reels com dados completos
- **Funciona**: Perfis públicos e privados (se você seguir)

#### `ensure_logged_in()`
- **Função**: Garante que está logado (login único)
- **Retorna**: True/False se login foi bem-sucedido
- **Uso**: Para controle manual da sessão

#### `test_instagram_connection(username)`
- **Login**: Único e automático
- **Retorna**: True/False se conexão funcionou
- **Uso**: Testar se tudo está funcionando

### 📊 Dados Capturados dos Reels

```python
{
    'reel_id': 'ABC123',
    'reel_url': 'https://www.instagram.com/reel/ABC123/',
    'likes': 15000,
    'comments': 500,
    'views': 100000,
    'caption': 'Texto do reel...',
    'date': '2024-01-01T12:00:00',
    'video_url': 'https://...',
    'thumbnail_url': 'https://...',
    'duration': 30,
    'hashtags': ['hashtag1', 'hashtag2'],
    'mentions': ['@user1', '@user2'],
    'type': 'reel'
}
```

### 🧪 Scripts de Teste

#### `exemplo_uso.py`
- Exemplo básico de uso
- Demonstra captura de perfil e reels
- Tratamento de erros

#### `test_instagram_scraper.py`
- Teste completo do sistema
- Verifica login, perfil e reels
- Relatório detalhado

#### `test_reels_scraper.py`
- Teste específico para reels
- Testa múltiplos perfis
- Salva dados em JSON

### ⚡ Executar Testes

```bash
# Teste básico
python exemplo_uso.py

# Teste completo
python test_instagram_scraper.py

# Teste específico de reels
python test_reels_scraper.py
```

### 🔍 Tratamento de Erros

#### Perfil Privado
```python
# Se o perfil for privado e você não seguir
profile_data = scraper.get_profile_data("perfil_privado")
# Retorna None se não conseguir acessar
```

#### Credenciais Inválidas
```python
# Se as credenciais estiverem incorretas
# O scraper tentará fazer login e falhará
# Verifique as credenciais no código
```

#### Rate Limiting
```python
# O scraper tem delays automáticos
# Entre requests para evitar bloqueios
# Aguarde entre chamadas se necessário
```

### 🛠️ Configurações

#### Proxy
- Configurado automaticamente
- Usa proxy brasileiro (São Paulo)
- Funciona para Instaloader e Selenium

#### Delays
- 0.5s entre reels (Instaloader)
- 1-3s entre posts (Selenium)
- Delays aleatórios para parecer humano

### 📈 Vantagens do Novo Sistema

1. **Login Automático**: Não precisa gerenciar sessões
2. **Mais Confiável**: Instaloader é mais estável que Selenium
3. **Dados Completos**: Captura mais informações dos reels
4. **Melhor Performance**: Mais rápido e eficiente
5. **Tratamento de Erros**: Melhor handling de exceções

### ⚠️ Limitações

1. **Login Obrigatório**: Não funciona sem login
2. **Rate Limiting**: Instagram pode limitar requests
3. **Perfis Privados**: Precisa seguir para acessar
4. **Credenciais**: Depende das credenciais configuradas

### 🔄 Atualizações Futuras

- Suporte a 2FA (autenticação de dois fatores)
- Cache de sessão para evitar logins repetidos
- Suporte a múltiplas contas
- Melhor tratamento de rate limiting

---

**Nota**: Este sistema foi atualizado para funcionar com as novas políticas do Instagram que exigem login para todos os acessos.
