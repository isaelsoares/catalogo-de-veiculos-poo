"""
Camada de repositórios para persistência de dados no banco SQLite.
Cada classe Repository é responsável pelas operações CRUD de uma entidade.
"""

from typing import List, Optional
from database import Database
from models.User import Usuario
from models.Admin import Admin
from models.Announcer import Anunciante
from models.Client import Cliente
from models.Vehicle import Veiculo
from models.Advertisement import Anuncio


class UsuarioRepository:
    """Repositório para operações com Usuários."""
    
    def __init__(self):
        self.db = Database()
    
    def salvar(self, usuario: Usuario, tipo: str, dados_especificos: dict = None) -> int:
        """
        Salva um usuário no banco de dados.
        
        Args:
            usuario: Objeto Usuario.
            tipo: Tipo do usuário ('admin', 'anunciante', 'cliente').
            dados_especificos: Dados específicos por tipo de usuário.
            
        Returns:
            int: ID do usuário salvo.
        """
        # Inserir na tabela usuarios
        cursor = self.db.execute("""
            INSERT INTO usuarios (cpf, nome, email, senha, tipo, logado)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (str(usuario.cpf), usuario.nome, usuario.email, 
              usuario._senha, tipo, int(usuario._logado)))
        
        usuario_id = cursor.lastrowid
        
        # Inserir dados específicos
        if tipo == 'admin' and dados_especificos:
            self.db.execute("""
                INSERT INTO admins (usuario_id, admin_id)
                VALUES (?, ?)
            """, (usuario_id, dados_especificos['admin_id']))
        
        elif tipo == 'anunciante' and dados_especificos:
            self.db.execute("""
                INSERT INTO anunciantes (usuario_id, telefone)
                VALUES (?, ?)
            """, (usuario_id, dados_especificos['telefone']))
        
        elif tipo == 'cliente':
            self.db.execute("""
                INSERT INTO clientes (usuario_id)
                VALUES (?)
            """, (usuario_id,))
        
        return usuario_id
    
    def buscar_por_id(self, usuario_id: int, tipo: str) -> Optional[Usuario]:
        """
        Busca um usuário por ID.
        
        Args:
            usuario_id: ID do usuário.
            tipo: Tipo do usuário ('admin', 'anunciante', 'cliente').
            
        Returns:
            Optional[Usuario]: Objeto Usuario ou None.
        """
        row = self.db.fetch_one("""
            SELECT * FROM usuarios WHERE id = ?
        """, (usuario_id,))
        
        if not row:
            return None
        
        return self._row_to_usuario(row, tipo)
    
    def buscar_por_email(self, email: str) -> Optional[tuple[Usuario, str]]:
        """
        Busca um usuário por email.
        
        Returns:
            Optional[tuple]: (Usuario, tipo) ou None.
        """
        row = self.db.fetch_one("""
            SELECT * FROM usuarios WHERE email = ?
        """, (email,))
        
        if not row:
            return None
        
        tipo = row['tipo']
        usuario = self._row_to_usuario(row, tipo)
        return (usuario, tipo)
    
    def listar_todos(self, tipo: Optional[str] = None) -> List[Usuario]:
        """
        Lista todos os usuários, opcionalmente filtrados por tipo.
        
        Args:
            tipo: Tipo de usuário para filtrar (opcional).
            
        Returns:
            List[Usuario]: Lista de usuários.
        """
        if tipo:
            rows = self.db.fetch_all("""
                SELECT * FROM usuarios WHERE tipo = ?
            """, (tipo,))
        else:
            rows = self.db.fetch_all("SELECT * FROM usuarios")
        
        usuarios = []
        for row in rows:
            usuario = self._row_to_usuario(row, row['tipo'])
            if usuario:
                usuarios.append(usuario)
        
        return usuarios
    
    def atualizar(self, usuario_id: int, dados: dict):
        """
        Atualiza os dados de um usuário.
        
        Args:
            usuario_id: ID do usuário.
            dados: Dicionário com os campos a atualizar.
        """
        campos_permitidos = ['nome', 'email', 'senha', 'logado']
        updates = []
        valores = []
        
        for campo, valor in dados.items():
            if campo in campos_permitidos:
                updates.append(f"{campo} = ?")
                valores.append(valor)
        
        if updates:
            valores.append(usuario_id)
            query = f"UPDATE usuarios SET {', '.join(updates)} WHERE id = ?"
            self.db.execute(query, tuple(valores))
    
    def deletar(self, usuario_id: int):
        """Remove um usuário do banco de dados."""
        self.db.execute("DELETE FROM usuarios WHERE id = ?", (usuario_id,))
    
    def _row_to_usuario(self, row, tipo: str) -> Optional[Usuario]:
        """Converte uma linha do banco em objeto Usuario."""
        if tipo == 'admin':
            admin_row = self.db.fetch_one("""
                SELECT admin_id FROM admins WHERE usuario_id = ?
            """, (row['id'],))
            
            if admin_row:
                return Admin(
                    id=row['id'],
                    cpf=int(row['cpf']),
                    nome=row['nome'],
                    email=row['email'],
                    senha=row['senha'],
                    adminID=admin_row['admin_id']
                )
        
        elif tipo == 'anunciante':
            anunciante_row = self.db.fetch_one("""
                SELECT telefone FROM anunciantes WHERE usuario_id = ?
            """, (row['id'],))
            
            if anunciante_row:
                anunciante = Anunciante(
                    cpf=int(row['cpf']),
                    nome=row['nome'],
                    email=row['email'],
                    senha=row['senha'],
                    telefone=anunciante_row['telefone']
                )
                # Ajustar o ID para corresponder ao banco
                anunciante._id = row['id']
                return anunciante
        
        elif tipo == 'cliente':
            cliente = Cliente(
                cpf=int(row['cpf']),
                nome=row['nome'],
                email=row['email'],
                senha=row['senha']
            )
            # Ajustar o ID para corresponder ao banco
            cliente._id = row['id']
            
            # Carregar histórico de pesquisas
            historico = self.db.fetch_all("""
                SELECT filtro FROM historico_pesquisas
                WHERE cliente_id = ?
                ORDER BY data_pesquisa
            """, (row['id'],))
            
            cliente._historicoPesquisas = [h['filtro'] for h in historico]
            return cliente
        
        return None


class VeiculoRepository:
    """Repositório para operações com Veículos."""
    
    def __init__(self):
        self.db = Database()
    
    def salvar(self, veiculo: Veiculo, anunciante_id: Optional[int] = None) -> int:
        """
        Salva um veículo no banco de dados.
        
        Args:
            veiculo: Objeto Veiculo.
            anunciante_id: ID do anunciante (opcional).
            
        Returns:
            int: ID do veículo salvo.
        """
        cursor = self.db.execute("""
            INSERT INTO veiculos (marca, modelo, ano, preco, quilometragem, anunciante_id)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (veiculo.marca, veiculo.modelo, veiculo.ano, 
              veiculo.preco, veiculo.quilometragem, anunciante_id))
        
        return cursor.lastrowid
    
    def buscar_por_id(self, veiculo_id: int) -> Optional[Veiculo]:
        """Busca um veículo por ID."""
        row = self.db.fetch_one("""
            SELECT * FROM veiculos WHERE id = ?
        """, (veiculo_id,))
        
        if not row:
            return None
        
        return self._row_to_veiculo(row)
    
    def listar_todos(self) -> List[Veiculo]:
        """Lista todos os veículos."""
        rows = self.db.fetch_all("SELECT * FROM veiculos")
        return [self._row_to_veiculo(row) for row in rows]
    
    def listar_por_anunciante(self, anunciante_id: int) -> List[Veiculo]:
        """Lista veículos de um anunciante específico."""
        rows = self.db.fetch_all("""
            SELECT * FROM veiculos WHERE anunciante_id = ?
        """, (anunciante_id,))
        return [self._row_to_veiculo(row) for row in rows]
    
    def buscar(self, filtro: str) -> List[Veiculo]:
        """
        Busca veículos por marca ou modelo.
        
        Args:
            filtro: Texto para buscar em marca ou modelo.
            
        Returns:
            List[Veiculo]: Lista de veículos encontrados.
        """
        rows = self.db.fetch_all("""
            SELECT * FROM veiculos 
            WHERE LOWER(marca) LIKE ? OR LOWER(modelo) LIKE ?
        """, (f"%{filtro.lower()}%", f"%{filtro.lower()}%"))
        
        return [self._row_to_veiculo(row) for row in rows]
    
    def atualizar(self, veiculo_id: int, dados: dict):
        """Atualiza os dados de um veículo."""
        campos_permitidos = ['marca', 'modelo', 'ano', 'preco', 'quilometragem']
        updates = []
        valores = []
        
        for campo, valor in dados.items():
            if campo in campos_permitidos:
                updates.append(f"{campo} = ?")
                valores.append(valor)
        
        if updates:
            valores.append(veiculo_id)
            query = f"UPDATE veiculos SET {', '.join(updates)} WHERE id = ?"
            self.db.execute(query, tuple(valores))
    
    def deletar(self, veiculo_id: int):
        """Remove um veículo do banco de dados."""
        self.db.execute("DELETE FROM veiculos WHERE id = ?", (veiculo_id,))
    
    def _row_to_veiculo(self, row) -> Veiculo:
        """Converte uma linha do banco em objeto Veiculo."""
        veiculo = Veiculo(
            marca=row['marca'],
            modelo=row['modelo'],
            ano=row['ano'],
            preco=row['preco'],
            quilometragem=row['quilometragem'],
            anunciante=None
        )
        veiculo._id = row['id']
        return veiculo


