import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from PIL import Image, ImageTk
import main
import os


class PlaceholderEntry(tk.Entry):
    """Entry com placeholder simples"""
    def __init__(self, master=None, placeholder="", **kwargs):
        self.placeholder = placeholder
        self.placeholder_color = 'grey'
        self.default_fg_color = kwargs.pop('fg', 'black')
        self.show_char = kwargs.pop('show', '')
        
        super().__init__(master, fg=self.placeholder_color, **kwargs)
        
        self.bind("<FocusIn>", self._clear_placeholder)
        self.bind("<FocusOut>", self._add_placeholder)
        
        if placeholder:
            self.insert(0, placeholder)
    
    def _clear_placeholder(self, e=None):
        if self['fg'] == self.placeholder_color and self.get() == self.placeholder:
            self.delete(0, "end")
            self.config(fg=self.default_fg_color)
            if self.show_char:
                self.config(show=self.show_char)
    
    def _add_placeholder(self, e=None):
        if not self.get():
            self.config(show='', fg=self.placeholder_color)
            self.insert(0, self.placeholder)
    
    def get_value(self):
        """Retorna o valor real (sem placeholder)"""
        value = self.get()
        return '' if value == self.placeholder else value
    
    def clear(self):
        """Limpa o campo e restaura o placeholder"""
        self.delete(0, 'end')
        self.config(show='', fg=self.placeholder_color)
        if self.placeholder:
            self.insert(0, self.placeholder)


