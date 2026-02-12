import pandas as pd
from utils.df_utils import (
    profesionales_clean_path,
    especialidades_clean_path,
    obras_sociales_clean_path,
    processor,
)
from schemas.master_schemas import (
    PROFESIONALES_MASTER,
    ESPECIALIDADES_MASTER,
    OBRAS_SOCIALES_MASTER,
)


def main():

    # filtra -> agrupa (con prioridad GoRed) -> popula Master Schema
    processor(
        df=pd.read_csv(profesionales_clean_path),
        schema=PROFESIONALES_MASTER,
        output_name="profesionales",
        filter_field="unificado_prof",
        condition=1,
    )

    processor(
        df=pd.read_csv(especialidades_clean_path),
        schema=ESPECIALIDADES_MASTER,
        output_name="especialidades",
        filter_field="unificado_esp",
        condition=1,
    )

    processor(
        df=pd.read_csv(obras_sociales_clean_path),
        schema=OBRAS_SOCIALES_MASTER,
        output_name="obras_sociales",
        filter_field="unificado_os",
        condition=1,
    )


if __name__ == "__main__":
    main()
