from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

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

# TF-IDFベクトル化とロジスティック回帰を組み合わせたパイプラインを定義
model = Pipeline([
    ('tfidf', TfidfVectorizer()),
    ('clf', LogisticRegression())
])

# アプリケーション起動時にモデルを学習
model.fit(train_texts, train_labels)

def predict_sentiment(text: str):
    """
    入力されたテキストの感情を予測し、ラベルと確信度を返す。
    """
    # 予測ラベルを取得
    prediction = model.predict([text])[0]
    
    # 各クラスに属する確率を取得
    proba = model.predict_proba([text])
    
    # 予測されたクラスのインデックスを見つける
    try:
        class_index = list(model.classes_).index(prediction)
    except ValueError:
        # 万が一、予期しないクラスが予測された場合のフォールバック
        return {"label": "ネガティブ", "score": 0.5} 

    # 予測されたクラスの確率（確信度）を取得
    score = proba[0][class_index]
    
    return {"label": prediction, "score": score}