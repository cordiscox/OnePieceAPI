import logging
import os

def setup_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Configura el manejador de consola
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)  
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Configura el manejador de archivo
    log_file = os.path.join(os.path.dirname(__file__), 'OnePieceAPI.log')
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG) 
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger

logger = setup_logger()
