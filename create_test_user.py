#!/usr/bin/env python3
"""
Script para criar um usuário de teste
"""

import os
import django

# Configurar o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'acionamento.settings')
django.setup()

from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate

def create_test_user():
    """Cria um usuário de teste se não existir"""
    
    username = 'testuser'
    email = 'test@example.com'
    password = 'testpass123'
    
    # Verificar se o usuário já existe
    if User.objects.filter(username=username).exists():
        print(f"✅ Usuário '{username}' já existe")
        user = User.objects.get(username=username)
    else:
        # Criar o usuário
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name='Usuário',
            last_name='Teste'
        )
        print(f"✅ Usuário '{username}' criado com sucesso")
    
    # Verificar se o grupo 'pa' existe
    if Group.objects.filter(name='pa').exists():
        pa_group = Group.objects.get(name='pa')
        user.groups.add(pa_group)
        print(f"✅ Usuário adicionado ao grupo 'pa'")
    else:
        print("⚠️  Grupo 'pa' não encontrado")
    
    # Testar autenticação
    auth_user = authenticate(username=username, password=password)
    if auth_user:
        print(f"✅ Autenticação bem-sucedida para '{username}'")
        print(f"   Nome: {auth_user.get_full_name()}")
        print(f"   Email: {auth_user.email}")
        print(f"   Grupos: {[g.name for g in auth_user.groups.all()]}")
    else:
        print(f"❌ Falha na autenticação para '{username}'")
    
    return user

if __name__ == "__main__":
    create_test_user()
