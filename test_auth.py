import requests
import json
import time

API_URL = "http://localhost:8000/api"
print("== Test de autenticación para LollyPOS ==")

try:
    # 1. Intentar login con credenciales
    print("\n1. Probando autenticación con credenciales...")
    auth_response = requests.post(
        f"{API_URL}/token/",
        json={"username": "admin", "password": "1234"},
        headers={"Content-Type": "application/json"}
    )
    
    if auth_response.status_code != 200:
        print(f"❌ Error de autenticación: {auth_response.status_code}")
        try:
            print(json.dumps(auth_response.json(), indent=2))
        except:
            print(auth_response.text)
        exit(1)
    
    tokens = auth_response.json()
    access_token = tokens.get("access")
    refresh_token = tokens.get("refresh")
    
    print(f"✅ Autenticación exitosa")
    print(f"   - Token de acceso: {access_token[:10]}...")
    print(f"   - Token de renovación: {refresh_token[:10]}...")
    
    # 2. Obtener información del empleado autenticado
    print("\n2. Obteniendo información del empleado...")
    employee_response = requests.get(
        f"{API_URL}/employees/me/",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    
    if employee_response.status_code != 200:
        print(f"❌ Error al obtener perfil: {employee_response.status_code}")
        try:
            print(json.dumps(employee_response.json(), indent=2))
        except:
            print(employee_response.text)
        exit(1)
    
    employee = employee_response.json()
    print(f"✅ Perfil obtenido correctamente")
    print(f"   - Nombre: {employee.get('first_name')} {employee.get('last_name')}")
    print(f"   - Rol: {employee.get('role_name')}")
    print(f"   - Activo: {employee.get('is_active')}")
    
    # 3. Probar renovación de token
    print("\n3. Probando renovación de token...")
    refresh_response = requests.post(
        f"{API_URL}/token/refresh/",
        json={"refresh": refresh_token},
        headers={"Content-Type": "application/json"}
    )
    
    if refresh_response.status_code != 200:
        print(f"❌ Error al renovar token: {refresh_response.status_code}")
        try:
            print(json.dumps(refresh_response.json(), indent=2))
        except:
            print(refresh_response.text)
        exit(1)
    
    new_tokens = refresh_response.json()
    new_access_token = new_tokens.get("access")
    print(f"✅ Token renovado correctamente")
    print(f"   - Nuevo token de acceso: {new_access_token[:10]}...")
    
    # 4. Verificar que el nuevo token funciona
    print("\n4. Verificando nuevo token...")
    verify_response = requests.get(
        f"{API_URL}/employees/me/",
        headers={"Authorization": f"Bearer {new_access_token}"}
    )
    
    if verify_response.status_code != 200:
        print(f"❌ Error al verificar nuevo token: {verify_response.status_code}")
        try:
            print(json.dumps(verify_response.json(), indent=2))
        except:
            print(verify_response.text)
        exit(1)
    
    print(f"✅ Nuevo token funciona correctamente")
    
    print("\n🎉 Todas las pruebas han sido exitosas!")
    print("   El sistema de autenticación está funcionando correctamente.")

except Exception as e:
    print(f"❌ Error general: {str(e)}")
