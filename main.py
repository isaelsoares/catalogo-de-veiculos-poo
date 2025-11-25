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

# Criar usuário admin padrão
admin_padrao = Admin(
    id=1,
    cpf="00000000000",
    nome="Administrador",
    email="admin@admin.com",
    senha="admin123",
    adminID=1
)
adminList.append(admin_padrao)
userList.append(admin_padrao)

def actions():
    print("Escolha uma Ação")



def CreateAdmin(cpf, nome, email, senha, adminID) -> Admin:
    a = Admin(
        id = None,
        cpf=cpf,
        nome=nome,
        email=email,
        senha=senha,
        adminID=adminID   
    )
    adminList.append(a)
    userList.append(a)
    return a

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

def CreateVeiculo(marca, modelo, ano, preco, km, anunciante=None):
    v = Veiculo(
        marca=marca,
        modelo=modelo,
        ano=ano,
        preco=preco,
        quilometragem=km,
        anunciante=anunciante,
    )
    return v


def CadastroUsuario(tipo, nome, email, senha, telefone=None):
    if tipo: #True=Anunciante, False=Cliente
        #Esperamos que o fluxo CLI use CPF; função genérica não faz criação direta
        raise ValueError("Use a função de fluxo CLI para cadastrar (precisa de CPF).")
    else:
        raise ValueError("Use a função de fluxo CLI para cadastrar (precisa de CPF).")


def anunciante_manage_flow(current_user):
    if not current_user or not hasattr(current_user, 'listarMeusAnuncios'):
        print("Acesso negado. Apenas anunciantes.")
        return
    while True:
        print("\n--- Gerenciar Meus Anúncios ---")
        print("1. Listar meus anúncios")
        print("2. Excluir anúncio")
        print("0. Voltar")
        op = _input("Escolha: ").strip()
        if op == '1':
            lista = current_user.listarMeusAnuncios()
            if not lista:
                print("Nenhum anúncio encontrado.")
            for a in lista:
                try:
                    v = a.veiculo
                    print(f"ID:{a.id} | {v.marca} {v.modelo} ({v.ano}) | Status: {a.status}")
                except Exception:
                    print(repr(a))
        elif op == '2':
            id_str = _input("ID do anúncio para excluir: ").strip()
            try:
                aid = int(id_str)
            except Exception:
                print("ID inválido.")
                continue
            ok = current_user.excluirAnuncio(aid)
            if ok:
                # remover da lista global de anúncios também
                anuncio = next((x for x in anuncioList if x.id == aid), None)
                if anuncio:
                    anuncioList.remove(anuncio)
                print("Anúncio excluído.")
            else:
                print("Anúncio não encontrado ou erro.")
        elif op == '0':
            break
        else:
            print("Opção inválida.")


def search_announcements(current_user):
    # Clientes should be able to search anúncios
    if not current_user or not hasattr(current_user, 'buscarVeiculos'):
        print("Acesso negado. Apenas clientes.")
        return
    filtro = _input("Filtro (marca/modelo): ").strip()
    resultados = [a for a in anuncioList if filtro.lower() in a.veiculo.marca.lower() or filtro.lower() in a.veiculo.modelo.lower()]
    if not resultados:
        print("Nenhum anúncio encontrado.")
        return
    for a in resultados:
        v = a.veiculo
        print(f"ID anúncio:{a.id} | Veículo: {v.marca} {v.modelo} ({v.ano}) | Anunciante: {getattr(a.anunciante,'nome','Desconhecido')} | Status: {a.status}")
    escolha = _input("Ver detalhes do anúncio ID? (vazio para voltar): ").strip()
    if escolha:
        try:
            aid = int(escolha)
            a = next((x for x in anuncioList if x.id == aid), None)
            if a:
                print(a.exibirResumo())
            else:
                print("Anúncio não encontrado.")
        except Exception:
            print("Entrada inválida.")


