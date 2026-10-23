from pathlib import Path
from threading import Lock

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

from .config import BASE_DIR, load_config
from .database import init_db, insert_alert, recent_alerts, stats, find_hash
from .detector import DetectionEngine
from .logger import setup_logging, write_event
from .watcher import start_watcher

cfg = load_config()
setup_logging()
init_db()

app = FastAPI(title="Cyberion Shield", version="1.0.0")
_state_lock = Lock()
_observer = None

def handle_alert(alert):
    data = alert.to_dict()
    with _state_lock:
        insert_alert(alert)
        write_event(data)

@app.on_event("startup")
def startup():
    global _observer
    monitor_path = Path(cfg["monitor"]["monitor_path"])
    if not monitor_path.is_absolute():
        monitor_path = BASE_DIR / monitor_path
    monitor_path.mkdir(parents=True, exist_ok=True)

    detector = DetectionEngine(handle_alert)
    _observer = start_watcher(
        str(monitor_path),
        detector,
        recursive=cfg["monitor"].get("recursive", True)
    )

@app.on_event("shutdown")
def shutdown():
    global _observer
    if _observer:
        _observer.stop()
        _observer.join()

@app.get("/")
def dashboard():
    return FileResponse(BASE_DIR / "dashboard" / "index.html")

@app.get("/health")
def health():
    return {"status": "ok", "service": "Cyberion Shield"}

@app.get("/alerts")
def alerts(limit: int = 50):
    limit = max(1, min(limit, 500))
    return recent_alerts(limit)

@app.get("/stats")
def statistics():
    return stats()

@app.get("/ioc/{sha256}")
def ioc_lookup(sha256: str):
    if len(sha256) != 64 or any(c not in "0123456789abcdefABCDEF" for c in sha256):
        raise HTTPException(status_code=400, detail="Invalid SHA-256 hash")
    return {"sha256": sha256, "observations": find_hash(sha256)}
    from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Cyberion ThreatShield is running"}
