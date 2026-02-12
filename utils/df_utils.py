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


profesionales_clean_path = get_file_path("cleaned", "profesionales.csv")
especialidades_clean_path = get_file_path("cleaned", "especialidades.csv")
obras_sociales_clean_path = get_file_path("cleaned", "obras_sociales.csv")


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
        eliminado = df["eliminado"].astype(str).str.lower() == "1"
        df_eliminados = df[eliminado].copy()
        df_activos = df[~eliminado].copy()
    else:
        df_eliminados = df.iloc[0:0].copy()
        df_activos = df.copy()

    return df_activos, df_eliminados


def filter_by_field_value(
    df: pd.DataFrame, field: str, value: int | str
) -> pd.DataFrame:
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


def normalizator(
    df: pd.DataFrame,
    path,
    schema: dict,
    output_name: str,
    rename_map: dict = None,
):
    df_cleaned = df.copy()

    if rename_map:
        # Filtramos para no intentar renombrar columnas que no existen
        actual_map = {
            old: new for old, new in rename_map.items() if old in df_cleaned.columns
        }

        # Aplicamos el renombrado
        df_cleaned = df_cleaned.rename(columns=actual_map)

        print(f"Renamed columns: {actual_map}")

    # 2. Columnas de auditoría
    for col in ["cambio", "createdAt"]:
        if col not in df_cleaned.columns:
            df_cleaned[col] = None

    # 3. Aplicar Schema (Crear columnas faltantes como NaN, NO como 0 todavía)
    target_order = schema.get("order", [])
    for col in target_order:
        if col not in df_cleaned.columns:
            df_cleaned[col] = None

    # 4. Tipificación Inteligente
    type_map = schema.get("types", {})
    for col, t_type in type_map.items():
        if col in df_cleaned.columns:
            if t_type == "bool":
                # Mapeamos cualquier variante a 1 y 0
                df_cleaned[col] = (
                    df_cleaned[col]
                    .map(
                        {
                            "True": 1,
                            "False": 0,
                            True: 1,
                            False: 0,
                            "1": 1,
                            "0": 0,
                            1: 1,
                            0: 0,
                        }
                    )
                    .fillna(0)
                    .astype(int)
                )

            elif t_type == "int":
                # Convertimos a numérico permitiendo NaNs (que luego serán NULL en el CSV)
                df_cleaned[col] = pd.to_numeric(df_cleaned[col], errors="coerce")
                df_cleaned[col] = df_cleaned[col].astype("Int64")

            # AGREGAR ESTO:
            elif t_type == "datetime":
                # Convertimos a datetime de pandas y luego a string en formato MySQL
                df_cleaned[col] = pd.to_datetime(df_cleaned[col], errors="coerce")
                # Lo pasamos a formato YYYY-MM-DD HH:MM:SS o None si es inválido
                df_cleaned[col] = df_cleaned[col].dt.strftime("%Y-%m-%d %H:%M:%S")

    # 5. Reordenar
    df_final = df_cleaned[target_order]

    # 5. Reordenar
    df_final = df_cleaned[target_order]

    # 6. Separar y Exportar
    df_activos, df_eliminados = split_by_status(df_final)

    # El secreto para MySQL está en 'na_rep'
    # Usamos '0' para que los campos INT vacíos no queden como ''
    df_activos.to_csv(path / f"{output_name}.csv", index=False, na_rep="NULL")

    df_eliminados.to_csv(
        path / f"{output_name}_eliminados.csv", index=False, na_rep="NULL"
    )

    return df_activos, df_eliminados


def processor(
    df: pd.DataFrame,
    schema: dict,
    output_name: str,
    filter_field: str,
    condition: int | str,
):

    # 1. FILTRAR: Solo lo que está marcado como unificado (1 / True)
    df_homologados = filter_by_field_value(df, filter_field, condition)

    if df_homologados.empty:
        print(f"No matches for {filter_field} == {condition} for {output_name}.")
        return

    # 2. AGRUPAR: Colapsar registros por 'master'
    # Esto asegura que si un profesional tenía 3 registros en cleaned,
    # ahora tengamos 1 solo con la info combinada.
    df_agrupado = group_by_field(df_homologados, "id_master")

    # 3. POPULAR MASTER SCHEMA:
    # Tomamos la lista de campos que definimos en el Schema Master
    cols_master = schema.get("columns")

    # Reindexamos: esto hace dos cosas:
    # - Descarta las columnas que no están en el Schema (como unificado_prof, idOrigen, etc.)
    # - Mantiene los valores de las columnas que SI están en el Schema (nombre, apellido, cuit...)
    df_master_final = df_agrupado.reindex(columns=cols_master)

    if "id_master" in df_master_final.columns:
        df_master_final["id_master"] = pd.to_numeric(
            df_master_final["id_master"], errors="coerce"
        ).astype("Int64")

    # 4. EXPORTAR: Guardamos el Master Final
    output_path = PROCESSED_DIR / f"{output_name}_master.csv"
    df_master_final.to_csv(output_path, index=False)

    print(f"Master {output_name} CSV created successfully in /processed.")
    print(
        f"   -> Populated fields: {len(cols_master)} | Records: {len(df_master_final)}"
    )
