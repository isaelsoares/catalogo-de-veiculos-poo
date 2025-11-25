import sqlite3
from typing import Optional
import os


class Database:
    """
    Classe responsável por gerenciar a conexão com o banco de dados SQLite.
    Implementa o padrão Singleton para garantir uma única instância.
    """
    _instance: Optional['Database'] = None
    _connection: Optional[sqlite3.Connection] = None
    
    def __new__(cls, db_path: str = "catalogo_veiculos.db"):
        """Implementa o padrão Singleton."""
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance._db_path = db_path
        return cls._instance
    
    def connect(self) -> sqlite3.Connection:
        """
        Estabelece conexão com o banco de dados SQLite.
        
        Returns:
            sqlite3.Connection: Objeto de conexão com o banco de dados.
        """
        if self._connection is None:
            self._connection = sqlite3.connect(self._db_path)
            self._connection.row_factory = sqlite3.Row  # Permite acessar colunas por nome
        return self._connection
    
    def close(self):
        """Fecha a conexão com o banco de dados."""
        if self._connection:
            self._connection.close()
            self._connection = None
    
    def execute(self, query: str, params: tuple = ()) -> sqlite3.Cursor:
        """
        Executa uma query SQL.
        
        Args:
            query (str): Query SQL a ser executada.
            params (tuple): Parâmetros da query.
            
        Returns:
            sqlite3.Cursor: Cursor com o resultado da query.
        """
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        return cursor
    
    def executemany(self, query: str, params_list: list) -> sqlite3.Cursor:
        """
        Executa múltiplas queries SQL.
        
        Args:
            query (str): Query SQL a ser executada.
            params_list (list): Lista de tuplas com parâmetros.
            
        Returns:
            sqlite3.Cursor: Cursor com o resultado da query.
        """
        conn = self.connect()
        cursor = conn.cursor()
        cursor.executemany(query, params_list)
        conn.commit()
        return cursor
    
    def fetch_one(self, query: str, params: tuple = ()) -> Optional[sqlite3.Row]:
        """
        Executa uma query e retorna um único resultado.
        
        Args:
            query (str): Query SQL.
            params (tuple): Parâmetros da query.
            
        Returns:
            Optional[sqlite3.Row]: Linha do resultado ou None.
        """
        cursor = self.execute(query, params)
        return cursor.fetchone()
    
    def fetch_all(self, query: str, params: tuple = ()) -> list[sqlite3.Row]:
        """
        Executa uma query e retorna todos os resultados.
        
        Args:
            query (str): Query SQL.
            params (tuple): Parâmetros da query.
            
        Returns:
            list[sqlite3.Row]: Lista com todas as linhas do resultado.
        """
        cursor = self.execute(query, params)
        return cursor.fetchall()
    
    def create_tables(self):
        """Cria todas as tabelas necessárias para o sistema."""
        
        # Tabela de Usuários
        self.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cpf TEXT NOT NULL UNIQUE,
                nome TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                senha TEXT NOT NULL,
                tipo TEXT NOT NULL CHECK(tipo IN ('admin', 'anunciante', 'cliente')),
                logado INTEGER DEFAULT 0
            )
        """)
        
        # Tabela de Admins (campos específicos)
        self.execute("""
            CREATE TABLE IF NOT EXISTS admins (
                usuario_id INTEGER PRIMARY KEY,
                admin_id INTEGER NOT NULL UNIQUE,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
            )
        """)
        
        # Tabela de Anunciantes (campos específicos)
        self.execute("""
            CREATE TABLE IF NOT EXISTS anunciantes (
                usuario_id INTEGER PRIMARY KEY,
                telefone TEXT NOT NULL,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
            )
        """)
        
        # Tabela de Clientes (campos específicos)
        self.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                usuario_id INTEGER PRIMARY KEY,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
            )
        """)
        
        # Tabela de Histórico de Pesquisas
        self.execute("""
            CREATE TABLE IF NOT EXISTS historico_pesquisas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente_id INTEGER NOT NULL,
                filtro TEXT NOT NULL,
                data_pesquisa TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (cliente_id) REFERENCES clientes(usuario_id) ON DELETE CASCADE
            )
        """)
        
        # Tabela de Veículos
        self.execute("""
            CREATE TABLE IF NOT EXISTS veiculos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                marca TEXT NOT NULL,
                modelo TEXT NOT NULL,
                ano INTEGER NOT NULL,
                preco REAL NOT NULL,
                quilometragem INTEGER NOT NULL,
                anunciante_id INTEGER,
                FOREIGN KEY (anunciante_id) REFERENCES anunciantes(usuario_id) ON DELETE SET NULL
            )
        """)
        
        # Tabela de Anúncios
        self.execute("""
            CREATE TABLE IF NOT EXISTS anuncios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data_publicacao TEXT NOT NULL,
                status TEXT NOT NULL CHECK(status IN ('Pendente', 'Aprovado', 'Rejeitado')),
                veiculo_id INTEGER NOT NULL UNIQUE,
                anunciante_id INTEGER NOT NULL,
                FOREIGN KEY (veiculo_id) REFERENCES veiculos(id) ON DELETE CASCADE,
                FOREIGN KEY (anunciante_id) REFERENCES anunciantes(usuario_id) ON DELETE CASCADE
            )
        """)
        
        print("✓ Tabelas criadas com sucesso!")
    
    def reset_database(self):
        """Remove todas as tabelas do banco de dados."""
        tables = ['anuncios', 'historico_pesquisas', 'veiculos', 
                  'clientes', 'anunciantes', 'admins', 'usuarios']
        
        for table in tables:
            self.execute(f"DROP TABLE IF EXISTS {table}")
        
        print("✓ Banco de dados resetado!")
