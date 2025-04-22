import uuid
from zoneinfo import ZoneInfo
import jwt
import os
import io
import secrets
from functools import wraps
from datetime import datetime, timedelta, timezone
from django import db
from flask import Flask, send_file, jsonify, request, Response
from app.core.usecases.huawei_router_service import huaweirouterservice
from app.core.usecases import user_service
from config import Config


# Dados do roteador Huawei
host        = os.getenv('HUAWEI_HOST')
username    = os.getenv('HUAWEI_USERNAME')
password    = os.getenv('HUAWEI_PASSWORD')
port        = os.getenv('HUAWEI_PORT')


TEST_FILE_PATH = "/tmp/test_20mb.bin"
if not os.path.exists(TEST_FILE_PATH):
    with open(TEST_FILE_PATH, "wb") as f:
        f.write(secrets.token_bytes(20 * 1024 * 1024))


def init_routes(app):
    
    def require_jwt(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            auth_header = request.headers.get("Authorization", "")
            if not auth_header.startswith("Bearer "):
                return jsonify({"msg": "Token não fornecido ou inválido"}), 401
            
            token = auth_header.split()[1]
            try:
                payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=["HS256"])
                request.jwt_payload = payload
            except jwt.ExpiredSignatureError:
                return jsonify({"msg": "Token expirado"}), 401
            except jwt.InvalidTokenError:
                return jsonify({"msg": "Token inválido"}), 401
            except Exception as e:
                return jsonify({"msg": f"Erro no processamento do token: {str(e)}"}), 401

            return f(*args, **kwargs)
        return wrapper

    def require_role(role):
        def decorator(f):
            @wraps(f)
            def wrapper(*args, **kwargs):
                payload = getattr(request, 'jwt_payload', None)
                if not payload:
                    return jsonify({"msg": "Token inválido"}), 401

                if payload.get("role") != role:
                    return jsonify({"msg": f"Permissão negada: Apenas {role}"}), 403

                return f(*args, **kwargs)
            return wrapper
        return decorator


    @app.route('/api/user/login', methods=['POST'])
    def login():
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        userAth = user_service.autenticar_login(username, password)
        if userAth :
            now = datetime.now(ZoneInfo("America/Sao_Paulo"))
            payload = {
                "sub": userAth.username,
                "role": userAth.role,
                "iat": now,
                "exp": now + timedelta(hours=1)
            }
            token = jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm="HS256")
            return jsonify(access_token=token), 200
        else:
            return jsonify({"msg": "Usuário ou senha inválidos"}), 401
        
    
    @app.route('/api/user/create', methods=['POST'])
    @require_jwt
    @require_role("admin")
    def user_create():
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        pass_encrypted = user_service.hash_password(password)
        role = data.get('role')
        now = datetime.now(ZoneInfo("America/Sao_Paulo"))

        payload = {
            "id": uuid.uuid4(),
            "username": username,
            "role": role,
            "password": pass_encrypted,
            "created": now.strftime('%Y-%m-%d %H:%M:%S %z'),
            "updated": now.strftime('%Y-%m-%d %H:%M:%S %z')
        }

        user_created = user_service.create(payload)
        return jsonify(user_created.to_dict()), 201


    @app.route('/api/user/list', methods=['GET'])
    @require_jwt
    @require_role("admin")
    def user_list_all():
        users = user_service.get_all()
        users_dict = [user.to_dict() for user in users]
        return jsonify(users_dict), 200

    
    @app.route('/api/usersPPPOE', methods=['GET'])
    @require_jwt
    @require_role("admin")
    def get_users():
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({"msg": "Authorization header is missing"}), 401
        try:
            response = huaweirouterservice.getUsersPPOE(host, port, username, password)
            if not response:
                return jsonify([]), 404
            
            return jsonify(response), 200
        
        except Exception as e:
            jsonify({"error": str(e)}), 500
    
    
    @app.route('/api/details', methods=['GET'])
    @require_jwt
    @require_role("admin")
    def get_details():
        try:
            router_service = huaweirouterservice(host, port, username, password)
            response = router_service.getRouterDetails()
            return jsonify(response)
        
        except Exception as e:
            jsonify({"error": str(e)}), 500
    
    @app.route('/api/interfaces', methods=['GET'])
    @require_jwt
    @require_role("admin")
    def get_interfaces():
        try:
            print(host+' = '+port+' = '+username+' = '+password)
            interfaces = huaweirouterservice.getInterfaces(host, port, username, password)
            if not interfaces:
                return jsonify([]), 404
            
            return interfaces, 200
        except Exception as e:
            jsonify({"error": str(e)}), 500


    @app.route('/api/statusRouter', methods=['GET'])
    @require_jwt
    @require_role("admin")
    def get_status_router():
        try:
            return huaweirouterservice.getStatusRouter(host, port, username, password)
            
        except Exception as e:
            jsonify({"error": str(e)}), 500
            

    @app.route('/api/interfaceDetails/<interface_name>', methods=['GET'])
    @require_jwt
    @require_role("admin")
    def get_interface_details(interface_name):
        try:
            response = huaweirouterservice.getInterfaceDetails(host, port, username, password, interface_name)
            return jsonify(response)
        
        except Exception as e:
            jsonify({"error": str(e)}), 500


    
    @app.route('/api/speed/download', methods=['POST'])
    @require_jwt
    def download_test():
        return send_file(
            TEST_FILE_PATH,
            mimetype="application/octet-stream",
            as_attachment=True,
            download_name="test.bin",
            max_age=0
        )
    

    @app.route('/api/speed/upload', methods=['POST'])
    @require_jwt
    def upload_test():
        if "file" not in request.files:
            return jsonify(error="Nenhum arquivo enviado"), 400

        file = request.files["file"]

        # Salva em disco para não estourar RAM
        tmp_path = "/tmp/upload.bin"
        file.save(tmp_path)
        size = os.path.getsize(tmp_path)
        os.remove(tmp_path)

        return jsonify(uploaded_bytes=size)
    

    @app.route('/api/speed/ping', methods=['GET'])
    @require_jwt
    def ping_test():
        resp = jsonify(status="ok")
        resp.headers["Cache-Control"] = "no-store"
        return resp