from fastapi import FastAPI

app = FastAPI(title="Cyberion ThreatShield")

@app.get("/")
def home():
    return {
        "status": "online",
        "message": "Cyberion ThreatShield is running"
    }

@app.get("/health")
def health():
    return {"status": "healthy"}
