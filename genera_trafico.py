import requests
import time
import random

# Leer dataset con nombres de dominio
with open("3rd_lev_domains.csv", "r") as f:
    domains = f.readlines()

# Simular tráfico de solicitudes enviadas a la API
def generar_trafico():
    while True:
        dominio = random.choice(domains).strip()
        response = requests.get(f"http://localhost:5000/api/resolve?domain={dominio}")
        print(f"Solicitado: {dominio}, Respuesta: {response.json()}")
        time.sleep(random.uniform(0.5, 2))  # Esperar entre 0.5 y 2 segundos

if __name__ == "__main__":
    generar_trafico()
