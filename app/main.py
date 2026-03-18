from fastapi import FastAPI
from app.routers import user, admin, file


app = FastAPI()

app.include_router(user.router)
app.include_router(admin.router)
app.include_router(file.router)

@app.get(path="/some")
def root():
    return {"message": "API работает"}
