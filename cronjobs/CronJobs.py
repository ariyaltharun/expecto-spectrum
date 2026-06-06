from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI
from contextlib import asynccontextmanager
from pytz import timezone
from .jobs import syncApplicationsWithDB
import json
from utils.logger import getLogger

logger = getLogger(__name__)


class CronJobs:
    def __init__(self):
        self.scheduler = BackgroundScheduler(
            timezone=timezone("Asia/Kolkata")
        )
        self.register()

    def start(self):
        logger.info("Starting cron jobs...")
        self.scheduler.start()

    def shutdown(self):
        logger.info("Shutting down cron jobs...")
        self.scheduler.shutdown()

    def register(self):
        logger.info("Registering cron jobs...")
        jobs = self._getJobs()
        for job in jobs:
            job['func'] = globals()[job['func']]
            self.scheduler.add_job(**job)
            logger.info(f"Registered job: {job['name']}")

    def _getJobs(self):
        logger.info("Fetching cron jobs from jobs.json...")
        with open("cronjobs/jobs.json", "r") as f:
            jobs = json.load(f)
        return jobs

    @asynccontextmanager
    async def lifespan(self, app: FastAPI):
        self.start()
        yield
        self.shutdown()

    def __del__(self):
        logger.info("CronJobs instance is being destroyed.")
