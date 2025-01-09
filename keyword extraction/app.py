from fastapi import FastAPI, HTTPException, Form, Request
from fastapi.templating import Jinja2Templates  
from fastapi.responses import JSONResponse
from rake_nltk import Rake

app = FastAPI()

# Serving HTML Templates
templates = Jinja2Templates(directory="templates")

# Function to extract keywords using RAKE
def extract_keywords_rake(text):
    rake = Rake()
    rake.extract_keywords_from_text(text)
    return rake.get_ranked_phrases()[:5]

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/extract_keywords")
async def extract_keywords(request: Request, text: str = Form(...)):
    try:
        # Extract keywords using RAKE
        keywords = extract_keywords_rake(text)
        return JSONResponse(content={"keywords": keywords})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
