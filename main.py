from models.Admin import Admin
from models.Advertisement import Anuncio
from models.Announcer import Anunciante
from models.User import Usuario
from models.Vehicle import Veiculo
from models.Client import Cliente
from typing import List

adminList: list[Admin] = []    
anuncianteList: List[Anunciante] = []
clienteList: List[Cliente] = []
userList = []
veiculoList: List[Veiculo] = []
anuncioList: List[Anuncio] = []

def actions():
    print("Escolha uma Ação")



def CreateAdmin(cpf, nome, email, senha, adminID) -> Admin:
    return Admin(
        id = None,
        cpf=cpf,
        nome=nome,
        email=email,
        senha=senha,
        adminID=adminID   
    )

def CreateAnunciante(cpf, nome, email,senha, telefone) -> Anunciante: 
    a = Anunciante(
        cpf=cpf,
        nome=nome,
        email=email,
        senha=senha,
        telefone=telefone
    )
    anuncianteList.append(a)
    return a

def CreateCliente(cpf, nome, email, senha) -> Cliente:
    c = Cliente(
                cpf=cpf,
                nome=nome,
               email=email,
               senha=senha
            )
    clienteList.append(c)
    return c

def CreateVeiculo(marca, modelo, ano, preco, km):
    v = Veiculo(
        marca=marca, 
        modelo=modelo,
        ano=ano,
        preco=preco,
        quilometragem=km
    )
    veiculoList.append(v)
    return v


def CadastroUsuario(tipo, nome, email, senha, telefone=None):
    if tipo: #True=Anunciante, False=Cliente
        #TODO: se não der para validar os campos na interface fazer aqui
        userList.append(CreateAnunciante(nome, email, senha, telefone))
        return "Anunciante Cadastrado"
    else:         
        #TODO: se não der para validar os campos na interface fazer aqui
        userList.append(CreateCliente(nome, email, senha))
        return "Cliente Cadastrado"

def Login(nome, senha):
    for i in userList:
        if nome == i.nome:
            if senha == i.senha:
                return "Logado"
            else:
                return "Usuario ou Senha Incorretos"
        else:
            return "Usuario ou Senha Incorretos"
    
def AnuncianteCriarAnuncio(anunciante, carro):
    a = anunciante.criarAnuncio(carro)
    anuncioList.append(a)
    return f"Anuncio Criado Carro: {a.veiculo.marca} {a.veiculo.modelo}"

