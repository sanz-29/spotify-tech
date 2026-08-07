from fastapi import FastAPI

app = FastAPI(
    title="Spotify Tech API",
    description="Music Streaming Platform Backend",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Spotify Tech API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }