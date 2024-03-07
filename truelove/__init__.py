from truelove.routes import app
from truelove.process.manager import TrueLoveManager

async def main():
    TrueLoveManager.update_core()
    
    TrueLoveManager.add_job(
        "interval",
        args=[TrueLoveManager.download_media],
        minutes=1,
        id="download_media",
    )
    
    TrueLoveManager.add_job(
        "interval",
        args=[TrueLoveManager.refresh],
        minutes=10,
        id="refresh",
    )


    TrueLoveManager.scheduler.start()
                    
@app.on_event("startup")
async def schedule():
    await main()