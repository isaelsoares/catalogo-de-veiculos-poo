from car import Veiculo
from announcer import Anunciante
class Anuncio:
    _proximo_id = 1

    def __init__(self, dataPublicacao: str, status: str, veiculo: Veiculo, anunciante):
        """
        Inicializa um objeto Anuncio.

        Args:
            dataPublicacao (str): Data da publicação do anúncio.
            status (str): Status atual do anúncio.
            veiculo: Objeto Veiculo associado ao anúncio.
            anunciante: Objeto Anunciante responsável pelo anúncio.
        """
        self._id = Anuncio._proximo_id
        Anuncio._proximo_id += 1

        self._dataPublicacao = dataPublicacao
        self._status = status
        self._veiculo = veiculo
        self._anunciante = anunciante

    @property
    def id(self):
        """Retorna o identificador único do anúncio."""
        return self._id

    @property
    def dataPublicacao(self):
        """Retorna a data de publicação do anúncio."""
        return self._dataPublicacao

    @dataPublicacao.setter
    def dataPublicacao(self, valor):
        """Define uma nova data de publicação."""
        self._dataPublicacao = valor

    @property
    def status(self):
        """Retorna o status atual do anúncio."""
        return self._status

    @status.setter
    def status(self, valor):
        """Define um novo status para o anúncio."""
        self._status = valor

    @property
    def veiculo(self):
        """Retorna o veículo associado ao anúncio."""
        return self._veiculo

    @veiculo.setter
    def veiculo(self, valor):
        """Define um novo veículo para o anúncio."""
        self._veiculo = valor

    @property
    def anunciante(self):
        """Retorna o anunciante responsável pelo anúncio."""
        return self._anunciante

    @anunciante.setter
    def anunciante(self, valor):
        """Define um novo anunciante responsável pelo anúncio."""
        self._anunciante = valor

    def aprovar(self):
        """
        Aprova este anúncio, definindo seu status como 'Aprovado'.
        """
        self._status = "Aprovado"

    def rejeitar(self):
        """
        Rejeita este anúncio, definindo seu status como 'Rejeitado'.
        """
        self._status = "Rejeitado"

    def exibirResumo(self) -> str:
        """
        Retorna um resumo textual do anúncio, contendo informações principais.

        Returns:
            str: Resumo formatado do anúncio.
        """
        return (
            f"=== Resumo do Anúncio ===\n"
            f"ID: {self.id}\n"
            f"Data: {self.dataPublicacao}\n"
            f"Status: {self.status}\n"
            f"Veículo: {self.veiculo}\n"
            f"Anunciante: {self.anunciante.nome if hasattr(self.anunciante, 'nome') else self.anunciante}\n"
        )
