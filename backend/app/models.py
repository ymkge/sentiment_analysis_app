from transformers import pipeline
import operator

def load_model():
    """
    Hugging Faceの事前学習済みモデルをロードして返す。
    この関数はアプリケーションの起動時に一度だけ呼ばれます。
    """
    try:
        sentiment_classifier = pipeline(
            "sentiment-analysis",
            model="nlptown/bert-base-multilingual-uncased-sentiment"
        )
        return sentiment_classifier
    except Exception as e:
        print(f"[エラー] モデルのロード中に例外が発生しました: {e}")
        return None

def predict_sentiment(classifier, text: str):
    """
    渡された分類器（AIモデル）を使って、テキストの感情を予測する。
    """
    if not classifier:
        return {"label": "ネガティブ", "score": 0.5, "details": []}

    try:
        # top_k=5 ですべてのクラス（1〜5つ星）の確率を取得
        all_results = classifier(text, top_k=5)
        
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