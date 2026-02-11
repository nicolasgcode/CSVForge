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
        field_to_rename="masterInst",  # Por si en el raw se llama distinto
        new_field_name="id_master",
    )

    # Procesar Obras Sociales
    df_os = pd.read_csv(get_file_path("raw", "obras_sociales_importadas.csv"))
    normalizator(
        df=df_os,
        path=CLEANED_DIR,
        schema=OBRAS_SOCIALES_ORIGEN,
        output_name="obras_sociales",
        field_to_rename="masterOs",  # Por si en el raw se llama distinto
        new_field_name="id_master",
    )

    # Procesar Especialidades
    df_esp = pd.read_csv(get_file_path("raw", "Especialidades_importadas.csv"))
    normalizator(
        df=df_esp,
        path=CLEANED_DIR,
        schema=ESPECIALIDADES_ORIGEN,
        output_name="especialidades",
        field_to_rename="masterEsp",  # Por si en el raw se llama distinto
        new_field_name="id_master",
    )


if __name__ == "__main__":
    main()
