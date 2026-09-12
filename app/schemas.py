from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List, Optional


class UsuarioBase(BaseModel):
    nombre: str
    correo: str
    telefono: Optional[str] = None


class UsuarioCreate(UsuarioBase):
    pass


class Usuario(UsuarioBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class ProductoBase(BaseModel):
    nombre: str
    precio: float
    stock: int = 0


class ProductoCreate(ProductoBase):
    pass


class Producto(ProductoBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class DetalleItem(BaseModel):
    producto_id: int
    cantidad: int


class DetallePedido(BaseModel):
    id: int
    producto_id: int
    cantidad: int
    precio_unitario: float
    producto: Producto
    model_config = ConfigDict(from_attributes=True)


class PedidoCreate(BaseModel):
    usuario_id: int
    productos: List[DetalleItem]


class Pedido(BaseModel):
    id: int
    usuario_id: int
    fecha: datetime
    total: float
    estado: str
    usuario: Usuario
    detalles: List[DetallePedido]
    model_config = ConfigDict(from_attributes=True)