import streamlit as st
import re

# ตั้งค่าหน้าเว็บให้แสดงผลแบบกว้าง (Wide mode)
st.set_page_config(page_title="Tkinter Calculator Challenge", layout="wide")

st.title("🧮 บทเรียน: สร้างเครื่องคิดเลขด้วย Tkinter")
st.write("ให้นักเรียนฝึกเขียนโค้ดสร้างโปรแกรมเครื่องคิดเลขตามโจทย์ที่กำหนด และกดตรวจคำตอบ")

# แบ่งหน้าจอเป็น 2 ฝั่ง (ซ้าย: โจทย์และช่องพิมพ์โค้ด | ขวา: ระบบตรวจคำตอบ)
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📝 โจทย์: โปรแกรมเครื่องคิดเลข")
    st.markdown("""
    **ความต้องการของระบบ:**
    1. Import ไลบรารีแบบ `from tkinter import *`
    2. มีฟังก์ชันหลัก 3 ฟังก์ชัน: `clear()`, `press(number)`, และ `equal()` (ใช้ `eval()` ในการคำนวณและดักจับ error)
    3. สร้างหน้าต่างหลัก `m = Tk()` ตั้งชื่อว่า `'Calculator from python'` และตั้งฟอนต์เป็น `'consolas 30'`
    4. มี `Label` แสดงผล และปุ่มกดตัวเลข (0-9), เครื่องหมาย (+, -, *, /), ปุ่ม Clear, และปุ่มเครื่องหมายเท่ากับ (=) พร้อมจัดตำแหน่งด้วย `.grid()`
    """)
    
    # โค้ดเริ่มต้น (เว้นส่วนปุ่มไว้ให้นักเรียนฝึกเขียน หรือจะลบออกเพื่อให้พิมพ์เองทั้งหมดก็ได้ครับ)
    default_code = """from tkinter import *

def clear():
    global expression
    global lable_show_cal
    result = "0"
    expression = ""
    lable_show_cal.set(result)
    
def press(number):
    global expression
    global lable_show_cal
    expression = expression + number
    lable_show
