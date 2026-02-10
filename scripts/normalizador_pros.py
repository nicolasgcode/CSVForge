import pandas as pd

from utils.df_utils import (
    CLEANED_DIR,
    standarize_column_names,
    split_by_status,
    get_file_path,
)

PROS_PATH = get_file_path("raw", "profesionales_importados.csv")


def main():
    df = pd.read_csv(PROS_PATH)

    df_cleaned = df.copy()

    df_cleaned = standarize_column_names(df_cleaned, "master", "master")

    df_activos, df_eliminados = split_by_status(df_cleaned)

    df_activos.to_csv(CLEANED_DIR / "profesionales.csv", index=False)
    df_eliminados.to_csv(CLEANED_DIR / "profesionales_eliminados.csv", index=False)


if __name__ == "__main__":
    main()
