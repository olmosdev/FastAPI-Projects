import logging
from uvicorn.logging import ColourizedFormatter
from logging.handlers import TimedRotatingFileHandler

client_logger = logging.getLogger("client.logger")
client_logger.setLevel(logging.INFO)

# Handler to print log messages to the console (This will stream the message to the console)
console_handler = logging.StreamHandler()

# Ceating a colorized formatter
# The formatter will format log messages in the same of the default logger uvicorn logger used by FastAPI
console_formatter = ColourizedFormatter(
    "%(levelprefix)s CLIENT CALL - %(message)s",
    use_colors=True,
)
console_handler.setFormatter(console_formatter)
# Adding the handler to the logger
client_logger.addHandler(console_handler)

# Creating a handler that stores messages into a file
file_handler = TimedRotatingFileHandler("app.log")
file_formatter = logging.Formatter(
    "time %(asctime)s, %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
file_handler.setFormatter(file_formatter)
client_logger.addHandler(file_handler)


