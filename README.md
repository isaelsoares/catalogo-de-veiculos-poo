# 🚗 Catálogo de Veículos - Sistema POO

## 📋 Sobre o Projeto

Este projeto implementa um **Sistema de Catálogo de Veículos** completo desenvolvido em Python utilizando os conceitos fundamentais de **Programação Orientada a Objetos (POO)** e **persistência de dados com SQLite**. O sistema simula uma plataforma de anúncios de veículos onde diferentes tipos de usuários podem interagir:

- **Clientes**: Buscam e visualizam veículos disponíveis
- **Anunciantes**: Cadastram veículos e criam anúncios
- **Administradores**: Gerenciam usuários e aprovam/rejeitam anúncios

## ✨ Funcionalidades do Sistema

### 👤 Para Todos os Usuários
- ✅ Cadastro de novos usuários (Anunciantes ou Clientes)
- ✅ Sistema de login/logout
- ✅ Validação de CPF e email únicos
- ✅ Proteção de senhas

### 🏢 Para Anunciantes
- ✅ Cadastrar veículos com informações detalhadas
- ✅ Criar anúncios dos veículos cadastrados
- ✅ Listar todos os seus veículos
- ✅ Gerenciar anúncios (editar, excluir)
- ✅ Visualizar status dos anúncios (Pendente, Aprovado, Rejeitado)

### 🔍 Para Clientes
- ✅ Buscar veículos por marca/modelo
- ✅ Visualizar anúncios aprovados
- ✅ Ver detalhes completos dos anúncios
- ✅ Histórico de pesquisas salvo

### 👨‍💼 Para Administradores
- ✅ Visualizar anúncios pendentes
- ✅ Aprovar ou rejeitar anúncios
- ✅ Gerenciar usuários (listar e excluir)
- ✅ Controle total sobre a plataforma

## 🎯 Conceitos de POO Utilizados

### 1. **Encapsulamento**

- Uso de atributos privados (prefixo `_`) em todas as classes
- Implementação de `@property` e `@setter` para controlar acesso aos atributos
- Exemplo na classe `Veiculo`: atributos como `_marca`, `_modelo`, `_preco` são encapsulados e acessados via properties

### 2. **Herança**

- Classe abstrata `Usuario` como base para `Anunciante` e `Admin`
- Reutilização de código através da herança
- Especialização de comportamentos nas classes filhas

### 3. **Abstração**

- Uso de classes abstratas (`ABC`) e métodos abstratos (`@abstractmethod`)
- Interface comum definida em `Usuario` com método `exibirPerfil()` abstrato
- Cada classe concreta implementa seu próprio comportamento

### 4. **Polimorfismo**

- Método `exibirPerfil()` implementado de forma diferente em cada classe
- Mesmo método, comportamentos distintos dependendo do tipo de objeto

### 5. **Composição**

- Classe `Anuncio` composta por objetos `Veiculo` e `Anunciante`
- Relacionamento "tem-um" entre classes

### 6. **Validações**

- Validações em setters (ex: nome não pode ser vazio, senha mínima de 6 caracteres)
- Tratamento de exceções (`ValueError`, `KeyError`)

## 📊 Modelo de Classes

O sistema foi desenvolvido com base no modelo do arquivo _diagrama-de-classes.drawio.pdf_

## 🏗️ Estrutura do Projeto

```
catalogo-de-veiculos-poo/
│
├── models/                  # Classes do domínio
│   ├── Vehicle.py          # Classe Veiculo
│   ├── User.py             # Classe abstrata Usuario
│   ├── Client.py           # Classe Cliente
│   ├── Announcer.py        # Classe Anunciante (herda de Usuario)
│   ├── Admin.py            # Classe Admin (herda de Usuario)
│   └── Advertisement.py    # Classe Anuncio
│
├── database.py             # Gerenciamento do banco SQLite
├── repository.py           # Camada de acesso aos dados (Repositories)
├── init_db.py             # Script de criação das tabelas
├── demo_database.py        # Script para popular banco com dados de exemplo
│
├── main.py                 # Aplicação principal (interface CLI)
├── interface.py            # Interface gráfica (opcional)
├── test.py                 # Testes completos do sistema
│
├── requirements.txt        # Dependências do projeto
├── README.md              # Este arquivo
└── README_DATABASE.md     # Documentação do banco de dados
```

