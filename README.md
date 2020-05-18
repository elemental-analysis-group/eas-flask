## Subindo o sistema

Instalação das bibliotecas:

    virtualenv -p python3 .virtualenv
    source .virtualenv/bin/activate
    pip3 install -r requirements.txt

Criar tabelas no banco de dados:

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

    INSERT INTO users (id, username,password,email) VALUES (1,'admin','admin','admin@example.com');

Gerar nova migration:

    python3 run.py db migrate
