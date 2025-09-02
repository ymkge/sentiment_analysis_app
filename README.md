# 感情分析Webアプリ (FastAPI + Next.js版)

ユーザーが入力したレビュー文を「ポジティブ」「ネガティブ」に分類するWebアプリです。
バックエンドはFastAPIとscikit-learn、フロントエンドはNext.jsで構築されています。

## プロジェクト構成

```
sentiment_analysis_app/
├── backend/         # FastAPIバックエンド
│   ├── app/
│   └── requirements.txt
├── frontend/        # Next.jsフロントエンド
│   ├── src/
│   └── package.json
└── README.md
```

## 実行方法

このアプリケーションを実行するには、バックエンドAPIとフロントエンドUIの両方を起動する必要があります。
それぞれのターミナル（コマンドプロンプト）で以下の手順を実行してください。

### 1. バックエンド (FastAPI) の起動

**ターミナル1**

```bash
# 1. バックエンドディレクトリに移動
cd /Users/ymto/Documents/git/sentiment_analysis_app/backend

# 2. 必要なライブラリをインストール
pip install -r requirements.txt

# 3. APIサーバーを起動
uvicorn app.main:app --reload
```

サーバーが `http://127.0.0.1:8000` で起動します。

### 2. フロントエンド (Next.js) の起動

**ターミナル2**

```bash
# 1. フロントエンドディレクトリに移動
cd /Users/ymto/Documents/git/sentiment_analysis_app/frontend

# 2. 必要なパッケージをインストール
npm install

# 3. 開発サーバーを起動
npm run dev
```

サーバーが `http://localhost:3000` で起動します。
ブラウザで `http://localhost:3000` を開くと、アプリケーションにアクセスできます。
