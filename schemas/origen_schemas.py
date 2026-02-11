PROFESIONALES_ORIGEN = {
    "table_name": "origen_profesionales",
    "order": [
        "id_master",
        "id",
        "idOrigen",
        "origen",
        "apellido",
        "nombre",
        "cuit",
        "genero",
        "titulo",
        "email",
        "telefono",
        "seo",
        "slug_apellido",
        "slug_nombre",
        "eliminado",
        "unificado_prof",
        "createdAt",
        "cambio",
    ],
    "types": {
        "eliminado": "bool",
        "unificado_prof": "bool",
        "id_master": "int",
        "createdAt": "datetime",
        "cambio": "datetime",
    },
}

ESPECIALIDADES_ORIGEN = {
    "table_name": "origen_especialidades",
    "order": [
        "id_master",  # FK al Master de Especialidades
        "id",  # PK Local del registro
        "idOrigen",  # ID en el sistema fuente
        "origen",  # Código de sistema (GoRed, OS, etc.)
        "descripcion",
        "slug_descripcion",  # Metadato para URL/SEO
        "eliminado",  # Estado lógico
        "unificado_esp",  # Flag de proceso de homologación
        "createdAt",  # Fecha de creación
        "cambio",  # Fecha de última modificación
    ],
    "types": {"id_master": "int", "eliminado": "bool", "unificado_esp": "bool"},
}

OBRAS_SOCIALES_ORIGEN = {
    "table_name": "origen_obras_sociales",
    "order": [
        "id_master",  # FK al Master de Obras Sociales
        "id",  # PK Local
        "idOrigen",  # ID Sistema Fuente
        "origen",  # Código de origen
        "nombre",  # Nombre oficial
        "descripcion",  # Descripción o Razón Social
        "habilitado",  # Estado de vigencia
        "slug_nombre",  # SEO Nombre
        "slug_descripcion",  # SEO Descripción
        "eliminado",  # Estado lógico
        "unificado_os",  # Flag de proceso
        "createdAt",  # Auditoría
        "cambio",  # Auditoría
    ],
    "types": {
        "id_master": "int",
        "eliminado": "bool",
        "habilitado": "bool",
        "unificado_os": "bool",
    },
}
