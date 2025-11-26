# README - Interface Gráfica (GUI)

## 📋 Visão Geral

A interface gráfica do Catálogo de Veículos foi desenvolvida utilizando **Tkinter**, a biblioteca padrão do Python para criação de interfaces gráficas. A implementação segue os princípios de **Programação Orientada a Objetos (POO)** e se integra perfeitamente com o sistema de persistência em banco de dados SQLite.

## 🏗️ Arquitetura da Interface

### Estrutura Principal

A interface é implementada através da classe `App` localizada no arquivo `interface.py`, que gerencia toda a lógica de apresentação e interação com o usuário.

```
interface.py
├── PlaceholderEntry (Classe auxiliar)
└── App (Classe principal)
    ├── Frames de navegação
    ├── Sistema de estilos
    └── Métodos de interação
```

## 🎨 Componentes Principais

### 1. **PlaceholderEntry - Campo com Placeholder**

Classe personalizada que estende `tk.Entry` para adicionar funcionalidade de placeholder (texto de sugestão).

**Características:**

- Exibe texto de sugestão quando o campo está vazio
- Remove o placeholder quando o usuário foca no campo
- Suporta campos de senha (caracteres ocultos)
- Método `get_value()` retorna apenas o valor real (sem o placeholder)

```python
class PlaceholderEntry(tk.Entry):
    def __init__(self, master=None, placeholder="", **kwargs):
        # Implementa placeholder com cores diferentes
        # Gerencia foco (FocusIn/FocusOut)
```

### 2. **Sistema de Estilos (`_setup_styles`)**

Utiliza `ttk.Style` para criar botões modernos com cores temáticas:

