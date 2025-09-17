# db/queries.py

def insertar_receta(nombre, descripcion):
    return """
    INSERT INTO recetas (nombre, descripcion)
    VALUES (%s, %s)
    RETURNING id;
    """, (nombre, descripcion)

def insertar_insumo(nombre):
    return """
    INSERT INTO insumos (nombre)
    VALUES (%s)
    ON CONFLICT (nombre) DO NOTHING
    RETURNING id;
    """, (nombre,)

def insertar_receta_insumo(receta_id, insumo_id, cantidad_por_persona, perdida_porcentaje, precio_por_unidad):
    return """
    INSERT INTO receta_insumos (receta_id, insumo_id, cantidad_por_persona, perdida_porcentaje, precio_por_unidad)
    VALUES (%s, %s, %s, %s, %s);
    """, (receta_id, insumo_id, cantidad_por_persona, perdida_porcentaje, precio_por_unidad)

def obtener_recetas():
    return "SELECT id, nombre FROM recetas ORDER BY nombre;"

def obtener_insumos_por_receta(receta_id):
    return """
    SELECT i.nombre, ri.cantidad_por_persona, ri.perdida_porcentaje, ri.precio_por_unidad
    FROM receta_insumos ri
    JOIN insumos i ON ri.insumo_id = i.id
    WHERE ri.receta_id = %s;
    """, (receta_id,)