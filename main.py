
from pathlib import Path
import os

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(
    title="Cyberion Shield",
    description="Cybersecurity Threat Detection and Response System",
    version="1.0.0",
)

BASE_DIR = Path(__file__).resolve().parent
DASHBOARD_PATH = BASE_DIR / "index.html"


@app.get("/", response_class=HTMLResponse)
async def home():
    """Display the Cyberion Shield homepage."""
    if DASHBOARD_PATH.exists():
        return DASHBOARD_PATH.read_text(encoding="utf-8")

    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Cyberion Shield</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: #0f172a;
                color: #e2e8f0;
                text-align: center;
                padding: 60px 20px;
            }
            .card {
                max-width: 650px;
                margin: auto;
                padding: 35px;
                background: #1e293b;
                border-radius: 16px;
            }
            h1 { color: #38bdf8; }
            .status { color: #4ade80; }
            a { color: #38bdf8; }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>Cyberion Shield</h1>
            <p>Cybersecurity Threat Detection &amp; Response System</p>
            <p class="status">API is running successfully</p>
            <p>Monitor threats, review security alerts, and protect your systems.</p>
            <p><a href="/docs">Explore API Documentation</a></p>
            <p><a href="/health">Check System Health</a></p>
        </div>
    </body>
    </html>
    """


@app.get("/health")
async def health():
    return {
        "status": "online",
        "project": "Cyberion Shield",
        "version": "1.0.0",
    }


@app.get("/api")
async def api_info():
    return {
        "project": "Cyberion Shield",
        "description": "Cybersecurity Threat Detection and Response System",
        "docs": "/docs",
        "health": "/health",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8000)),
    )
