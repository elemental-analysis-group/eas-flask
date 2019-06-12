## Subindo o sistema

Instalação das bibliotecas:

    virtualenv -p python3 .eas-flask
    . .eas-flask/bin/activate
    .eas-flask/bin/pip3 install -r requirements.txt

Criar tabelas no banco de dados:

    python3 run.py db upgrade

Criar pasta files:

    mkdir files
    
Para executar:

    python3 run.py runserver

## Dicas

Para recriar o arquivo se necessário:

    .eas-flask/bin/pip3 freeze > requirements.txt

Sair do virtualenv:

    deactivate

Dicas:

Criar usuário no banco de dados:

    INSERT INTO users (id, username,password,email) VALUES ((SELECT nextval ('users_id_seq')),'admin','admin','admin@example.com');

Gerar nova migration:

    python3 run.py db migrate
