AWS_ACCESS_KEY_ID=`vault kv get -field=AWS_ACCESS_KEY onyxia-kv/projet-gaia/s3` && export AWS_ACCESS_KEY
AWS_SECRET_ACCESS_KEY=`vault kv get -field=AWS_SECRET_KEY onyxia-kv/projet-gaia/s3` && export AWS_SECRET_KEY
export MC_HOST_s3=https://$AWS_ACCESS_KEY_ID:$AWS_SECRET_ACCESS_KEY@$AWS_S3_ENDPOINT
pip install -r requirements.txt
python -m spacy download fr_dep_news_trf
python -m unittest
pip install -U pip setuptools wheel
pip install -U 'spacy[cuda118,transformers,lookups]'
mc cp s3/projet-gaia/test/majic_2021.parquet.gz data/
cd src/