#!/usr/bin/env python3
"""
Script para testar se os campos do formulário estão sendo encontrados corretamente
"""

import requests
from bs4 import BeautifulSoup
import re

def test_form_fields():
    """Testa se os campos do formulário estão presentes no DOM"""
    
    # Criar uma sessão para manter cookies
    session = requests.Session()
    
    # URL de login
    login_url = "http://127.0.0.1:8000/"
    form_url = "http://127.0.0.1:8000/formacompanhamento/registro_pagamento/novo/"
    
    try:
        # Primeiro, obter a página de login para pegar o CSRF token
        print("🔐 Obtendo página de login...")
        login_page = session.get(login_url)
        soup = BeautifulSoup(login_page.text, 'html.parser')
        csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})
        
        if csrf_token:
            csrf_value = csrf_token.get('value')
            print(f"✅ CSRF token encontrado: {csrf_value[:10]}...")
        else:
            print("❌ CSRF token não encontrado")
            csrf_value = ""
        
        # Fazer login
        print("🔐 Fazendo login...")
        login_data = {
            'username': 'testuser',
            'password': 'testpass123',
            'csrfmiddlewaretoken': csrf_value
        }
        
        login_response = session.post(login_url, data=login_data)
        print(f"Login status: {login_response.status_code}")
        print(f"Login URL final: {login_response.url}")
        
        # Agora fazer a requisição para o formulário
        print("📋 Acessando formulário...")
        response = session.get(form_url)
        response.raise_for_status()
        
        # Parse do HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Verifica se foi redirecionado para login
        if 'login' in response.url.lower() or 'accounts/login' in response.url:
            print("⚠️  REDIRECIONADO PARA LOGIN")
            print("💡 O usuário precisa estar logado para acessar o formulário")
            print("💡 URL final:", response.url)
            return
        
        # Lista de campos que devem existir
        campos_principais = [
            'id_prestador',
            'id_acionamento',
            'id_franquia_hora',
            'id_km_franquia',
            'id_valor_hora_excedente',
            'id_valor_km_excedente',
            'id_motivo'
        ]
        
        # Lista de campos dos agentes adicionais
        campos_agentes = [
            'id_prestador1', 'id_acionamento1', 'id_franquia_hora1', 'id_km_franquia1', 'id_valor_hora_excedente1', 'id_valor_km_excedente1', 'id_motivo1',
            'id_prestador2', 'id_acionamento2', 'id_franquia_hora2', 'id_km_franquia2', 'id_valor_hora_excedente2', 'id_valor_km_excedente2', 'id_motivo2',
            'id_prestador3', 'id_acionamento3', 'id_franquia_hora3', 'id_franquia_hora3', 'id_km_franquia3', 'id_valor_hora_excedente3', 'id_valor_km_excedente3', 'id_motivo3'
        ]
        
        print("============================================================")
        print("TESTE DOS CAMPOS DO FORMULÁRIO")
        print("============================================================")
        print(f"URL final: {response.url}")
        print(f"Status code: {response.status_code}")
        print(f"Tamanho da resposta: {len(response.text)} caracteres")
        
        # Testa campos principais
        print("\n📋 CAMPOS PRINCIPAIS:")
        for campo in campos_principais:
            elemento = soup.find('input', {'id': campo}) or soup.find('select', {'id': campo})
            if elemento:
                print(f"✅ {campo}: ENCONTRADO")
            else:
                print(f"❌ {campo}: NÃO ENCONTRADO")
        
        # Testa campos dos agentes adicionais
        print("\n👥 CAMPOS DOS AGENTES ADICIONAIS:")
        for campo in campos_agentes:
            elemento = soup.find('input', {'id': campo}) or soup.find('select', {'id': campo})
            if elemento:
                print(f"✅ {campo}: ENCONTRADO")
            else:
                print(f"❌ {campo}: NÃO ENCONTRADO")
        
        # Testa se os blocos de agentes existem
        print("\n🔍 BLOCOS DE AGENTES:")
        agentes_blocks = soup.find_all('div', class_='agente-dinamico')
        print(f"Blocos de agentes encontrados: {len(agentes_blocks)}")
        
        for i, block in enumerate(agentes_blocks):
            block_id = block.get('id', f'agente{i+1}')
            display_style = block.get('style', '')
            print(f"  - {block_id}: {display_style}")
        
        # Testa se o botão de adicionar agente existe
        print("\n🔘 BOTÃO ADICIONAR AGENTE:")
        btn_adicionar = soup.find('button', {'id': 'btnAdicionarAgente'})
        if btn_adicionar:
            print("✅ Botão 'Adicionar Agente' encontrado")
        else:
            print("❌ Botão 'Adicionar Agente' NÃO encontrado")
        
        # Testa se há JavaScript no formulário
        print("\n📜 JAVASCRIPT:")
        scripts = soup.find_all('script')
        print(f"Scripts encontrados: {len(scripts)}")
        
        # Procura por funções específicas no JavaScript
        js_content = ' '.join([script.string or '' for script in scripts])
        
        funcoes_js = [
            'attachPrestadorChangeListener',
            'updateAcionamentoByMotivo',
            'btnAdicionarAgente'
        ]
        
        for funcao in funcoes_js:
            if funcao in js_content:
                print(f"✅ Função '{funcao}' encontrada no JavaScript")
            else:
                print(f"❌ Função '{funcao}' NÃO encontrada no JavaScript")
        
        print("\n============================================================")
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao acessar o formulário: {e}")
        print("💡 Certifique-se de que o servidor está rodando: python manage.py runserver")

if __name__ == "__main__":
    test_form_fields()
