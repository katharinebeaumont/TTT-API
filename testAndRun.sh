echo "******Running unit and server tests******"

python -m pytest tests/*.py

echo "******Starting server******"

flask run --host=localhost --port=8083