from fastapi import FastAPI
from utils.logger import setup_logger
from utils.proxy_manager import ProxyManager

app = FastAPI()

logger = setup_logger()
logger.info("Server started")
@app.get("/")
async def read_root():
    return {"message": "Hello, world!"}
@app.get("/scrape")
async def scrape():
    from scrapers.selenium_scraper import run_scraper
    return {"data": run_scraper()}
@app.get("/rotate_proxy")
async def rotate_proxy():
    proxy_manager = ProxyManager()
    new_proxy = proxy_manager.rotate_proxy()
    return {"proxy": new_proxy.to_dict() if new_proxy else "No working proxy available"}

@app.get("/rotate_proxy")
async def rotate_proxy():
    new_proxy = proxy_manager.rotate_proxy()
    return {"proxy": new_proxy.to_dict() if new_proxy else "No working proxy available"}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)