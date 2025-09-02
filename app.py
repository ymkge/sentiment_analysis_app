import streamlit as st
from transformers import pipeline

# キャッシュを使用してモデルのロードを高速化
@st.cache_resource
def load_model():
    """
    HuggingFaceの事前学習済みBERTモデルをロードするための関数。
    'sentiment-analysis'タスクに特化しています。
    """
    model = pipeline(
        "sentiment-analysis",
        model="nlptown/bert-base-multilingual-uncased-sentiment"
    )
    return model

def convert_label_and_score(prediction):
    """
    モデルの出力（例: '5 stars'）をより分かりやすいラベル（ポジティブ/ネガティブ）に変換します。
    """
    label = prediction['label']
    score = prediction['score']
    
    stars = int(label.split(' ')[0])
    
    if stars >= 4:
        return "ポジティブ", score
    elif stars <= 2:
        return "ネガティブ", score
    else:  # 3 stars
        return "ニュートラル", score

# --- Streamlit UIの構築 ---

st.set_page_config(page_title="感情分析アプリ", page_icon="😊")

st.title("レビュー感情分析アプリ")
st.write("レビュー文を入力すると、AIがその内容を「ポジティブ」「ネガティブ」「ニュートラル」に分類します。")

# HuggingFaceモデルのロード
with st.spinner("分析モデルを準備しています..."):
    sentiment_classifier = load_model()

# ユーザーからのテキスト入力を受け取る
user_input = st.text_area(
    "ここに分析したいレビュー文を入力してください:",
    "このレストランは最高でした！料理も美味しく、サービスも素晴らしかったです。",
    height=150
)

# 分析実行ボタン
if st.button("分析する"):
    if user_input:
        # 入力テキストに対して推論を実行
        with st.spinner("AIが分析中です..."):
            result = sentiment_classifier(user_input)
            # resultはリスト形式で返されるため、最初の要素を取得
            prediction = result[0]
            
            # ラベルとスコアを変換
            final_label, final_score = convert_label_and_score(prediction)

        st.subheader("分析結果")
        
        # 結果に応じて表示を切り替え
        if final_label == "ポジティブ":
            st.success(f"判定: {final_label}")
        elif final_label == "ネガティブ":
            st.error(f"判定: {final_label}")
        else:
            st.info(f"判定: {final_label}")

        # 確信度をプログレスバーで表示
        st.write(f"確信度: {final_score:.2f}")
        st.progress(final_score)

        # モデルの生の出力を参考情報として表示
        with st.expander("モデルの元出力を表示"):
            st.write(prediction)
    else:
        # テキストが入力されていない場合に警告
        st.warning("分析するレビュー文を入力してください。")
