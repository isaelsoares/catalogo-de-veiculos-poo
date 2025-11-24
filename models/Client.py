from typing import List
from models.Vehicle import Veiculo
from models.User import Usuario


class Cliente(Usuario):
    _proximo_id = 1

    def __init__(self, cpf: int, nome: str, email: str, senha: str) -> None:
        super().__init__(Cliente._proximo_id, cpf, nome, email, senha)
        Cliente._proximo_id += 1
        self._historicoPesquisas: List[str] = []

    @property
    def historicoPesquisas(self) -> List[str]:
        return self._historicoPesquisas

    @historicoPesquisas.setter
    def historicoPesquisas(self, valor: List[str]):
        self._historicoPesquisas = valor

    def buscarVeiculos(self, filtro: str, listaVeiculos: List[Veiculo]) -> List[Veiculo]:
        """
        Busca veículos cujo modelo ou marca contenha o filtro.
        Também salva o filtro no histórico.
        """
        self._historicoPesquisas.append(filtro)

        resultado = [
            v for v in listaVeiculos
            if filtro.lower() in v.marca.lower() or filtro.lower() in v.modelo.lower()
        ]

        return resultado

    def visualizarDetalhes(self, idVeiculo: int, listaVeiculos: List[Veiculo]) -> Veiculo | None:
        """
        Retorna o veículo com o ID informado, ou None se não existir.
        """
        for v in listaVeiculos:
            if v.id == idVeiculo:
                return v
        return None

    def exibirPerfil(self, info: str = "") -> str:
        """
        Override: exibe informações sobre o cliente.
        """
        return (
            f"Cliente ID: {self.id}\n"
            f"Nome: {self.nome}\n"
            f"Email: {self.email}\n"
            f"Histórico de Pesquisas: {', '.join(self.historicoPesquisas) if self.historicoPesquisas else 'Nenhuma pesquisa realizada'}\n"
            f"{info}"
        )
