"""Defines dstamp's logging configuration."""

import platformdirs

import dstamp

LOG_DIR = platformdirs.user_log_path(dstamp.APP_NAME, ensure_exists=True)

CONFIG = {
    "version": 1,
    "formatters": {
        "short": {"format": "%(levelname)s: %(message)s"},
        "full": {"format": "%(asctime)s %(levelname)s: %(name)s: %(message)s"},
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "short",
            "level": "WARNING",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "full",
            "filename": LOG_DIR / f"{dstamp.APP_NAME}.log",
            "encoding": "utf-8",
            "maxBytes": 50_000,
            "backupCount": 1,
        },
    },
    "root": {
        "level": "INFO",
        "handlers": ["console", "file"],
    },
    "disable_existing_loggers": False,
}
