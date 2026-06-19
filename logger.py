import logging
from logging.handlers import RotatingFileHandler


def setup_logging(level=logging.INFO):
    root = logging.getLogger()
    if root.handlers:
        return  # evitar handlers duplicados si se llama más de una vez
    root.setLevel(level)

    # Consola — formato limpio, sin timestamp
    console = logging.StreamHandler()
    console.setLevel(level)
    console.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
    root.addHandler(console)

    # Archivo — formato completo con timestamp y módulo
    fh = RotatingFileHandler(
        "cidi.log",
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
        encoding="utf-8",
    )
    fh.setLevel(level)
    fh.setFormatter(logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    ))
    root.addHandler(fh)
