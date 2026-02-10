import pandas as pd


from utils.df_utils import (
    PROCESSED_DIR,
    filter_by_field_value,
    group_by_field,
    get_file_path,
)

profesionales_clean = get_file_path("cleaned", "profesionales.csv")


def main():
    df_profesionales = pd.read_csv(profesionales_clean)

    df_profesionales_homologados = filter_by_field_value(
        df_profesionales, "unificado_prof", True
    )

    df_profesionales_homologados = group_by_field(
        df_profesionales_homologados, "master"
    )

    df_profesionales_homologados.to_csv(
        PROCESSED_DIR / "profesionales_homologados.csv", index=False
    )


if __name__ == "__main__":
    main()
