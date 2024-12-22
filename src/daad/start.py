import subprocess

from src.daad.constants import __prod__
from src.daad.helpers import get_file_path


def start_rabbitmq():
    if not __prod__:
        # starts rabbitmq on local machine
        subprocess.run(["bash", get_file_path("start_rabbitmq.sh")], check=True)


def connect_rabbitmq():
    pass
