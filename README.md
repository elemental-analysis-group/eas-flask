## Subindo o sistema

Instalação das bibliotecas:

    virtualenv -p python3 .virtualenv
    source .virtualenv/bin/activate
    pip3 install -r requirements.txt

Criar tabelas no banco de dados:

    cp config.py.example config.py # editar
    python3 run.py db upgrade

Para executar:

    python3 run.py runserver

## Dicas

Para recriar o arquivo se necessário:

     pip3 freeze > requirements.txt

Sair do virtualenv:

    deactivate

Dicas:

Criar usuário no banco de dados:

    sqlite3 /tmp/test.db
    INSERT INTO users (id, username,password,email) VALUES (1,'admin','admin','admin@example.com');
    .quit

Gerar nova migration:

    python3 run.py db migrate

Atualizar tudo do requiriments:

    pip install --ignore-installed -r requirements.txt
    pip3 freeze > requirements.txt


    gunicorn -w 2 app:app
