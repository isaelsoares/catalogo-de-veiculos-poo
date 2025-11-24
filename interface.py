import tkinter as tk
from tkinter import simpledialog, messagebox
import main


class App:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title('Catálogo de Veículos - GUI')
        self.current_user = None
        # Frames: login_frame shown first; main_frame hidden until login
        self.login_frame = tk.Frame(root, padx=10, pady=10)
        tk.Label(self.login_frame, text='Login', font=('Arial', 14)).grid(row=0, column=0, columnspan=2, pady=(0,8))
        tk.Label(self.login_frame, text='Email:').grid(row=1, column=0, sticky='e')
        self.email_entry = tk.Entry(self.login_frame, width=30)
        self.email_entry.grid(row=1, column=1)
        tk.Label(self.login_frame, text='Senha:').grid(row=2, column=0, sticky='e')
        self.senha_entry = tk.Entry(self.login_frame, show='*', width=30)
        self.senha_entry.grid(row=2, column=1)
        tk.Button(self.login_frame, text='Entrar', width=15, command=self.login_from_entries).grid(row=3, column=0, pady=8)
        tk.Button(self.login_frame, text='Cadastrar', width=15, command=self.register_user).grid(row=3, column=1, pady=8)
        tk.Button(self.login_frame, text='Sair', width=32, command=root.quit).grid(row=4, column=0, columnspan=2)

        self.login_frame.pack()

        # Main frame (menu) - hidden until login
        self.main_frame = tk.Frame(root, padx=10, pady=10)
        # create buttons and keep references so we can show/hide according to role
        self.btn_cadastrar_usuario = tk.Button(self.main_frame, text='Cadastrar usuário', width=30, command=self.register_user)
        self.btn_cadastrar_usuario.grid(row=0, column=0, pady=2)

        self.btn_cadastrar_veiculo = tk.Button(self.main_frame, text='Cadastrar veículo', width=30, command=self.show_vehicle_form)
        self.btn_cadastrar_veiculo.grid(row=1, column=0, pady=2)

        self.btn_criar_anuncio = tk.Button(self.main_frame, text='Criar anúncio (anunciante)', width=30, command=self.create_ad)
        self.btn_criar_anuncio.grid(row=2, column=0, pady=2)

        self.btn_manage_ads = tk.Button(self.main_frame, text='Gerenciar meus anúncios', width=30, command=self.manage_my_ads)
        self.btn_manage_ads.grid(row=3, column=0, pady=2)

        self.btn_buscar = tk.Button(self.main_frame, text='Buscar anúncios (cliente)', width=30, command=self.search_announcements)
        self.btn_buscar.grid(row=4, column=0, pady=2)

        self.btn_admin_panel = tk.Button(self.main_frame, text='Painel Admin', width=30, command=self.admin_panel)
        self.btn_admin_panel.grid(row=5, column=0, pady=2)

        self.btn_list_announcements = tk.Button(self.main_frame, text='Listar anúncios', width=30, command=self.list_announcements)
        self.btn_list_announcements.grid(row=6, column=0, pady=2)

        self.btn_list_vehicles = tk.Button(self.main_frame, text='Listar meus veículos', width=30, command=self.list_my_vehicles)
        self.btn_list_vehicles.grid(row=7, column=0, pady=2)

        self.btn_logout = tk.Button(self.main_frame, text='Logout', width=30, command=self.logout)
        self.btn_logout.grid(row=8, column=0, pady=6)

        # initially hide all main buttons; they'll be shown after login by update_main_buttons
        for w in (self.btn_cadastrar_usuario, self.btn_cadastrar_veiculo, self.btn_criar_anuncio,
                  self.btn_manage_ads, self.btn_buscar, self.btn_admin_panel,
                  self.btn_list_announcements, self.btn_list_vehicles, self.btn_logout):
            w.grid_remove()
        # vehicle registration frame (inline)
        self.vehicle_frame = tk.Frame(root, padx=10, pady=10)
        tk.Label(self.vehicle_frame, text='Cadastro de Veículo', font=('Arial', 14)).grid(row=0, column=0, columnspan=2, pady=(0,8))
        tk.Label(self.vehicle_frame, text='Marca:').grid(row=1, column=0, sticky='e')
        self.v_marca = tk.Entry(self.vehicle_frame, width=30)
        self.v_marca.grid(row=1, column=1)
        tk.Label(self.vehicle_frame, text='Modelo:').grid(row=2, column=0, sticky='e')
        self.v_modelo = tk.Entry(self.vehicle_frame, width=30)
        self.v_modelo.grid(row=2, column=1)
        tk.Label(self.vehicle_frame, text='Ano:').grid(row=3, column=0, sticky='e')
        self.v_ano = tk.Entry(self.vehicle_frame, width=30)
        self.v_ano.grid(row=3, column=1)
        tk.Label(self.vehicle_frame, text='Preço:').grid(row=4, column=0, sticky='e')
        self.v_preco = tk.Entry(self.vehicle_frame, width=30)
        self.v_preco.grid(row=4, column=1)
        tk.Label(self.vehicle_frame, text='Quilometragem:').grid(row=5, column=0, sticky='e')
        self.v_km = tk.Entry(self.vehicle_frame, width=30)
        self.v_km.grid(row=5, column=1)
        vf_btns = tk.Frame(self.vehicle_frame)
        vf_btns.grid(row=6, column=0, columnspan=2, pady=8)
        tk.Button(vf_btns, text='Salvar', width=12, command=self.vehicle_submit).pack(side='left', padx=6)
        tk.Button(vf_btns, text='Cancelar', width=12, command=self.hide_vehicle_form).pack(side='left', padx=6)

        self.status = tk.Label(root, text='Não autenticado', anchor='w')
        self.status.pack(fill='x', padx=10)

        # registration frame (same window) - hidden until needed
        self.register_frame = tk.Frame(root, padx=10, pady=10)
        tk.Label(self.register_frame, text='Cadastro de Usuário', font=('Arial', 14)).grid(row=0, column=0, columnspan=2, pady=(0,8))
        tk.Label(self.register_frame, text='Tipo:').grid(row=1, column=0, sticky='e')
        self.reg_tipo = tk.StringVar(value='1')
        tk.Radiobutton(self.register_frame, text='Anunciante', variable=self.reg_tipo, value='1', command=lambda: self._toggle_telefone()).grid(row=1, column=1, sticky='w')
        tk.Radiobutton(self.register_frame, text='Cliente', variable=self.reg_tipo, value='2', command=lambda: self._toggle_telefone()).grid(row=1, column=1, sticky='e')

        tk.Label(self.register_frame, text='CPF:').grid(row=2, column=0, sticky='e')
        self.reg_cpf = tk.Entry(self.register_frame, width=30)
        self.reg_cpf.grid(row=2, column=1)

        tk.Label(self.register_frame, text='Nome:').grid(row=3, column=0, sticky='e')
        self.reg_nome = tk.Entry(self.register_frame, width=30)
        self.reg_nome.grid(row=3, column=1)

        tk.Label(self.register_frame, text='Email:').grid(row=4, column=0, sticky='e')
        self.reg_email = tk.Entry(self.register_frame, width=30)
        self.reg_email.grid(row=4, column=1)

        tk.Label(self.register_frame, text='Senha:').grid(row=5, column=0, sticky='e')
        self.reg_senha = tk.Entry(self.register_frame, show='*', width=30)
        self.reg_senha.grid(row=5, column=1)

        tk.Label(self.register_frame, text='Telefone:').grid(row=6, column=0, sticky='e')
        self.reg_telefone = tk.Entry(self.register_frame, width=30)
        self.reg_telefone.grid(row=6, column=1)

        btn_frame = tk.Frame(self.register_frame)
        btn_frame.grid(row=7, column=0, columnspan=2, pady=8)
        tk.Button(btn_frame, text='Enviar', width=12, command=self.register_submit).pack(side='left', padx=6)
        tk.Button(btn_frame, text='Cancelar', width=12, command=self.hide_register_form).pack(side='left', padx=6)

        # default: telefone only for anunciante
        self._toggle_telefone()

    def _update_status(self):
        if self.current_user:
            self.status.config(text=f'Logado como: {getattr(self.current_user, "nome", repr(self.current_user))} ({self.current_user.__class__.__name__})')
        else:
            self.status.config(text='Não autenticado')

    def register_user(self):
        # show the register frame on the same window
        self.show_register_form()

    def login(self):
        # kept for backwards compatibility (not used by initial screen)
        self.login_from_entries()

    def login_from_entries(self):
        email = self.email_entry.get().strip()
        senha = self.senha_entry.get().strip()
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
        cpf = (self.reg_cpf.get() or '').strip()
        nome = (self.reg_nome.get() or '').strip()
        email = (self.reg_email.get() or '').strip()
        senha = (self.reg_senha.get() or '').strip()
        telefone = (self.reg_telefone.get() or '').strip()

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
                self.reg_cpf.delete(0, 'end')
                self.reg_nome.delete(0, 'end')
                self.reg_email.delete(0, 'end')
                self.reg_senha.delete(0, 'end')
                self.reg_telefone.delete(0, 'end')
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
            meus = [v for v in main.veiculoList if getattr(v, 'anunciante', None) == self.current_user]
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
                main.veiculoList.append(v)
            except Exception as e:
                messagebox.showerror('Erro', f'Erro ao criar veículo: {e}')
                return
        anuncio = self.current_user.criarAnuncio(v)
        main.anuncioList.append(anuncio)
        messagebox.showinfo('Anúncio', f'Anúncio criado: {v.marca} {v.modelo}')

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
        meus = [v for v in main.veiculoList if getattr(v, 'anunciante', None) == self.current_user]
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
            self.v_marca.delete(0, 'end')
            self.v_modelo.delete(0, 'end')
            self.v_ano.delete(0, 'end')
            self.v_preco.delete(0, 'end')
            self.v_km.delete(0, 'end')
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
        marca = (self.v_marca.get() or '').strip()
        modelo = (self.v_modelo.get() or '').strip()
        ano = (self.v_ano.get() or '').strip()
        preco = (self.v_preco.get() or '').strip()
        km = (self.v_km.get() or '').strip()

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
            if v not in main.veiculoList:
                main.veiculoList.append(v)
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
            ok = self.current_user.excluirAnuncio(aid)
            if ok:
                # remover global
                ann = next((x for x in main.anuncioList if x.id == aid), None)
                if ann:
                    main.anuncioList.remove(ann)
                messagebox.showinfo('Remover', 'Anúncio removido.')
                top.destroy()
            else:
                messagebox.showerror('Erro', 'Não foi possível remover.')

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
            anuncio = next((x for x in main.anuncioList if x.id == aid), None)
            if anuncio:
                self.current_user.aprovarAnuncio(anuncio)
                messagebox.showinfo('Admin', 'Anúncio aprovado.')
                top.destroy()

        def rejeitar():
            sel = lb.curselection()
            if not sel:
                return
            text = lb.get(sel[0])
            aid = int(text.split('|')[0].replace('ID:', '').strip())
            anuncio = next((x for x in main.anuncioList if x.id == aid), None)
            if anuncio:
                self.current_user.rejeitarAnuncio(anuncio)
                messagebox.showinfo('Admin', 'Anúncio rejeitado.')
                top.destroy()

        tk.Button(top, text='Aprovar selecionado', command=aprovar).pack(side='left', padx=8, pady=6)
        tk.Button(top, text='Rejeitar selecionado', command=rejeitar).pack(side='left', padx=8, pady=6)


def main_gui():
    root = tk.Tk()
    # Define tamanho padrão e centraliza a janela
    width, height = 800, 600
    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()
    x = (screen_w - width) // 2
    y = (screen_h - height) // 2
    root.geometry(f"{width}x{height}+{x}+{y}")
    root.minsize(640, 480)
    app = App(root)
    root.mainloop()


if __name__ == '__main__':
    main_gui()
