from fastapi import FastAPI
from app.routers import admin_router, file_router, user_router


app = FastAPI()

app.include_router(user_router.router)
app.include_router(admin_router.router)
app.include_router(file_router.router)

@app.get(path="/some")
def root():
    return {"message": "API работает"}