def admin_manage_flow(current_user):
    if not current_user or not isinstance(current_user, Admin):
        print("Acesso negado. Área restrita a administradores.")
        return
    while True:
        print("\n--- Painel do Admin ---")
        print("1. Listar anúncios pendentes")
        print("2. Aprovar anúncio")
        print("3. Rejeitar anúncio")
        print("4. Gerenciar usuários (listar/excluir)")
        print("0. Voltar")
        op = _input("Escolha: ").strip()
        if op == '1':
            pendentes = [a for a in anuncioList if a.status.lower() == 'pendente']
            if not pendentes:
                print("Nenhum anúncio pendente.")
            for a in pendentes:
                v = a.veiculo
                print(f"ID:{a.id} | {v.marca} {v.modelo} ({v.ano}) | Anunciante: {getattr(a.anunciante,'nome', 'Desconhecido')}")
        elif op in ('2', '3'):
            id_str = _input("ID do anúncio: ").strip()
            try:
                aid = int(id_str)
            except Exception:
                print("ID inválido.")
                continue
            anuncio = next((x for x in anuncioList if x.id == aid), None)
            if not anuncio:
                print("Anúncio não encontrado.")
                continue
            if op == '2':
                current_user.aprovarAnuncio(anuncio)
                print("Anúncio aprovado.")
            else:
                current_user.rejeitarAnuncio(anuncio)
                print("Anúncio rejeitado.")
        elif op == '4':
            print("Usuários cadastrados:")
            for idx, u in enumerate(userList, start=1):
                print(f"{idx}. {getattr(u,'nome', repr(u))} ({u.__class__.__name__})")
            escolha = _input("Excluir usuário número (vazio para voltar): ").strip()
            if not escolha:
                continue
            try:
                ui = int(escolha)-1
                usuario = userList[ui]
            except Exception:
                print("Escolha inválida.")
                continue
            msg = current_user.gerenciarUsuario('deletar', usuario, None, userList)
            # também remover de listas específicas
            if usuario in anuncianteList:
                anuncianteList.remove(usuario)
            if usuario in clienteList:
                clienteList.remove(usuario)
            if usuario in adminList:
                adminList.remove(usuario)
            print(msg)
        elif op == '0':
            break
        else:
            print("Opção inválida.")

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
    # legacy: keep signature without owner for compatibility
    print("--- Cadastrar Veículo (use o fluxo do usuário logado) ---")
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
    if escolha == 's':
        meus = [v for v in veiculoList if getattr(v, 'anunciante', None) == current_user]
        if not meus:
            print("Você não possui veículos cadastrados. Crie um novo.")
            v = None
        else:
            for idx, v0 in enumerate(meus, start=1):
                print(f"{idx}: {v0.marca} {v0.modelo} ({v0.ano}) - {v0.quilometragem}km - {v0.preco}")
            sel = _input("Escolha número do veículo: ").strip()
            try:
                v = meus[int(sel)-1]
            except Exception:
                print("Seleção inválida.")
                return
    else:
        # criar veículo pertencente ao anunciante
        marca = _input("Marca: ").strip()
        modelo = _input("Modelo: ").strip()
        ano = _input("Ano: ").strip()
        preco = _input("Preço: ").strip()
        km = _input("Quilometragem: ").strip()
        try:
            v = CreateVeiculo(marca, modelo, ano, preco, km, anunciante=current_user)
            veiculoList.append(v)
        except Exception as e:
            print("Erro ao criar veículo:", e)
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


def list_my_vehicles(current_user):
    print("--- Meus Veículos ---")
    if not current_user or not hasattr(current_user, 'criarAnuncio'):
        print("Acesso negado. Apenas anunciantes.")
        return
    meus = [v for v in veiculoList if getattr(v, 'anunciante', None) == current_user]
    if not meus:
        print("Você não possui veículos cadastrados.")
        return
    for v in meus:
        print(f"ID:{v.id} | {v.marca} {v.modelo} ({v.ano}) - {v.quilometragem}km - {v.preco}")


def main():
    current_user = None
    while True:
        print("\n=== Catálogo de Veículos ===")
        print("1. Cadastrar usuário")
        print("2. Login")
        print("3. Cadastrar veículo")
        print("4. Criar anúncio (anunciantes)")
        print("5. Listar anúncios")
        print("6. Listar meus veículos (anunciantes)")
        print("7. Logout")
        print("8. Gerenciar meus anúncios (anunciantes)")
        print("9. Buscar veículos (clientes)")
        print("10. Painel Admin")
        print("0. Sair")
        opc = _input("Escolha uma opção: ").strip()
        if opc == '1':
            register_user_flow()
        elif opc == '2':
            user = login_flow()
            if user:
                current_user = user
        elif opc == '3':
            # Cadastrar veículo: apenas anunciantes logados
            if not current_user or not hasattr(current_user, 'criarAnuncio'):
                print("Apenas anunciantes podem cadastrar veículos.")
            else:
                print("--- Cadastrar Veículo ---")
                marca = _input("Marca: ").strip()
                modelo = _input("Modelo: ").strip()
                ano = _input("Ano: ").strip()
                preco = _input("Preço: ").strip()
                km = _input("Quilometragem: ").strip()
                try:
                    v = CreateVeiculo(marca, modelo, ano, preco, km, anunciante=current_user)
                    veiculoList.append(v)
                    print(f"Veículo criado: {v.marca} {v.modelo}")
                except Exception as e:
                    print("Erro ao criar veículo:", e)
        elif opc == '4':
            create_ad_flow(current_user)
        elif opc == '5':
            list_announcements()
        elif opc == '6':
            list_my_vehicles(current_user)
        elif opc == '8':
            anunciante_manage_flow(current_user)
        elif opc == '9':
            search_announcements(current_user)
        elif opc == '10':
            admin_manage_flow(current_user)
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

