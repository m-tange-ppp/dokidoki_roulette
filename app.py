import streamlit as st
import random
import sqlite3

st.title("ドキドキルーレット")
st.header("放てことばのきらめき")
con = sqlite3.connect("main.db")
cur = con.cursor()
cur.execute(
    """CREATE TABLE IF NOT EXISTS items  (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word STRING
    )"""
)

if 'temp' not in st.session_state:
    st.session_state.temp = ""

def submit():
    st.session_state.temp = st.session_state.widget
    st.session_state.widget = ""

word_input = st.text_input("ことばを入力してね", placeholder="ことば", on_change=submit, key="widget")
if word_input:
    cur.execute("INSERT INTO items (word) VALUES (?)", (word_input, ))
    con.commit()
    print(cur.execute("SELECT * FROM items").fetchall())

if st.button("テーブルをリセットする"):
    cur.execute("DELETE FROM items")
    con.commit()
    print(cur.execute("SELECT * FROM items").fetchall())

if st.button("Let's TokiMeki!!"):
    res = list(x[0] for x in cur.execute("SELECT word FROM items").fetchall())
    nums = random.choices(list(res), k=3)
    st.write(f"{nums[0]} {nums[1]} {nums[2]}")

cur.close()
con.close()