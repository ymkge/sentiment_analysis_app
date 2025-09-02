from transformers import pipeline
import operator

# アプリケーション起動時に、Hugging Faceの事前学習済みモデルをロードする
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
        return {"label": "ネガティブ", "score": 0.5, "details": []}

    try:
        # top_k=5 ですべてのクラス（1〜5つ星）の確率を取得
        all_results = sentiment_classifier(text, top_k=5)
        
        # 星の数でソート (例: '1 star' が最初に来るように)
        all_results.sort(key=lambda x: int(x['label'].split(' ')[0]))

        # 最も確率の高い結果を取得（これがモデルの第一の予測）
        top_result = max(all_results, key=operator.itemgetter('score'))
        
        # 最も確率の高い結果を基に、最終的なラベルと確信度を決定
        top_stars = int(top_result['label'].split(' ')[0])
        final_label = "ポジティブ" if top_stars >= 4 else "ネガティブ"
        final_score = top_result['score']

        return {
            "label": final_label,
            "score": final_score,
            "details": all_results # 5段階評価の全確率を返す
        }

    except Exception as e:
        print(f"[エラー] 推論中に例外が発生しました: {e}")
        return {"label": "ネガティブ", "score": 0.5, "details": []}