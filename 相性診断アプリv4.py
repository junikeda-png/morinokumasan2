import streamlit as st
import os
from openai import OpenAI

# APIキーの設定
os.environ["OPENAI_API_KEY"] = "各自で入れる"

client = OpenAI()

# セッションステートの初期化
if "partner_personality" not in st.session_state:
    st.session_state["partner_personality"] = ""
if "diagnosis_result" not in st.session_state:  # 性格診断結果を保持するためのセッションステート
    st.session_state["diagnosis_result"] = None


# 性格タイプのデータ
personality_descriptions = {
    "INTJ - 建築家": "戦略的で創造力があり、理想を実現するために計画を立てるタイプ。",
    "INTP - 論理学者": "知識欲が強く、物事を深く分析する思想家。",
    "ENTJ - 指揮官": "リーダーシップを発揮し、効率を追求する指揮官タイプ。",
    "ENTP - 討論者": "新しいアイデアを追い求め、論理的に議論を楽しむタイプ。",
    "INFJ - 提唱者": "人の成長を助け、使命感を持つ理想主義者。",
    "INFP - 仲介者": "誠実で価値観を大切にする優しい仲介者。",
    "ENFJ - 主人公": "他人を導き、成長を助けるカリスマ的なリーダー。",
    "ENFP - 運動家": "創造性豊かで、人を鼓舞する自由奔放な人。",
    "ISTJ - 管理者": "責任感が強く、伝統を重んじる実直なタイプ。",
    "ISFJ - 擁護者": "周囲を助けることに努力を惜しまない思いやりのあるタイプ。",
    "ESTJ - 幹部": "実務的で効率的、伝統を尊重するリーダー。",
    "ESFJ - 領事": "社交的で人を助けることに喜びを感じるタイプ。",
    "ISTP - 巨匠": "実用的な問題解決が得意で冒険を好む。",
    "ISFP - 冒険家": "芸術的で柔軟、自己表現を大切にする人。",
    "ESTP - 起業家": "行動力があり、現実的な冒険家。",
    "ESFP - エンターテイナー": "楽しい雰囲気を作るムードメーカー。",
}


# 性格タイプのデータ
personality_categories = {
    "外交官タイプ（直観＋感情タイプ）": [
        "INFJ - 提唱者型: 理想主義的で、共感力が高く、人を導くのが得意。静かだが強い信念を持つ。",
        "INFP - 仲介者型: 想像力豊かで、理想や価値観に基づいて行動する。周囲に優しく、助け合いを重視する。",
        "ENFJ - 主人公型: カリスマ性があり、周囲を巻き込んで大きな目標を達成する。他者の成長をサポートするのが得意。",
        "ENFP - 運動家型: 自由を愛し、新しいアイデアや可能性を探求する。他者を元気づけるエネルギーに溢れている。",
    ],
    "分析家タイプ（直観＋思考タイプ）": [
        "INTJ - 建築家型: 長期的なビジョンを持ち、計画を立てて目標を達成する。独立心が強く、効率を重視する。",
        "INTP - 論理学者型: 知識欲が旺盛で、物事を深く分析するのが得意。アイデアを追求するのが好き。",
        "ENTJ - 指揮官型: リーダーシップがあり、効率的に目標達成に向かう。問題解決力が高く、論理的な決断を下す。",
        "ENTP - 討論者型: 新しいアイデアを楽しみ、議論を通じて学ぶのが得意。革新的で、制約を嫌う。",
    ],
    "実務家タイプ（現実＋思考タイプ）": [
        "ISTJ - 管理者型: 責任感が強く、規律を守りながら効率よく仕事を進める。実践的で、伝統やルールを重視する。",
        "ISFJ - 擁護者型: 誠実で思いやりがあり、他者をサポートすることに喜びを感じる。実務的で、安定した環境を好む。",
        "ESTJ - 幹部型: リーダーシップを発揮し、規律を守りながら効率を追求する。現実的な問題解決が得意。",
        "ESFJ - 領事型: 社交的で、他者との調和を重視する。実際のニーズに応じて迅速に行動する。",
    ],
    "探検家タイプ（現実＋感情タイプ）": [
        "ISTP - 巨匠型: 実践的で、道具や機械の扱いが得意。静かだが好奇心旺盛で、問題解決が得意。",
        "ISFP - 冒険家型: 自分の価値観を大切にし、芸術的な感性を持つ。柔軟で、他者に優しい。",
        "ESTP - 起業家型: 行動力があり、リスクを恐れず挑戦する。現実的な課題に即応するのが得意。",
        "ESFP - エンターテイナー型: 社交的で、人を楽しませることが得意。新しい経験を好み、自由奔放。",
    ],
}

# 性格タイプリストの構築
personality_options = []
for category, types in personality_categories.items():
    for type_info in types:
        personality_options.append(type_info)


