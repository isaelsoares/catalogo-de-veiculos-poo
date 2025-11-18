from user import Usuario
from Advertisement import Anuncio


class Admin(Usuario):
    def __init__(self, id: int, cpf: int, nome: str, email: str, senha: str, adminID: int) -> None:
        """
        Inicializa um objeto Administrador.

        Args:
            id (int): ID do usuário.
            cpf (int): CPF do administrador.
            nome (str): Nome completo.
            email (str): Email do administrador.
            senha (str): Senha de acesso.
            adminID (int): Identificador exclusivo do administrador.
        """
        super().__init__(id, cpf, nome, email, senha)
        self._adminID = adminID

    @property
    def adminID(self) -> int:
        """
        Retorna o identificador exclusivo do administrador.

        Returns:
            int: ID específico do administrador.
        """
        return self._adminID

    def aprovarAnuncio(self, anuncio: Anuncio) -> None:
        """
        Aprova um anúncio alterando seu status para 'Aprovado'.

        Args:
            anuncio (Anuncio): Objeto anúncio a ser aprovado.
        """
        anuncio.aprovar()

    def rejeitarAnuncio(self, anuncio: Anuncio) -> None:
        """
        Rejeita um anúncio alterando seu status para 'Rejeitado'.

        Args:
            anuncio (Anuncio): Objeto anúncio a ser rejeitado.
        """
        anuncio.rejeitar()

    def gerenciarUsuario(self, acao: str, usuario: Usuario | None = None, dados: dict | None = None, lista_usuarios: list | None = None):
        """
        Gerencia usuários realizando operações CRUD (criar, ler, atualizar, deletar).

        Args:
            acao (str): A ação a ser executada. Pode ser 'criar', 'ler', 'atualizar' ou 'deletar'.
            usuario (Usuario | None): Usuário alvo da ação (necessário em ler, atualizar e deletar).
            dados (dict | None): Dados necessários para criação ou atualização.
            lista_usuarios (list | None): Lista onde os usuários são armazenados.

        Returns:
            str: Mensagem descrevendo o resultado da operação.

        Raises:
            ValueError: Se informações obrigatórias não forem fornecidas.
        """
        if lista_usuarios is None:
            raise ValueError("É necessário fornecer a lista de usuários para gerenciar.")

        if acao == "criar":
            if dados is None:
                raise ValueError("Dados são necessários para criar um usuário.")

            novo_usuario = dados["classe"](
                dados["id"], dados["cpf"], dados["nome"],
                dados["email"], dados["senha"]
            )
            lista_usuarios.append(novo_usuario)
            return f"Usuário {novo_usuario.nome} criado com sucesso."

        elif acao == "ler":
            if usuario is None:
                raise ValueError("É necessário passar um usuário para consultar.")
            return usuario.exibirPerfil()

        elif acao == "atualizar":
            if usuario is None or dados is None:
                raise ValueError("É preciso passar usuário e dados para atualizar.")
            usuario.atualizarInfo(dados)
            return f"Usuário {usuario.nome} atualizado."

        elif acao == "deletar":
            if usuario is None:
                raise ValueError("É necessário passar um usuário para deletar.")
            if usuario in lista_usuarios:
                lista_usuarios.remove(usuario)
                return f"Usuário {usuario.nome} removido."
            return "Usuário não encontrado na lista."

        else:
            raise ValueError("Ação inválida. Use: criar, ler, atualizar, deletar.")

    def exibirPerfil(self, info: str = "") -> str:
        """
        Retorna uma string contendo os dados do perfil do administrador.

        Args:
            info (str): Texto adicional opcional a ser exibido.

        Returns:
            str: Descrição formatada do perfil do administrador.
        """
        return (
            f"=== Perfil do Administrador ===\n"
            f"ID do usuário: {self.id}\n"
            f"Admin ID: {self.adminID}\n"
            f"Nome: {self.nome}\n"
            f"Email: {self.email}\n"
            f"{info}"
        )
