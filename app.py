import streamlit as st
import random
import sqlite3

st.title("ドキドキルーレット")
st.header("放てことばのきらめき")
st.text("ことばを3個以上登録して、TokiMekiしてね")
con = sqlite3.connect("main.db")
cur = con.cursor()
cur.execute(
    """CREATE TABLE IF NOT EXISTS items  (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word STRING
    )"""
)

with st.form(key="submit_form", clear_on_submit=True):
    word_input = st.text_input("ことばをスペース区切りで入力してね", placeholder="ことば")
    submit_button = st.form_submit_button("ことばを登録")
    if submit_button and word_input != "":
        word_list = word_input.split()
        for i in range(len(word_list)):
            cur.execute("INSERT INTO items (word) VALUES (?)", (word_list[i], ))
            con.commit()
        # print(cur.execute("SELECT * FROM items").fetchall())

res = list(x[0] for x in cur.execute("SELECT word FROM items").fetchall())
if st.button("Let's TokiMeki!!") and len(res) >= 3:
    nums = random.sample(list(res), 3)
    st.markdown(f"# {nums[0]} {nums[1]} {nums[2]}", )

if st.button("ことばのテーブルをリセットする"):
    cur.execute("DELETE FROM items")
    con.commit()
    # print(cur.execute("SELECT * FROM items").fetchall())

cur.close()
con.close()