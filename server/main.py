

from app.scraper.indeed_scraper import indeed_scraper  # Adjust the function name as needed
# main.py
from fastapi import FastAPI


app = FastAPI()

@app.get("/indeed_scraper")
def trigger():
    result = indeed_scraper()  # Call the actual function from the module
    return {"status": "success", "data": result}



