# Catálogo de Veículos - Sistema POO com SQLite

Este projeto implementa um sistema de catálogo de veículos usando Programação Orientada a Objetos (POO) e banco de dados SQLite.

## Estrutura do Projeto

```
catalogo-de-veiculos-poo/
│
├── models/                 # Classes do domínio
│   ├── User.py            # Classe base Usuario
│   ├── Admin.py           # Administrador
│   ├── Announcer.py       # Anunciante
│   ├── Client.py          # Cliente
│   ├── Vehicle.py         # Veículo
│   └── Advertisement.py   # Anúncio
│
├── database.py            # Gerenciamento do banco SQLite
├── repository.py          # Camada de persistência (repositórios)
├── init_db.py            # Script para inicializar o banco
├── main.py               # Aplicação principal (CLI)
├── interface.py          # Interface adicional
└── test.py              # Testes
```

## Recursos

- ✅ Persistência de dados com SQLite
- ✅ Gerenciamento de usuários (Admin, Anunciante, Cliente)
- ✅ Cadastro e gerenciamento de veículos
- ✅ Sistema de anúncios com aprovação
- ✅ Histórico de pesquisas para clientes
- ✅ Padrão Repository para acesso aos dados

## Instalação

### Pré-requisitos

- Python 3.10 ou superior
- SQLite3 (geralmente já incluído no Python)

### Passo 1: Clonar o repositório

```bash
git clone https://github.com/isaelsoares/catalogo-de-veiculos-poo.git
cd catalogo-de-veiculos-poo
```

### Passo 2: Inicializar o banco de dados

Execute o script de inicialização:

```bash
python init_db.py
```

Este comando irá:
- Criar o banco de dados `catalogo_veiculos.db`
- Criar todas as tabelas necessárias
- Inserir o usuário administrador padrão:
  - Email: `admin@admin.com`
  - Senha: `admin123`

### Passo 3: Executar a aplicação

```bash
python main.py
```

## Uso

### Login como Administrador

1. Execute `python main.py`
2. Escolha a opção **2. Login**
3. Use as credenciais:
   - Email: `admin@admin.com`
   - Senha: `admin123`

### Funcionalidades por Tipo de Usuário

#### Cliente
- Buscar veículos por marca/modelo
- Visualizar anúncios aprovados
- Histórico de pesquisas salvo automaticamente

#### Anunciante
- Cadastrar veículos
- Criar anúncios
- Gerenciar próprios anúncios
- Ver lista de veículos cadastrados

#### Administrador
- Aprovar/Rejeitar anúncios
- Gerenciar usuários
- Visualizar todos os anúncios pendentes

## Banco de Dados

### Estrutura das Tabelas

**usuarios**
- id, cpf, nome, email, senha, tipo, logado

**admins**
- usuario_id, admin_id

**anunciantes**
- usuario_id, telefone

**clientes**
- usuario_id

**veiculos**
- id, marca, modelo, ano, preco, quilometragem, anunciante_id

**anuncios**
- id, data_publicacao, status, veiculo_id, anunciante_id

**historico_pesquisas**
- id, cliente_id, filtro, data_pesquisa

### Resetar o Banco de Dados

Para apagar todos os dados e reinicializar:

```bash
python init_db.py --reset
```

## Arquitetura

### Camadas

1. **Models** (`models/`): Classes de domínio com lógica de negócio
2. **Database** (`database.py`): Gerenciamento de conexões SQLite
3. **Repository** (`repository.py`): Padrão Repository para persistência
4. **Main** (`main.py`): Interface CLI e fluxo da aplicação

### Padrões Utilizados

- **Singleton**: Classe Database
- **Repository Pattern**: Separação entre lógica de negócio e persistência
- **Herança**: Hierarquia de usuários (Usuario -> Admin/Anunciante/Cliente)
- **Encapsulamento**: Properties para acesso controlado aos atributos

## Exemplos de Uso

### Cadastrar um Anunciante

```python
from repository import UsuarioRepository
from models.Announcer import Anunciante

repo = UsuarioRepository()
anunciante = Anunciante(
    cpf=12345678900,
    nome="João Silva",
    email="joao@example.com",
    senha="senha123",
    telefone="11999999999"
)
usuario_id = repo.salvar(anunciante, 'anunciante', {'telefone': '11999999999'})
```

### Buscar Veículos

```python
from repository import VeiculoRepository

repo = VeiculoRepository()
veiculos = repo.buscar("honda")  # Busca por marca ou modelo
```

## Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

## Licença

Este projeto é educacional e pode ser usado livremente para fins de aprendizado.

## Contato

Isael Soares - [@isaelsoares](https://github.com/isaelsoares)

Link do Projeto: [https://github.com/isaelsoares/catalogo-de-veiculos-poo](https://github.com/isaelsoares/catalogo-de-veiculos-poo)
