# 感情分析Webアプリ (FastAPI + Next.js版)

ユーザーが入力したレビュー文を「ポジティブ」「ネガティブ」に分類するWebアプリです。
バックエンドはFastAPIとHugging Face Transformers、フロントエンドはNext.jsで構築されています。

## 主な特徴

- **高精度なAIモデル:** Hugging Faceの事前学習済みモデル (`nlptown/bert-base-multilingual-uncased-sentiment`) を利用し、高精度な感情分析を実現。
- **モダンなUI:** Next.jsとTailwind CSSで構築された、インタラクティブで分かりやすいユーザーインターフェース。
- **AIの透明性:** AIがどのように判断したか（5段階評価の確率分布）を可視化し、結果の信頼性をユーザーが確認可能。
- **クリーンな設計:** FastAPIのライフサイクル管理や、Reactのコンポーネント分割など、メンテナンス性を考慮したリファクタリングが実施されています。

## 技術スタック

- **バックエンド:** FastAPI, Uvicorn, Pydantic
- **AIモデル:** Hugging Face Transformers, PyTorch
- **フロントエンド:** Next.js, React, TypeScript, Tailwind CSS
- **アイコン:** Lucide React

## プロジェクト構成

```
sentiment_analysis_app/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py       # FastAPIアプリケーション + Lifespan管理
│   │   ├── models.py     # モデルのロードと推論ロジック
│   │   └── schemas.py    # データ検証モデル
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   └── page.tsx      # メインページ（コンポーネントを組み立てる）
│   │   └── components/       # UIコンポーネント群
│   │       ├── AppTitle.tsx
│   │       ├── InputForm.tsx
│   │       ├── ResultDisplay.tsx
│   │       └── StarRating.tsx
│   ├── package.json
│   └── tailwind.config.ts
└── README.md
```

## 実行方法

このアプリケーションを実行するには、バックエンドAPIとフロントエンドUIの両方を起動する必要があります。
それぞれのターミナル（コマンドプロンプト）で以下の手順を実行してください。

### 1. バックエンド (FastAPI) の起動

**ターミナル1 (プロジェクトルートから)**

```bash
# 1. バックエンドディレクトリに移動
cd backend

# 2. 必要なライブラリをインストール
pip install -r requirements.txt

# 3. APIサーバーを起動
uvicorn app.main:app --reload
```
サーバーが `http://127.0.0.1:8000` で起動します。

### 2. フロントエンド (Next.js) の起動

**ターミナル2 (プロジェクトルートから)**

```bash
# 1. フロントエンドディレクトリに移動
cd frontend

# 2. 必要なパッケージをインストール
npm install

# 3. 開発サーバーを起動
npm run dev
```
サーバーが `http://localhost:3000` で起動します。
ブラウザで `http://localhost:3000` を開くと、アプリケーションにアクセスできます。
