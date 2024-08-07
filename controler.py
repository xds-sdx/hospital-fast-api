from sqlalchemy import create_engine, or_
from sqlalchemy.orm import sessionmaker, joinedload
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from models.models import Base, Employer, Feria, Transferencia, Reforma, Suspenso, Falecido
import os

# Configurar a conexão com o banco de dados
DATABASE_URI = os.getenv('CONNECT_SQL')
engine = create_engine(DATABASE_URI, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Criar as tabelas do banco de dados se não existirem
def create_base():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def getEmployerByReparticao(reparticao):
    """Retorna a lista de empregados filtrados pela repartição"""
    with SessionLocal() as db:
        return db.query(Employer).filter_by(reparticao=reparticao).all()

def getEmployerBySector(sector):
    """Retorna a lista de empregados filtrados pelo setor"""
    with SessionLocal() as db:
        return db.query(Employer).filter_by(sector=sector).all()

def getById(id):
    """Retorna um empregado com base no ID"""
    with SessionLocal() as db:
        return db.query(Employer).filter_by(id=id).first()

def getLen():
    """Retorna o número de empregados em setores específicos"""
    setores = ["Maternidade", "Laboratorio", "Psiquiatria", "Medicina 1"]
    contagem = {}
    with SessionLocal() as db:
        for setor in setores:
            contagem[setor] = db.query(Employer).filter_by(sector=setor).count()
    return contagem

def addFerias(id, start=datetime.now(), end=datetime.now()):
    try:
        with SessionLocal() as db:
            nova_feria = Feria(
                funcionario_id=id,
                data_inicio_ferias=start,
                data_fim_ferias=end
            )
            funcionario = db.query(Employer).filter_by(id=id).first()
            funcionario.status = "LICENCA"
            db.add(nova_feria)
            db.commit()
            return nova_feria
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Database error occurred: {str(e)}")
        raise

def addTransferencia(id, start=datetime.now(), lugar=""):
    try:
        with SessionLocal() as db:
            transferencia = Transferencia(
                funcionario_id=id,
                data_transferido=start,
                lugar_transferido=lugar
            )
            funcionario = db.query(Employer).filter_by(id=id).first()
            funcionario.status = "TRANSFERIDO"
            db.add(transferencia)
            db.commit()
            return transferencia
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Database error occurred: {str(e)}")
        raise

def addReforma(id, data, idade):
    try:
        with SessionLocal() as db:
            reforma = Reforma(
                funcionario_id=id,
                data_reforma=data,
                idade_reforma=idade
            )
            funcionario = db.query(Employer).filter_by(id=id).first()
            funcionario.status = "APOSENTADO"
            db.add(reforma)
            db.commit()
            return reforma
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Database error occurred: {str(e)}")
        raise

def addSuspenso(id, data=datetime.now(), motivo=""):
    try:
        with SessionLocal() as db:
            suspenso = Suspenso(
                funcionario_id=id,
                data_suspenso=data,
                motivo=motivo
            )
            funcionario = db.query(Employer).filter_by(id=id).first()
            funcionario.status = "SUSPENSO"
            db.add(suspenso)
            db.commit()
            return suspenso
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Database error occurred: {str(e)}")
        raise

def addFalecido(id,data, idade):
    try:
        with SessionLocal() as db:
            falecido = Falecido(
                funcionario_id=id,
                data_falecimento=data,
                idade=idade
            )
            funcionario = db.query(Employer).filter_by(id=id).first()
            funcionario.status = "FALECIDO"
            db.add(falecido)
            db.commit()
            return falecido
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Database error occurred: {str(e)}")
        raise

def getTransferencia():
    with SessionLocal() as db:
        return db.query(Transferencia).join(Employer).all()

def getSuspenso():
    with SessionLocal() as db:
        return db.query(Suspenso).join(Employer).all()

def getReforma():
    with SessionLocal() as db:
        return db.query(Reforma).join(Employer).all()

def getFalecido():
    with SessionLocal() as db:
        return db.query(Falecido).join(Employer).all()

def getFerias():
    with SessionLocal() as db:
        return db.query(Feria).join(Employer).all()

def getEmployers():
    try:
        with SessionLocal() as db:
            employers = db.query(Employer).outerjoin(Feria).filter(
                or_(
                    Employer.status == "ACTIVO",
                    Employer.status == "DISPENSA",
                    Employer.status == "LICENCA"
                )
            ).options(joinedload(Employer.ferias)).all()
            return employers
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Database error occurred: {str(e)}")
        raise
