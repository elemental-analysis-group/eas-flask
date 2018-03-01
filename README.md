## Subindo o sistema

Instalação das bibliotecas:

    virtualenv -p python3 vendor
    . vendor/bin/activate
    vendor/bin/pip3 install -r requirements.txt

Banco de dados:

    python3 run.py db upgrade

Criar pasta files:

    mkdir files
    
Para executar:

    python3 run.py runserver

## Dicas

Para recriar o arquivo se necessário:

    .vendor/bin/pip3 freeze > requirements.txt

Sair do virtualenv:

    deactivate

Criar usuário no postgres:

    INSERT INTO users (id, username,password,email) VALUES ((SELECT nextval ('users_id_seq')),'admin','admin','admin@example.com');

