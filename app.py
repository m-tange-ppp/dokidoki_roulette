import streamlit as st
import random
import sqlite3

st.title("ドキドキルーレット")
st.text("ことばを3個以上登録して、TokiMekiしてね")

# データベースに接続する
con = sqlite3.connect("main.db")
cur = con.cursor()
cur.execute(
    """CREATE TABLE IF NOT EXISTS items  (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word STRING
    )"""
)

# ことばを追加する
with st.form(key="submit_form", clear_on_submit=True):
    word_input_form = st.text_input("ことばをスペース区切りで入力してね", placeholder="ことば")
    submit_button = st.form_submit_button("ことばを登録")
    if submit_button and word_input_form != "":
        word_list = word_input_form.split()
        for i in range(len(word_list)):
            cur.execute("INSERT INTO items (word) VALUES (?)", (word_list[i], ))
            con.commit()
        # print(cur.execute("SELECT * FROM items").fetchall())

# 助詞の設定
JOSHI_LIST = ["が", "の", "を", "に", "へ", "と", "より", "から", "で", "や"]
first_joshi_checkbox = st.checkbox("1つ目と2つ目のことばの間に助詞を入れる")
second_joshi_checkbox = st.checkbox("2つ目と3つ目のことばの間に助詞を入れる")

# 追加した言葉でルーレットを回す
res = list(x[0] for x in cur.execute("SELECT word FROM items").fetchall())
if st.button("Let's TokiMeki!!") and len(res) >= 3:
    nums = random.sample(list(res), 3)
    first_joshi = random.choice(JOSHI_LIST)
    second_joshi = random.choice(JOSHI_LIST)
    if first_joshi_checkbox and second_joshi_checkbox:
        st.markdown(f"# {nums[0]} {first_joshi} {nums[1]} {second_joshi} {nums[2]}")
    elif first_joshi_checkbox and not second_joshi_checkbox:
        st.markdown(f"# {nums[0]} {first_joshi} {nums[1]} {nums[2]}")
    elif not first_joshi_checkbox and second_joshi_checkbox:
        st.markdown(f"# {nums[0]} {nums[1]} {second_joshi} {nums[2]}")
    else:
        st.markdown(f"# {nums[0]} {nums[1]} {nums[2]}")

# テーブルをリセットする
if st.button("ことばのテーブルをリセットする"):
    cur.execute("DELETE FROM items")
    con.commit()
    # print(cur.execute("SELECT * FROM items").fetchall())

cur.close()
con.close()