import pandas as pd

from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
CLEANED_DIR = DATA_DIR / "cleaned"
PROCESSED_DIR = DATA_DIR / "processed"


def get_dir(stage: str) -> Path:

    path = DATA_DIR / stage
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_file_path(stage: str, filename: str) -> Path:

    return get_dir(stage) / filename


def add_columns(df: pd.DataFrame, columns: list, default_value="") -> pd.DataFrame:
    for col in columns:
        if col not in df.columns:
            df[col] = default_value
    return df


def standarize_column_names(
    df: pd.DataFrame, field_to_rename: str, new_field_name: str
):

    # estandarizar el nombre de la columna elegida
    col = [c for c in df.columns if c.lower().startswith(field_to_rename.lower())]
    if col:
        df = df.rename(columns={col[0]: new_field_name})

    return df


def split_by_status(df: pd.DataFrame) -> pd.DataFrame:
    # separar eliminados
    if "eliminado" in df.columns:
        eliminado = df["eliminado"].astype(str).str.lower() == "true"
        df_eliminados = df[eliminado].copy()
        df_activos = df[~eliminado].copy()
    else:
        df_eliminados = df.iloc[0:0].copy()
        df_activos = df.copy()

    return df_activos, df_eliminados


def filter_by_field_value(df: pd.DataFrame, field: str, value) -> pd.DataFrame:
    return df[df[field] == value].copy()


def group_by_field(df: pd.DataFrame, field: str) -> pd.DataFrame:
    # 1. Creamos una columna temporal para priorizar Origen 4 (GoRed)
    # Le asignamos 0 a GoRed y 1 a los demás para que al ordenar de menor a mayor, GoRed quede arriba
    df["prioridad_origen"] = df["origen"].apply(lambda x: 0 if x == 4 else 1)

    # 2. Convertimos la columna de cambio a fecha para asegurar que el orden sea cronológico
    if "cambio" in df.columns:
        df["cambio"] = pd.to_datetime(df["cambio"], errors="coerce")

    # 3. Ordenamos:
    # Primero por el campo de agrupación (master)
    # Segundo por prioridad (GoRed primero)
    # Tercero por fecha de cambio (la más reciente arriba)
    df_sorted = df.sort_values(
        by=[field, "prioridad_origen", "cambio"], ascending=[True, True, False]
    )

    # 4. Agrupamos y tomamos el primero (.first()) de cada grupo.
    # Esto nos devuelve un DataFrame con una sola fila por cada 'master'
    df_master = df_sorted.groupby(field).first().reset_index()

    # 5. Eliminamos la columna de prioridad temporal antes de devolver
    df_master = df_master.drop(columns=["prioridad_origen"])

    return df_master
