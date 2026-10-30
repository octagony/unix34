import asyncio
import logging
import sys

from worker.scheduler import start_scheduler
from config import settings

logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


async def main():
    scheduler = start_scheduler()
    
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        scheduler.shutdown(wait=False)
    except Exception as e:
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())