| Estilo              | Cor Base               | Uso                                     |
| ------------------- | ---------------------- | --------------------------------------- |
| `Primary.TButton`   | Azul (#3498db)         | Ações principais (Login, Buscar)        |
| `Success.TButton`   | Verde (#2ecc71)        | Ações de confirmação (Cadastrar, Criar) |
| `Danger.TButton`    | Vermelho (#e74c3c)     | Ações críticas (Sair, Logout)           |
| `Secondary.TButton` | Cinza (#95a5a6)        | Ações secundárias (Cancelar)            |
| `TButton`           | Cinza escuro (#34495e) | Ações padrão                            |

### 3. **Frames de Navegação**

A interface utiliza múltiplos frames que são alternados conforme a navegação do usuário:

#### **Login Frame** (`login_frame`)

- Tela inicial do sistema
- Campos: email e senha
- Botões: Entrar, Cadastrar, Sair

#### **Main Frame** (`main_frame`)

- Menu principal após login
- Botões dinâmicos baseados no tipo de usuário
- Adapta-se aos perfis: Cliente, Anunciante, Admin

#### **Register Frame** (`register_frame`)

- Formulário de cadastro de usuário
- Campos: CPF, nome, email, senha, telefone (condicional)
- Radio buttons para escolher tipo (Anunciante/Cliente)

#### **Vehicle Frame** (`vehicle_frame`)

- Formulário de cadastro de veículo
- Campos: marca, modelo, ano, preço, quilometragem
- Apenas para anunciantes

## 🔄 Fluxo de Navegação

```
┌─────────────┐
│ Login Frame │
└──────┬──────┘
       │
       ├──→ Cadastrar ──→ Register Frame ──→ Login Frame
       │
       └──→ Entrar ──→ Main Frame
                        │
                        ├──→ Cadastrar Veículo ──→ Vehicle Frame
                        ├──→ Criar Anúncio
                        ├──→ Gerenciar Anúncios
                        ├──→ Buscar Anúncios
                        ├──→ Painel Admin (apenas Admin)
                        └──→ Logout ──→ Login Frame
```

## 🎭 Controle de Acesso por Perfil

A interface implementa um sistema dinâmico de exibição de botões baseado no tipo de usuário logado através do método `update_main_buttons()`:

### **Todos os Usuários**

- ✅ Cadastrar usuário
- ✅ Listar anúncios
- ✅ Logout

### **Cliente**

- ✅ Buscar veículos
- ❌ Criar/gerenciar anúncios
- ❌ Cadastrar veículos

### **Anunciante**

- ✅ Cadastrar veículo
- ✅ Criar anúncio
- ✅ Gerenciar meus anúncios
- ✅ Listar meus veículos
- ❌ Painel Admin

### **Administrador**

- ✅ Painel Admin
- ✅ Aprovar/Rejeitar anúncios
- ✅ Gerenciar usuários
- ✅ Cadastrar veículo

## 🔐 Segurança e Validações

### Validações no Cadastro de Usuário

```python
# Email
if '@' not in email or '.' not in email:
    messagebox.showerror('Validação', 'Email inválido.')

# Senha
if len(senha) < 6:
    messagebox.showerror('Validação', 'Senha deve ter ao menos 6 caracteres.')
```

### Validações no Cadastro de Veículo

```python
# Ano (entre 1886 e 2025)
if ano_int < 1886 or ano_int > 2025:
    raise ValueError()

# Preço (maior que 0)
if preco_f <= 0:
    raise ValueError()

# Quilometragem (não negativa)
if km_int < 0:
    raise ValueError()
```

## 🎯 Funcionalidades Principais

### 1. **Sistema de Login**

```python
def login_from_entries(self):
    email = self.email_entry.get_value().strip()
    senha = self.senha_entry.get_value().strip()
    user = main.Login(email, senha)
    if user:
        self.current_user = user
        # Atualiza interface para mostrar apenas opções permitidas
        self.update_main_buttons()
```

### 2. **Cadastro de Usuário**

- Seleção de tipo (Anunciante/Cliente)
- Campo telefone condicional (apenas para Anunciante)
- Validação de dados
- Integração com repositórios do banco de dados

### 3. **Gestão de Veículos**

- Cadastro com validações robustas
- Listagem de veículos do anunciante
- Vínculo automático ao anunciante logado

### 4. **Gestão de Anúncios**

**Para Anunciantes:**

- Criar anúncio (veículo novo ou existente)
- Listar anúncios próprios
- Excluir anúncios

**Para Clientes:**

- Buscar anúncios por marca/modelo
- Ver detalhes dos anúncios
- Histórico de pesquisas salvo no banco

**Para Admins:**

- Listar anúncios pendentes
- Aprovar/rejeitar anúncios
- Gerenciar usuários

### 5. **Janelas Modais (Toplevel)**

```python
top = tk.Toplevel(self.root)
top.title('Título da Janela')
# Usado para: listagens, buscas, painel admin
```

## 🎨 Design e Experiência do Usuário

### Tela Cheia

```python
self.root.attributes('-fullscreen', True)
self.root.bind('<Escape>', lambda e: self.root.attributes('-fullscreen', False))
```

- Interface ocupa toda a tela
- Tecla ESC permite sair do modo tela cheia

### Imagem de Fundo (Opcional)

```python
bg_image = Image.open('background.png')
bg_image = bg_image.resize((screen_w, screen_h), Image.Resampling.LANCZOS)
self.bg_photo = ImageTk.PhotoImage(bg_image)
```

- Suporte a imagem de fundo decorativa
- Redimensionamento automático
- Fallback para cor sólida se imagem não existir

### Status do Usuário

```python
def _update_status(self):
    if self.current_user:
        self.status.config(text=f'Logado como: {self.current_user.nome} ({self.current_user.__class__.__name__})')
```

- Barra de status mostra usuário logado e tipo
- Oculta quando não há usuário logado

## 🔗 Integração com Backend

A interface se comunica com o sistema através do módulo `main.py`, que fornece funções de alto nível:

```python
import main

# Login
user = main.Login(email, senha)

# Criar usuário
user = main.CreateAnunciante(cpf, nome, email, senha, telefone)
user = main.CreateCliente(cpf, nome, email, senha)

# Criar veículo
v = main.CreateVeiculo(marca, modelo, ano, preco, km, anunciante)

# Criar anúncio
main.AnuncianteCriarAnuncio(anunciante, veiculo)
```

### Integração com Repositórios

A interface utiliza os repositórios para operações diretas no banco de dados:

```python
from repository import VeiculoRepository, AnuncioRepository, ClienteRepository

veiculo_repo = VeiculoRepository()
anuncio_repo = AnuncioRepository()
cliente_repo = ClienteRepository()

# Buscar veículos do anunciante
meus = veiculo_repo.listar_por_anunciante(self.current_user.id)

# Atualizar status de anúncio
anuncio_repo.atualizar_status(aid, 'Aprovado')

# Salvar pesquisa do cliente
cliente_repo.salvar_pesquisa(current_user.id, filtro)
```

## 📦 Dependências

```python
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from PIL import Image, ImageTk  # Para imagem de fundo (opcional)
```

## 🚀 Execução

### Interface Gráfica

```bash
python interface.py
```

### Interface CLI (Terminal)

```bash
python main.py
```

## 💡 Decisões de Design

### 1. **Por que Tkinter?**

- ✅ Biblioteca padrão do Python (sem instalação adicional)
- ✅ Multiplataforma (Windows, Linux, macOS)
- ✅ Leve e rápida
- ✅ Adequada para aplicações desktop de médio porte

### 2. **Frames Intercambiáveis**

- Permite navegação fluida sem abrir múltiplas janelas
- Mantém estado da aplicação centralizado
- Economiza recursos do sistema

### 3. **Validações Cliente-Servidor**

- Validações imediatas na interface (UX)
- Validações adicionais no backend (segurança)
- Mensagens de erro claras e específicas

### 4. **Controle Dinâmico de Botões**

```python
# Esconde botões não autorizados
self.btn_admin_panel.grid_remove()

# Exibe apenas botões permitidos
if isinstance(self.current_user, Admin):
    self.btn_admin_panel.grid()
```

### 5. **Janelas Modais para Visualizações**

- Listagens e buscas abrem em janelas separadas
- Não interferem no fluxo principal
- Podem ser fechadas independentemente

## 🐛 Tratamento de Erros

A interface implementa tratamento de exceções robusto:

```python
try:
    v = main.CreateVeiculo(marca, modelo, ano, preco, km, anunciante)
    messagebox.showinfo('Veículo', f'Veículo cadastrado: {v.marca} {v.modelo}')
except ValueError as e:
    messagebox.showerror('Validação', str(e))
except Exception as e:
    messagebox.showerror('Erro', f'Erro ao cadastrar veículo: {e}')
```

## 📊 Melhorias Futuras

- [ ] Adicionar filtros avançados de busca
- [ ] Implementar edição de veículos e anúncios
- [ ] Upload de imagens dos veículos
- [ ] Relatórios e dashboards para admin
- [ ] Sistema de notificações
- [ ] Tema escuro/claro
- [ ] Múltiplos idiomas

## 🎓 Conceitos de POO Aplicados

1. **Encapsulamento**: Classe `App` encapsula toda lógica da interface
2. **Herança**: `PlaceholderEntry` herda de `tk.Entry`
3. **Polimorfismo**: Métodos diferentes para cada tipo de usuário
4. **Abstração**: Interface simplifica operações complexas do backend

## 📝 Conclusão

A interface gráfica do Catálogo de Veículos foi projetada para ser:

- **Intuitiva**: Navegação clara e lógica
- **Segura**: Validações e controle de acesso
- **Responsiva**: Feedback imediato ao usuário
- **Manutenível**: Código organizado e bem documentado
- **Escalável**: Fácil adicionar novas funcionalidades

O uso de Tkinter combinado com POO resultou em uma aplicação desktop completa, integrada com banco de dados e pronta para uso em ambiente de produção.
