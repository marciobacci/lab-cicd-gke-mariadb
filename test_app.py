from app import app

def test_healthz_ok():
    client = app.test_client()
    resp = client.get("/healthz")
    assert resp.status_code == 200
    assert resp.json["status"] ==  "ok"
