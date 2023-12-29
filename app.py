import streamlit as st
import random
import sqlite3
import time
import threading

# ルーレットのクラス
class Roulette(threading.Thread):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.should_stop = threading.Event()
        self.first_joshi = ""
        self.second_joshi = ""
        self.words = []
    
    def run(self):
        while not self.should_stop.wait(0):
            self.first_joshi = random.choice(JOSHI_LIST)
            self.second_joshi = random.choice(JOSHI_LIST)
            self.words = random.sample(list(res), 3)

# タイトルと初めの処理
st.title("ドキドキルーレット")
st.text("ことばを3個以上登録してルーレットを回してね")
if not "roulette" in st.session_state:
    st.session_state["roulette"] = None
roulette = st.session_state["roulette"]
if not "result" in st.session_state:
    st.session_state["result"] = ""
result = st.session_state["result"]

# データベースに接続
con = sqlite3.connect("main.db")
cur = con.cursor()
cur.execute(
    """CREATE TABLE IF NOT EXISTS items  (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word STRING
    )"""
)

# ことばを追加
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

# ルーレットの挙動
res = list(x[0] for x in cur.execute("SELECT word FROM items").fetchall())
if st.button("ルーレットを回す") and len(res) >= 3:
    roulette = st.session_state["roulette"] = Roulette(daemon=True)
    roulette.start()
    st.experimental_rerun()
if st.button("ルーレットを止める") and roulette:
    roulette.should_stop.set() # set()でTrueに
    roulette.join() # 前の処理を待つ
    roulette = st.session_state["roulette"] = None
    st.experimental_rerun()

if roulette:
    placeholder = st.empty()
    while roulette.is_alive():
        if first_joshi_checkbox and second_joshi_checkbox:
            gen = f"# {roulette.words[0]} {roulette.first_joshi} {roulette.words[1]} {roulette.second_joshi} {roulette.words[2]}"
        elif first_joshi_checkbox and not second_joshi_checkbox:
            gen = f"# {roulette.words[0]} {roulette.first_joshi} {roulette.words[1]} {roulette.words[2]}"
        elif not first_joshi_checkbox and second_joshi_checkbox:
            gen = f"# {roulette.words[0]} {roulette.words[1]} {roulette.second_joshi} {roulette.words[2]}"
        else:
            gen = f"# {roulette.words[0]} {roulette.words[1]} {roulette.words[2]}"
        st.session_state["result"] = gen # 生成したものをresultに格納する
        placeholder.markdown(gen)
        time.sleep(0.5)
st.markdown(result) # resultを表示する

# テーブルをリセットする
if st.button("ことばのテーブルをリセットする"):
    cur.execute("DELETE FROM items")
    con.commit()
    # print(cur.execute("SELECT * FROM items").fetchall())

cur.close()
con.close()