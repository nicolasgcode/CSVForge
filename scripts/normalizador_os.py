import pandas as pd

from utils.df_utils import (
    CLEANED_DIR,
    add_columns,
    split_by_status,
    standarize_column_names,
    get_file_path,
)

OBRAS_SOCIALES_PATH = get_file_path("raw", "obras_sociales_importadas.csv")


def main():
    df = pd.read_csv(OBRAS_SOCIALES_PATH)

    df_cleaned = df.copy()

    df_cleaned = add_columns(df_cleaned, ["cambio", "createdAt"])

    df_cleaned = standarize_column_names(df_cleaned, "master", "master")

    df_activos, df_eliminados = split_by_status(df_cleaned)

    df_activos.to_csv(CLEANED_DIR / "obras_sociales.csv", index=False)
    df_eliminados.to_csv(CLEANED_DIR / "obras_sociales_eliminados.csv", index=False)


if __name__ == "__main__":
    main()
