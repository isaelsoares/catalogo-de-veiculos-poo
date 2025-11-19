# 🚗 Catálogo de Veículos - Sistema POO

## 📋 Sobre o Projeto

Este projeto implementa um **Sistema de Catálogo de Veículos** desenvolvido em Python utilizando os conceitos fundamentais de **Programação Orientada a Objetos (POO)**. O sistema simula uma plataforma de anúncios de veículos onde diferentes tipos de usuários podem interagir: clientes buscam veículos, anunciantes publicam anúncios e administradores gerenciam o sistema.

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
├── models/
│   ├── Vehicle.py          # Classe Veiculo
│   ├── User.py             # Classe abstrata Usuario
│   ├── Client.py           # Classe Cliente
│   ├── Announcer.py        # Classe Anunciante (herda de Usuario)
│   ├── Admin.py            # Classe Admin (herda de Usuario)
│   └── Advertisement.py    # Classe Anuncio
│
├── main.py                 # Arquivo principal (exemplo de uso)
├── test.py                 # Testes completos do sistema
└── README.md               # Este arquivo
```

## 🚀 Como Clonar e Executar

### Pré-requisitos

- Python 3.8 ou superior instalado
- Git instalado (para clonar o repositório)

### Passo 1: Clonar o Repositório

```bash
git clone https://github.com/isaelsoares/catalogo-de-veiculos-poo.git
cd catalogo-de-veiculos-poo
```

### Passo 2: Executar os Testes

O projeto inclui um arquivo `test.py` com uma bateria completa de testes para validar todas as funcionalidades:

```bash
python test.py
```

O arquivo de testes irá:

- ✅ Testar criação de veículos com dados válidos e inválidos
- ✅ Validar funcionalidades de busca e visualização de clientes
- ✅ Testar criação, listagem e exclusão de anúncios
- ✅ Validar aprovação e rejeição de anúncios por administradores
- ✅ Testar autenticação e gerenciamento de usuários
- ✅ Verificar validações de dados (senhas, nomes vazios, etc.)

### Passo 3: Teste Manual das Classes

Você também pode testar as classes individualmente no interpretador Python:

```bash
python3
```

Depois, no interpretador Python:

```python
# Importar as classes
from models.Vehicle import Veiculo
from models.Client import Cliente
from models.Announcer import Anunciante
from models.Advertisement import Anuncio
from models.Admin import Admin

# Criar um veículo
veiculo = Veiculo("Toyota", "Corolla", 2020, 85000.00, 50000)
print(veiculo.exibirInformacoes())

# Criar um cliente e buscar veículos
cliente = Cliente()
veiculos = [veiculo]
resultados = cliente.buscarVeiculos("Toyota", veiculos)
print(f"Encontrados: {len(resultados)} veículo(s)")

# Criar um anunciante e publicar anúncio
anunciante = Anunciante(12345678900, "João Silva", "joao@email.com", "senha123", "(11) 98765-4321")
anuncio = anunciante.criarAnuncio(veiculo)
print(anuncio.exibirResumo())

# Criar admin e aprovar anúncio
admin = Admin(1, 99999999999, "Admin", "admin@sistema.com", "admin123", 1001)
admin.aprovarAnuncio(anuncio)
print(f"Status do anúncio: {anuncio.status}")
```

## 📚 Exemplos de Uso

### Criar e Gerenciar Veículos

```python
from models.Vehicle import Veiculo

# Criar veículo
carro = Veiculo("Honda", "Civic", 2019, 75000.00, 40000)

# Acessar propriedades
print(f"Marca: {carro.marca}")
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

## 🧪 Testes Disponíveis

O arquivo `test.py` contém mais de 50 casos de teste cobrindo:

1. **Classe Veiculo**: criação, validações, tipos de dados
2. **Classe Cliente**: busca, visualização, histórico
3. **Classe Anunciante**: criação de anúncios, validações de telefone/nome
4. **Classe Anuncio**: aprovação, rejeição, alteração de status
5. **Classe Admin**: gerenciamento de usuários, aprovação de anúncios, login

## 🎓 Aprendizados do Projeto

Este projeto demonstra:

- ✨ Estruturação de código orientado a objetos
- 🔒 Encapsulamento e proteção de dados
- 🧬 Herança e reutilização de código
- 🎭 Polimorfismo através de métodos abstratos
- 🔗 Composição de objetos
- ✅ Validação e tratamento de erros
- 🧪 Testes de software

## 📝 Licença

Este projeto foi desenvolvido para fins educacionais.