class AnuncioRepository:
    """Repositório para operações com Anúncios."""
    
    def __init__(self):
        self.db = Database()
        self.veiculo_repo = VeiculoRepository()
    
    def salvar(self, anuncio: Anuncio, veiculo_id: int, anunciante_id: int) -> int:
        """
        Salva um anúncio no banco de dados.
        
        Args:
            anuncio: Objeto Anuncio.
            veiculo_id: ID do veículo.
            anunciante_id: ID do anunciante.
            
        Returns:
            int: ID do anúncio salvo.
        """
        cursor = self.db.execute("""
            INSERT INTO anuncios (data_publicacao, status, veiculo_id, anunciante_id)
            VALUES (?, ?, ?, ?)
        """, (anuncio.dataPublicacao, anuncio.status, veiculo_id, anunciante_id))
        
        return cursor.lastrowid
    
    def buscar_por_id(self, anuncio_id: int) -> Optional[Anuncio]:
        """Busca um anúncio por ID."""
        row = self.db.fetch_one("""
            SELECT * FROM anuncios WHERE id = ?
        """, (anuncio_id,))
        
        if not row:
            return None
        
        return self._row_to_anuncio(row)
    
    def listar_todos(self) -> List[Anuncio]:
        """Lista todos os anúncios."""
        rows = self.db.fetch_all("SELECT * FROM anuncios")
        return [self._row_to_anuncio(row) for row in rows]
    
    def listar_por_anunciante(self, anunciante_id: int) -> List[Anuncio]:
        """Lista anúncios de um anunciante específico."""
        rows = self.db.fetch_all("""
            SELECT * FROM anuncios WHERE anunciante_id = ?
        """, (anunciante_id,))
        return [self._row_to_anuncio(row) for row in rows]
    
    def listar_por_status(self, status: str) -> List[Anuncio]:
        """Lista anúncios por status."""
        rows = self.db.fetch_all("""
            SELECT * FROM anuncios WHERE status = ?
        """, (status,))
        return [self._row_to_anuncio(row) for row in rows]
    
    def atualizar_status(self, anuncio_id: int, novo_status: str):
        """Atualiza o status de um anúncio."""
        self.db.execute("""
            UPDATE anuncios SET status = ? WHERE id = ?
        """, (novo_status, anuncio_id))
    
    def deletar(self, anuncio_id: int):
        """Remove um anúncio do banco de dados."""
        self.db.execute("DELETE FROM anuncios WHERE id = ?", (anuncio_id,))
    
    def _row_to_anuncio(self, row) -> Optional[Anuncio]:
        """Converte uma linha do banco em objeto Anuncio."""
        veiculo = self.veiculo_repo.buscar_por_id(row['veiculo_id'])
        
        if not veiculo:
            return None
        
        # Criar anúncio com dados simplificados
        anuncio = Anuncio(
            dataPublicacao=row['data_publicacao'],
            status=row['status'],
            veiculo=veiculo,
            anunciante=None  # Simplified - avoid circular references
        )
        anuncio._id = row['id']
        
        return anuncio


