from utils.logger import getLogger
from imap_tools import MailBox
from dotenv import load_dotenv
from pytz import timezone
import os
from apps.JobApplications.models.SyncApplicationModels import (
    DirectApplicationModel,
    RejectionModel,
    ReferralModel,
    OnlineAssessmentModel,
    InterviewModel,
    ColdMailModel
)
from utils.logger import getLogger
from datetime import datetime, timedelta

load_dotenv()
logger = getLogger(__name__)


class SyncApplications:
    def __init__(self):
        self.mailFolders = [
            "JobApplications/Rejections",
            "JobApplications/DirectApplications",
            "JobApplications/Referrals",
            "JobApplications/OnlineAssessments",
            "JobApplications/Interviews",
            "JobApplications/ColdMails"
        ]
        self.models = [
            RejectionModel,
            DirectApplicationModel,
            ReferralModel,
            OnlineAssessmentModel,
            InterviewModel,
            ColdMailModel
        ]
        self.IMAP_SERVER = os.getenv("IMAP_SERVER")
        self.EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
        self.GOOGLE_APP_PASSWORD = os.getenv("GOOGLE_APP_PASSWORD")

    def sync(self):
        logger.info("Starting sync process...")
        self._getApplicationsFromMailBox()
        # Save to Database
        # print(applications)

    def _getApplicationsFromMailBox(self):
        mails = []
        for mailFolder, CollectionModel in zip(self.mailFolders, self.models):
            folderMails = self._fetchFolderMails(mailFolder, CollectionModel)
            mails.extend(folderMails)
        return mails

    def _fetchFolderMails(self, folderName, CollectionModel):
        folderMails = []
        with MailBox(self.IMAP_SERVER).login(self.EMAIL_ADDRESS, self.GOOGLE_APP_PASSWORD) as mailBox:
            mailBox.folder.set(folderName)
            date = (datetime.now() - timedelta(days=1)).strftime("%d-%b-%Y")
            logger.info(f"Fetching mails from folder: {folderName} on date: {date}")
            mails = mailBox.fetch(f"ON {date}")
            unique_mail_uids = set()
            for mail in mails:
                # If it start iterating mails again, stop it
                if mail.uid in unique_mail_uids:
                    break
                unique_mail_uids.add(mail.uid)
                # Store Data in some structure
                collectionModel = CollectionModel(
                    email_uid=mail.uid,
                    email_from=mail.from_,
                    email_date=mail.date.astimezone(tz=timezone("Asia/Kolkata")).strftime("%Y-%m-%d %H:%M:%S"),
                    email_subject=mail.subject,
                    email_body=(mail.text or mail.html)
                )
                collectionModel.save()
                folderMails.append(collectionModel.to_mongo().to_dict())
        return folderMails

