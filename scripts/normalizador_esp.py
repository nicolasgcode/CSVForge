import pandas as pd

from utils.df_utils import (
    CLEANED_DIR,
    add_columns,
    standarize_column_names,
    split_by_status,
    get_file_path,
)

ESPECIALIDADES_PATH = get_file_path("raw", "especialidades_importadas.csv")


def main():
    df = pd.read_csv(ESPECIALIDADES_PATH)

    df_cleaned = df.copy()

    df_cleaned = add_columns(df_cleaned, ["cambio", "createdAt"])

    df_cleaned = standarize_column_names(df_cleaned, "master", "master")

    df_activos, df_eliminados = split_by_status(df_cleaned)

    df_activos.to_csv(CLEANED_DIR / "especialidades.csv", index=False)
    df_eliminados.to_csv(CLEANED_DIR / "especialidades_eliminados.csv", index=False)


if __name__ == "__main__":
    main()
