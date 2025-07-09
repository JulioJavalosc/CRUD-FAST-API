from datetime import datetime
from sqlalchemy import VARCHAR, Boolean, CheckConstraint, Column, ForeignKey, Integer, String,DateTime, text
from database import Base
from sqlalchemy.orm import declarative_base, relationship


class LotesSaboresBase(Base):
    __tablename__ = 'lotes_sabores_base'

    id_lote = Column(Integer, primary_key=True, autoincrement=True)
    id_sabor = Column(Integer, ForeignKey('Sabores_Base.id_Sabor'), nullable=False)
    peso_total_gr = Column(Integer, nullable=False)
    peso_disponible_gr = Column(Integer, nullable=False)
    fecha_ingreso = Column(DateTime, default=datetime.now())
    numero_lote = Column(String(45), nullable=True)
    sabor = relationship("SaboresBase", back_populates="lotes")
    consumos = relationship("ConsumoLoteHelado", back_populates="lote")
class ConsumoLoteHelado(Base):
    __tablename__ = 'consumo_lote_helado'

    id_consumo = Column(Integer, primary_key=True, autoincrement=True)
    id_detalle_helado = Column(Integer, ForeignKey('Detalle_Helado_Personalizado.idDetalle_Helado_Personalizado'), nullable=False)    
    id_lote = Column(Integer, ForeignKey('lotes_sabores_base.id_lote'), nullable=False)
    cantidad_utilizada_gr = Column(Integer, nullable=False)

    lote = relationship("LotesSaboresBase", back_populates="consumos")
    detalle_helado = relationship("DetalleHeladoPersonalizado", back_populates="consumos_lote")

class TipoUsuarios(Base):#Listo
    __tablename__ = 'Tipo_Usuarios'
    id = Column(Integer, primary_key=True, autoincrement=True)
    Nombre = Column(String(45), nullable=True)
    activo = Column(Boolean, default=True)
class Usuarios(Base):#Listo
    __tablename__ = 'Usuarios'
    id = Column(Integer, primary_key=True, autoincrement=True)
    Nombre = Column(String(45), nullable=False)
    telefono = Column(String(45), nullable=True)
    email = Column(String(45), nullable=True)
    password = Column(String(45), nullable=False)
    activo = Column(Boolean, default=True)
    Tipo_Usuarios_id = Column(Integer, ForeignKey('Tipo_Usuarios.id'), nullable=False)

    tipo_usuario = relationship("TipoUsuarios", backref="usuarios")

class Clientes(Base):#Listo
    __tablename__ = 'Clientes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    Nombre = Column(String(45), nullable=False)
    Apellido = Column(String(45), nullable=True)
    telefono = Column(String(45), nullable=True)

class TipoPago(Base):
    __tablename__ = 'Tipo_Pago'
    id = Column(Integer, primary_key=True, autoincrement=True)
    Descripcion = Column(String(45), nullable=True)


class SaboresBase(Base):#Listo
    __tablename__ = 'Sabores_Base'
    id_Sabor = Column(Integer, primary_key=True, autoincrement=True)
    Nombre = Column(String(45), nullable=False)
    Precio = Column(Integer, nullable=False)
    lotes = relationship("LotesSaboresBase", back_populates="sabor")

class ProductosFijos(Base):#Listo
    __tablename__ = 'Productos_Fijos'
    idProducto = Column(Integer, primary_key=True, autoincrement=True)
    Descripcion = Column(String(45), nullable=False)
    Precio = Column(Integer, nullable=False)
    Stock = Column(Integer, nullable=False)

class HeladosPersonalizados(Base):
    __tablename__ = 'Helados_Personalizados'
    idHelado = Column(Integer, primary_key=True, autoincrement=True)
    precio_total = Column(Integer, nullable=False)

class DetalleHeladoPersonalizado(Base):
    __tablename__ = 'Detalle_Helado_Personalizado'

    idDetalle_Helado_Personalizado = Column(Integer, primary_key=True, autoincrement=True)
    idHelado = Column(Integer, ForeignKey('Helados_Personalizados.idHelado'), nullable=False)
    id_Sabor = Column(Integer, ForeignKey('Sabores_Base.id_Sabor'), nullable=False)
    Cantidad_Bolas = Column(Integer, nullable=False)

    helado_personalizado = relationship("HeladosPersonalizados", backref="detalles")
    sabor_base = relationship("SaboresBase", backref="detalles_helado")
    consumos_lote = relationship("ConsumoLoteHelado", back_populates="detalle_helado")
class Ventas(Base):
    __tablename__ = 'Ventas'
    idVenta = Column(Integer, primary_key=True, autoincrement=True)
    Fecha = Column(DateTime, nullable=False, server_default=text("(datetime('now'))"))    
    Clientes_id = Column(Integer, ForeignKey('Clientes.id'), nullable=False)
    total = Column(Integer, nullable=False)
    estado = Column(Integer, nullable=False)
    Usuarios_id = Column(Integer, ForeignKey('Usuarios.id'), nullable=False)

    cliente = relationship("Clientes", backref="ventas")
    usuario = relationship("Usuarios", backref="ventas")
class DetalleVenta(Base):
    __tablename__ = 'Detalle_Venta'
    idDetalle_Venta = Column(Integer, primary_key=True, autoincrement=True)
    Cantidad = Column(Integer, nullable=False)
    subtotal = Column(Integer, nullable=False)
    idVenta = Column(Integer, ForeignKey('Ventas.idVenta'), nullable=False)
    idProducto = Column(Integer, ForeignKey('Productos_Fijos.idProducto'), nullable=True)
    idHelado = Column(Integer, ForeignKey('Helados_Personalizados.idHelado'), nullable=True)

    venta = relationship("Ventas", backref="detalles")
    producto_fijo = relationship("ProductosFijos", backref="detalles_venta")
    helado_personalizado = relationship("HeladosPersonalizados", backref="detalles_venta")

class MovimientosStock(Base):
    __tablename__ = 'Movimientos_Stock'

    id = Column(Integer, primary_key=True, autoincrement=True)
    Cantidad = Column(Integer, nullable=False)
    Fecha = Column(DateTime, nullable=False)
    
    # Nuevo campo para tipo de movimiento (1 = Entrada, 2 = Salida)
    Tipo_Movimiento = Column(Integer, nullable=False)
    __table_args__ = (
        CheckConstraint(Tipo_Movimiento.in_([1, 2]), name='check_tipo_movimiento'),
    )
    idUsuario = Column(Integer, ForeignKey('Usuarios.id'), nullable=False)   
    idProducto = Column(Integer, ForeignKey('Productos_Fijos.idProducto'), nullable=True)
    producto_fijo = relationship("ProductosFijos", backref="movimientos_stock")
    usuario = relationship("Usuarios", backref="movimientos_stock")

    