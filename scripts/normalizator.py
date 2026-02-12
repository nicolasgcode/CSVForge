import pandas as pd

from utils.df_utils import CLEANED_DIR, get_file_path, normalizator
from schemas.origen_schemas import (
    PROFESIONALES_ORIGEN,
    OBRAS_SOCIALES_ORIGEN,
    ESPECIALIDADES_ORIGEN,
)


def main():
    # Procesar Profesionales
    df_pros = pd.read_csv(get_file_path("raw", "profesionales_importados.csv"))
    normalizator(
        df=df_pros,
        path=CLEANED_DIR,
        schema=PROFESIONALES_ORIGEN,
        output_name="profesionales",
        rename_map={
            "masterInst": "id_master",
        },
    )

    # Procesar Obras Sociales
    df_os = pd.read_csv(get_file_path("raw", "obras_sociales_importadas.csv"))
    normalizator(
        df=df_os,
        path=CLEANED_DIR,
        schema=OBRAS_SOCIALES_ORIGEN,
        output_name="obras_sociales",
        rename_map={
            "masterOs": "id_master",
        },
    )

    # Procesar Especialidades
    df_esp = pd.read_csv(get_file_path("raw", "Especialidades_importadas.csv"))
    normalizator(
        df=df_esp,
        path=CLEANED_DIR,
        schema=ESPECIALIDADES_ORIGEN,
        output_name="especialidades",
        rename_map={
            "masterEsp": "id_master",
            "descripcion": "nombre",
        },
    )


if __name__ == "__main__":
    main()
