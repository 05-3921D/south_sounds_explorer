import logging
import sys

def setup_logging():
    """Configures structured logging for the application."""
    
    # Format for logs
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Configure root logger
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Set levels for specific libraries to avoid noise
    logging.getLogger("httpx").setLevel(logging.WARNING)

    # Validate that logger works
    logger = logging.getLogger("south_sounds_explorer")
    logger.info("Logging configured successfully")