class App:
    def _setup_styles(self):
        """Configura estilos ttk para botões modernos"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Botão primário (azul)
        style.configure('Primary.TButton',
                       background='#3498db',
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       font=('Arial', 10, 'bold'),
                       padding=10)
        style.map('Primary.TButton',
                 background=[('active', '#2980b9'), ('pressed', '#2573a7')])
        
        # Botão sucesso (verde)
        style.configure('Success.TButton',
                       background='#2ecc71',
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       font=('Arial', 10, 'bold'),
                       padding=10)
        style.map('Success.TButton',
                 background=[('active', '#27ae60'), ('pressed', '#229954')])
        
        # Botão perigo (vermelho)
        style.configure('Danger.TButton',
                       background='#e74c3c',
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       font=('Arial', 10, 'bold'),
                       padding=10)
        style.map('Danger.TButton',
                 background=[('active', '#c0392b'), ('pressed', '#a93226')])
        
        # Botão secundário (cinza)
        style.configure('Secondary.TButton',
                       background='#95a5a6',
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       font=('Arial', 10),
                       padding=8)
        style.map('Secondary.TButton',
                 background=[('active', '#7f8c8d'), ('pressed', '#707b7c')])
        
        # Botão normal estilizado
        style.configure('TButton',
                       background='#34495e',
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       font=('Arial', 10),
                       padding=8)
        style.map('TButton',
                 background=[('active', '#2c3e50'), ('pressed', '#1c2833')])
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title('Catálogo de Veículos - GUI')
        
        # Tela inteira (compatível com Linux)
        self.root.attributes('-fullscreen', True)
        # Permitir sair com ESC
        self.root.bind('<Escape>', lambda e: self.root.attributes('-fullscreen', False))
        
        # Configurar estilos
        self._setup_styles()
        
        self.current_user = None
        
        # Canvas para imagem de fundo
        self.canvas = tk.Canvas(root, highlightthickness=0)
        self.canvas.pack(fill='both', expand=True)
        
        # Carregar imagem de fundo
        try:
            bg_path = os.path.join(os.path.dirname(__file__), 'background.png')
            bg_image = Image.open(bg_path)
            # Redimensionar para caber na tela mantendo aspecto
            screen_w = root.winfo_screenwidth()
            screen_h = root.winfo_screenheight()
            bg_image = bg_image.resize((screen_w, screen_h), Image.Resampling.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(bg_image)
            self.canvas.create_image(0, 0, image=self.bg_photo, anchor='nw')
        except Exception as e:
            print(f"Erro ao carregar imagem de fundo: {e}")
            self.canvas.configure(bg='#2c3e50')
        
        # Frame container para centralizar o login
        self.container = tk.Frame(self.canvas, bg='white', bd=0)
        self.canvas_window = self.canvas.create_window(
            root.winfo_screenwidth() // 2,
            root.winfo_screenheight() // 2,
            window=self.container,
            anchor='center'
        )
        
        # Frames: login_frame shown first; main_frame hidden until login
        self.login_frame = tk.Frame(self.container, padx=40, pady=30, bg='white', relief='raised', bd=2)
        
        # Título
        tk.Label(self.login_frame, text='Catálogo de Veículos', font=('Arial', 20, 'bold'), bg='white', fg='#2c3e50').pack(pady=(0,8))
        tk.Label(self.login_frame, text='Login', font=('Arial', 14), bg='white', fg='#34495e').pack(pady=(0,20))
        
        # Campos de entrada
        self.email_entry = PlaceholderEntry(self.login_frame, placeholder='Digite seu email', 
                                           font=('Arial', 11), relief='solid', bd=1, bg='white')
        self.email_entry.pack(pady=(0,15), padx=20, fill='x', ipady=6)
        
        self.senha_entry = PlaceholderEntry(self.login_frame, placeholder='Digite sua senha',
                                           show='•', font=('Arial', 11), relief='solid', bd=1, bg='white')
        self.senha_entry.pack(pady=(0,15), padx=20, fill='x', ipady=6)
        
        # Botões com ttk
        btn_frame = tk.Frame(self.login_frame, bg='white')
        btn_frame.pack(pady=(10,10))
        ttk.Button(btn_frame, text='Entrar', width=15, command=self.login_from_entries, 
                  style='Primary.TButton', cursor='hand2').pack(side='left', padx=5)
        ttk.Button(btn_frame, text='Cadastrar', width=15, command=self.register_user, 
                  style='Success.TButton', cursor='hand2').pack(side='left', padx=5)
        
        ttk.Button(self.login_frame, text='Sair', width=34, command=root.quit, 
                  style='Danger.TButton', cursor='hand2').pack(pady=(5,0))

        self.login_frame.pack()

        # Main frame (menu) - hidden until login
        self.main_frame = tk.Frame(self.container, padx=30, pady=30, bg='white', relief='raised', bd=2)
        
        # Título do menu
        tk.Label(self.main_frame, text='Menu Principal', font=('Arial', 18, 'bold'), 
                bg='white', fg='#2c3e50').grid(row=0, column=0, pady=(0,20))
        
        # create buttons and keep references so we can show/hide according to role
        self.btn_cadastrar_usuario = ttk.Button(self.main_frame, text='👤 Cadastrar usuário', 
                                               width=35, command=self.register_user, style='TButton')
        self.btn_cadastrar_usuario.grid(row=1, column=0, pady=4, ipady=3)

        self.btn_cadastrar_veiculo = ttk.Button(self.main_frame, text='🚗 Cadastrar veículo', 
                                               width=35, command=self.show_vehicle_form, style='TButton')
        self.btn_cadastrar_veiculo.grid(row=2, column=0, pady=4, ipady=3)

        self.btn_criar_anuncio = ttk.Button(self.main_frame, text='📢 Criar anúncio', 
                                           width=35, command=self.create_ad, style='Success.TButton')
        self.btn_criar_anuncio.grid(row=3, column=0, pady=4, ipady=3)

        self.btn_manage_ads = ttk.Button(self.main_frame, text='📝 Gerenciar meus anúncios', 
                                        width=35, command=self.manage_my_ads, style='TButton')
        self.btn_manage_ads.grid(row=4, column=0, pady=4, ipady=3)

        self.btn_buscar = ttk.Button(self.main_frame, text='🔍 Buscar anúncios', 
                                    width=35, command=self.search_announcements, style='Primary.TButton')
        self.btn_buscar.grid(row=5, column=0, pady=4, ipady=3)

        self.btn_admin_panel = ttk.Button(self.main_frame, text='⚙️ Painel Admin', 
                                         width=35, command=self.admin_panel, style='TButton')
        self.btn_admin_panel.grid(row=6, column=0, pady=4, ipady=3)

        self.btn_list_announcements = ttk.Button(self.main_frame, text='📋 Listar anúncios', 
                                                width=35, command=self.list_announcements, style='TButton')
        self.btn_list_announcements.grid(row=7, column=0, pady=4, ipady=3)

        self.btn_list_vehicles = ttk.Button(self.main_frame, text='🚙 Listar meus veículos', 
                                           width=35, command=self.list_my_vehicles, style='TButton')
        self.btn_list_vehicles.grid(row=8, column=0, pady=4, ipady=3)

        self.btn_logout = ttk.Button(self.main_frame, text='🚪 Logout', width=35, 
                                    command=self.logout, style='Danger.TButton')
        self.btn_logout.grid(row=9, column=0, pady=(15,0), ipady=3)

        # initially hide all main buttons; they'll be shown after login by update_main_buttons
        for w in (self.btn_cadastrar_usuario, self.btn_cadastrar_veiculo, self.btn_criar_anuncio,
                  self.btn_manage_ads, self.btn_buscar, self.btn_admin_panel,
                  self.btn_list_announcements, self.btn_list_vehicles, self.btn_logout):
            w.grid_remove()
        # vehicle registration frame (inline)
        self.vehicle_frame = tk.Frame(self.container, padx=40, pady=30, bg='white', relief='raised', bd=2)
        tk.Label(self.vehicle_frame, text='Cadastro de Veículo', font=('Arial', 18, 'bold'), 
                bg='white', fg='#2c3e50').pack(pady=(0,20))
        
        self.v_marca = PlaceholderEntry(self.vehicle_frame, placeholder='Marca (Ex: Toyota)', 
                                       font=('Arial', 11), relief='solid', bd=1, bg='white')
        self.v_marca.pack(pady=8, padx=20, fill='x', ipady=6)
        
        self.v_modelo = PlaceholderEntry(self.vehicle_frame, placeholder='Modelo (Ex: Corolla)', 
                                        font=('Arial', 11), relief='solid', bd=1, bg='white')
        self.v_modelo.pack(pady=8, padx=20, fill='x', ipady=6)
        
        self.v_ano = PlaceholderEntry(self.vehicle_frame, placeholder='Ano (Ex: 2020)', 
                                     font=('Arial', 11), relief='solid', bd=1, bg='white')
        self.v_ano.pack(pady=8, padx=20, fill='x', ipady=6)
        
        self.v_preco = PlaceholderEntry(self.vehicle_frame, placeholder='Preço (Ex: 50000)', 
                                       font=('Arial', 11), relief='solid', bd=1, bg='white')
        self.v_preco.pack(pady=8, padx=20, fill='x', ipady=6)
        
        self.v_km = PlaceholderEntry(self.vehicle_frame, placeholder='Quilometragem (Ex: 15000)', 
                                    font=('Arial', 11), relief='solid', bd=1, bg='white')
        self.v_km.pack(pady=8, padx=20, fill='x', ipady=6)
        
        vf_btns = tk.Frame(self.vehicle_frame, bg='white')
        vf_btns.pack(pady=(15,0))
        ttk.Button(vf_btns, text='✓ Salvar', width=15, command=self.vehicle_submit, 
                  style='Success.TButton').pack(side='left', padx=6)
        ttk.Button(vf_btns, text='✗ Cancelar', width=15, command=self.hide_vehicle_form, 
                  style='Secondary.TButton').pack(side='left', padx=6)

        # registration frame (same window) - hidden until needed
        self.register_frame = tk.Frame(self.container, padx=40, pady=30, bg='white', relief='raised', bd=2)
        
        # Status só aparece após login
        self.status = tk.Label(self.container, text='', anchor='w', bg='white', fg='#7f8c8d', font=('Arial', 9))
        
        tk.Label(self.register_frame, text='Cadastro de Usuário', font=('Arial', 18, 'bold'), 
                bg='white', fg='#2c3e50').pack(pady=(0,15))
        
        tipo_frame = tk.Frame(self.register_frame, bg='white')
        tipo_frame.pack(pady=8)
        self.reg_tipo = tk.StringVar(value='1')
        tk.Radiobutton(tipo_frame, text='Anunciante', variable=self.reg_tipo, value='1', 
                      bg='white', font=('Arial', 11), command=lambda: self._toggle_telefone()).pack(side='left', padx=15)
        tk.Radiobutton(tipo_frame, text='Cliente', variable=self.reg_tipo, value='2', 
                      bg='white', font=('Arial', 11), command=lambda: self._toggle_telefone()).pack(side='left', padx=15)

        self.reg_cpf = PlaceholderEntry(self.register_frame, placeholder='CPF (000.000.000-00)', 
                                       font=('Arial', 11), relief='solid', bd=1, bg='white')
        self.reg_cpf.pack(pady=8, padx=20, fill='x', ipady=6)

        self.reg_nome = PlaceholderEntry(self.register_frame, placeholder='Nome completo', 
                                        font=('Arial', 11), relief='solid', bd=1, bg='white')
        self.reg_nome.pack(pady=8, padx=20, fill='x', ipady=6)

        self.reg_email = PlaceholderEntry(self.register_frame, placeholder='Email (seu@email.com)', 
                                         font=('Arial', 11), relief='solid', bd=1, bg='white')
        self.reg_email.pack(pady=8, padx=20, fill='x', ipady=6)

        self.reg_senha = PlaceholderEntry(self.register_frame, placeholder='Senha (mínimo 6 caracteres)', 
                                         show='•', font=('Arial', 11), relief='solid', bd=1, bg='white')
        self.reg_senha.pack(pady=8, padx=20, fill='x', ipady=6)

        self.reg_telefone = PlaceholderEntry(self.register_frame, placeholder='Telefone (00) 00000-0000', 
                                            font=('Arial', 11), relief='solid', bd=1, bg='white')
        self.reg_telefone.pack(pady=8, padx=20, fill='x', ipady=6)

        btn_frame = tk.Frame(self.register_frame, bg='white')
        btn_frame.pack(pady=(15,0))
        ttk.Button(btn_frame, text='✓ Enviar', width=15, command=self.register_submit, 
                  style='Success.TButton').pack(side='left', padx=6)
        ttk.Button(btn_frame, text='✗ Cancelar', width=15, command=self.hide_register_form, 
                  style='Secondary.TButton').pack(side='left', padx=6)

        # default: telefone only for anunciante
        self._toggle_telefone()

    def _update_status(self):
        if self.current_user:
            self.status.pack(side='bottom', fill='x', padx=10, pady=5)
            self.status.config(text=f'Logado como: {getattr(self.current_user, "nome", repr(self.current_user))} ({self.current_user.__class__.__name__})')
        else:
            self.status.pack_forget()

    def register_user(self):
        # show the register frame on the same window
        self.show_register_form()

    def login(self):
        # kept for backwards compatibility (not used by initial screen)
        self.login_from_entries()

    def login_from_entries(self):
        email = self.email_entry.get_value().strip()
        senha = self.senha_entry.get_value().strip()
        if not email or not senha:
            messagebox.showwarning('Login', 'Preencha email e senha.')
            return
        user = main.Login(email, senha)
        if user:
            self.current_user = user
            self._update_status()
            messagebox.showinfo('Login', f'Logado como: {user.nome}')
            # switch to main menu
            self.login_frame.pack_forget()
            # update which buttons are accessible for this user
            self.update_main_buttons()
            self.main_frame.pack()
        else:
            messagebox.showerror('Login', 'Usuário ou senha incorretos.')

    def show_register_form(self):
        # remember which frame was visible
        self._prev_frame = 'main' if self.main_frame.winfo_ismapped() else 'login'
        try:
            if self.login_frame.winfo_ismapped():
                self.login_frame.pack_forget()
        except Exception:
            pass
        try:
            if self.main_frame.winfo_ismapped():
                self.main_frame.pack_forget()
        except Exception:
            pass
        self.register_frame.pack()

    def hide_register_form(self):
        try:
            self.register_frame.pack_forget()
        except Exception:
            pass
        # return to previous frame
        if getattr(self, '_prev_frame', 'login') == 'main':
            self.main_frame.pack()
        else:
            self.login_frame.pack()

    def _toggle_telefone(self):
        # enable telefone entry only for anunciante (value '1')
        if getattr(self, 'reg_tipo', None) and self.reg_tipo.get() == '1':
            try:
                self.reg_telefone.configure(state='normal')
            except Exception:
                pass
        else:
            try:
                self.reg_telefone.delete(0, 'end')
                self.reg_telefone.configure(state='disabled')
            except Exception:
                pass

    def register_submit(self):
        tipo = self.reg_tipo.get()
        cpf = self.reg_cpf.get_value().strip()
        nome = self.reg_nome.get_value().strip()
        email = self.reg_email.get_value().strip()
        senha = self.reg_senha.get_value().strip()
        telefone = self.reg_telefone.get_value().strip()

        # validações
        if not cpf:
            messagebox.showerror('Validação', 'CPF é obrigatório.')
            return
        if not nome:
            messagebox.showerror('Validação', 'Nome é obrigatório.')
            return
        if '@' not in email or '.' not in email:
            messagebox.showerror('Validação', 'Email inválido.')
            return
        if len(senha) < 6:
            messagebox.showerror('Validação', 'Senha deve ter ao menos 6 caracteres.')
            return

        try:
            if tipo == '1':
                user = main.CreateAnunciante(cpf, nome, email, senha, telefone)
            else:
                user = main.CreateCliente(cpf, nome, email, senha)
            # garantir que usuário também está na lista geral
            if user not in main.userList:
                main.userList.append(user)
            messagebox.showinfo('Cadastro', f'{"Anunciante" if tipo=="1" else "Cliente"} cadastrado com sucesso.')
            # preencha email no formulário de login para facilitar
            try:
                self.reg_cpf.clear()
                self.reg_nome.clear()
                self.reg_email.clear()
                self.reg_senha.clear()
                self.reg_telefone.clear()
            except Exception:
                pass
            # go back to login
            self.hide_register_form()
            try:
                self.email_entry.delete(0, 'end')
                self.email_entry.insert(0, email)
                self.senha_entry.delete(0, 'end')
            except Exception:
                pass
        except Exception as e:
            messagebox.showerror('Erro', f'Erro ao cadastrar: {e}')

    def logout(self):
        if self.current_user and hasattr(self.current_user, 'logout'):
            try:
                self.current_user.logout()
            except Exception:
                pass
        self.current_user = None
        self._update_status()
        # return to login screen
        try:
            self.main_frame.pack_forget()
        except Exception:
            pass
        # hide main buttons when returning to login
        for w in (self.btn_cadastrar_usuario, self.btn_cadastrar_veiculo, self.btn_criar_anuncio,
                  self.btn_manage_ads, self.btn_buscar, self.btn_admin_panel,
                  self.btn_list_announcements, self.btn_list_vehicles, self.btn_logout):
            try:
                w.grid_remove()
            except Exception:
                pass
        self.login_frame.pack()
        messagebox.showinfo('Logout', 'Desconectado.')

    def create_vehicle(self):
        # kept for backwards compatibility — prefer using the inline form
        self.show_vehicle_form()

    def create_ad(self):
        if not self.current_user or not hasattr(self.current_user, 'criarAnuncio'):
            messagebox.showwarning('Permissão', 'Apenas anunciantes podem criar anúncios.')
            return
        # escolher veículo existente ou criar novo
        use_existing = messagebox.askyesno('Criar Anúncio', 'Usar veículo existente?')
        if use_existing:
            # Buscar veículos do banco de dados
            from repository import VeiculoRepository
            veiculo_repo = VeiculoRepository()
            meus = veiculo_repo.listar_por_anunciante(self.current_user.id)
            if not meus:
                messagebox.showinfo('Criar Anúncio', 'Você não possui veículos. Crie um novo primeiro.')
                return
            choices = '\n'.join([f'{v.id}: {v.marca} {v.modelo} ({v.ano})' for v in meus])
            sel = simpledialog.askstring('Veículos', f'Selecione ID:\n{choices}')
            try:
                vid = int(sel)
                v = next((x for x in meus if x.id == vid), None)
            except Exception:
                v = None
            if not v:
                messagebox.showerror('Erro', 'Seleção inválida.')
                return
        else:
            # criar novo veículo já vinculado ao anunciante
            marca = simpledialog.askstring('Veículo', 'Marca:')
            modelo = simpledialog.askstring('Veículo', 'Modelo:')
            ano = simpledialog.askstring('Veículo', 'Ano:')
            preco = simpledialog.askstring('Veículo', 'Preço:')
            km = simpledialog.askstring('Veículo', 'Quilometragem:')
            try:
                v = main.CreateVeiculo(marca, modelo, ano, preco, km, anunciante=self.current_user)
            except Exception as e:
                messagebox.showerror('Erro', f'Erro ao criar veículo: {e}')
                return
        # Usar função que salva no banco de dados
        try:
            main.AnuncianteCriarAnuncio(self.current_user, v)
            messagebox.showinfo('Anúncio', f'Anúncio criado: {v.marca} {v.modelo}')
        except Exception as e:
            messagebox.showerror('Erro', f'Erro ao criar anúncio: {e}')

    def update_main_buttons(self):
        """Show/hide main menu buttons according to the logged-in user's role."""
        # hide all first
        for w in (self.btn_cadastrar_usuario, self.btn_cadastrar_veiculo, self.btn_criar_anuncio,
                  self.btn_manage_ads, self.btn_buscar, self.btn_admin_panel,
                  self.btn_list_announcements, self.btn_list_vehicles, self.btn_logout):
            try:
                w.grid_remove()
            except Exception:
                pass

        # buttons available to all logged-in users
        self.btn_cadastrar_usuario.grid()
        self.btn_list_announcements.grid()
        self.btn_logout.grid()

        # role specific
        if isinstance(self.current_user, main.Admin):
            # admin sees admin panel and can manage vehicles/users
            self.btn_admin_panel.grid()
            self.btn_cadastrar_veiculo.grid()
        else:
            # Anunciante: has criarAnuncio and manage ads, and can cadastrar veículo
            if hasattr(self.current_user, 'criarAnuncio'):
                self.btn_criar_anuncio.grid()
                self.btn_manage_ads.grid()
                self.btn_cadastrar_veiculo.grid()
                # anunciantes podem listar seus veículos
                self.btn_list_vehicles.grid()
            # Cliente: can buscar veículos
            if hasattr(self.current_user, 'buscarVeiculos'):
                self.btn_buscar.grid()

    def list_announcements(self):
        top = tk.Toplevel(self.root)
        top.title('Anúncios')
        lb = tk.Listbox(top, width=80)
        lb.pack(padx=10, pady=10)
        if not main.anuncioList:
            lb.insert('end', 'Nenhum anúncio cadastrado.')
            return
        for a in main.anuncioList:
            v = a.veiculo
            anunc = getattr(a.anunciante, 'nome', 'Desconhecido')
            lb.insert('end', f'ID:{a.id} | {v.marca} {v.modelo} ({v.ano}) | {anunc} | Status: {a.status}')

    def list_vehicles(self):
        # kept for backwards compatibility
        top = tk.Toplevel(self.root)
        top.title('Veículos')
        lb = tk.Listbox(top, width=80)
        lb.pack(padx=10, pady=10)
        if not main.veiculoList:
            lb.insert('end', 'Nenhum veículo cadastrado.')
            return
        for v in main.veiculoList:
            lb.insert('end', f'ID:{v.id} | {v.marca} {v.modelo} ({v.ano}) - {v.quilometragem}km - {v.preco} | Anunciante: {getattr(v, "anunciante", None) and getattr(v.anunciante, "nome", "Desconhecido")}')

    def list_my_vehicles(self):
        if not self.current_user or not hasattr(self.current_user, 'criarAnuncio'):
            messagebox.showwarning('Permissão', 'Apenas anunciantes podem ver seus veículos.')
            return
        top = tk.Toplevel(self.root)
        top.title('Meus Veículos')
        lb = tk.Listbox(top, width=80)
        lb.pack(padx=10, pady=10)
        # Buscar do banco de dados
        from repository import VeiculoRepository
        veiculo_repo = VeiculoRepository()
        meus = veiculo_repo.listar_por_anunciante(self.current_user.id)
        if not meus:
            lb.insert('end', 'Você não possui veículos cadastrados.')
            return
        for v in meus:
            lb.insert('end', f'ID:{v.id} | {v.marca} {v.modelo} ({v.ano}) - {v.quilometragem}km - {v.preco}')

    def show_vehicle_form(self):
        if not self.current_user or not hasattr(self.current_user, 'criarAnuncio'):
            messagebox.showwarning('Permissão', 'Apenas anunciantes podem cadastrar veículos.')
            return
        # hide other frames
        try:
            if self.login_frame.winfo_ismapped():
                self.login_frame.pack_forget()
        except Exception:
            pass
        try:
            if self.main_frame.winfo_ismapped():
                self.main_frame.pack_forget()
        except Exception:
            pass
        # clear previous inputs
        try:
            self.v_marca.clear()
            self.v_modelo.clear()
            self.v_ano.clear()
            self.v_preco.clear()
            self.v_km.clear()
        except Exception:
            pass
        self.vehicle_frame.pack()

    def hide_vehicle_form(self):
        try:
            self.vehicle_frame.pack_forget()
        except Exception:
            pass
        # return to main menu if logged, else login
        if self.current_user and self.main_frame:
            self.main_frame.pack()
        else:
            self.login_frame.pack()

    def vehicle_submit(self):
        marca = self.v_marca.get_value().strip()
        modelo = self.v_modelo.get_value().strip()
        ano = self.v_ano.get_value().strip()
        preco = self.v_preco.get_value().strip()
        km = self.v_km.get_value().strip()

        # validações simples
        if not marca:
            messagebox.showerror('Validação', 'Marca é obrigatória.')
            return
        if not modelo:
            messagebox.showerror('Validação', 'Modelo é obrigatório.')
            return
        try:
            ano_int = int(ano)
            # ano deve ser plausível e não pode ser maior que 2025
            if ano_int < 1886 or ano_int > 2025:
                raise ValueError()
        except Exception:
            messagebox.showerror('Validação', 'Ano inválido. Informe um ano entre 1886 e 2025.')
            return
        try:
            preco_f = float(preco)
            # preço deve ser estritamente maior que 0
            if preco_f <= 0:
                raise ValueError()
        except Exception:
            messagebox.showerror('Validação', 'Preço inválido. Informe valor maior que 0.')
            return
        try:
            km_int = int(km)
            # quilometragem não pode ser negativa
            if km_int < 0:
                raise ValueError()
        except Exception:
            messagebox.showerror('Validação', 'Quilometragem inválida. Informe número inteiro >= 0.')
            return

        try:
            v = main.CreateVeiculo(marca, modelo, ano_int, preco_f, km_int, anunciante=self.current_user)
            messagebox.showinfo('Veículo', f'Veículo cadastrado: {v.marca} {v.modelo}')
            self.hide_vehicle_form()
        except Exception as e:
            messagebox.showerror('Erro', f'Erro ao cadastrar veículo: {e}')

    def search_vehicles(self):
        # kept for compatibility
        self.search_announcements()

    def search_announcements(self):
        if not self.current_user or not hasattr(self.current_user, 'buscarVeiculos'):
            messagebox.showwarning('Permissão', 'Apenas clientes podem buscar anúncios.')
            return
        filtro = simpledialog.askstring('Buscar', 'Filtro (marca/modelo):')
        if not filtro:
            return
        resultados = [a for a in main.anuncioList if filtro.lower() in a.veiculo.marca.lower() or filtro.lower() in a.veiculo.modelo.lower()]
        top = tk.Toplevel(self.root)
        top.title('Resultados da Busca (Anúncios)')
        lb = tk.Listbox(top, width=120)
        lb.pack(padx=10, pady=10)
        if not resultados:
            lb.insert('end', 'Nenhum anúncio encontrado.')
            return
        for a in resultados:
            v = a.veiculo
            lb.insert('end', f'Anúncio ID:{a.id} | Veículo: {v.marca} {v.modelo} ({v.ano}) | Anunciante: {getattr(a.anunciante, "nome", "Desconhecido")} | Status: {a.status}')

    def manage_my_ads(self):
        if not self.current_user or not hasattr(self.current_user, 'listarMeusAnuncios'):
            messagebox.showwarning('Permissão', 'Apenas anunciantes podem gerenciar anúncios.')
            return
        top = tk.Toplevel(self.root)
        top.title('Meus Anúncios')
        lb = tk.Listbox(top, width=80)
        lb.pack(padx=10, pady=10)
        anuncios = self.current_user.listarMeusAnuncios()
        for a in anuncios:
            v = a.veiculo
            lb.insert('end', f'ID:{a.id} | {v.marca} {v.modelo} ({v.ano}) | Status: {a.status}')

        def excluir():
            sel = lb.curselection()
            if not sel:
                return
            text = lb.get(sel[0])
            aid = int(text.split('|')[0].replace('ID:', '').strip())
            # Buscar anúncio no banco para verificar permissão
            from repository import AnuncioRepository
            anuncio_repo = AnuncioRepository()
            anuncio = anuncio_repo.buscar_por_id(aid)
            
            if anuncio and anuncio._anunciante == self.current_user:
                anuncio_repo.deletar(aid)
                # Também remover da lista interna do anunciante
                self.current_user.excluirAnuncio(aid)
                messagebox.showinfo('Remover', 'Anúncio removido.')
                top.destroy()
            else:
                messagebox.showerror('Erro', 'Anúncio não encontrado ou você não tem permissão.')

        tk.Button(top, text='Excluir selecionado', command=excluir).pack(pady=6)

    def admin_panel(self):
        if not self.current_user or not isinstance(self.current_user, main.Admin):
            messagebox.showwarning('Permissão', 'Apenas administradores têm acesso ao painel.')
            return
        top = tk.Toplevel(self.root)
        top.title('Painel Admin')

        lb = tk.Listbox(top, width=100)
        lb.pack(padx=10, pady=10)
        pendentes = [a for a in main.anuncioList if a.status.lower() == 'pendente']
        for a in pendentes:
            v = a.veiculo
            lb.insert('end', f'ID:{a.id} | {v.marca} {v.modelo} ({v.ano}) | Anunciante: {getattr(a.anunciante, "nome", "Desconhecido")}')

        def aprovar():
            sel = lb.curselection()
            if not sel:
                return
            text = lb.get(sel[0])
            aid = int(text.split('|')[0].replace('ID:', '').strip())
            from repository import AnuncioRepository
            anuncio_repo = AnuncioRepository()
            anuncio = anuncio_repo.buscar_por_id(aid)
            if anuncio:
                anuncio_repo.atualizar_status(aid, 'Aprovado')
                messagebox.showinfo('Admin', 'Anúncio aprovado.')
                top.destroy()
            else:
                messagebox.showerror('Erro', 'Anúncio não encontrado.')

        def rejeitar():
            sel = lb.curselection()
            if not sel:
                return
            text = lb.get(sel[0])
            aid = int(text.split('|')[0].replace('ID:', '').strip())
            from repository import AnuncioRepository
            anuncio_repo = AnuncioRepository()
            anuncio = anuncio_repo.buscar_por_id(aid)
            if anuncio:
                anuncio_repo.atualizar_status(aid, 'Rejeitado')
                messagebox.showinfo('Admin', 'Anúncio rejeitado.')
                top.destroy()
            else:
                messagebox.showerror('Erro', 'Anúncio não encontrado.')

        tk.Button(top, text='Aprovar selecionado', command=aprovar).pack(side='left', padx=8, pady=6)
        tk.Button(top, text='Rejeitar selecionado', command=rejeitar).pack(side='left', padx=8, pady=6)


def main_gui():
    root = tk.Tk()
    # App será em tela inteira
    app = App(root)
    root.mainloop()


if __name__ == '__main__':
    main_gui()
