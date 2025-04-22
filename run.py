from app import create_app, db
import os
from app.infra.initial_config import create_user_admin

port = os.getenv("PORT", "4001")
app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        create_user_admin.create(db.session)

    app.run(host="0.0.0.0", port=int(port))