## 🚀 Como Executar o Projeto

### Pré-requisitos

- **Python 3.10 ou superior** instalado
- **SQLite3** (já incluído na biblioteca padrão do Python)
- **Git** (para clonar o repositório)

### Passo 1: Clonar o Repositório

```bash
git clone https://github.com/isaelsoares/catalogo-de-veiculos-poo.git
cd catalogo-de-veiculos-poo
```

### Passo 2: Instalar Dependências (Opcional)

Se desejar usar a interface gráfica (`interface.py`), instale as dependências:

```bash
pip install -r requirements.txt
```

### Passo 3: Executar o Sistema

**Opção 1: Executar com banco vazio**
```bash
python main.py
```

**Opção 2: Popular banco com dados de exemplo**
```bash
python demo_database.py
python main.py
```

O arquivo `demo_database.py` cria usuários e anúncios de exemplo para facilitar os testes:
- **Admin**: admin@sistema.com / senha: admin123
- **Anunciante**: joao@email.com / senha: senha123
- **Cliente**: maria@email.com / senha: senha123

### Passo 4: Navegação no Sistema

Após executar `main.py`, você verá o menu principal:

```
=== Catálogo de Veículos ===
1. Cadastrar usuário
2. Login
3. Cadastrar veículo
4. Criar anúncio (anunciantes)
5. Listar anúncios
6. Listar meus veículos (anunciantes)
7. Logout
8. Gerenciar meus anúncios (anunciantes)
9. Buscar veículos (clientes)
10. Painel Admin
0. Sair
```

#### Fluxo Recomendado para Teste:

1. **Cadastre um usuário** (opção 1)
   - Escolha tipo: 1 para Anunciante ou 2 para Cliente
   - Informe CPF, nome, email e senha

2. **Faça login** (opção 2)
   - Use o email e senha cadastrados

3. **Como Anunciante:**
   - Cadastre veículos (opção 3)
   - Crie anúncios dos veículos (opção 4)
   - Gerencie seus anúncios (opção 8)

4. **Como Cliente:**
   - Busque veículos (opção 9)
   - Visualize anúncios aprovados (opção 5)

5. **Como Admin:**
   - Acesse o painel admin (opção 10)
   - Aprove ou rejeite anúncios pendentes
   - Gerencie usuários

### Passo 5: Executar Testes

O projeto inclui testes completos em `test.py`:

```bash
python test.py
```

Os testes validam:
- ✅ Criação de veículos com dados válidos e inválidos
- ✅ Funcionalidades de busca e visualização
- ✅ Criação, listagem e exclusão de anúncios
- ✅ Aprovação e rejeição por administradores
- ✅ Autenticação e gerenciamento de usuários
- ✅ Validações de dados (senhas, CPF único, etc.)

## 🗄️ Banco de Dados

O sistema utiliza **SQLite** para persistência de dados com as seguintes tabelas:

- **usuarios**: Dados comuns (CPF, nome, email, senha, tipo)
- **admins**: Dados específicos de administradores
- **anunciantes**: Dados específicos (telefone)
- **clientes**: Dados específicos dos clientes
- **veiculos**: Informações dos veículos
- **anuncios**: Anúncios com status (Pendente/Aprovado/Rejeitado)
- **historico_pesquisas**: Buscas realizadas pelos clientes

Para mais detalhes sobre o esquema do banco, consulte `README_DATABASE.md`.

## 📚 Exemplos de Uso Programático

### Criar e Gerenciar Veículos

```python
from models.Vehicle import Veiculo

# Criar veículo
carro = Veiculo("Honda", "Civic", 2019, 75000.00, 40000)

# Acessar propriedades
print(f"Marca: {carro.marca}")https://github.com/isaelsoares/catalogo-de-veiculos-poo/blob/master/README.md
print(f"Preço: R${carro.preco:.2f}")

# Modificar atributos
carro.preco = 73000.00
carro.quilometragem = 42000

# Exibir informações completas
print(carro.exibirInformacoes())
```

