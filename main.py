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

def CreateAnunciante(cpf, nome, email, senha, telefone=None) -> Anunciante: 
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
        #Esperamos que o fluxo CLI use CPF; função genérica não faz criação direta
        raise ValueError("Use a função de fluxo CLI para cadastrar (precisa de CPF).")
    else:
        raise ValueError("Use a função de fluxo CLI para cadastrar (precisa de CPF).")

def Login(email, senha):
    # Retorna o objeto de usuário quando login bem-sucedido, senão None
    for i in userList:
        # usa o método `login` definido em Usuario
        try:
            if hasattr(i, 'login') and i.login(email, senha):
                return i
        except Exception:
            continue
    return None
    
def AnuncianteCriarAnuncio(anunciante, carro):
    a = anunciante.criarAnuncio(carro)
    anuncioList.append(a)
    return f"Anuncio Criado Carro: {a.veiculo.marca} {a.veiculo.modelo}"


def _input(prompt: str) -> str:
    try:
        return input(prompt)
    except EOFError:
        return ""


def register_user_flow():
    print("--- Cadastro de Usuário ---")
    tipo = _input("Tipo (1=Anunciante, 2=Cliente): ").strip()
    cpf = _input("CPF: ").strip()
    nome = _input("Nome: ").strip()
    email = _input("Email: ").strip()
    senha = _input("Senha: ").strip()
    telefone = None
    if tipo == '1':
        telefone = _input("Telefone (opcional): ").strip() or None
        user = CreateAnunciante(cpf, nome, email, senha, telefone)
        userList.append(user)
        print("Anunciante cadastrado com sucesso.")
    else:
        user = CreateCliente(cpf, nome, email, senha)
        userList.append(user)
        print("Cliente cadastrado com sucesso.")


def login_flow():
    print("--- Login ---")
    email = _input("Email: ").strip()
    senha = _input("Senha: ").strip()
    user = Login(email, senha)
    if user:
        print(f"Logado como: {user.nome}")
        return user
    else:
        print("Usuário ou senha incorretos.")
        return None


def create_vehicle_flow():
    print("--- Cadastrar Veículo ---")
    marca = _input("Marca: ").strip()
    modelo = _input("Modelo: ").strip()
    ano = _input("Ano: ").strip()
    preco = _input("Preço: ").strip()
    km = _input("Quilometragem: ").strip()
    try:
        v = CreateVeiculo(marca, modelo, ano, preco, km)
        print(f"Veículo criado: {v.marca} {v.modelo}")
        return v
    except Exception as e:
        print("Erro ao criar veículo:", e)
        return None


def create_ad_flow(current_user):
    if not current_user:
        print("É preciso estar logado como anunciante para criar anúncio.")
        return
    # Verifica se o usuário é um anunciante (tem método criarAnuncio)
    if not hasattr(current_user, 'criarAnuncio'):
        print("Apenas anunciantes podem criar anúncios.")
        return
    print("--- Criar Anúncio ---")
    # Permitir usar um veículo já cadastrado ou criar novo
    escolha = _input("Usar veículo existente? (s/n): ").strip().lower()
    if escolha == 's' and veiculoList:
        for idx, v in enumerate(veiculoList, start=1):
            print(f"{idx}: {v.marca} {v.modelo} ({v.ano}) - {v.quilometragem}km - {v.preco}")
        sel = _input("Escolha número do veículo: ").strip()
        try:
            v = veiculoList[int(sel)-1]
        except Exception:
            print("Seleção inválida.")
            return
    else:
        v = create_vehicle_flow()
        if not v:
            return
    msg = AnuncianteCriarAnuncio(current_user, v)
    print(msg)


def list_announcements():
    print("--- Anúncios ---")
    if not anuncioList:
        print("Nenhum anúncio cadastrado.")
        return
    for a in anuncioList:
        try:
            anunciante_nome = getattr(a.anunciante, 'nome', 'Desconhecido')
            veic = a.veiculo
            print(f"Anunciante: {anunciante_nome} | Veículo: {veic.marca} {veic.modelo} ({veic.ano}) | Preço: {veic.preco}")
        except Exception:
            print(repr(a))


def list_vehicles():
    print("--- Veículos ---")
    if not veiculoList:
        print("Nenhum veículo cadastrado.")
        return
    for v in veiculoList:
        print(f"{v.marca} {v.modelo} ({v.ano}) - {v.quilometragem}km - {v.preco}")


def main():
    current_user = None
    while True:
        print("\n=== Catálogo de Veículos ===")
        print("1. Cadastrar usuário")
        print("2. Login")
        print("3. Cadastrar veículo")
        print("4. Criar anúncio (anunciantes)")
        print("5. Listar anúncios")
        print("6. Listar veículos")
        print("7. Logout")
        print("0. Sair")
        opc = _input("Escolha uma opção: ").strip()
        if opc == '1':
            register_user_flow()
        elif opc == '2':
            user = login_flow()
            if user:
                current_user = user
        elif opc == '3':
            v = create_vehicle_flow()
            if v:
                veiculoList.append(v)
        elif opc == '4':
            create_ad_flow(current_user)
        elif opc == '5':
            list_announcements()
        elif opc == '6':
            list_vehicles()
        elif opc == '7':
            current_user = None
            print("Desconectado.")
        elif opc == '0':
            print("Saindo...")
            break
        else:
            print("Opção inválida.")


if __name__ == '__main__':
    main()

