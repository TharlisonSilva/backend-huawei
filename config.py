import os
db_host = os.getenv("DB_HOST", "localhost")
db_name = os.getenv("DB_NAME", "RavenBox")
db_user = os.getenv("DB_USER", "RavenUser")
db_pass = os.getenv("DB_PASS", "91553154")

class Config:
    JWT_SECRET_KEY = 'asdfaksfaksjdfafj124178243785sfjaksdhfhasdf786738156435782623847hfhajksfhajk'
    JWT_TOKEN_LOCATION = ['headers']
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'
    PROPAGATE_EXCEPTIONS = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://'+db_user+':'+db_pass+'@'+db_host+':3306/'+db_name
    #SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://RavenUser:91553154@localhost:3306/RavenBox'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
