from fastapi import FastAPI, Depends
from app.dependencies.rbac import require_role, Role, get_current_user

app = FastAPI(title="Secure Auth & RBAC API")

@app.get("/public")
async def public_data():
    return {"message": "Anyone can see this"}

@app.get("/user-profile", dependencies=[Depends(require_role([Role.USER, Role.ADMIN]))])
async def user_profile(user: dict = Depends(get_current_user)):
    return {"message": f"Welcome {user['username']}!"}

@app.get("/admin-dashboard", dependencies=[Depends(require_role([Role.ADMIN]))])
async def admin_dashboard():
    return {"message": "Super secret admin data"}
