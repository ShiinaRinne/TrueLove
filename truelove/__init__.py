from truelove.routes import app
from truelove.process.plugin import *
from truelove.process.manager import TrueLoveManager
from datetime import datetime


async def main():
    TrueLoveManager.update_core()
    
    TrueLoveManager.scheduler.add_job(TrueLoveManager.download_media,   'interval', minutes=1,  next_run_time=datetime.now(), id="download_media")
    TrueLoveManager.scheduler.add_job(TrueLoveManager.refresh,          'interval', minutes=10, next_run_time=datetime.now(), id="refresh")
    TrueLoveManager.scheduler.start()
                    
@app.on_event("startup")
async def schedule():
    await main()