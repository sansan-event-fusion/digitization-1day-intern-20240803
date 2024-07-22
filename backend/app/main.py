from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.router.delivered import router as delivered_router
from app.router.inspector import router as inspector_router
from app.router.normalizer import router as normalizer_router
from app.router.virtual_card import router as virtual_card_router

app = FastAPI()

# CORSミドルウェアの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # フロントエンドのオリジンを指定
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def read_root():
    return {"Hello": "World!!!"}


app.include_router(delivered_router, prefix="/card")
app.include_router(virtual_card_router, prefix="/virtual_card")
app.include_router(normalizer_router, prefix="/normalizer")
app.include_router(inspector_router, prefix="/inspector")
