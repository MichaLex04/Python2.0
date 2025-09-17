# py/calculos.py
import numpy as np

def ajustar_cantidad(cantidad_por_persona, perdida_porcentaje, personas):
    """
    Ajusta la cantidad total considerando pérdidas.
    """
    perdida = perdida_porcentaje / 100
    cantidad_total = cantidad_por_persona / (1 - perdida) * personas
    return round(cantidad_total, 3)

def calcular_precio_por_racion(cantidad_por_persona, precio_por_unidad):
    """
    Calcula el precio por ración.
    """
    return round(cantidad_por_persona * precio_por_unidad, 2)

# Ejemplo de uso con numpy para vectorizar cálculos si se requiere
def calcular_varios(insumos, personas):
    cantidades = np.array([i['cantidad_por_persona'] for i in insumos])
    perdidas = np.array([i['perdida_porcentaje'] for i in insumos]) / 100
    precios = np.array([i['precio_por_unidad'] for i in insumos])

    cantidades_ajustadas = cantidades / (1 - perdidas) * personas
    precios_por_racion = cantidades * precios

    return np.round(cantidades_ajustadas, 3), np.round(precios_por_racion, 2)