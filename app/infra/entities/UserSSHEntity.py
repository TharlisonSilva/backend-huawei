from app import db

class UserSSHEntity(db.Model):
    __tablename__ = 'USER_SSH'
    id = db.Column(db.String(100), primary_key=True)
    host = db.Column(db.String(25), nullable=False)
    port = db.Column(db.String(10), nullable=False)
    user = db.Column(db.String(25), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        colunas = {col.name: getattr(self, col.name) for col in self.__table__.columns}
        return f"<UserSSHEntity {colunas}>"