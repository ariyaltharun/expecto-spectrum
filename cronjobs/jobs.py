from apps.JobApplications.services.SyncApplicationService import SyncApplications
from mongoengine import connect, disconnect
from dotenv import load_dotenv
import os

load_dotenv()


def syncApplicationsWithDB():
    connect(db=os.getenv("DB_NAME"), host=os.getenv("MONGODB_URL"), alias="default")
    try:
        s = SyncApplications()
        s.sync()
    finally:
        disconnect(alias="default")
