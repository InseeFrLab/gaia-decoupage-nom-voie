"""
Lecture et écriture des fichiers de données — S3 et local.
"""
import pandas as pd
import pyarrow.parquet as pq
import pyarrow.dataset as ds
import s3fs
import os


def connect_s3(platform: str) -> s3fs.S3FileSystem:
    """Retourne un filesystem S3 authentifié selon la plateforme."""
    endpoints = {
        "ls3":     "minio.datascience.kube.insee.fr",
        "datalab": "minio.lab.sspcloud.fr",
    }
    if platform not in endpoints:
        raise ValueError(f"Plateforme inconnue : '{platform}'. Valeurs attendues : ls3, datalab.")

    os.environ["AWS_ACCESS_KEY_ID"] = '0EQB5M6XCAUJ22GPSY73'
    os.environ["AWS_SECRET_ACCESS_KEY"] = 'vcCaDPB3o+UhNVElGWQNTetSv6YJl9tSy6z71hSn'
    os.environ["AWS_SESSION_TOKEN"] = 'eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NLZXkiOiIwRVFCNU02WENBVUoyMkdQU1k3MyIsImFjciI6IjAiLCJhdWQiOiJtaW5pby1rdWJlLWxzMyxtaW5pby1rdWJlLWRhdGFzY2llbmNlIiwiYXV0aF90aW1lIjoxNzc5MzQ5Nzc5LCJhenAiOiJvbnl4aWEtbWluaW8ta3ViZS1sczMiLCJjbmYiOnsiamt0IjoiWVlvUC1oeUhqbDZwR2FpWm5yeWhFY3Rjb0M5M2k2aTNmaGNBTGkzd0xWSSJ9LCJlbWFpbCI6InJheWEuYmVyb3ZhQGluc2VlLmZyIiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJleHAiOjE3Nzk3ODI1NzgsImZhbWlseV9uYW1lIjoiQmVyb3ZhIiwiZ2l2ZW5fbmFtZSI6IlJheWEiLCJncm91cHMiOlsiY29uZnBzLWRzZHMtbGl2cmFibGVzLXJlc2lsLXJ3IiwiY29uZnBucy1kbWdjLWdlb2dyYXBoaWUtcnciXSwiaWF0IjoxNzc5MzUwNTc4LCJpc3MiOiJodHRwczovL2F1dGguaW5zZWUuZnIvYXV0aC9yZWFsbXMvaW5zZWUtZGF0YXNjaWVuY2UiLCJqdGkiOiJvbnJ0cnQ6OTdjYmRlNzgtOTJiMi05MGE2LTNhMzUtOWJjMTA4ZDI0ZTIxIiwibmFtZSI6IlJheWEgQmVyb3ZhIiwicG9saWN5IjoiY29uZnBucy1kbWdjLWdlb2dyYXBoaWUsY29uZnBzLWRzZHMtbGl2cmFibGVzLXJlc2lsLHByb2pldC1kYi1nZW9sb2MtZmlkZWxpLHByb2pldC1tbC1tb3RldXItaWRlbnRpZmljYXRpb24tZ2FpYSxwcm9qZXQtbW90ZXVyLXJlc2lsLHByb2pldC1wb2MtbWFkLXR1aWxlcy1jYXJ0byxwdWJsaWMsdHJhdmFpbCIsInByZWZlcnJlZF91c2VybmFtZSI6ImZpN2w3dCIsInNjb3BlIjoib3BlbmlkIGVtYWlsIHByb2ZpbGUiLCJzaWQiOiJtaEZNaXk2dW83akFXbnYzQ2p2MEx0NFoiLCJzdWIiOiJmOjE4YzFlOGQ5LTJjYTQtNDRkZi04YmU4LTY1OWZmZjQ2NDhkYjpGSTdMN1QiLCJ0eXAiOiJEUG9QIn0.d_N6ZfBXGdy5FMnHJTb2tirdSYYnPPawDOO9rLVim158Ohwl1w92u7-qS_-GrJ3-aR_jrABfH9zFHpY9S0w-9A'
    os.environ["AWS_DEFAULT_REGION"] = 'us-east-1'

    return s3fs.S3FileSystem(
        client_kwargs={"endpoint_url": "https://" + endpoints[platform]},
        key=os.environ["AWS_ACCESS_KEY_ID"],
        secret=os.environ["AWS_SECRET_ACCESS_KEY"],
        token=os.environ["AWS_SESSION_TOKEN"],
    )


def detect_file_type(path: str) -> str:
    """Détermine le type de fichier depuis le chemin."""
    if "." not in path.split("/")[-1]:
        return "dossier_parquet"
    ext = path.rsplit(".", 1)[-1].lower()
    if ext in ("csv", "parquet"):
        return ext
    raise ValueError(f"Extension non supportée : '{ext}'")


def iter_chunks(path: str, file_type: str, chunk_size: int, fs=None):
    """
    Génère des DataFrames par chunks depuis un fichier CSV, parquet ou dossier parquet.
    fs : filesystem s3fs ou None pour local.
    """
    opener = fs.open if fs else open

    if file_type == "csv":
        with opener(path, "rb") as f:
            yield from pd.read_csv(f, chunksize=chunk_size, dtype=str)

    elif file_type == "parquet":
        with opener(path, "rb") as f:
            for batch in pq.ParquetFile(f).iter_batches(batch_size=chunk_size):
                yield batch.to_pandas()

    elif file_type == "dossier_parquet":
        dataset = ds.dataset(path, format="parquet", filesystem=fs)
        for batch in dataset.to_batches(batch_size=chunk_size):
            yield batch.to_pandas()


def save(df: pd.DataFrame, path: str, output_format: str, sep: str, encoding: str, fs=None) -> None:
    """Sauvegarde un DataFrame en CSV ou parquet, localement ou sur S3."""
    opener = fs.open if fs else open
    with opener(path, "wb") as f:
        if output_format == "csv":
            df.to_csv(f, index=False, sep=sep, encoding=encoding)
        elif output_format == "parquet":
            df.to_parquet(f, engine="pyarrow", index=False)
        else:
            raise ValueError(f"Format non reconnu : '{output_format}'")
    print(f"Résultat enregistré : {path}")


def output_path(input_path: str, output_format: str) -> str:
    """Dérive le chemin de sortie depuis le chemin d'entrée."""
    base = input_path.rsplit(".", 1)[0] if "." in input_path.split("/")[-1] else input_path
    return f"{base}_parsed.{output_format}"
