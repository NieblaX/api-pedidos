from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])


@router.get("/", response_model=list[schemas.Pedido])
def listar_pedidos(db: Session = Depends(get_db)):
    return db.query(models.Pedido).all()


@router.get("/{pedido_id}", response_model=schemas.Pedido)
def obtener_pedido(pedido_id: int, db: Session = Depends(get_db)):
    pedido = db.query(models.Pedido).filter(models.Pedido.id == pedido_id).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return pedido


@router.post("/", response_model=schemas.Pedido, status_code=201)
def crear_pedido(pedido: schemas.PedidoCreate, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.id == pedido.usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if not pedido.productos:
        raise HTTPException(status_code=400, detail="El pedido debe incluir al menos un producto")

    nuevo_pedido = models.Pedido(usuario_id=pedido.usuario_id, total=0, estado="pendiente")
    db.add(nuevo_pedido)
    db.flush()  # para obtener el id del pedido antes de crear los detalles

    total = 0

    for item in pedido.productos:
        producto = db.query(models.Producto).filter(models.Producto.id == item.producto_id).first()
        if not producto:
            db.rollback()
            raise HTTPException(status_code=404, detail=f"Producto {item.producto_id} no encontrado")

        if producto.stock < item.cantidad:
            db.rollback()
            raise HTTPException(
                status_code=400,
                detail=f"Stock insuficiente para '{producto.nombre}' (disponible: {producto.stock})"
            )

        producto.stock -= item.cantidad

        detalle = models.DetallePedido(
            pedido_id=nuevo_pedido.id,
            producto_id=producto.id,
            cantidad=item.cantidad,
            precio_unitario=producto.precio
        )
        db.add(detalle)

        total += producto.precio * item.cantidad

    nuevo_pedido.total = total
    db.commit()
    db.refresh(nuevo_pedido)
    return nuevo_pedido


@router.delete("/{pedido_id}", status_code=200)
def eliminar_pedido(pedido_id: int, db: Session = Depends(get_db)):
    pedido = db.query(models.Pedido).filter(models.Pedido.id == pedido_id).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    db.delete(pedido)
    db.commit()
    return {"mensaje": "Pedido eliminado correctamente"}