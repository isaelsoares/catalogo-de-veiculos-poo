from __future__ import annotations
from abc import ABC, abstractmethod


class Usuario(ABC):
    _proximo_id = 1

    def __init__(self, id: int | None = None, cpf: int = 0, nome: str = "", email: str = "", senha: str = "") -> None:
        if id is None:
            self._id = Usuario._proximo_id
            Usuario._proximo_id += 1
        else:
            self._id = id
            if id >= Usuario._proximo_id:
                Usuario._proximo_id = id + 1
        self._cpf = cpf
        self._nome = nome
        self._email = email
        self._senha = senha
        self._logado = False

    @property
    def id(self) -> int:
        return self._id

    @property
    def cpf(self) -> int:
        return self._cpf

    @property
    def nome(self) -> str:
        return self._nome

    @nome.setter
    def nome(self, novo_nome: str) -> None:
        if not novo_nome.strip():
            raise ValueError("Nome não pode ser vazio.")
        self._nome = novo_nome

    @property
    def email(self) -> str:
        return self._email

    @staticmethod
    def _validar_senha(senha: str) -> bool:
        return len(senha) >= 6

    def login(self, email: str, senha: str) -> bool:
        if email == self._email and senha == self._senha:
            self._logado = True
            return True
        return False

    def logout(self) -> None:
        self._logado = False

    @abstractmethod
    def exibirPerfil(self, info: str = "") -> str:
        pass

    def atualizarInfo(self, info: dict) -> bool:
        try:
            for chave, valor in info.items():
                if chave == "nome":
                    self.nome = valor
                elif chave == "email":
                    self._email = valor
                elif chave == "senha":
                    if not self._validar_senha(valor):
                        raise ValueError("Senha deve ter pelo menos 6 caracteres.")
                    self._senha = valor
                else:
                    raise KeyError(f"Campo '{chave}' não é permitido.")
            return True
        except Exception:
            return False
