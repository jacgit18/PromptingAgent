from fastapi import FastAPI

app = FastAPI(title="Financial Dashboard API")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
