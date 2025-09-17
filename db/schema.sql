-- Esquema para recetas e insumos

CREATE TABLE IF NOT EXISTS recetas (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    descripcion TEXT
);

CREATE TABLE IF NOT EXISTS insumos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS receta_insumos (
    id SERIAL PRIMARY KEY,
    receta_id INTEGER REFERENCES recetas(id) ON DELETE CASCADE,
    insumo_id INTEGER REFERENCES insumos(id),
    cantidad_por_persona NUMERIC(10,3) NOT NULL, -- en gramos o kilogramos (definir unidad)
    perdida_porcentaje NUMERIC(5,2) DEFAULT 0, -- porcentaje de pérdida (ej: 5.00)
    precio_por_unidad NUMERIC(10,2) NOT NULL -- precio por kg o g según unidad
);

-- Índices para optimizar consultas
CREATE INDEX idx_receta_insumos_receta ON receta_insumos(receta_id);
CREATE INDEX idx_receta_insumos_insumo ON receta_insumos(insumo_id);