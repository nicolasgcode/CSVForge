import pandas as pd

from pathlib import Path

from utils.df_utils import filter_by_field_value, group_by_field

BASE_DIR = Path(__file__).parent.parent
CLEANED_DIR = BASE_DIR / "data" / "cleaned"
PROCESSED_DIR = BASE_DIR / "data" / "processed"


def main():
    profesionales_clean_path = CLEANED_DIR / "profesionales.csv"
    df_profesionales = pd.read_csv(profesionales_clean_path)

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
