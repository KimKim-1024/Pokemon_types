import streamlit as st
from PIL import Image, ImageDraw

# --- ページ設定 ---
st.set_page_config(page_title="ポケモンタイプ診断", layout="centered")

# --- CSSでUI強化 ---
st.markdown("""
<style>
body {
    background-color: #f5f5f5;
}
.stButton button {
    width: 100%;
    height: 60px;
    font-size: 18px;
    border-radius: 12px;
}
.title {
    text-align: center;
    font-size: 28px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# --- 初期化 ---
if "q" not in st.session_state:
    st.session_state.q = 0
    st.session_state.traits = {k:0 for k in [
        "attack","defense","order","freedom","stable","change",
        "extrovert","introvert","logic","emotion","intuition","real"
    ]}

# --- 質問 ---
questions = [
    ("強敵トレーナーと目が合った！", ("先手で攻める","attack"), ("様子を見る","defense")),
    ("ピンチのときは？", ("大技で逆転","attack"), ("守り優先","defense")),
    ("ジム挑戦のタイミングは？", ("準備してから","order"), ("すぐ行く","freedom")),
    ("冒険スタイルは？", ("計画的","order"), ("気分","freedom")),
    ("手持ちは？", ("固定で育成","stable"), ("入れ替え","change")),
    ("新ポケモン発見！", ("今のメンバー優先","stable"), ("試してみる","change")),
    ("他トレーナーとの関係は？", ("話しかける","extrovert"), ("必要なときだけ","introvert")),
    ("新しい街では？", ("人に聞く","extrovert"), ("一人で探索","introvert")),
    ("ポケモン選びは？", ("性能重視","logic"), ("好み重視","emotion")),
    ("バトル重視は？", ("勝率","logic"), ("スタイル","emotion")),
    ("ダンジョンでは？", ("勘で進む","intuition"), ("地図確認","real")),
    ("初めての場所では？", ("気になる方へ","intuition"), ("安全優先","real")),
]

# --- タイプ定義 ---
types = {
    "ほのお":[("emotion",3),("extrovert",2),("attack",1)],
    "みず":[("change",3),("freedom",2),("intuition",1)],
    "でんき":[("extrovert",3),("intuition",2),("logic",1)],
    "くさ":[("real",3),("order",2),("introvert",1)],
    "こおり":[("introvert",3),("defense",2),("order",1)],
    "かくとう":[("attack",3),("order",2),("extrovert",1)],
    "どく":[("attack",3),("introvert",2),("stable",1)],
    "じめん":[("stable",3),("defense",2),("real",1)],
    "ひこう":[("freedom",3),("intuition",2),("extrovert",1)],
    "エスパー":[("intuition",3),("emotion",2),("freedom",1)],
    "むし":[("real",3),("freedom",2),("intuition",1)],
    "いわ":[("stable",3),("defense",2),("logic",1)],
    "ゴースト":[("introvert",3),("intuition",2),("freedom",1)],
    "ドラゴン":[("attack",3),("order",2),("extrovert",1)],
    "あく":[("attack",3),("freedom",2),("logic",1)],
    "はがね":[("defense",3),("stable",2),("logic",1)],
    "フェアリー":[("order",3),("stable",2),("extrovert",1)],
    "ノーマル":[("stable",3),("real",2),("logic",1)]
}

# --- 相性 ---
compatibility = {
    "ほのお":"くさ","みず":"でんき","でんき":"ひこう","くさ":"みず",
    "こおり":"ドラゴン","かくとう":"いわ","どく":"くさ","じめん":"でんき",
    "ひこう":"かくとう","エスパー":"ゴースト","むし":"くさ","いわ":"ほのお",
    "ゴースト":"エスパー","ドラゴン":"ドラゴン","あく":"ゴースト",
    "はがね":"フェアリー","フェアリー":"あく","ノーマル":"みず"
}

# --- 画像生成 ---
def generate_image(type_name):
    img = Image.new("RGB", (200,200), "white")
    draw = ImageDraw.Draw(img)

    colors = {
        "ほのお":"red","みず":"blue","でんき":"yellow","くさ":"green",
        "こおり":"cyan","かくとう":"orange","どく":"purple","じめん":"brown",
        "ひこう":"skyblue","エスパー":"pink","むし":"lime","いわ":"gray",
        "ゴースト":"black","ドラゴン":"darkred","あく":"darkgray",
        "はがね":"silver","フェアリー":"magenta","ノーマル":"beige"
    }

    c = colors.get(type_name, "black")

    if type_name == "ほのお":
        draw.polygon([(100,40),(160,160),(40,160)], fill=c)
    elif type_name == "でんき":
        draw.polygon([(80,40),(120,100),(90,100),(130,160),(70,110),(100,110)], fill=c)
    elif type_name == "みず":
        draw.arc((40,60,160,180), 0, 180, fill=c, width=10)
    elif type_name == "いわ":
        draw.rectangle((50,50,150,150), fill=c)
    elif type_name == "ゴースト":
        draw.ellipse((50,50,150,150), fill=c)
        draw.rectangle((50,100,150,150), fill="white")
    else:
        draw.ellipse((50,50,150,150), fill=c)

    return img

# --- 表示 ---
if st.session_state.q < len(questions):
    q,a,b = questions[st.session_state.q]

    st.markdown(f"<div class='title'>{q}</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    if col1.button("▶ " + a[0]):
        st.session_state.traits[a[1]] += 3
        st.session_state.q += 1
        st.rerun()

    if col2.button("▶ " + b[0]):
        st.session_state.traits[b[1]] += 3
        st.session_state.q += 1
        st.rerun()

else:
    scores = {}
    for t,conds in types.items():
        scores[t] = sum(st.session_state.traits[c]*w for c,w in conds)

    result = max(scores, key=scores.get)

    st.markdown(f"<div class='title'>あなたのタイプ：{result}</div>", unsafe_allow_html=True)
    st.write("相性がいいタイプ：", compatibility[result])

    img = generate_image(result)
    st.image(img)
