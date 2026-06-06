from fastapi import FastAPI
from cronjobs.CronJobs import CronJobs

app = FastAPI(lifespan=CronJobs().lifespan)


@app.get("/")
def home():
    return {"Hello": "World"}
