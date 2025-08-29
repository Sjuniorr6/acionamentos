#!/usr/bin/env python3
"""
Script para corrigir as permissões do usuário de teste
"""

import os
import django

# Configurar o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'acionamento.settings')
django.setup()

from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from formacompanhamento.models import agentes

def fix_user_permissions():
    """Adiciona as permissões necessárias ao usuário de teste"""
    
    username = 'testuser'
    
    # Verificar se o usuário existe
    if not User.objects.filter(username=username).exists():
        print(f"❌ Usuário '{username}' não encontrado")
        return
    
    user = User.objects.get(username=username)
    print(f"✅ Usuário '{username}' encontrado")
    
    # Obter o content type para o modelo agentes
    content_type = ContentType.objects.get_for_model(agentes)
    
    # Permissões necessárias
    permissions_needed = [
        'view_agentes',
        'add_agentes', 
        'change_agentes',
        'delete_agentes',
        'view_registropagamento',
        'add_registropagamento',
        'change_registropagamento',
        'delete_registropagamento',
        'view_prestadores',
        'add_prestadores',
        'change_prestadores',
        'delete_prestadores',
    ]
    
    print("🔧 Adicionando permissões...")
    
    for perm_name in permissions_needed:
        try:
            # Tentar obter a permissão
            if 'agentes' in perm_name:
                perm = Permission.objects.get(
                    codename=perm_name.replace('agentes', ''),
                    content_type=content_type
                )
            elif 'registropagamento' in perm_name:
                from formacompanhamento.models import RegistroPagamento
                ct = ContentType.objects.get_for_model(RegistroPagamento)
                perm = Permission.objects.get(
                    codename=perm_name.replace('registropagamento', ''),
                    content_type=ct
                )
            elif 'prestadores' in perm_name:
                from formacompanhamento.models import prestadores
                ct = ContentType.objects.get_for_model(prestadores)
                perm = Permission.objects.get(
                    codename=perm_name.replace('prestadores', ''),
                    content_type=ct
                )
            else:
                continue
                
            user.user_permissions.add(perm)
            print(f"✅ Permissão '{perm_name}' adicionada")
            
        except Permission.DoesNotExist:
            print(f"⚠️  Permissão '{perm_name}' não encontrada")
        except Exception as e:
            print(f"❌ Erro ao adicionar permissão '{perm_name}': {e}")
    
    # Verificar se o usuário é superuser
    if not user.is_superuser:
        print("🔧 Tornando usuário superuser...")
        user.is_superuser = True
        user.is_staff = True
        user.save()
        print("✅ Usuário agora é superuser")
    
    print(f"✅ Permissões corrigidas para '{username}'")
    print(f"   Superuser: {user.is_superuser}")
    print(f"   Staff: {user.is_staff}")
    print(f"   Permissões: {[p.codename for p in user.user_permissions.all()]}")

if __name__ == "__main__":
    fix_user_permissions()
