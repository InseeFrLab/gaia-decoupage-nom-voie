rm -r dist/
rm -r src/decoupage_libelles.egg-info/
python3 -m build
python3 -m twine upload --repository pypi dist/*
# python3 -m pip install --upgrade decoupage_libelles