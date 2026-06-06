from mongoengine import Document, StringField, DateTimeField

class EmailModel(Document):
    email_uid = StringField()
    email_from = StringField()
    email_date = DateTimeField()
    email_subject = StringField()
    email_body = StringField()

    meta = {'abstract': True}


class DirectApplicationModel(EmailModel):
    meta = {'collection': 'direct_applications'}


class RejectionModel(EmailModel):
    meta = {'collection': 'rejections'}


class ReferralModel(EmailModel):
    meta = {'collection': 'referrals'}


class OnlineAssessmentModel(EmailModel):
    meta = {'collection': 'online_assessments'}


class InterviewModel(EmailModel):
    meta = {'collection': 'interviews'}


class ColdMailModel(EmailModel):
    meta = {'collection': 'cold_mails'}
