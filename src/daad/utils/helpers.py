import os


def get_file_path(file_name):
    """Retrieves the file path, starting at the project root."""
    project_root = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )
    file_path = os.path.join(project_root, file_name)
    absolute_path = os.path.abspath(file_path)
    return absolute_path


# logger functionality
# fix later with a logger class
# import logging
# from requests import Response
# def configure_logger() -> logging.Logger:
#     """Configures and returns a global logger."""
#     logger = logging.getLogger("kalshi_logger")
#     logger.setLevel(logging.DEBUG)
#     handler = logging.StreamHandler()
#     formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(message)s")
#     handler.setFormatter(formatter)
#     logger.addHandler(handler)
#     return logger


def log_cache_status(response):
    if getattr(response, "from_cache", False):
        print(f"Cache HIT: {response.url}")
    else:
        print(f"Cache MISS: {response.url}")