# 性格診断の質問セット
personality_questions = {
    "E/I": "初対面の人と話すのは苦にならない",
    "S/N": "経験や事実に基づいて行動することが多い",
    "T/F": "判断する際には、感情よりも論理的な理由を重視する",
    "J/P": "計画通りに物事を進めるのが好きだ",
}

# サイドバー: ユーザー情報入力
user_personality = st.sidebar.selectbox("あなたの性格タイプを選択してください", options=list(personality_descriptions.keys()))

# 画像が格納されているフォルダの指定
image_dir = os.path.join(os.getcwd(), "image")  # "image" フォルダを指定


# サイドバーで自分の性格タイプを選択したときに対応する画像を表示
if user_personality:
    # 性格タイプの名称から対応する画像ファイル名を生成
    image_filename = user_personality.split(" - ")[1] + ".png"  # "建築家.png" などを生成
    image_path = os.path.join(image_dir, image_filename)  # "image" フォルダ内の画像パス

    # 画像の存在を確認して表示
    if os.path.exists(image_path):
        st.markdown("## あなたの性格タイプの画像")
        st.image(image_path, caption=f"あなたのタイプ: {user_personality}", use_container_width=True)
    else:
        st.sidebar.write("画像が見つかりませんでした")

if user_personality:
    st.sidebar.write("あなたの性格タイプの概要")

# personality_categoriesから該当のカテゴリーを表示
for category, types in personality_categories.items():
    for type_info in types:
        if type_info.startswith(user_personality):
            # カテゴリー部分を赤字に設定
            st.sidebar.markdown(f"<span style='color:red;'>**{category}**</span>: {type_info}", unsafe_allow_html=True)
            break


user_age = st.sidebar.number_input("あなたの年齢を選択してください", min_value=18, max_value=100, value=35, step=1)

# 関係性選択
relationship = st.sidebar.selectbox(
    "どんな関係ですか？",
    ["上司・部下", "夫・妻", "恋人同士", "営業マンとお客さん"]
)

# 立場選択
if relationship == "上司・部下":
    user_role = st.sidebar.selectbox("あなたの立場を選択してください", ["上司", "部下"])
elif relationship == "夫・妻":
    user_role = st.sidebar.selectbox("あなたの立場を選択してください", ["夫", "妻"])
elif relationship == "恋人同士":
    user_role = st.sidebar.selectbox("あなたの立場を選択してください", ["恋人A", "恋人B"])
else:
    user_role = st.sidebar.selectbox("あなたの立場を選択してください", ["営業マン", "お客さん"])

# 相手情報の年齢入力
st.header("相手の情報を入力してください")
partner_age = st.number_input("相手の年齢を入力", min_value=18, max_value=100, value=35, step=1)

# 性格診断の質問をインタラクティブに表示
st.header("相手の性格タイプを診断する")
answers = {}
for key, question in personality_questions.items():
    answers[key] = st.radio(question, options=["はい", "いいえ"], key=key)

# 「性格診断判定」ボタンで診断を実行
if st.button("性格診断判定"):
    # 性格タイプを算出
    partner_personality = ""
    for key, answer in answers.items():
        partner_personality += key.split("/")[0] if answer == "はい" else key.split("/")[1]

    # 性格タイプを「形式: INTJ-建築家」で表示する
    partner_personality_full = next(
        (ptype for ptype in personality_descriptions.keys() if ptype.startswith(partner_personality)),
        partner_personality
    )

    # セッションステートに保存
    st.session_state["partner_personality"] = partner_personality_full

    # 診断結果を保存（具体的な名称を含む形式で表示）
    st.session_state["diagnosis_result"] = (
        f"相手の性格タイプ: {partner_personality_full}<br>"
        f"説明: {personality_descriptions.get(partner_personality_full, '説明なし')}"
    )

# 性格診断結果を表示
if st.session_state["diagnosis_result"]:
    st.markdown(st.session_state["diagnosis_result"], unsafe_allow_html=True)

    # 相手の性格タイプに対応する画像を表示
    partner_personality = st.session_state.get("partner_personality", "")
    if partner_personality:
        # 性格タイプの名称から対応する画像ファイル名を生成
        image_filename = partner_personality.split(" - ")[1] + ".png"  # "建築家.png" などを生成
        image_path = os.path.join(image_dir, image_filename)  # "image" フォルダ内の画像パス

        # 画像の存在を確認して表示
        if os.path.exists(image_path):
            st.image(image_path, caption=f"相手のタイプ: {partner_personality}", use_container_width=True)
        else:
            st.write("相手のタイプに対応する画像が見つかりませんでした")
    
 


