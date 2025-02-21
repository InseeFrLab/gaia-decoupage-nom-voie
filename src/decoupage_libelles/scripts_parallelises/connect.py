import s3fs
import os


def cred_s3(plateform="ls3"):
    if plateform == "ls3":
        plateform_path = 'minio.datascience.kube.insee.fr'
    elif plateform == "datalab":
        plateform_path = 'minio.lab.sspcloud.fr'

    fs = s3fs.S3FileSystem(
        client_kwargs={'endpoint_url': 'https://' + plateform_path},
        key=os.environ["AWS_ACCESS_KEY_ID"],
        secret=os.environ["AWS_SECRET_ACCESS_KEY"],
        token=os.environ["AWS_SESSION_TOKEN"]
    )

    return fs
