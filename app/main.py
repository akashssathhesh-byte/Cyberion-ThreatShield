from pathlib import Path
from threading import Lock

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

from app.config import BASE_DIR, load_config
from app.database import (
    init_db,
    insert_alert,
    recent_alerts,
    stats,
    find_hash,
)
from app.detector import DetectionEngine
from app.logger import setup_logging, write_event
from app.watcher import start_watcher

# Load configuration
cfg = load_config()

# Initialize application
setup_logging()
init_db()

app = FastAPI(
    title="Cyberion Shield",
    description="Cybersecurity Threat Detection and Response Dashboard",
    version="1.0.0",
)

state_lock = Lock()
observer = None


def handle_alert(alert):
    """Save detected security alerts to the database and JSONL log."""
    data = alert.to_dict()

    with state_lock:
        insert_alert(alert)
        write_event(data)


@app.on_event("startup")
def startup():
    """Start monitoring the configured directory."""
    global observer

    monitor_path = Path(cfg["monitor"]["monitor_path"])

    if not monitor_path.is_absolute():
        monitor_path = BASE_DIR / monitor_path

    monitor_path.mkdir(parents=True, exist_ok=True)

    detector = DetectionEngine(handle_alert)

    observer = start_watcher(
        str(monitor_path),
        detector,
        recursive=cfg["monitor"].get("recursive", True),
    )


@app.on_event("shutdown")
def shutdown():
    """Stop the filesystem watcher gracefully."""
    global observer

    if observer is not None:
        observer.stop()
        observer.join()
        observer = None


@app.get("/")
def dashboard():
    """Serve the Cyberion Shield dashboard."""
    dashboard_file = BASE_DIR / "dashboard" / "index.html"

    if not dashboard_file.exists():
        raise HTTPException(
            status_code=404,
            detail="Dashboard file not found",
        )

    return FileResponse(dashboard_file)


@app.get("/health")
def health():
    """Check whether the API is running."""
    return {
        "status": "ok",
        "service": "Cyberion Shield",
        "version": "1.0.0",
    }


@app.get("/alerts")
def get_alerts(limit: int = 50):
    """Return recent security alerts."""
    limit = max(1, min(limit, 500))
    return recent_alerts(limit)


@app.get("/stats")
def get_stats():
    """Return alert statistics."""
    return stats()


@app.get("/ioc/{sha256}")
def lookup_ioc(sha256: str):
    """Find alerts associated with a SHA-256 hash."""
    if (
        len(sha256) != 64
        or any(c not in "0123456789abcdefABCDEF" for c in sha256)
    ):
        raise HTTPException(
            status_code=400,
            detail="Invalid SHA-256 hash",
        )

    return {
        "sha256": sha256.lower(),
        "observations": find_hash(sha256.lower()),
    if len(sha256) != 64 or any(c not in "0123456789abcdefABCDEF" for c in sha256):
        raise HTTPException(status_code=400, detail="Invalid SHA-256 hash")
    return {"sha256": sha256, "observations": find_hash(sha256)}
    from fastapi import FastAPI
