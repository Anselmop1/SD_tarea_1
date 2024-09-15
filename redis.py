from flask import Flask, request, jsonify
import redis
import grpc
import dns_resolver_pb2
import dns_resolver_pb2_grpc

# Configuración de Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

# Configuración de la API
app = Flask(__name__)

# Comunicación con el cliente gRPC
def consultar_dns_grpc(domain):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = dns_resolver_pb2_grpc.DNSResolverStub(channel)
        request = dns_resolver_pb2.DNSRequest(domain=domain)
        response = stub.ResolveDNS(request)
        return response.ip

# Endpoint de la API para la resolución DNS
@app.route('/api/resolve', methods=['GET'])
def resolver_dominio():
    domain = request.args.get('domain')
    # Intentar obtener la entrada de Redis
    ip = redis_client.get(domain)
    if ip:
        return jsonify({'domain': domain, 'ip': ip.decode('utf-8'), 'cached': True})
    else:
        # Si no está en caché, llamar al servidor gRPC
        ip = consultar_dns_grpc(domain)
        redis_client.set(domain, ip)  # Almacenar la respuesta en Redis
        return jsonify({'domain': domain, 'ip': ip, 'cached': False})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
