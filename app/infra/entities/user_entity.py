from datetime import datetime
from uuid import UUID
from app import db

class user_entity(db.Model):
    __tablename__ = 'HC_USERS'
    id = db.Column(db.String(100), primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(25), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    created = db.Column(db.String(100), nullable=False)
    updated = db.Column(db.String(100), nullable=False)
    
    def __repr__(self):
        colunas = {col.name: getattr(self, col.name) for col in self.__table__.columns}
        return f"<UserEntity {colunas}>"
    
    def to_dict(self) -> dict:
            return {
                "id": str(self.id) if isinstance(self.id, UUID) else self.id,
                "username": self.username,
                "role": self.role,
                "created": (
                    self.created.isoformat()
                    if isinstance(self.created, datetime) else str(self.created)
                ),
                "updated": (
                    self.updated.isoformat()
                    if isinstance(self.updated, datetime) else str(self.updated)
                ),
            }