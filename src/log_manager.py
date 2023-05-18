from loguru import logger
import os   
# logger.remove()  # Remove any default handlers that might already be configured
log_folder = "logs"
logger.add(os.path.join(log_folder, "logs.log"), level="DEBUG", rotation="1 week")
# Add a sink to output logs to the console
logger.add(lambda message: print(message), level="DEBUG")