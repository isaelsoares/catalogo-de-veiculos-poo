#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Inicialização do Banco de Dados
==========================================

Este script cria/recria o banco de dados SQLite com todas as tabelas
e insere dados padrão (admin inicial e dados de exemplo).

Uso:
    python init_db.py              # Cria tabelas e insere admin padrão
    python init_db.py --reset      # Reseta o banco e recria tudo
    python init_db.py --with-data  # Inclui dados de exemplo
"""

import sys
import os
from database import Database
from datetime import datetime


def criar_admin_padrao(db: Database):
    """
    Cria o usuário administrador padrão no sistema.
    
    Credenciais:
        Email: admin@admin.com
        Senha: admin123
    """
    print("\n📌 Criando administrador padrão...")
    
    try:
        # Inserir usuário
        cursor = db.execute("""
            INSERT INTO usuarios (cpf, nome, email, senha, tipo)
            VALUES (?, ?, ?, ?, ?)
        """, ("00000000000", "Administrador", "admin@admin.com", "admin123", "admin"))
        
        usuario_id = cursor.lastrowid
        
        # Inserir registro específico de admin
        db.execute("""
            INSERT INTO admins (usuario_id, admin_id)
            VALUES (?, ?)
        """, (usuario_id, 1))
        
        print("✓ Admin criado com sucesso!")
        print(f"  Email: admin@admin.com")
        print(f"  Senha: admin123")
        
    except Exception as e:
        print(f"✗ Erro ao criar admin: {e}")


def criar_dados_exemplo(db: Database):
    """
    Insere dados de exemplo no banco para testes e demonstração.
    Inclui: usuários, veículos e anúncios.
    """
    print("\n📌 Inserindo dados de exemplo...")
    
    try:
        # ========== ANUNCIANTES ==========
        print("  → Criando anunciantes...")
        
        # Anunciante 1
        cursor = db.execute("""
            INSERT INTO usuarios (cpf, nome, email, senha, tipo)
            VALUES (?, ?, ?, ?, ?)
        """, ("12345678900", "João Silva", "joao@email.com", "senha123", "anunciante"))
        
        anunciante1_id = cursor.lastrowid
        db.execute("""
            INSERT INTO anunciantes (usuario_id, telefone)
            VALUES (?, ?)
        """, (anunciante1_id, "(11) 98765-4321"))
        
        # Anunciante 2
        cursor = db.execute("""
            INSERT INTO usuarios (cpf, nome, email, senha, tipo)
            VALUES (?, ?, ?, ?, ?)
        """, ("98765432100", "Maria Santos", "maria@email.com", "senha456", "anunciante"))
        
        anunciante2_id = cursor.lastrowid
        db.execute("""
            INSERT INTO anunciantes (usuario_id, telefone)
            VALUES (?, ?)
        """, (anunciante2_id, "(21) 99999-8888"))
        
        # Anunciante 3
        cursor = db.execute("""
            INSERT INTO usuarios (cpf, nome, email, senha, tipo)
            VALUES (?, ?, ?, ?, ?)
        """, ("11111111111", "Pedro Costa", "pedro@email.com", "senha789", "anunciante"))
        
        anunciante3_id = cursor.lastrowid
        db.execute("""
            INSERT INTO anunciantes (usuario_id, telefone)
            VALUES (?, ?)
        """, (anunciante3_id, "(31) 97777-6666"))
        
        print(f"    ✓ 3 anunciantes criados")
        
        # ========== CLIENTES ==========
        print("  → Criando clientes...")
        
        # Cliente 1
        cursor = db.execute("""
            INSERT INTO usuarios (cpf, nome, email, senha, tipo)
            VALUES (?, ?, ?, ?, ?)
        """, ("22222222222", "Ana Lima", "ana@email.com", "senha000", "cliente"))
        
        cliente1_id = cursor.lastrowid
        db.execute("""
            INSERT INTO clientes (usuario_id)
            VALUES (?)
        """, (cliente1_id,))
        
        # Cliente 2
        cursor = db.execute("""
            INSERT INTO usuarios (cpf, nome, email, senha, tipo)
            VALUES (?, ?, ?, ?, ?)
        """, ("33333333333", "Carlos Souza", "carlos@email.com", "senha111", "cliente"))
        
        cliente2_id = cursor.lastrowid
        db.execute("""
            INSERT INTO clientes (usuario_id)
            VALUES (?)
        """, (cliente2_id,))
        
        print(f"    ✓ 2 clientes criados")
        
        # ========== VEÍCULOS ==========
        print("  → Criando veículos...")
        
        veiculos = [
            # Veículos do Anunciante 1
            ("Toyota", "Corolla", 2020, 85000.00, 50000, anunciante1_id),
            ("Honda", "Civic", 2019, 75000.00, 40000, anunciante1_id),
            
            # Veículos do Anunciante 2
            ("Ford", "Ka", 2018, 35000.00, 45000, anunciante2_id),
            ("Volkswagen", "Gol", 2018, 45000.00, 60000, anunciante2_id),
            ("Chevrolet", "Onix", 2021, 60000.00, 30000, anunciante2_id),
            
            # Veículos do Anunciante 3
            ("Toyota", "Hilux", 2021, 150000.00, 20000, anunciante3_id),
            ("Fiat", "Palio", 2015, 28000.00, 70000, anunciante3_id),
        ]
        
        veiculo_ids = []
        for veiculo in veiculos:
            cursor = db.execute("""
                INSERT INTO veiculos (marca, modelo, ano, preco, quilometragem, anunciante_id)
                VALUES (?, ?, ?, ?, ?, ?)
            """, veiculo)
            veiculo_ids.append(cursor.lastrowid)
        
        print(f"    ✓ {len(veiculos)} veículos criados")
        
        # ========== ANÚNCIOS ==========
        print("  → Criando anúncios...")
        
        data_atual = datetime.now().strftime("%Y-%m-%d")
        
        anuncios = [
            # Anúncios aprovados
            (data_atual, "Aprovado", veiculo_ids[0], anunciante1_id),
            (data_atual, "Aprovado", veiculo_ids[1], anunciante1_id),
            (data_atual, "Aprovado", veiculo_ids[2], anunciante2_id),
            (data_atual, "Aprovado", veiculo_ids[4], anunciante2_id),
            
            # Anúncios pendentes
            (data_atual, "Pendente", veiculo_ids[3], anunciante2_id),
            (data_atual, "Pendente", veiculo_ids[5], anunciante3_id),
            
            # Anúncio rejeitado
            (data_atual, "Rejeitado", veiculo_ids[6], anunciante3_id),
        ]
        
        for anuncio in anuncios:
            db.execute("""
                INSERT INTO anuncios (data_publicacao, status, veiculo_id, anunciante_id)
                VALUES (?, ?, ?, ?)
            """, anuncio)
        
        print(f"    ✓ {len(anuncios)} anúncios criados")
        
        # ========== HISTÓRICO DE PESQUISAS ==========
        print("  → Criando histórico de pesquisas...")
        
        pesquisas = [
            (cliente1_id, "Toyota"),
            (cliente1_id, "Honda"),
            (cliente2_id, "Ford"),
            (cliente2_id, "Volkswagen"),
        ]
        
        for pesquisa in pesquisas:
            db.execute("""
                INSERT INTO historico_pesquisas (cliente_id, filtro)
                VALUES (?, ?)
            """, pesquisa)
        
        print(f"    ✓ {len(pesquisas)} pesquisas no histórico")
        
        print("\n✓ Dados de exemplo inseridos com sucesso!")
        
    except Exception as e:
        print(f"\n✗ Erro ao inserir dados de exemplo: {e}")
        raise


def exibir_estatisticas(db: Database):
    """Exibe estatísticas do banco de dados após inicialização."""
    print("\n" + "="*60)
    print("📊 ESTATÍSTICAS DO BANCO DE DADOS")
    print("="*60)
    
    try:
        # Contar usuários por tipo
        result = db.fetch_one("SELECT COUNT(*) as total FROM usuarios WHERE tipo = 'admin'")
        print(f"👨‍💼 Administradores: {result['total']}")
        
        result = db.fetch_one("SELECT COUNT(*) as total FROM usuarios WHERE tipo = 'anunciante'")
        print(f"👤 Anunciantes: {result['total']}")
        
        result = db.fetch_one("SELECT COUNT(*) as total FROM usuarios WHERE tipo = 'cliente'")
        print(f"🧑 Clientes: {result['total']}")
        
        # Contar veículos
        result = db.fetch_one("SELECT COUNT(*) as total FROM veiculos")
        print(f"🚗 Veículos: {result['total']}")
        
        # Contar anúncios por status
        result = db.fetch_one("SELECT COUNT(*) as total FROM anuncios WHERE status = 'Aprovado'")
        print(f"✅ Anúncios aprovados: {result['total']}")
        
        result = db.fetch_one("SELECT COUNT(*) as total FROM anuncios WHERE status = 'Pendente'")
        print(f"⏳ Anúncios pendentes: {result['total']}")
        
        result = db.fetch_one("SELECT COUNT(*) as total FROM anuncios WHERE status = 'Rejeitado'")
        print(f"❌ Anúncios rejeitados: {result['total']}")
        
    except Exception as e:
        print(f"✗ Erro ao exibir estatísticas: {e}")
    
    print("="*60)


def main():
    """Função principal do script de inicialização."""
    print("\n" + "="*60)
    print("🚀 INICIALIZAÇÃO DO BANCO DE DADOS")
    print("   Catálogo de Veículos - Sistema POO")
    print("="*60)
    
    # Verificar argumentos
    reset = "--reset" in sys.argv
    with_data = "--with-data" in sys.argv
    
    # Inicializar banco
    db = Database()
    
    # Reset se solicitado
    if reset:
        print("\n⚠️  MODO RESET: Removendo banco existente...")
        if os.path.exists(db._db_path):
            os.remove(db._db_path)
            print("✓ Banco de dados removido")
        else:
            print("  (Nenhum banco existente encontrado)")
    
    # Criar tabelas
    print("\n📌 Criando estrutura do banco de dados...")
    try:
        db.create_tables()
    except Exception as e:
        print(f"✗ Erro ao criar tabelas: {e}")
        return 1
    
    # Criar admin padrão
    criar_admin_padrao(db)
    
    # Inserir dados de exemplo se solicitado
    if with_data:
        criar_dados_exemplo(db)
    
    # Exibir estatísticas
    exibir_estatisticas(db)
    
    # Fechar conexão
    db.close()
    
    print("\n✅ Inicialização concluída com sucesso!")
    print(f"📁 Banco de dados: {db._db_path}")
    
    if not with_data:
        print("\n💡 Dica: Use 'python init_db.py --with-data' para incluir dados de exemplo")
    
    print("\n" + "="*60 + "\n")
    
    return 0


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠️  Operação cancelada pelo usuário.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ ERRO FATAL: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
