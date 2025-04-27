from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.user_router.users import router as user_router
from routers.auth_router.auth import router as auth_router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Welcome to the Restaurant Booking API"}


app.include_router(user_router)
app.include_router(auth_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
