
import requests
import json

# --- Configuración ---
BASE_URL = "http://127.0.0.1:9002/api/"
# Reemplaza esto con el token de autenticación que generaste
TOKEN = "904a9a7608f3e6102911cce9b5a54c443e65524a" 
HEADERS = {
    "Authorization": f"Token {TOKEN}",
    "Content-Type": "application/json"
}

# --- Datos a Crear ---

PLATILLOS = [
    {
        "nombre": "Sopa de Tortilla",
        "descripcion": "Clásica sopa de tortilla con aguacate, queso y crema.",
        "precio": "8.50",
        "categoria": "Entrada",
        "tiempo_preparacion": 10
    },
    {
        "nombre": "Enchiladas Verdes",
        "descripcion": "Tortillas de maíz rellenas de pollo, bañadas en salsa verde.",
        "precio": "14.00",
        "categoria": "Plato Fuerte",
        "tiempo_preparacion": 20
    },
    {
        "nombre": "Flan Napolitano",
        "descripcion": "Postre cremoso de huevo y leche condensada.",
        "precio": "6.00",
        "categoria": "Postre",
        "tiempo_preparacion": 60 # Tiempo de preparación total, no de servicio
    }
]

CLIENTES = [
    {
        "nombre": "Ana",
        "apellido": "García",
        "email": "ana.garcia@example.com",
        "telefono": "555-123-4567"
    }
]

EMPLEADOS = [
    {
        "nombre": "Carlos",
        "apellido": "Ruiz",
        "puesto": "Mesero",
        "fecha_contratacion": "2023-01-15"
    }
]


def poblar_datos():
    """
    Función principal para enviar los datos a la API.
    """
    print("--- Poblando Platillos ---")
    for platillo in PLATILLOS:
        response = requests.post(f"{BASE_URL}platillos/", data=json.dumps(platillo), headers=HEADERS)
        if response.status_code == 201:
            print(f"  > Platillo '{platillo['nombre']}' creado exitosamente.")
        else:
            print(f"  > Error creando platillo '{platillo['nombre']}': {response.status_code} {response.text}")

    print("\n--- Poblando Clientes ---")
    for cliente in CLIENTES:
        response = requests.post(f"{BASE_URL}clientes/", data=json.dumps(cliente), headers=HEADERS)
        if response.status_code == 201:
            print(f"  > Cliente '{cliente['nombre']} {cliente['apellido']}' creado exitosamente.")
        else:
            print(f"  > Error creando cliente '{cliente['nombre']}': {response.status_code} {response.text}")

    print("\n--- Poblando Empleados ---")
    for empleado in EMPLEADOS:
        response = requests.post(f"{BASE_URL}empleados/", data=json.dumps(empleado), headers=HEADERS)
        if response.status_code == 201:
            print(f"  > Empleado '{empleado['nombre']} {empleado['apellido']}' creado exitosamente.")
        else:
            print(f"  > Error creando empleado '{empleado['nombre']}': {response.status_code} {response.text}")


if __name__ == "__main__":
    # Primero, limpiamos los datos existentes para evitar duplicados
    print("--- Limpiando datos existentes (Platillos, Clientes, Empleados) ---")
    
    # NOTA: En un entorno real, la eliminación masiva debería ser manejada con más cuidado.
    # Aquí es seguro porque es un script de desarrollo.
    
    # Limpiar platillos
    resp = requests.get(f"{BASE_URL}platillos/", headers=HEADERS)
    for item in resp.json():
        requests.delete(f"{BASE_URL}platillos/{item['id']}/", headers=HEADERS)
    print("  > Platillos eliminados.")
        
    # Limpiar clientes
    resp = requests.get(f"{BASE_URL}clientes/", headers=HEADERS)
    for item in resp.json():
        requests.delete(f"{BASE_URL}clientes/{item['id']}/", headers=HEADERS)
    print("  > Clientes eliminados.")

    # Limpiar empleados
    resp = requests.get(f"{BASE_URL}empleados/", headers=HEADERS)
    for item in resp.json():
        requests.delete(f"{BASE_URL}empleados/{item['id']}/", headers=HEADERS)
    print("  > Empleados eliminados.")
    
    print("\n--- Empezando a poblar la base de datos ---\n")
    poblar_datos()
    print("\n--- Proceso de población completado ---")
