# API de Pedidos

Este es mi proyecto para la práctica de **Bases de Datos en la Nube**: una API REST con FastAPI conectada a PostgreSQL en Neon, que maneja un sistema de pedidos con usuarios, productos e inventario.

## Por qué este stack

Elegí Neon porque es PostgreSQL real pero con un free tier fácil de usar para un proyecto escolar, y FastAPI porque genera documentación Swagger automáticamente, lo cual me sirvió muchísimo para probar los endpoints sin tener que montar Postman desde cero. Para el ORM usé SQLAlchemy, conectado mediante variables de entorno para no dejar credenciales expuestas en el código.

## Modelo de datos

El sistema tiene 4 tablas: `usuarios`, `productos`, `pedidos` y `detalle_pedido`. La razón de la cuarta tabla es que un pedido puede tener varios productos y un producto puede aparecer en varios pedidos, así que `detalle_pedido` funciona como tabla intermedia entre ambos. Un usuario puede tener muchos pedidos, y cada pedido tiene su propio detalle con la cantidad y precio unitario de cada producto al momento de la compra.

Puedes ver el diagrama entidad-relación completo en `diagrama-der.png`.

## Estructura del proyecto

```
api-pedidos/
│
├── app/
│   ├── main.py            # Punto de entrada de la aplicación
│   ├── database.py        # Conexión a Neon
│   ├── models.py          # Tablas (SQLAlchemy)
│   ├── schemas.py         # Validación de datos (Pydantic)
│   └── routers/
│       ├── usuarios.py
│       ├── productos.py
│       └── pedidos.py
│
├── capturas/               # Evidencia de pruebas en Swagger
├── .env                    # Variables de entorno (no se sube a GitHub)
├── .gitignore
├── requirements.txt
├── diagrama-der.png
└── README.md
```

## Cómo correrlo

1. Clona el repo y entra a la carpeta:
   ```bash
   git clone https://github.com/NieblaX/api-pedidos.git
   cd api-pedidos
   ```

2. Crea el entorno virtual y actívalo:
   ```bash
   python -m venv venv
   ```
   En Windows (PowerShell):
   ```powershell
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
   .\venv\Scripts\Activate.ps1
   ```

3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Crea un archivo `.env` en la raíz con tu propia cadena de conexión de Neon:
   ```
   DATABASE_URL="postgresql://usuario:contraseña@servidor/neondb?sslmode=require"
   ```

5. Levanta el servidor:
   ```bash
   uvicorn app.main:app --reload
   ```

La API queda en `http://127.0.0.1:8000` y la documentación interactiva en `http://127.0.0.1:8000/docs`. Al arrancar, las 4 tablas se crean solas en Neon si todavía no existen.

## Endpoints

Usuarios y productos tienen el CRUD completo: `GET /usuarios/`, `GET /usuarios/{id}`, `POST`, `PUT` y `DELETE` (igual para `/productos/`).

El endpoint que más trabajo me costó fue `POST /pedidos/`, porque no solo crea el registro, sino que valida que el usuario y los productos existan, revisa que haya stock suficiente para cada producto, descuenta el inventario, calcula el total sumando cada línea, y crea los registros de `detalle_pedido` correspondientes — todo en una sola transacción. Ejemplo de lo que espera:

```json
{
  "usuario_id": 1,
  "productos": [
    { "producto_id": 1, "cantidad": 2 },
    { "producto_id": 2, "cantidad": 1 }
  ]
}
```

`GET /pedidos/{id}` regresa el pedido completo con los datos del usuario y el detalle de cada producto anidado, y `DELETE /pedidos/{id}` borra el pedido junto con su detalle gracias al cascade configurado en el modelo.

## Manejo de errores

Los endpoints regresan `404` cuando no encuentran un usuario, producto o pedido, y `400` en casos como intentar registrar un correo que ya existe o pedir más cantidad de un producto de la que hay en stock. Las capturas de estas pruebas están en la carpeta `capturas/`.

## Un problema que me tocó resolver

Mientras probaba, me empezó a tronar el `POST /pedidos/` con un error 500 de `SSL connection has been closed unexpectedly`. Investigando encontré que Neon cierra las conexiones inactivas después de un rato, y SQLAlchemy seguía intentando usar una conexión del pool que ya estaba muerta del lado del servidor. Se resolvió agregando `pool_pre_ping=True` y `pool_recycle=300` al engine en `database.py`, para que verifique la conexión antes de usarla y la recicle cada 5 minutos.

## Seguridad

La cadena de conexión a Neon vive únicamente en `.env`, el cual está excluido del repositorio mediante `.gitignore` — nunca se sube a GitHub.