# 診断スタイル選択肢を定義
default_styles = [
    "論理重視の一般的な回答",
    "寄り添ってくれる年上の女性の回答(アンミカ風)",
    "ざっくばらんな関西弁のおじさんの回答",
    "総理大臣の様な大局的な回答（安倍晋三風）",
    "毒舌な回答（ビートたけし風）",
    "モチベーションが上がる熱い関西弁の回答（本田圭佑風）",
    "関西弁ですごくてきとうな回答（明石家さんま風）",
]


# 条件付きで「りじちょー」を追加
content_styles = default_styles.copy()  # デフォルトスタイルをコピー
if user_age == 23 and user_personality == "ENFJ - 主人公":
    content_styles.append("りじちょー")

# サイドバーに診断スタイルを表示
style = st.sidebar.selectbox("診断スタイルを選んでください", options=content_styles)


# GPTへのリクエスト
def run_gpt(user_data, partner_data, relationship, user_role, style):
    prompt = f"""
    以下の情報に基づき、{relationship}の関係性について、選択された回答スタイル（{style}）で診断を行い、以下のフォーマットに沿って回答してください。

    【入力情報】
    - あなた（{user_role}）のタイプ: {user_data['mebi']}、年齢: {user_data['age']}歳
    - 相手のタイプ: {partner_data['mebi']}、年齢: {partner_data['age']}歳

    【診断結果フォーマット】
    1. **そもそもの相性の良し悪し**:
       - {user_data['mebi']}タイプと{partner_data['mebi']}タイプの相性について、良し悪しを簡潔に述べてください。
       - 結果を以下のような形で提供してください：
         - 「◯◯タイプと△△タイプの相性はあまりよくないようなので、良い関係を築くにはお互いの努力が必要です。」
         - 「◯◯タイプと△△タイプの相性は抜群なので、大きな成果（楽しい結婚生活）が期待できます。」

    2. **お互いの目線からの好ましい行動**:
       - {user_data['mebi']}タイプが{partner_data['mebi']}タイプに対して取るべき具体的な好ましい行動を3つ挙げてください。
         - 行動例: 「◯◯タイプの方は、△△タイプが好む自由な発想を尊重することで、信頼を深めることができます。」
       - 同様に、{partner_data['mebi']}タイプが{user_data['mebi']}タイプに対して取るべき具体的な好ましい行動を3つ挙げてください。

    3. **お互いの目線からの注意点**:
       - {user_data['mebi']}タイプが{partner_data['mebi']}タイプに対して注意すべき点を2～3つ挙げてください。
         - 注意例: 「△△タイプは約束や期限を守らないことを嫌うため、計画的に行動する必要があります。」
       - 同様に、{partner_data['mebi']}タイプが{user_data['mebi']}タイプに対して注意すべき点を2～3つ挙げてください。

    【注意事項】
    - 回答は具体的で実用的なものとしてください。
    - 相性診断に基づくアドバイスが現実的で読者が行動に移しやすいものにしてください。
    - 可能な限りポジティブなトーンを使用し、双方が改善の余地を感じられるようにしてください。
    - 年齢が１０歳以上離れている時は、必ず年齢差による影響に言及ください
    - 診断結果を表示するときは、タイプの表記で回答するのではなく、「あなた」と「相手」という表記にしてください。
    - 診断スタイルが「明石家さんま風」のときは語尾にランダムで「知らんけど」とつけてください。
    - 診断スタイルが「りじちょー」のときは、【診断結果フォーマット】を無視して必ず「性格診断なんか関係あらへん、早く行きたければ一人で進め！遠くまで行きたければみんなで勧め！」という回答だけ表示してください。
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"APIリクエストエラー: {e}")
        return None
# 診断ボタンが押されたかどうかを記録
if "diagnosis_started" not in st.session_state:
    st.session_state["diagnosis_started"] = False

# 「診断を開始」ボタン
if st.button("診断を開始"):
    st.session_state["diagnosis_started"] = True  # 診断開始を記録
    partner_personality = st.session_state.get("partner_personality", "")
    if partner_personality:
        user_data = {"age": user_age, "mebi": user_personality}
        partner_data = {"age": partner_age, "mebi": partner_personality}
        result = run_gpt(user_data, partner_data, relationship, user_role, style)
        if result:
            st.markdown(f"<h2>診断結果</h2>", unsafe_allow_html=True)
            st.markdown(result, unsafe_allow_html=True)
        else:
            st.warning("診断結果が取得できませんでした。")
    else:
        st.warning("相手の性格診断を完了してください！")

# 診断後に「りじちょー.png」を表示
if st.session_state["diagnosis_started"] and style == "りじちょー":
    # 「りじちょー.png」のパスを指定
    rijicho_image_path = os.path.join(image_dir, "りじちょー.png")

    # 画像の存在を確認して表示
    if os.path.exists(rijicho_image_path):
        st.image(rijicho_image_path, caption="りじちょー", use_container_width=True)
    else:
        st.write("「りじちょー.png」の画像が見つかりませんでした")



