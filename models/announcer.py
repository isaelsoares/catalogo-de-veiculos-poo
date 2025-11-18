from __future__ import annotations
from typing import List
from user import Usuario


class Anunciante(Usuario):
    _auto_id = 1

    def __init__(self, cpf: int, nome: str, email: str, senha: str, telefone: str) -> None:
        super().__init__(Anunciante._auto_id, cpf, nome, email, senha)
        Anunciante._auto_id += 1

        self._telefone = telefone
        self._listaAnuncios: List[Anuncio] = []

    @property
    def telefone(self) -> str:
        return self._telefone

    @telefone.setter
    def telefone(self, valor: str) -> None:
        if not valor.strip():
            raise ValueError("Telefone inválido.")
        self._telefone = valor

    def criarAnuncio(self, v: Veiculo) -> Anuncio:
        anuncio = Anuncio(v, self)
        self._listaAnuncios.append(anuncio)
        return anuncio

    def editarAnuncio(self, id: int, dados: dict) -> bool:
        anuncio = next((a for a in self._listaAnuncios if a.id == id), None)
        if not anuncio:
            return False
        try:
            for k, v in dados.items():
                if hasattr(anuncio, k):
                    setattr(anuncio, k, v)
            return True
        except Exception:
            return False

    def excluirAnuncio(self, id: int) -> bool:
        anuncio = next((a for a in self._listaAnuncios if a.id == id), None)
        if anuncio:
            self._listaAnuncios.remove(anuncio)
            return True
        return False

    def listarMeusAnuncios(self) -> List[Anuncio]:
        return self._listaAnuncios

    def aprovarAnuncio(self, idAnuncio: int) -> None:
        anuncio = next((a for a in self._listaAnuncios if a.id == idAnuncio), None)
        if anuncio:
            anuncio.aprovar()

    def exibirPerfil(self, info: str = "") -> str:
        return (
            f"Anunciante: {self.nome}\n"
            f"Email: {self.email}\n"
            f"Telefone: {self.telefone}\n"
            f"Total de anúncios: {len(self._listaAnuncios)}"
        )
