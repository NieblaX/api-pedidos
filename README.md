# API de Pedidos

API REST para gestionar usuarios, productos y pedidos, desarrollada como práctica de la materia **Bases de Datos en la Nube**.

## Stack utilizado

- **Base de datos:** PostgreSQL en Neon (cloud)
- **Backend:** FastAPI (Python)
- **ORM:** SQLAlchemy
- **Documentación interactiva:** Swagger (OpenAPI, generado automáticamente por FastAPI)

## Estructura del proyecto

```
api-pedidos/
│
├── app/
│   ├── main.py            # Punto de entrada de la aplicación
│   ├── database.py        # Conexión a la base de datos (Neon)
│   ├── models.py          # Modelos SQLAlchemy (tablas)
│   ├── schemas.py         # Esquemas Pydantic (validación de datos)
│   │
│   └── routers/
│       ├── usuarios.py
│       ├── productos.py
│       └── pedidos.py
│
├── .env                    # Variables de entorno (NO se sube a GitHub)
├── .gitignore
├── requirements.txt
├── diagrama-der.png
└── README.md
```

## Modelo de datos

El sistema cuenta con 4 tablas relacionadas:

- **usuarios** → puede tener muchos **pedidos** (1:N)
- **pedidos** → puede tener muchos **detalle_pedido** (1:N)
- **productos** → puede aparecer en muchos **detalle_pedido** (1:N)

`detalle_pedido` funciona como tabla intermedia, permitiendo que un pedido tenga varios productos y que un producto aparezca en varios pedidos (N:M entre `pedidos` y `productos`).

Ver diagrama entidad-relación: `diagrama-der.png`

## Instalación y ejecución local

### 1. Clonar el repositorio

```bash
git clone https://github.com/TU_USUARIO/api-pedidos.git
cd api-pedidos
```

### 2. Crear entorno virtual

```bash
python -m venv venv
```

Activarlo:

- **Windows (PowerShell):**
  ```powershell
  Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
  .\venv\Scripts\Activate.ps1
  ```
- **Linux / macOS:**
  ```bash
  source venv/bin/activate
  ```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Crear un archivo `.env` en la raíz del proyecto con tu cadena de conexión de Neon:

```
DATABASE_URL="postgresql://usuario:contraseña@servidor/neondb?sslmode=require"
```

### 5. Ejecutar el servidor

```bash
uvicorn app.main:app --reload
```

La API quedará disponible en:

- App: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- Documentación Swagger: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

Al iniciar, las tablas se crean automáticamente en Neon si no existen (`Base.metadata.create_all`).

## Endpoints

### Usuarios

| Método | Endpoint          | Descripción                |
|--------|-------------------|-----------------------------|
| GET    | `/usuarios/`       | Lista todos los usuarios   |
| GET    | `/usuarios/{id}`   | Obtiene un usuario por ID  |
| POST   | `/usuarios/`       | Crea un nuevo usuario      |
| PUT    | `/usuarios/{id}`   | Actualiza un usuario       |
| DELETE | `/usuarios/{id}`   | Elimina un usuario         |

### Productos

| Método | Endpoint            | Descripción                  |
|--------|---------------------|-------------------------------|
| GET    | `/productos/`        | Lista todos los productos    |
| GET    | `/productos/{id}`    | Obtiene un producto por ID   |
| POST   | `/productos/`        | Crea un nuevo producto       |
| PUT    | `/productos/{id}`    | Actualiza un producto        |
| DELETE | `/productos/{id}`    | Elimina un producto          |

### Pedidos

| Método | Endpoint          | Descripción                                              |
|--------|-------------------|-----------------------------------------------------------|
| GET    | `/pedidos/`        | Lista todos los pedidos                                   |
| GET    | `/pedidos/{id}`    | Obtiene un pedido con su usuario y detalle de productos    |
| POST   | `/pedidos/`        | Crea un pedido, valida stock, descuenta inventario y calcula el total |
| DELETE | `/pedidos/{id}`    | Elimina un pedido (elimina en cascada su detalle)          |

## Ejemplo de creación de pedido

```json
POST /pedidos/
{
  "usuario_id": 1,
  "productos": [
    { "producto_id": 1, "cantidad": 2 },
    { "producto_id": 2, "cantidad": 1 }
  ]
}
```

La API valida que el usuario y los productos existan, verifica que haya stock suficiente, descuenta el inventario y calcula el total automáticamente.

## Manejo de errores

| Código | Caso                                              |
|--------|----------------------------------------------------|
| 200    | Operación exitosa (GET, DELETE)                    |
| 201    | Recurso creado exitosamente (POST)                 |
| 400    | Solicitud inválida (correo duplicado, stock insuficiente) |
| 404    | Recurso no encontrado (usuario, producto o pedido)  |
| 422    | Error de validación de datos (tipo de dato incorrecto) |

## Seguridad

Las credenciales de conexión a la base de datos se manejan mediante variables de entorno (`.env`), el cual está excluido del control de versiones mediante `.gitignore`.
