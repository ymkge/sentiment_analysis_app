# 感情分析Webアプリ

ユーザーが入力したレビュー文を「ポジティブ」「ネガティブ」に分類するWebアプリです。

## 技術スタック

- **フレームワーク**: Streamlit
- **モデル**: HuggingFace Transformers (`nlptown/bert-base-multilingual-uncased-sentiment`)
- **言語**: Python

## ローカルでの実行方法

1. 必要なライブラリをインストールします。
   ```bash
   pip install -r requirements.txt
   ```

2. Streamlitアプリを実行します。
   ```bash
   streamlit run app.py
   ```

3. ブラウザで `http://localhost:8501` を開きます。

## 処理フロー

```mermaid
graph TD
    subgraph "準備フェーズ"
        A[アプリ起動] --> B{AIモデルは<br>準備できてる？};
        B -- いいえ --> C[Hugging Faceから<br>感情分析AIを呼び出す<br>（初回のみ時間がかかる）];
        C --> D[呼び出したAIを<br>キャッシュに保存し待機させる];
        B -- はい --> D;
    end

    subgraph "操作フェーズ"
        D --> E[ウェブ画面を表示<br>・タイトル<br>・テキスト入力欄<br>・分析ボタン];
        E --> F{分析ボタンが<br>押されるのを待つ};
        F -- 押された --> G[入力された文章を<br>読み取る];
    end

    subgraph "分析・結果表示フェーズ"
        G --> H{文章は空っぽ？};
        H -- いいえ --> I[待機していたAIに<br>文章を渡して分析を依頼];
        H -- はい --> J[「文章を入力してください」<br>と警告を出す];
        J --> E;
        I --> K[AIが分析結果を返す<br>（例：「4 stars」, 確信度：0.8）];
        K --> L[AIの結果を人間に<br>分かりやすく翻訳<br>（例：「ポジティブ」）];
        L --> M[翻訳した最終結果を<br>画面にきれいに表示する];
        M --> E;
    end
```

## デプロイ手順 (Vercel)

このStreamlitアプリはVercelにデプロイできます。

1. **GitHubリポジトリの作成**:
   - このプロジェクトをGitHubにプッシュします。

2. **Vercelプロジェクトの作成**:
   - Vercelにログインし、`Add New...` -> `Project` を選択します。
   - 作成したGitHubリポジトリをインポートします。

3. **プロジェクトの設定**:
   - **Framework Preset**: `Other` を選択します。
   - **Build and Output Settings** を以下のように設定します。
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `streamlit run app.py --server.port $PORT --server.headless true`

4. **デプロイ**:
   - `Deploy` ボタンをクリックします。デプロイが完了すると、公開URLが発行されます。