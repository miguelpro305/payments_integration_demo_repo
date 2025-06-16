from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Plan(Base):
    __tablename__ = 'plan'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    precio = Column(Float, nullable=False)
    rol = Column(String(50), nullable=False)
    duracion = Column(Integer, nullable=False)  # En días

class Compra(Base):
    __tablename__ = 'compra'
    id = Column(Integer, primary_key=True)
    id_usuario = Column(Integer, nullable=False)
    id_plan = Column(Integer, ForeignKey('plan.id'), nullable=False)
    url_pago = Column(String, nullable=False)
    id_transaccion = Column(String, nullable=False)
    estado_pago = Column(String, default='Pendiente', nullable=False)
    activo = Column(Boolean, default=False)
    fecha_compra = Column(DateTime, nullable=False)
    fecha_finalizacion = Column(DateTime, nullable=False)