### Sistema de Anúncios

```python
from models.Announcer import Anunciante
from models.Advertisement import Anuncio
from models.Vehicle import Veiculo

# Criar anunciante
anunciante = Anunciante(
    cpf=12345678900,
    nome="Maria Santos",
    email="maria@email.com",
    senha="senha123",
    telefone="(21) 99999-8888"
)

# Criar veículo
veiculo = Veiculo("Ford", "Ka", 2018, 35000, 45000)

# Publicar anúncio
anuncio = anunciante.criarAnuncio(veiculo)

# Listar anúncios do anunciante
meus_anuncios = anunciante.listarMeusAnuncios()
print(f"Total de anúncios: {len(meus_anuncios)}")
```

### Busca de Veículos

```python
from models.Client import Cliente
from models.Vehicle import Veiculo

# Criar lista de veículos
veiculos = [
    Veiculo("Toyota", "Corolla", 2020, 85000, 50000),
    Veiculo("Honda", "Civic", 2019, 75000, 40000),
    Veiculo("Toyota", "Hilux", 2021, 150000, 20000)
]

# Cliente busca veículos
cliente = Cliente()
resultados = cliente.buscarVeiculos("Toyota", veiculos)

print(f"Encontrados {len(resultados)} veículo(s):")
for v in resultados:
    print(f"- {v.marca} {v.modelo} ({v.ano})")

# Ver histórico de pesquisas
print(f"Histórico: {cliente.historicoPesquisas}")
```

## 🔒 Segurança e Validações

O sistema implementa diversas validações:

- **CPF único**: Não permite cadastro duplicado
- **Email único**: Validação de unicidade
- **Senha**: Mínimo de 6 caracteres
- **Nome**: Não pode ser vazio
- **Preço e KM**: Devem ser valores numéricos positivos
- **Ano**: Validação de formato
- **Controle de acesso**: Funcionalidades restritas por tipo de usuário

## 🧪 Testes e Validação

O arquivo `test.py` contém mais de 50 casos de teste automatizados cobrindo:

1. **Classe Veiculo**: Criação, validações, tipos de dados
2. **Classe Cliente**: Busca, visualização, histórico de pesquisas
3. **Classe Anunciante**: Criação de anúncios, validações de telefone/nome
4. **Classe Anuncio**: Aprovação, rejeição, alteração de status
5. **Classe Admin**: Gerenciamento de usuários, aprovação de anúncios, login
6. **Persistência**: Salvamento e recuperação de dados do SQLite
7. **Integridade**: Constraints de banco (CPF único, email único)

## 🎓 Aprendizados do Projeto

Este projeto demonstra:

- ✨ Estruturação de código orientado a objetos
- 🔒 Encapsulamento e proteção de dados
- 🧬 Herança e reutilização de código
- 🎭 Polimorfismo através de métodos abstratos
- 🔗 Composição de objetos
- ✅ Validação e tratamento de erros
- 🗄️ Persistência de dados com SQLite
- 🏗️ Padrão Repository para acesso a dados
- 🔐 Controle de acesso e autenticação
- 🧪 Testes de software

## 🐛 Solução de Problemas

### Erro: "UNIQUE constraint failed: usuarios.cpf"
Este erro ocorre quando você tenta cadastrar um CPF que já existe no banco. Use um CPF diferente ou limpe o banco de dados deletando o arquivo `catalogo_veiculos.db`.

### Banco de dados não inicializa
Se o sistema não criar as tabelas automaticamente, execute:
```bash
python init_db.py
```

### Resetar banco de dados
Para limpar todos os dados e recomeçar:
```bash
# No Windows PowerShell
Remove-Item catalogo_veiculos.db -ErrorAction SilentlyContinue
python demo_database.py
```

## 👥 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

## 📝 Licença

Este projeto foi desenvolvido para fins educacionais.