class ClienteRepository:
    """Repositório específico para operações com histórico de clientes."""
    
    def __init__(self):
        self.db = Database()
    
    def salvar_pesquisa(self, cliente_id: int, filtro: str):
        """
        Salva uma pesquisa no histórico do cliente.
        
        Args:
            cliente_id: ID do cliente.
            filtro: Termo pesquisado.
        """
        self.db.execute("""
            INSERT INTO historico_pesquisas (cliente_id, filtro)
            VALUES (?, ?)
        """, (cliente_id, filtro))
    
    def obter_historico(self, cliente_id: int) -> List[str]:
        """
        Obtém o histórico de pesquisas de um cliente.
        
        Args:
            cliente_id: ID do cliente.
            
        Returns:
            List[str]: Lista de termos pesquisados.
        """
        rows = self.db.fetch_all("""
            SELECT filtro FROM historico_pesquisas
            WHERE cliente_id = ?
            ORDER BY data_pesquisa DESC
        """, (cliente_id,))
        
        return [row['filtro'] for row in rows]
    
    def limpar_historico(self, cliente_id: int):
        """Limpa o histórico de pesquisas de um cliente."""
        self.db.execute("""
            DELETE FROM historico_pesquisas WHERE cliente_id = ?
        """, (cliente_id,))
