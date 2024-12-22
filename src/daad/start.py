import os
import subprocess
from typing import Dict

from src.daad.constants import RABBITMQ_CONFIG, TEST_RABBITMQ_PROD, __prod__
from src.daad.helpers import get_file_path


def start_rabbitmq():
    env = os.environ.copy()
    env.update(
        {
            "RABBITMQ_DEFAULT_USER": RABBITMQ_CONFIG["user"],
            "RABBITMQ_DEFAULT_PASS": RABBITMQ_CONFIG["password"],
            "RABBITMQ_PORT": RABBITMQ_CONFIG["port"],
            "RABBITMQ_MANAGEMENT_PORT": RABBITMQ_CONFIG["management_port"],
        }
    )
    # starts rabbitmq on local machine with environment variables
    subprocess.run(["bash", get_file_path("start_rabbitmq.sh")], env=env, check=True)


def connect_rabbitmq():
    pass
