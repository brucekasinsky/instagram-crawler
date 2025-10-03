import json
import os
import smtplib
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart
from datetime import datetime
import random
import time

class UserManager:
    def __init__(self, users_file="users.json", email_config=None):
        """
        Gerenciador de usuários para Instagram
        
        Args:
            users_file (str): Caminho para arquivo de usuários
            email_config (dict): Configuração de email para notificações
        """
        self.users_file = users_file
        self.email_config = email_config or {}
        self.load_users()
    
    def load_users(self):
        """Carrega usuários do arquivo JSON"""
        try:
            if os.path.exists(self.users_file):
                with open(self.users_file, 'r', encoding='utf-8') as f:
                    self.users = json.load(f)
            else:
                self.users = {
                    "active_users": [],
                    "blocked_users": [],
                    "failed_logins": []
                }
                self.save_users()
        except Exception as e:
            print(f"Erro ao carregar usuários: {e}")
            self.users = {
                "active_users": [],
                "blocked_users": [],
                "failed_logins": []
            }
    
    def save_users(self):
        """Salva usuários no arquivo JSON"""
        try:
            with open(self.users_file, 'w', encoding='utf-8') as f:
                json.dump(self.users, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Erro ao salvar usuários: {e}")
    
    def add_user(self, username, password, email=None, notes=""):
        """
        Adiciona um novo usuário ativo
        
        Args:
            username (str): Nome de usuário do Instagram
            password (str): Senha do Instagram
            email (str): Email do usuário (opcional)
            notes (str): Notas sobre o usuário
        """
        user = {
            "username": username,
            "password": password,
            "email": email,
            "notes": notes,
            "added_date": datetime.now().isoformat(),
            "last_used": None,
            "status": "active",
            "login_attempts": 0,
            "successful_logins": 0
        }
        
        # Verificar se usuário já existe
        for existing_user in self.users["active_users"]:
            if existing_user["username"] == username:
                print(f"Usuário {username} já existe!")
                return False
        
        self.users["active_users"].append(user)
        self.save_users()
        print(f"Usuário {username} adicionado com sucesso!")
        return True
    
    def get_active_user(self):
        """
        Retorna um usuário ativo aleatório
        
        Returns:
            dict: Dados do usuário ou None se não houver usuários ativos
        """
        if not self.users["active_users"]:
            print("Nenhum usuário ativo disponível!")
            return None
        
        # Filtrar apenas usuários ativos
        active_users = [u for u in self.users["active_users"] if u["status"] == "active"]
        
        if not active_users:
            print("Nenhum usuário ativo disponível!")
            return None
        
        # Selecionar usuário aleatório
        user = random.choice(active_users)
        
        # Atualizar último uso
        user["last_used"] = datetime.now().isoformat()
        self.save_users()
        
        return user
    
    def mark_login_failed(self, username, error_message="Wrong login / password"):
        """
        Marca um login como falhado e move para lista de bloqueados se necessário
        
        Args:
            username (str): Nome de usuário que falhou
            error_message (str): Mensagem de erro
        """
        # Encontrar usuário na lista ativa
        user_found = False
        for user in self.users["active_users"]:
            if user["username"] == username:
                user["login_attempts"] += 1
                user_found = True
                
                # Se falhou 3 vezes, mover para bloqueados
                if user["login_attempts"] >= 3:
                    user["status"] = "blocked"
                    user["blocked_date"] = datetime.now().isoformat()
                    user["block_reason"] = error_message
                    
                    # Mover para lista de bloqueados
                    self.users["blocked_users"].append(user)
                    self.users["active_users"].remove(user)
                    
                    print(f"⚠️ Usuário {username} bloqueado após 3 tentativas falhadas!")
                    
                    # Enviar email de notificação
                    self.send_blocked_user_notification(user, error_message)
                else:
                    print(f"⚠️ Login falhado para {username} (tentativa {user['login_attempts']}/3)")
                
                break
        
        if not user_found:
            print(f"Usuário {username} não encontrado na lista ativa!")
        
        # Adicionar à lista de falhas
        self.users["failed_logins"].append({
            "username": username,
            "error_message": error_message,
            "timestamp": datetime.now().isoformat()
        })
        
        self.save_users()
    
    def mark_login_success(self, username):
        """
        Marca um login como bem-sucedido
        
        Args:
            username (str): Nome de usuário que teve sucesso
        """
        for user in self.users["active_users"]:
            if user["username"] == username:
                user["successful_logins"] += 1
                user["login_attempts"] = 0  # Reset contador de falhas
                user["last_successful_login"] = datetime.now().isoformat()
                print(f"✅ Login bem-sucedido para {username}")
                break
        
        self.save_users()
    
    def unblock_user(self, username):
        """
        Desbloqueia um usuário e move de volta para lista ativa
        
        Args:
            username (str): Nome de usuário para desbloquear
        """
        for user in self.users["blocked_users"]:
            if user["username"] == username:
                user["status"] = "active"
                user["login_attempts"] = 0
                user["unblocked_date"] = datetime.now().isoformat()
                
                # Mover de volta para ativos
                self.users["active_users"].append(user)
                self.users["blocked_users"].remove(user)
                
                print(f"✅ Usuário {username} desbloqueado!")
                self.save_users()
                return True
        
        print(f"Usuário {username} não encontrado na lista de bloqueados!")
        return False
    
    def get_user_stats(self):
        """
        Retorna estatísticas dos usuários
        
        Returns:
            dict: Estatísticas dos usuários
        """
        return {
            "total_active": len([u for u in self.users["active_users"] if u["status"] == "active"]),
            "total_blocked": len(self.users["blocked_users"]),
            "total_failed_logins": len(self.users["failed_logins"]),
            "recent_failures": self.users["failed_logins"][-10:] if self.users["failed_logins"] else []
        }
    
    def send_blocked_user_notification(self, user, error_message):
        """
        Envia email de notificação quando um usuário é bloqueado
        
        Args:
            user (dict): Dados do usuário bloqueado
            error_message (str): Mensagem de erro
        """
        if not self.email_config.get("enabled", False):
            return
        
        try:
            # Configurar email
            msg = MimeMultipart()
            msg['From'] = self.email_config["from_email"]
            msg['To'] = self.email_config["to_email"]
            msg['Subject'] = f"Instagram Bot - Usuário Bloqueado: {user['username']}"
            
            # Corpo do email
            body = f"""
            <h2>🚨 Usuário Instagram Bloqueado</h2>
            
            <p><strong>Usuário:</strong> {user['username']}</p>
            <p><strong>Motivo:</strong> {error_message}</p>
            <p><strong>Data/Hora:</strong> {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>
            <p><strong>Tentativas de Login:</strong> {user['login_attempts']}</p>
            
            <h3>Detalhes:</h3>
            <ul>
                <li>Email do usuário: {user.get('email', 'N/A')}</li>
                <li>Notas: {user.get('notes', 'N/A')}</li>
                <li>Data de adição: {user.get('added_date', 'N/A')}</li>
            </ul>
            
            <p><em>Este usuário foi automaticamente movido para a lista de bloqueados e não será mais usado.</em></p>
            """
            
            msg.attach(MimeText(body, 'html'))
            
            # Enviar email
            server = smtplib.SMTP(self.email_config["smtp_server"], self.email_config["smtp_port"])
            server.starttls()
            server.login(self.email_config["username"], self.email_config["password"])
            text = msg.as_string()
            server.sendmail(self.email_config["from_email"], self.email_config["to_email"], text)
            server.quit()
            
            print(f"📧 Email de notificação enviado para {self.email_config['to_email']}")
            
        except Exception as e:
            print(f"Erro ao enviar email: {e}")
    
    def cleanup_old_failures(self, days=30):
        """
        Remove falhas de login antigas
        
        Args:
            days (int): Número de dias para manter as falhas
        """
        cutoff_date = datetime.now().timestamp() - (days * 24 * 60 * 60)
        
        original_count = len(self.users["failed_logins"])
        self.users["failed_logins"] = [
            failure for failure in self.users["failed_logins"]
            if datetime.fromisoformat(failure["timestamp"]).timestamp() > cutoff_date
        ]
        
        removed_count = original_count - len(self.users["failed_logins"])
        if removed_count > 0:
            print(f"🧹 Removidas {removed_count} falhas antigas")
            self.save_users()
    
    def export_users(self, filename=None):
        """
        Exporta dados dos usuários para arquivo
        
        Args:
            filename (str): Nome do arquivo (opcional)
        """
        if not filename:
            filename = f"users_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.users, f, indent=2, ensure_ascii=False)
            print(f"📁 Backup salvo em: {filename}")
            return filename
        except Exception as e:
            print(f"Erro ao exportar usuários: {e}")
            return None

