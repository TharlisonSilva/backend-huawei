from datetime import datetime
from uuid import UUID
from app import db

class user_ssh_entity(db.Model):
    __tablename__ = 'HC_USERS_SSH'
    id = db.Column(db.String(100), primary_key=True)
    host = db.Column(db.String(25), nullable=False)
    port = db.Column(db.String(10), nullable=False)
    user = db.Column(db.String(25), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    created = db.Column(db.String(100), nullable=False)
    updated = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        colunas = {col.name: getattr(self, col.name) for col in self.__table__.columns}
        return f"<UserSSHEntity {colunas}>"
    
    def to_dict(self) -> dict:
            return {
                "id": str(self.id) if isinstance(self.id, UUID) else self.id,
                "host": self.host,
                "port": self.port,
                "user": self.user,
                "password": self.port,
                "created": (
                    self.created.isoformat()
                    if isinstance(self.created, datetime) else str(self.created)
                ),
                "updated": (
                    self.updated.isoformat()
                    if isinstance(self.updated, datetime) else str(self.updated)
                ),
            }