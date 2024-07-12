from dataclasses import dataclass

from environs import Env


@dataclass
class Config:
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    }


def load_config(path: str | None):
    if path is not None:
        env = Env()
        env.read_env(path)

    return Config()
