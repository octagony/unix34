import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from config import settings
from worker.runner import run_sync

logger = logging.getLogger(__name__)


def start_scheduler():
    scheduler = AsyncIOScheduler()
    
    scheduler.add_job(
        run_sync,
        trigger=IntervalTrigger(minutes=settings.sync_interval_minutes),
        id="reddit_sync",
        name="Reddit Sync Job",
        replace_existing=True,
        max_instances=1,
        misfire_grace_time=60
    )
    
    scheduler.add_job(
        run_sync,
        id="reddit_sync_initial",
        name="Initial Reddit Sync",
        replace_existing=True
    )
    
    scheduler.start()
    return scheduler