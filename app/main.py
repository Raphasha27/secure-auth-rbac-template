from fastapi import FastAPI

app = FastAPI(title="Secure Auth + RBAC Template")

@app.get("/")
def root():
    return {"message": "Auth + RBAC Template"}
