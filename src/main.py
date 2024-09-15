from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session
from database import get_db, log_user_request, rate_limit_check
from models import Document
from cache import set_cache, get_cache
from scraper import start_scraper
import hashlib

@app.on_event("startup")
def on_startup():
    # Create all tables (Document and UserRequest)
    Base.metadata.create_all(bind=engine)

app = FastAPI()
start_scraper()

@app.get("/health")
def health_check():
    return {"status": "API is running"}

@app.post("/documents/")
async def upload_document(user_id: str, title: str, content: str, db: Session = Depends(get_db)):
    # Check for rate limiting
    if rate_limit_check(user_id):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    # Log user request
    log_user_request(user_id)

    # Create a new document entry
    document = Document(title=title, content=content)
    db.add(document)
    db.commit()
    db.refresh(document)
    return {"id": document.id, "title": document.title, "content": document.content}

@app.get("/search/")
async def search_documents(
    user_id: str,  
    text: str = Query(..., description="The search query text"),
    top_k: int = Query(5, description="Number of top results to return"),
    threshold: float = Query(0.5, description="Similarity threshold for the search"),
    db: Session = Depends(get_db)
):
    cache_key = hashlib.md5(f"{user_id}-{text}-{top_k}-{threshold}".encode()).hexdigest()
    cached_result = await get_cache(cache_key)
    
    if cached_result:
        return {"results": cached_result}

    documents = db.query(Document).filter(
        Document.content.ilike(f"%{text}%")  
    ).limit(top_k).all()

    results = [
        {"id": doc.id, "title": doc.title, "content": doc.content}
        for doc in documents
        if len(doc.content) > threshold  
    ]
    await set_cache(cache_key, results)
    
    return {"results": results}


