def create(db_session):
    from datetime import datetime
    import uuid
    from zoneinfo import ZoneInfo

    from app.infra.entities.user_entity import user_entity
    from app.core.usecases import user_service

    usuario_existente = db_session.query(user_entity).filter_by(username="admin.app@appcreations.com.br").first()

    if not usuario_existente:
        pass_encrypted = user_service.hash_password("user.admin.login")
        now = datetime.now(ZoneInfo("America/Sao_Paulo"))

        payload = {
            "id": uuid.uuid4(),
            "username": "admin.app@appcreations.com.br",
            "role": "admin",
            "password": pass_encrypted,
            "created": now.strftime('%Y-%m-%d %H:%M:%S %z'),
            "updated": now.strftime('%Y-%m-%d %H:%M:%S %z')
        }

        user = user_entity(**payload)
        db_session.add(user)
        db_session.commit()
        print("✅ Usuário admin criado com sucesso.")
    else:
        print("ℹ️ Usuário admin já existe.")