#!/usr/bin/env python
"""
Script para testar a API do prestador
"""
import os
import django
import requests

# Configurar o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'acionamento.settings')
django.setup()

from formacompanhamento.models import prestadores

def test_prestador_api():
    """Testa a API do prestador"""
    print("=" * 60)
    print("TESTE DA API DO PRESTADOR")
    print("=" * 60)
    
    # Buscar um prestador para teste
    prestador = prestadores.objects.first()
    if not prestador:
        print("❌ Nenhum prestador encontrado no banco de dados")
        return
    
    print(f"✅ Prestador encontrado: {prestador.Nome} (ID: {prestador.id})")
    print(f"   Valor Acionamento: {prestador.valor_acionamento}")
    print(f"   Valor Antenista: {prestador.valor_antenista}")
    print(f"   Valor Pronta Resposta Armado: {prestador.valor_prontaresposta_armado}")
    print(f"   Valor Pronta Resposta Desarmado: {prestador.valor_prontaresposta_desarmado}")
    print(f"   Franquia Hora Antenista: {prestador.franquia_hora_antenista}")
    print(f"   Franquia KM Antenista: {prestador.franquia_km_antenista}")
    print(f"   Valor Hora Antenista: {prestador.valorh_antenista}")
    print(f"   Valor KM Antenista: {prestador.valorkm_antenista}")
    
    # Testar a API
    try:
        url = f"http://127.0.0.1:8000/formacompanhamento/prestador-detail/?id={prestador.id}"
        print(f"\n🌐 Testando URL: {url}")
        
        response = requests.get(url)
        print(f"📡 Status da resposta: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Dados recebidos com sucesso!")
            print("\n📋 Campos recebidos:")
            for key, value in data.items():
                if 'valor' in key.lower() or 'franquia' in key.lower() or 'hora' in key.lower() or 'km' in key.lower():
                    print(f"   {key}: {value}")
        else:
            print(f"❌ Erro na resposta: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Erro de conexão - Servidor não está rodando")
        print("💡 Execute: python manage.py runserver")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    test_prestador_api()
