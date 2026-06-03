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
    os.environ["AWS_ACCESS_KEY_ID"] = 'HVMHXRH8SXNHDYMMN9J3'
    os.environ["AWS_SECRET_ACCESS_KEY"] = 'mii9Q+bju8hOn3qBY1qMuCHFgyJ+3CtBlVFaQarn'
    os.environ["AWS_SESSION_TOKEN"] = 'eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NLZXkiOiJIVk1IWFJIOFNYTkhEWU1NTjlKMyIsImFjciI6IjAiLCJhdWQiOiJtaW5pby1rdWJlLWxzMyxtaW5pby1rdWJlLWRhdGFzY2llbmNlIiwiYXV0aF90aW1lIjoxNzgwNDc5Nzk0LCJhenAiOiJvbnl4aWEtbWluaW8ta3ViZS1sczMiLCJjbmYiOnsiamt0IjoiYWlKem51Y3JIZzRBNVlOb3VWbWRKM1FoSW1JRXZ2ZGlZRUpDN05Bd0c1byJ9LCJlbWFpbCI6InJheWEuYmVyb3ZhQGluc2VlLmZyIiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJleHAiOjE3ODA5MTE3OTYsImZhbWlseV9uYW1lIjoiQmVyb3ZhIiwiZ2l2ZW5fbmFtZSI6IlJheWEiLCJncm91cHMiOlsiY29uZnBzLWRzZHMtbGl2cmFibGVzLXJlc2lsLXJ3IiwiY29uZnBucy1kbWdjLWdlb2dyYXBoaWUtcnciXSwiaWF0IjoxNzgwNDc5Nzk2LCJpc3MiOiJodHRwczovL2F1dGguaW5zZWUuZnIvYXV0aC9yZWFsbXMvaW5zZWUtZGF0YXNjaWVuY2UiLCJqdGkiOiJvbnJ0cnQ6YTQ0ZDVmZGQtYTgxYS05MmM3LTA0NWMtMmRmMGJiZDRkMWM4IiwibmFtZSI6IlJheWEgQmVyb3ZhIiwicG9saWN5IjoiY29uZnBucy1kbWdjLWdlb2dyYXBoaWUsY29uZnBzLWRzZHMtbGl2cmFibGVzLXJlc2lsLHByb2pldC1kYi1nZW9sb2MtZmlkZWxpLHByb2pldC1tbC1tb3RldXItaWRlbnRpZmljYXRpb24tZ2FpYSxwcm9qZXQtbW90ZXVyLXJlc2lsLHByb2pldC1wb2MtbWFkLXR1aWxlcy1jYXJ0byxwdWJsaWMsdHJhdmFpbCIsInByZWZlcnJlZF91c2VybmFtZSI6ImZpN2w3dCIsInNjb3BlIjoib3BlbmlkIGVtYWlsIHByb2ZpbGUiLCJzaWQiOiJrNEhIeHhPdzhuNWVDYS02SkxDRXNHQnMiLCJzdWIiOiJmOjE4YzFlOGQ5LTJjYTQtNDRkZi04YmU4LTY1OWZmZjQ2NDhkYjpGSTdMN1QiLCJ0eXAiOiJEUG9QIn0.29KhqrcAps5zt5LRZ5bHo0V9FumUxUTHrCVDbr0SjIzH3sEenw_ImcMJXlnHn04VVbKIj-5lWCkFI-nOnXy7gQ'
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
