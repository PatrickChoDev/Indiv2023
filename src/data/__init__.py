import logging
import dotenv

dotenv.load_dotenv()

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

log.info('Initializing Data Module')