"""
Logger utility for creating and configuring loggers.
"""

from datetime import datetime
import logging
import os

from pytz import timezone


LOGGING_LEVEL = logging.INFO
currentDateTime = datetime.now(tz=timezone("Asia/Kolkata"))

# Create log directory if not exists
os.makedirs("logs/", exist_ok=True)


def getLogger(name):
    logger = logging.getLogger(name)
    logger.setLevel(LOGGING_LEVEL)
    prefixLogDirectory = f"logs/logs_{currentDateTime}"
    # Create logs directory with current time and date
    if not os.path.exists(prefixLogDirectory):
        os.makedirs(prefixLogDirectory)
    # Logging format
    logFmt = logging.Formatter(fmt="%(asctime)s [ %(levelname)s ] : %(message)s")
    # Add File Handler | For logging in file
    fileHandler = logging.FileHandler(filename=f"{prefixLogDirectory}/{name}.log")
    fileHandler.setFormatter(fmt=logFmt)
    logger.addHandler(fileHandler)
    # Add Stream Handler | For logging in terminal
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(fmt=logFmt)
    logger.addHandler(streamHandler)
    return logger
