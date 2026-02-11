import pandas as pd
from utils.df_utils import get_file_path, processor
from schemas.master_schemas import (
    PROFESIONALES_MASTER,
    ESPECIALIDADES_MASTER,
    OBRAS_SOCIALES_MASTER,
)


def main():
    # 1. Cargar el archivo cleaned (el que ya pasó por el normalizador)
    profesionales_clean_path = get_file_path("cleaned", "profesionales.csv")
    especialidades_clean_path = get_file_path("cleaned", "especialidades.csv")
    obras_sociales_clean_path = get_file_path("cleaned", "obras_sociales.csv")
    df_pros = pd.read_csv(profesionales_clean_path)

    # 2. Ejecutar el procesador
    # Este paso: filtra -> agrupa (con prioridad GoRed) -> popula Master Schema
    processor(
        df=df_pros,
        schema=PROFESIONALES_MASTER,
        output_name="profesionales",
        filter_field="unificado_prof",
    )

    processor(
        df=pd.read_csv(especialidades_clean_path),
        schema=ESPECIALIDADES_MASTER,
        output_name="especialidades",
        filter_field="unificado_esp",
    )

    processor(
        df=pd.read_csv(obras_sociales_clean_path),
        schema=OBRAS_SOCIALES_MASTER,
        output_name="obras_sociales",
        filter_field="unificado_os",
    )


if __name__ == "__main__":
    main()
