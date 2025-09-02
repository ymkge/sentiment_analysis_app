from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .schemas import SentimentRequest, SentimentResponse
from .models import predict_sentiment

app = FastAPI(
    title="感情分析API",
    description="scikit-learnモデルを使った感情分析APIです。",
    version="1.0.0"
)

# CORS (Cross-Origin Resource Sharing) の設定
# フロントエンド（今回はNext.js）からのアクセスを許可するために必要
origins = [
    "http://localhost:3000",  # Next.js開発サーバーのデフォルトURL
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
    """
    APIのルートエンドポイント。動作確認用。
    """
    return {"message": "Sentiment Analysis API is running."}

@app.post("/predict", response_model=SentimentResponse, tags=["Prediction"])
def predict(request: SentimentRequest):
    """
    テキストを受け取り、感情分析の結果を返します。

    - **text**: 分析したいテキスト文字列。
    - **return**: 分析結果のラベル（'ポジティブ' or 'ネガティブ'）と確信度。
    """
    result = predict_sentiment(request.text)
    return SentimentResponse(label=result['label'], score=result['score'])
