from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.user_router.users import router as user_router
from routers.auth_router.auth import router as auth_router
from routers.restaurant_router.restaurant import router as restaurant_router
from routers.table_router.table import router as table_router
from routers.schedule_router.schedule import router as schedule_router
from routers.booking_router.booking import router as booking_router

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
app.include_router(restaurant_router)
app.include_router(table_router)
app.include_router(schedule_router)
app.include_router(booking_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
