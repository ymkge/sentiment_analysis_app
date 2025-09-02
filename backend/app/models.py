from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

# デモ用の簡単な学習データ
train_texts = [
    "この映画は本当に素晴らしかった。感動した！",
    "最高のサービスでした。また来たいです。",
    "この製品はとても使いやすい。",
    "味は最悪だった。二度と行かない。",
    "ひどい品質。お金の無駄だった。",
    "サポートの対応が悪すぎる。"
]
train_labels = ["ポジティブ", "ポジティブ", "ポジティブ", "ネガティブ", "ネガティブ", "ネガティブ"]

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
    class_index = list(model.classes_).index(prediction)
    
    # 予測されたクラスの確率（確信度）を取得
    score = proba[0][class_index]
    
    return {"label": prediction, "score": score}
