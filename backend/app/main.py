from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .schemas import SentimentRequest, SentimentResponse
from .models import load_model, predict_sentiment


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPIアプリケーションのライフサイクルを管理します。
    起動時にモデルをロードし、app.stateに格納します。
    """
    print("--- アプリケーション起動処理開始 ---")
    app.state.model = load_model()
    yield
    # アプリケーション終了時のクリーンアップ処理
    print("--- アプリケーション終了処理開始 ---")
    app.state.model = None


app = FastAPI(
    title="感情分析API",
    description="Hugging Faceモデルを使った感情分析APIです。",
    version="1.1.0", # Refactored
    lifespan=lifespan  # lifespanを登録
)

# CORS (Cross-Origin Resource Sharing) の設定
origins = [
    "http://localhost:3000",
    "localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["General"])
def read_root():
    return {"message": "Sentiment Analysis API is running."}


@app.post("/predict", response_model=SentimentResponse, tags=["Prediction"])
def predict(request: SentimentRequest, fastapi_request: Request):
    """
    テキストを受け取り、感情分析の結果を返します。
    """
    # アプリケーションの状態(app.state)からロード済みのモデルを取得
    model = fastapi_request.app.state.model
    result = predict_sentiment(model, request.text)
    return SentimentResponse(**result)
