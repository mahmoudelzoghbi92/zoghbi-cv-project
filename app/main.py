from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "cvdb")

client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]
collection = db["interactions"]


@app.on_event("startup")
async def startup():
    existing = await collection.find_one({"_id": "counts"})
    if not existing:
        await collection.insert_one({"_id": "counts", "likes": 0, "dislikes": 0})


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/api/counts")
async def get_counts():
    doc = await collection.find_one({"_id": "counts"})
    return {"likes": doc["likes"], "dislikes": doc["dislikes"]}


@app.post("/api/like")
async def like():
    await collection.update_one(
        {"_id": "counts"},
        {"$inc": {"likes": 1}}
    )
    doc = await collection.find_one({"_id": "counts"})
    return {"likes": doc["likes"], "dislikes": doc["dislikes"]}


@app.post("/api/dislike")
async def dislike():
    await collection.update_one(
        {"_id": "counts"},
        {"$inc": {"dislikes": 1}}
    )
    doc = await collection.find_one({"_id": "counts"})
    return {"likes": doc["likes"], "dislikes": doc["dislikes"]}


app.mount("/", StaticFiles(directory="app/static", html=True), name="static")


@app.get("/")
async def root():
    return FileResponse("app/static/index.html")
