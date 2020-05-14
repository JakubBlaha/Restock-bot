# Installation commands
First, make sure to install python and that you can run it with the following command.

```bash
python3 --version
```
If it displays the version correctly follow the next steps. Otherwise, please install python correctly.

```bash
python3 -m pip install pipenv

git clone https://github.com/JakubBlaha/Restock-bot.git

cd Restock-bot

python3 -m pipenv install
python3 -m pipenv shell

python -m bot
```

Now it's gonna display an error message about the config. Fix the config (`nano config.ini`)and run again.

```bash
python -m bot
```