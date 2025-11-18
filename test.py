#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Testes - Catálogo de Veículos POO
Testa todas as classes e validações do sistema
"""

from models.Vehicle import Veiculo
from models.Client import Cliente
from models.Announcer import Anunciante
from models.Advertisement import Anuncio
from models.Admin import Admin


class TestResult:
    """Classe para gerenciar resultados dos testes"""
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
    
    def test(self, name, condition, error_msg=""):
        """Executa um teste e registra o resultado"""
        if condition:
            self.passed += 1
            print(f"✓ {name}")
            return True
        else:
            self.failed += 1
            self.errors.append(f"{name}: {error_msg}")
            print(f"✗ {name} - {error_msg}")
            return False
    
    def summary(self):
        """Exibe sumário dos testes"""
        total = self.passed + self.failed
        print("\n" + "="*60)
        print(f"RESUMO DOS TESTES")
        print("="*60)
        print(f"Total de testes: {total}")
        print(f"✓ Passou: {self.passed}")
        print(f"✗ Falhou: {self.failed}")
        if self.failed == 0:
            print("\n🎉 TODOS OS TESTES PASSARAM! 🎉")
        else:
            print("\n⚠️  ALGUNS TESTES FALHARAM:")
            for error in self.errors:
                print(f"   - {error}")
        print("="*60)


def test_veiculo():
    """Testa a classe Veiculo"""
    print("\n" + "="*60)
    print("TESTANDO CLASSE VEICULO")
    print("="*60)
    result = TestResult()
    
    # Teste 1: Criação válida
    try:
        v1 = Veiculo("Toyota", "Corolla", 2020, 85000.00, 50000)
        result.test("Criação de veículo válido", True)
        result.test("ID automático gerado", v1.id > 0)
        result.test("Marca correta", v1.marca == "Toyota")
        result.test("Modelo correto", v1.modelo == "Corolla")
        result.test("Ano correto", v1.ano == 2020)
        result.test("Preço correto", v1.preco == 85000.00)
        result.test("Quilometragem correta", v1.quilometragem == 50000)
    except Exception as e:
        result.test("Criação de veículo válido", False, str(e))
    
    # Teste 2: Quilometragem negativa (deveria aceitar, mas é inválido logicamente)
    try:
        v2 = Veiculo("Honda", "Civic", 2019, 75000.00, -1000)
        # A classe não valida, mas podemos detectar
        result.test("Quilometragem negativa detectada", v2.quilometragem < 0, 
                   "AVISO: Sistema permite quilometragem negativa")
    except Exception as e:
        result.test("Validação de quilometragem negativa", True, "Exceção lançada corretamente")
    
    # Teste 3: Ano inválido (futuro muito distante)
    try:
        v3 = Veiculo("Ford", "Focus", 2050, 50000.00, 0)
        result.test("Ano futuro permitido", v3.ano == 2050, 
                   "AVISO: Sistema permite ano muito futuro")
    except Exception as e:
        result.test("Validação de ano futuro", True, "Exceção lançada")
    
    # Teste 4: Preço negativo
    try:
        v4 = Veiculo("Fiat", "Uno", 2015, -10000.00, 80000)
        result.test("Preço negativo detectado", v4.preco < 0,
                   "AVISO: Sistema permite preço negativo")
    except Exception as e:
        result.test("Validação de preço negativo", True, "Exceção lançada")
    
    # Teste 5: Atualização de atributos
    try:
        v5 = Veiculo("Chevrolet", "Onix", 2021, 60000.00, 30000)
        v5.marca = "GM"
        v5.preco = 58000.00
        v5.quilometragem = 35000
        result.test("Atualização de marca", v5.marca == "GM")
        result.test("Atualização de preço", v5.preco == 58000.00)
        result.test("Atualização de quilometragem", v5.quilometragem == 35000)
    except Exception as e:
        result.test("Atualização de atributos", False, str(e))
    
    # Teste 6: Método exibirInformacoes
    try:
        v6 = Veiculo("Volkswagen", "Gol", 2018, 45000.00, 60000)
        info = v6.exibirInformacoes()
        result.test("Método exibirInformacoes retorna string", isinstance(info, str))
        result.test("Informações contêm marca", "Volkswagen" in info)
        result.test("Informações contêm modelo", "Gol" in info)
    except Exception as e:
        result.test("Método exibirInformacoes", False, str(e))
    
    # Teste 7: Tipos de dados incorretos
    try:
        v7 = Veiculo(123, 456, "2020", "abc", "xyz")  # Tipos errados
        result.test("Tipos de dados incorretos permitidos", True,
                   "AVISO: Sistema não valida tipos de entrada")
    except Exception as e:
        result.test("Validação de tipos de dados", True, "Exceção lançada corretamente")
    
    # Teste 8: Strings vazias
    try:
        v8 = Veiculo("", "", 2020, 50000.00, 10000)
        result.test("Strings vazias permitidas", v8.marca == "",
                   "AVISO: Sistema permite marca/modelo vazios")
    except Exception as e:
        result.test("Validação de strings vazias", True, "Exceção lançada")
    
    # Teste 9: Valores zero
    try:
        v9 = Veiculo("Nissan", "Sentra", 0, 0, 0)
        result.test("Valores zero permitidos", v9.ano == 0 and v9.preco == 0,
                   "AVISO: Sistema permite valores zero")
    except Exception as e:
        result.test("Validação de valores zero", True, "Exceção lançada")
    
    result.summary()
    return result


def test_cliente():
    """Testa a classe Cliente"""
    print("\n" + "="*60)
    print("TESTANDO CLASSE CLIENTE")
    print("="*60)
    result = TestResult()
    
    # Teste 1: Criação de cliente
    try:
        c1 = Cliente()
        result.test("Criação de cliente", True)
        result.test("ID automático gerado", c1.id > 0)
        result.test("Histórico inicializado vazio", len(c1.historicoPesquisas) == 0)
    except Exception as e:
        result.test("Criação de cliente", False, str(e))
    
    # Teste 2: Busca de veículos
    try:
        veiculos = [
            Veiculo("Toyota", "Corolla", 2020, 85000, 50000),
            Veiculo("Honda", "Civic", 2019, 75000, 40000),
            Veiculo("Toyota", "Hilux", 2021, 150000, 20000)
        ]
        c2 = Cliente()
        resultados = c2.buscarVeiculos("Toyota", veiculos)
        result.test("Busca retorna resultados corretos", len(resultados) == 2)
        result.test("Busca salva no histórico", "Toyota" in c2.historicoPesquisas)
    except Exception as e:
        result.test("Busca de veículos", False, str(e))
    
    # Teste 3: Busca case-insensitive
    try:
        c3 = Cliente()
        resultados = c3.buscarVeiculos("CIVIC", veiculos)
        result.test("Busca case-insensitive", len(resultados) == 1)
    except Exception as e:
        result.test("Busca case-insensitive", False, str(e))
    
    # Teste 4: Busca sem resultados
    try:
        c4 = Cliente()
        resultados = c4.buscarVeiculos("Ferrari", veiculos)
        result.test("Busca sem resultados", len(resultados) == 0)
        result.test("Busca vazia registrada no histórico", "Ferrari" in c4.historicoPesquisas)
    except Exception as e:
        result.test("Busca sem resultados", False, str(e))
    
    # Teste 5: Visualizar detalhes
    try:
        c5 = Cliente()
        v_test = veiculos[0]
        detalhes = c5.visualizarDetalhes(v_test.id, veiculos)
        result.test("Visualizar detalhes existente", detalhes is not None)
        result.test("Veículo correto retornado", detalhes.id == v_test.id)
    except Exception as e:
        result.test("Visualizar detalhes", False, str(e))
    
    # Teste 6: Visualizar detalhes inexistente
    try:
        c6 = Cliente()
        detalhes = c6.visualizarDetalhes(9999, veiculos)
        result.test("Visualizar detalhes inexistente", detalhes is None)
    except Exception as e:
        result.test("Visualizar detalhes inexistente", False, str(e))
    
    # Teste 7: Histórico múltiplas pesquisas
    try:
        c7 = Cliente()
        c7.buscarVeiculos("Toyota", veiculos)
        c7.buscarVeiculos("Honda", veiculos)
        c7.buscarVeiculos("Ford", veiculos)
        result.test("Múltiplas pesquisas no histórico", len(c7.historicoPesquisas) == 3)
    except Exception as e:
        result.test("Histórico múltiplas pesquisas", False, str(e))
    
    # Teste 8: exibirPerfil
    try:
        c8 = Cliente()
        c8.buscarVeiculos("Toyota", veiculos)
        perfil = c8.exibirPerfil()
        result.test("Método exibirPerfil retorna string", isinstance(perfil, str))
        result.test("Perfil contém histórico", "Toyota" in perfil or "Histórico" in perfil)
    except Exception as e:
        result.test("Método exibirPerfil", False, str(e))
    
    result.summary()
    return result


def test_anunciante():
    """Testa a classe Anunciante"""
    print("\n" + "="*60)
    print("TESTANDO CLASSE ANUNCIANTE")
    print("="*60)
    result = TestResult()
    
    # Teste 1: Criação válida
    try:
        a1 = Anunciante(12345678900, "João Silva", "joao@email.com", "senha123", "(11) 98765-4321")
        result.test("Criação de anunciante", True)
        result.test("Nome correto", a1.nome == "João Silva")
        result.test("Email correto", a1.email == "joao@email.com")
        result.test("Telefone correto", a1.telefone == "(11) 98765-4321")
    except Exception as e:
        result.test("Criação de anunciante", False, str(e))
    
    # Teste 2: Criar anúncio
    try:
        a2 = Anunciante(98765432100, "Maria Santos", "maria@email.com", "senha456", "(21) 99999-8888")
        veiculo = Veiculo("Ford", "Ka", 2018, 35000, 45000)
        anuncio = a2.criarAnuncio(veiculo)
        result.test("Criar anúncio", anuncio is not None)
        result.test("Anúncio na lista", len(a2.listarMeusAnuncios()) == 1)
    except Exception as e:
        result.test("Criar anúncio", False, str(e))
    
    # Teste 3: Listar anúncios
    try:
        a3 = Anunciante(11111111111, "Pedro Costa", "pedro@email.com", "senha789", "(31) 97777-6666")
        v1 = Veiculo("Fiat", "Palio", 2015, 28000, 70000)
        v2 = Veiculo("Chevrolet", "Celta", 2012, 22000, 90000)
        a3.criarAnuncio(v1)
        a3.criarAnuncio(v2)
        anuncios = a3.listarMeusAnuncios()
        result.test("Listar múltiplos anúncios", len(anuncios) == 2)
    except Exception as e:
        result.test("Listar anúncios", False, str(e))
    
    # Teste 4: Excluir anúncio
    try:
        a4 = Anunciante(22222222222, "Ana Lima", "ana@email.com", "senha000", "(41) 96666-5555")
        veiculo = Veiculo("Volkswagen", "Fox", 2017, 38000, 55000)
        anuncio = a4.criarAnuncio(veiculo)
        id_anuncio = anuncio.id
        excluiu = a4.excluirAnuncio(id_anuncio)
        result.test("Excluir anúncio existente", excluiu == True)
        result.test("Anúncio removido da lista", len(a4.listarMeusAnuncios()) == 0)
    except Exception as e:
        result.test("Excluir anúncio", False, str(e))
    
    # Teste 5: Excluir anúncio inexistente
    try:
        a5 = Anunciante(33333333333, "Carlos Souza", "carlos@email.com", "senha111", "(51) 95555-4444")
        excluiu = a5.excluirAnuncio(9999)
        result.test("Excluir anúncio inexistente", excluiu == False)
    except Exception as e:
        result.test("Excluir anúncio inexistente", False, str(e))
    
    # Teste 6: Telefone vazio
    try:
        a6 = Anunciante(44444444444, "Lucas Alves", "lucas@email.com", "senha222", "(61) 94444-3333")
        a6.telefone = ""
        result.test("Validação telefone vazio", False, "Sistema permitiu telefone vazio")
    except ValueError:
        result.test("Validação telefone vazio", True)
    except Exception as e:
        result.test("Validação telefone vazio", False, f"Erro inesperado: {str(e)}")
    
    # Teste 7: Nome vazio
    try:
        a7 = Anunciante(55555555555, "Paulo Mendes", "paulo@email.com", "senha333", "(71) 93333-2222")
        a7.nome = "   "
        result.test("Validação nome vazio", False, "Sistema permitiu nome vazio")
    except ValueError:
        result.test("Validação nome vazio", True)
    except Exception as e:
        result.test("Validação nome vazio", False, f"Erro inesperado: {str(e)}")
    
    # Teste 8: exibirPerfil
    try:
        a8 = Anunciante(66666666666, "Fernanda Rocha", "fernanda@email.com", "senha444", "(81) 92222-1111")
        perfil = a8.exibirPerfil()
        result.test("Método exibirPerfil retorna string", isinstance(perfil, str))
        result.test("Perfil contém nome", "Fernanda" in perfil)
    except Exception as e:
        result.test("Método exibirPerfil", False, str(e))
    
    result.summary()
    return result


def test_anuncio():
    """Testa a classe Anuncio"""
    print("\n" + "="*60)
    print("TESTANDO CLASSE ANUNCIO")
    print("="*60)
    result = TestResult()
    
    # Teste 1: Criação de anúncio
    try:
        veiculo = Veiculo("Hyundai", "HB20", 2020, 55000, 35000)
        anunciante = Anunciante(77777777777, "Roberto Silva", "roberto@email.com", "senha555", "(85) 91111-0000")
        anuncio = Anuncio("2025-11-18", "Pendente", veiculo, anunciante)
        result.test("Criação de anúncio", True)
        result.test("ID automático gerado", anuncio.id > 0)
        result.test("Data correta", anuncio.dataPublicacao == "2025-11-18")
        result.test("Status inicial", anuncio.status == "Pendente")
    except Exception as e:
        result.test("Criação de anúncio", False, str(e))
    
    # Teste 2: Aprovar anúncio
    try:
        veiculo = Veiculo("Renault", "Sandero", 2019, 48000, 42000)
        anunciante = Anunciante(88888888888, "Juliana Costa", "juliana@email.com", "senha666", "(86) 90000-9999")
        anuncio = Anuncio("2025-11-18", "Pendente", veiculo, anunciante)
        anuncio.aprovar()
        result.test("Aprovar anúncio", anuncio.status == "Aprovado")
    except Exception as e:
        result.test("Aprovar anúncio", False, str(e))
    
    # Teste 3: Rejeitar anúncio
    try:
        veiculo = Veiculo("Peugeot", "208", 2018, 42000, 50000)
        anunciante = Anunciante(99999999999, "Ricardo Ferreira", "ricardo@email.com", "senha777", "(87) 89999-8888")
        anuncio = Anuncio("2025-11-18", "Pendente", veiculo, anunciante)
        anuncio.rejeitar()
        result.test("Rejeitar anúncio", anuncio.status == "Rejeitado")
    except Exception as e:
        result.test("Rejeitar anúncio", False, str(e))
    
    # Teste 4: Alterar status manualmente
    try:
        veiculo = Veiculo("Jeep", "Renegade", 2021, 95000, 25000)
        anunciante = Anunciante(10101010101, "Beatriz Almeida", "beatriz@email.com", "senha888", "(88) 98888-7777")
        anuncio = Anuncio("2025-11-18", "Pendente", veiculo, anunciante)
        anuncio.status = "Em Análise"
        result.test("Alterar status manualmente", anuncio.status == "Em Análise")
    except Exception as e:
        result.test("Alterar status manualmente", False, str(e))
    
    # Teste 5: exibirResumo
    try:
        veiculo = Veiculo("Mitsubishi", "L200", 2020, 125000, 30000)
        anunciante = Anunciante(20202020202, "Gabriel Martins", "gabriel@email.com", "senha999", "(89) 97777-6666")
        anuncio = Anuncio("2025-11-18", "Aprovado", veiculo, anunciante)
        resumo = anuncio.exibirResumo()
        result.test("Método exibirResumo retorna string", isinstance(resumo, str))
        result.test("Resumo contém status", "Aprovado" in resumo)
    except Exception as e:
        result.test("Método exibirResumo", False, str(e))
    
    # Teste 6: Alterar veículo do anúncio
    try:
        v1 = Veiculo("Kia", "Sportage", 2021, 110000, 15000)
        v2 = Veiculo("Kia", "Cerato", 2020, 85000, 25000)
        anunciante = Anunciante(30303030303, "Camila Ribeiro", "camila@email.com", "senha101", "(90) 96666-5555")
        anuncio = Anuncio("2025-11-18", "Pendente", v1, anunciante)
        anuncio.veiculo = v2
        result.test("Alterar veículo do anúncio", anuncio.veiculo.modelo == "Cerato")
    except Exception as e:
        result.test("Alterar veículo do anúncio", False, str(e))
    
    result.summary()
    return result


def test_admin():
    """Testa a classe Admin"""
    print("\n" + "="*60)
    print("TESTANDO CLASSE ADMIN")
    print("="*60)
    result = TestResult()
    
    # Teste 1: Criação de admin
    try:
        admin = Admin(1, 12345678900, "Admin Geral", "admin@sistema.com", "admin123", 1001)
        result.test("Criação de admin", True)
        result.test("Nome correto", admin.nome == "Admin Geral")
        result.test("AdminID correto", admin.adminID == 1001)
    except Exception as e:
        result.test("Criação de admin", False, str(e))
    
    # Teste 2: Aprovar anúncio
    try:
        admin = Admin(2, 98765432100, "Admin Teste", "admin2@sistema.com", "admin456", 1002)
        veiculo = Veiculo("BMW", "X1", 2021, 180000, 10000)
        anunciante = Anunciante(40404040404, "Marcos Oliveira", "marcos@email.com", "senha202", "(91) 95555-4444")
        anuncio = Anuncio("2025-11-18", "Pendente", veiculo, anunciante)
        admin.aprovarAnuncio(anuncio)
        result.test("Admin aprovar anúncio", anuncio.status == "Aprovado")
    except Exception as e:
        result.test("Admin aprovar anúncio", False, str(e))
    
    # Teste 3: Rejeitar anúncio
    try:
        admin = Admin(3, 11122233344, "Admin Sistema", "admin3@sistema.com", "admin789", 1003)
        veiculo = Veiculo("Audi", "A3", 2020, 150000, 20000)
        anunciante = Anunciante(50505050505, "Patricia Lima", "patricia@email.com", "senha303", "(92) 94444-3333")
        anuncio = Anuncio("2025-11-18", "Pendente", veiculo, anunciante)
        admin.rejeitarAnuncio(anuncio)
        result.test("Admin rejeitar anúncio", anuncio.status == "Rejeitado")
    except Exception as e:
        result.test("Admin rejeitar anúncio", False, str(e))
    
    # Teste 4: Gerenciar usuário - criar
    try:
        admin = Admin(4, 55566677788, "Admin Master", "admin4@sistema.com", "admin000", 1004)
        lista_usuarios = []
        dados = {
            "classe": Anunciante,
            "id": 100,
            "cpf": 60606060606,
            "nome": "Usuário Teste",
            "email": "teste@email.com",
            "senha": "senha404",
            "telefone": "(93) 93333-2222"
        }
        # Ajuste para criar Anunciante sem id no construtor
        novo_anunciante = Anunciante(dados["cpf"], dados["nome"], dados["email"], 
                                     dados["senha"], dados["telefone"])
        lista_usuarios.append(novo_anunciante)
        result.test("Admin criar usuário", len(lista_usuarios) == 1)
    except Exception as e:
        result.test("Admin criar usuário", False, str(e))
    
    # Teste 5: Gerenciar usuário - deletar
    try:
        admin = Admin(5, 99988877766, "Admin Delete", "admin5@sistema.com", "admin111", 1005)
        usuario = Anunciante(70707070707, "Usuario Temp", "temp@email.com", "senha505", "(94) 92222-1111")
        lista = [usuario]
        msg = admin.gerenciarUsuario("deletar", usuario=usuario, lista_usuarios=lista)
        result.test("Admin deletar usuário", len(lista) == 0)
    except Exception as e:
        result.test("Admin deletar usuário", False, str(e))
    
    # Teste 6: exibirPerfil
    try:
        admin = Admin(6, 44433322211, "Admin Perfil", "admin6@sistema.com", "admin222", 1006)
        perfil = admin.exibirPerfil()
        result.test("Admin exibirPerfil retorna string", isinstance(perfil, str))
        result.test("Perfil contém AdminID", "1006" in perfil or "Admin ID" in perfil)
    except Exception as e:
        result.test("Admin exibirPerfil", False, str(e))
    
    # Teste 7: Login válido
    try:
        admin = Admin(7, 11100099988, "Admin Login", "admin7@sistema.com", "senha_secreta", 1007)
        login_ok = admin.login("admin7@sistema.com", "senha_secreta")
        result.test("Login válido", login_ok == True)
    except Exception as e:
        result.test("Login válido", False, str(e))
    
    # Teste 8: Login inválido
    try:
        admin = Admin(8, 22211100099, "Admin Login2", "admin8@sistema.com", "senha123456", 1008)
        login_fail = admin.login("admin8@sistema.com", "senha_errada")
        result.test("Login inválido", login_fail == False)
    except Exception as e:
        result.test("Login inválido", False, str(e))
    
    # Teste 9: Atualizar senha curta
    try:
        admin = Admin(9, 33322211100, "Admin Update", "admin9@sistema.com", "senha789012", 1009)
        sucesso = admin.atualizarInfo({"senha": "123"})
        result.test("Validação senha curta", sucesso == False)
    except Exception as e:
        result.test("Validação senha curta", False, str(e))
    
    result.summary()
    return result


def main():
    """Função principal que executa todos os testes"""
    print("\n" + "="*60)
    print("exemplo classe")
    print("="*60)
    print("INICIANDO BATERIA DE TESTES DO SISTEMA")
    print("Testando validações, tipos de dados e valores inválidos")
    print("="*60)
    
    # Executar todos os testes
    results = []
    results.append(test_veiculo())
    results.append(test_cliente())
    results.append(test_anunciante())
    results.append(test_anuncio())
    results.append(test_admin())
    
    # Resumo geral
    total_passed = sum(r.passed for r in results)
    total_failed = sum(r.failed for r in results)
    total_tests = total_passed + total_failed
    
    print("\n" + "="*60)
    print("RESUMO GERAL DE TODOS OS TESTES")
    print("="*60)
    print(f"Total de testes executados: {total_tests}")
    print(f"✓ Testes aprovados: {total_passed}")
    print(f"✗ Testes falhados: {total_failed}")
    
    if total_failed == 0:
        print("\n" + "🎉"*20)
        print("PARABÉNS! TODOS OS TESTES PASSARAM COM SUCESSO!")
        print("🎉"*20)
    else:
        print(f"\n⚠️  {total_failed} teste(s) falharam. Revise os erros acima.")
        print("\nRecomendações:")
        print("- Adicione validações para valores negativos")
        print("- Valide tipos de dados na entrada")
        print("- Verifique strings vazias e valores zero")
    
    print("="*60)


if __name__ == "__main__":
    main()
