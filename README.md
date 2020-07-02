## Subindo o sistema

Instalação das bibliotecas:

    virtualenv -p python3 .virtualenv
    source .virtualenv/bin/activate
    pip3 install pip-tools
    pip-compile -r requirements.in
    pip3 install -r requirements.txt

Criar tabelas no banco de dados:

    cp config.py.example config.py # editar
    python3 run.py db upgrade

Para executar em modo dev:

    python3 run.py runserver

Sair do virtualenv:

    deactivate

Criar usuário no banco de dados sqlite:

    sqlite3 /CAMINHO-SEU-DB/test.db
    INSERT INTO users (id, username,password,email) VALUES (1,'admin','admin','admin@example.com');
    .quit

Exemplo de para serviço em ~/.config/systemd/user/edx.service:

    [Unit]
    Description=iag usp

    [Service]
    Environment=TZ=America/Sao_Paulo
    ExecStart=/home/edx/elemental_analysis_tools_flask/.virtualenv/bin/gunicorn --bind 0.0.0.0:8000  -w 2 app:app
    ExecStop=/bin/kill -INT $MAINPID
    ExecReload=/bin/kill -TERM $MAINPID
    Restart=on-failure
    
    [Install]
    WantedBy=default.target


47342

    apt install python3-pip python3-venv python3-virtualenv git mariadb-server
    pip3 install --upgrade virtualenv
    hash -r

    

