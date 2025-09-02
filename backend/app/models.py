from transformers import pipeline

# アプリケーション起動時に、Hugging Faceの事前学習済みモデルをロードする
# この処理は一度だけ実行され、モデルはメモリに保持される
print("--- Hugging Faceモデルのロードを開始します ---")
try:
    sentiment_classifier = pipeline(
        "sentiment-analysis",
        model="nlptown/bert-base-multilingual-uncased-sentiment"
    )
    print("--- Hugging Faceモデルのロードが完了しました ---")
except Exception as e:
    print(f"[エラー] モデルのロード中に例外が発生しました: {e}")
    sentiment_classifier = None

def predict_sentiment(text: str):
    """
    Hugging Faceモデルを使って、入力されたテキストの感情を予測する。
    """
    if not sentiment_classifier:
        return {"label": "ネガティブ", "score": 0.5, "error": "モデルがロードされていません"}

    try:
        # モデルで推論を実行
        result = sentiment_classifier(text)[0]
        
        # モデルの出力（例: '5 stars'）をアプリの仕様（ポジティブ/ネガティブ）に変換
        label = result['label']
        score = result['score']
        
        stars = int(label.split(' ')[0])
        
        if stars >= 4:
            final_label = "ポジティブ"
        else: # 1, 2, 3つ星はネガティブに分類
            final_label = "ネガティブ"

        return {"label": final_label, "score": score}

    except Exception as e:
        print(f"[エラー] 推論中に例外が発生しました: {e}")
        return {"label": "ネガティブ", "score": 0.5, "error": str(e)}
