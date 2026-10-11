import json, os, uuid, datetime
from flask import Flask, render_template, request, redirect, url_for, Response, abort
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, ContentSettings

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024  # max 5 MB per bild
ALLOWED = {"image/jpeg", "image/png", "image/webp"}
_svc = None

def svc():
    global _svc
    if _svc is None:  # hanterad identitet, ingen nyckel i koden
        _svc = BlobServiceClient(os.environ["STORAGE_ACCOUNT_URL"], credential=DefaultAzureCredential())
    return _svc

@app.get("/")
def index():
    items, error = [], None
    try:
        c = svc().get_container_client("anmalningar")
        for b in c.list_blobs():
            items.append(json.loads(c.download_blob(b.name).readall()))
        items.sort(key=lambda x: x["skapad"], reverse=True)
    except Exception as e:
        error = str(e)
    return render_template("index.html", items=items, error=error)

@app.post("/anmal")
def anmal():
    rubrik = request.form.get("rubrik", "").strip()[:120]
    beskrivning = request.form.get("beskrivning", "").strip()[:2000]
    if not rubrik or not beskrivning:
        abort(400, "Rubrik och beskrivning kravs")
    rid = str(uuid.uuid4())
    bild = request.files.get("bild")
    bildnamn = None
    if bild and bild.filename:
        if bild.mimetype not in ALLOWED:
            abort(400, "Endast JPG, PNG eller WEBP")
        bildnamn = f"{rid}{os.path.splitext(bild.filename)[1].lower()}"
        svc().get_blob_client("bilder", bildnamn).upload_blob(
            bild.stream, content_settings=ContentSettings(content_type=bild.mimetype))
    doc = {"id": rid, "rubrik": rubrik, "beskrivning": beskrivning, "bild": bildnamn,
           "status": "Ny", "skapad": datetime.datetime.utcnow().isoformat() + "Z"}
    svc().get_blob_client("anmalningar", f"{rid}.json").upload_blob(
        json.dumps(doc, ensure_ascii=False), content_settings=ContentSettings(content_type="application/json"))
    return redirect(url_for("index"))

@app.get("/bild/<name>")
def bild(name):
    b = svc().get_blob_client("bilder", os.path.basename(name))
    d = b.download_blob()
    return Response(d.readall(), mimetype=d.properties.content_settings.content_type)

@app.get("/health")
def health():
    return "ok"
