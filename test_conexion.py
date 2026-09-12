from app.database import engine
from sqlalchemy import text

try:
    with engine.connect() as conn:
        resultado = conn.execute(text("SELECT version();"))
        print("✅ Conexión exitosa a Neon")
        print(resultado.fetchone())
except Exception as e:
    print("❌ Error de conexión:")
    print(e)