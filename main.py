import asyncio
from truelove.db import init_db

if __name__ == "__main__":
    asyncio.run(init_db())
    
    import uvicorn
    uvicorn.run("truelove.routes:app", host="0.0.0.0", port=33200, reload=True)
    
    
    