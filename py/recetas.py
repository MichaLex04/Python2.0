# py/recetas.py
from db import queries
from py.db_connection import query_fetchall, query_fetchone, query_execute

def listar_recetas():
    query = queries.obtener_recetas()
    return query_fetchall(query)

def obtener_insumos(receta_id):
    query, params = queries.obtener_insumos_por_receta(receta_id)
    return query_fetchall(query, params)

def calcular_cantidades(receta_id, personas):
    insumos = obtener_insumos(receta_id)
    resultado = []
    for insumo in insumos:
        cantidad_base = float(insumo['cantidad_por_persona'])
        perdida = float(insumo['perdida_porcentaje']) / 100
        precio_unit = float(insumo['precio_por_unidad'])

        # Ajuste por pérdida: cantidad necesaria = cantidad_base / (1 - perdida)
        cantidad_ajustada = cantidad_base / (1 - perdida) * personas

        # Precio por ración = cantidad_base * precio_unit (asumiendo precio_unit por unidad base)
        precio_por_racion = cantidad_base * precio_unit

        resultado.append({
            "nombre": insumo['nombre'],
            "cantidad_ajustada": round(cantidad_ajustada, 3),
            "precio_por_racion": round(precio_por_racion, 2)
        })
    return resultado

def guardar_receta(nombre, descripcion, insumos):
    """
    insumos: lista de dicts con keys:
        - nombre
        - cantidad_por_persona
        - perdida_porcentaje
        - precio_por_unidad
    """
    # Insertar receta
    query, params = queries.insertar_receta(nombre, descripcion)
    conn = None
    try:
        from py.db_connection import get_connection
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute(query, params)
            receta_id = cur.fetchone()[0]

            for ins in insumos:
                # Insertar insumo si no existe
                query_insumo, params_insumo = queries.insertar_insumo(ins['nombre'])
                cur.execute(query_insumo, params_insumo)
                if cur.rowcount == 0:
                    # Ya existe, obtener id
                    cur.execute("SELECT id FROM insumos WHERE nombre = %s", (ins['nombre'],))
                    insumo_id = cur.fetchone()[0]
                else:
                    insumo_id = cur.fetchone()[0]

                # Insertar relación receta_insumo
                query_ri, params_ri = queries.insertar_receta_insumo(
                    receta_id,
                    insumo_id,
                    ins['cantidad_por_persona'],
                    ins['perdida_porcentaje'],
                    ins['precio_por_unidad']
                )
                cur.execute(query_ri, params_ri)
        conn.commit()
        return receta_id
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()