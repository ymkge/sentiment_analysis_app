from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import numpy as np

# デモ用の学習データを拡充
train_texts = [
    # ポジティブなサンプル (10件)
    "この映画は本当に素晴らしかった。感動した！",
    "最高のサービスでした。また来たいです。",
    "この製品はとても使いやすいし、デザインも良い。",
    "料理が美味しくて、店の雰囲気も素敵でした。",
    "彼のパフォーマンスは圧巻だった。",
    "迅速な対応に感謝します。非常に助かりました。",
    "この本は面白くて一気に読んでしまった。",
    "価格も手頃で品質も良く、大満足です。",
    "景色が綺麗で、心からリラックスできた。",
    "全てが期待以上でした。強くお勧めします。",

    # ネガティブなサンプル (10件)
    "味は最悪だった。二度と行かない。",
    "ひどい品質。お金の無駄だった。",
    "サポートの対応が悪すぎる。問題が解決しなかった。",
    "映画は退屈で、途中で寝てしまった。",
    "製品はすぐに壊れた。全くお勧めできない。",
    "説明が分かりにくく、非常に不親切だと感じた。",
    "サービスが遅すぎて、とてもがっかりした。",
    "うるさくて落ち着かなかった。",
    "期待外れの内容に失望しました。",
    "この値段でこの内容はありえない。"
]
train_labels = [
    "ポジティブ", "ポジティブ", "ポジティブ", "ポジティブ", "ポジティブ", 
    "ポジティブ", "ポジティブ", "ポジティブ", "ポジティブ", "ポジティブ",
    "ネガティブ", "ネガティブ", "ネガティブ", "ネガティブ", "ネガティブ", 
    "ネガティブ", "ネガティブ", "ネガティブ", "ネガティブ", "ネガティブ"
]

# === モデルの定義を修正 ===
# TfidfVectorizerに analyzer='char' と ngram_range=(2, 3) を追加
# これにより、単語ではなく「文字の組み合わせ」で文章を分析するようになる
model = Pipeline([
    ('tfidf', TfidfVectorizer(analyzer='char', ngram_range=(2, 3))),
    ('clf', LogisticRegression(random_state=42))
])

# アプリケーション起動時にモデルを学習
print("--- モデルの学習を開始します ---")
model.fit(train_texts, train_labels)
print("--- モデルの学習が完了しました ---")
print(f"学習後の特徴量数: {len(model.named_steps['tfidf'].get_feature_names_out())}")
print(f"モデルのクラス: {model.classes_}")

def predict_sentiment(text: str):
    print("\n--- 感情分析処理開始 ---")
    print(f"入力テキスト: '{text}'")

    # 予測
    try:
        prediction = model.predict([text])[0]
        proba = model.predict_proba([text])
    except Exception as e:
        print(f"[エラー] 予測中に例外が発生しました: {e}")
        return {"label": "ネガティブ", "score": 0.5}

    print(f"モデルのクラス順序 (model.classes_): {model.classes_}")
    print(f"各クラスの確率 (proba): {np.round(proba, 3)}")
    print(f"予測されたラベル (prediction): {prediction}")

    try:
        class_index = list(model.classes_).index(prediction)
        score = proba[0][class_index]
        print(f"予測ラベルのインデックス: {class_index}")
        print(f"取得した確信度 (score): {score:.3f}")
    except ValueError:
        print("[エラー] 予測ラベルがモデルのクラス内に見つかりません。")
        # 万が一、予期しないクラスが予測された場合のフォールバック
        return {"label": "ネガティブ", "score": 0.5} 
    
    print("--- 感情分析処理終了 ---")
    
    return {"label": prediction, "score": score}