from fastapi import FastAPI, HTTPException
# from api.routes import router as api_router

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "API is running"}

# app.include_router(api_router)
