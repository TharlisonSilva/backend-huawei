from app import db

class CustomerEntity(db.Model):
    __tablename__ = 'CUSTOMERS'
    id = db.Column(db.String(100), primary_key=True)
    razao_social = db.Column(db.String(255), nullable=False)
    cnpj = db.Column(db.String(25), nullable=False)
    phone = db.Column(db.String(25), nullable=True)
    name_user = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        colunas = {col.name: getattr(self, col.name) for col in self.__table__.columns}
        return f"<CustomerEntity {colunas}>"