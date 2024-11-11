# server

## Installation

```bash
pip install -r requirements.txt
```

## Run

```bash
# cp supervisor config file
bash cp_supervisor_file.sh
```

```bash
vim supervisor.conf
# add or delete server[program]
```

```bash
# supervisor start
bash start.sh
```

Browse http://127.0.0.1:9001 to manage services. (username: admin, password: admin, config in `supervisor.conf`)

Click 'Tail -f Stderr' to view logs or cat `server/logs/supervisord/*.log`

```bash
# supervisor stop
bash stop.sh
```

```bash
# supervisor restart
bash restart
```

