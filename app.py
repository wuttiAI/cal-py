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
    lable_show_cal.set(expression)

def equal():
    try:
        global expression
        global lable_show_cal
        result = str(eval(expression))
        lable_show_cal.set(result)
    except:
        result = "error"
        expression = ""
    lable_show_cal.set(result)

m = Tk()
m.title('Calculator from python')
m.option_add("font", "consolas 30")
lable_show_cal = StringVar()
lable_show_cal.set(0)
expression = ""

Label(m, textvariable=lable_show_cal).grid(row=0, column=0, columnspan=4)
Button(m, text="clear", command=clear).grid(row=1, column=0, columnspan=4, sticky="news")

# ---- ให้นักเรียนเขียนโค้ดสร้างปุ่มตัวเลข 0-9 และเครื่องหมายต่างๆ ต่อจากตรงนี้ ----



m.mainloop()
"""
    
    # ช่องพิมพ์โค้ad
    user_code = st.text_area("✍️ พิมพ์โค้ด Python ของคุณที่นี่:", value=default_code, height=500)
    check_button = st.button("🚀 ส่งคำตอบ / ตรวจสอบโค้ด")

with col2:
    st.subheader("🎯 ผลการตรวจคำตอบ (Grader Output)")
    
    if check_button:
        score = 0
        total_checks = 6
        feedback = []
        
        # ลบช่องว่างออกเพื่อให้ง่ายต่อการตรวจด้วย Regex
        clean_code = user_code.replace(" ", "").replace("'", '"')
        
        # 1. ตรวจสอบฟังก์ชัน clear, press, equal
        if "defclear()" in clean_code and "defpress(number):" in clean_code and "defequal():" in clean_code:
            feedback.append("✅ โครงสร้างฟังก์ชันลอจิก `clear`, `press`, และ `equal` ครบถ้วน")
            score += 1
        else:
            feedback.append("❌ ฟังก์ชันลอจิกไม่ครบถ้วน (ต้องมี clear(), press(number) และ equal())")
            
        # 2. ตรวจสอบการใช้ eval() ดักจับข้อผิดพลาด
        if "eval(expression)" in clean_code and "except:" in clean_code:
            feedback.append("✅ มีการใช้ `eval()` และระบบ `try-except` ดักจับ Error ได้ถูกต้อง")
            score += 1
        else:
            feedback.append("❌ ฟังก์ชัน equal() ควรมีระบบ `try-except` และใช้ `eval(expression)`")
            
        # 3. ตรวจสอบการตั้งค่าหน้าต่างหลัก
        if "m=Tk()" in clean_code and 'm.title("Calculatorfrompython")' in clean_code:
            feedback.append("✅ สร้างหน้าต่าง `m` และตั้งชื่อ Title ถูกต้อง")
            score += 1
        else:
            feedback.append("❌ หน้าต่างหลัก `Tk()` หรือชื่อ Title ไม่ถูกต้อง")
            
        # 4. ตรวจสอบการสร้างหน้าจอผลลัพธ์ (Label)
        if "Label(m,textvariable=lable_show_cal).grid" in clean_code:
            feedback.append("✅ สร้างหน้าจอแสดงผล `Label` และผูกกับ `lable_show_cal` ถูกต้อง")
            score += 1
        else:
            feedback.append("❌ ไม่พบการสร้าง `Label` ที่ผูกกับ `textvariable=lable_show_cal`")

        # 5. ตรวจสอบปุ่มตัวเลขและเครื่องหมาย (สุ่มตรวจปุ่มสำคัญ เช่น ปุ่ม 7, ปุ่ม +, ปุ่ม Clear)
        has_buttons = True
        if 'text="clear",command=clear' not in clean_code:
            has_buttons = False
        if 'text="7",command=lambda:press("7")' not in clean_code:
            has_buttons = False
        if 'text="+",command=lambda:press("+")' not in clean_code:
            has_buttons = False
        if 'text="=",command=equal' not in clean_code:
            has_buttons = False
            
        if has_buttons:
            feedback.append("✅ ปุ่มตัวเลข ปุ่มเครื่องหมายสำคัญ และการใช้ Lambda ถูกต้องครบบริบูรณ์")
            score += 1
        else:
            feedback.append("❌ ปุ่มกดบางปุ่มหรือการตั้งค่า `command=lambda: press(...)` ยังไม่ถูกต้องตามรูปแบบ")

        # 6. ตรวจสอบคำสั่งรันระบบในบรรทัดสุดท้าย
        if "m.mainloop()" in clean_code:
            feedback.append("✅ มีการสั่งรันโปรแกรมปิดท้ายด้วย `m.mainloop()`")
            score += 1
        else:
            feedback.append("❌ อย่าลืมใส่ `m.mainloop()` ที่บรรทัดสุดท้ายเพื่อสั่งให้ GUI ทำงาน")
            
        # แสดงผลคะแนนรวม
        st.write("---")
        if score == total_checks:
            st.success(f"🎉 ยอดเยี่ยมมาก! โค้ดเครื่องคิดเลขของคุณถูกต้องสมบูรณ์ ได้ {score}/{total_checks} คะแนน")
            st.balloons()
        else:
            st.warning(f"💡 พยายามอีกนิด! คะแนนของคุณคือ: {score}/{total_checks}")
            
        # แสดงรายละเอียดผลการตรวจทีละข้อ
        for item in feedback:
            st.write(item)
            
    else:
        st.info("ℹ️ พิมพ์ซี้อหรือแก้ไขโค้ดเสร็จแล้ว ให้กดปุ่ม 'ส่งคำตอบ' ด้านล่างซ้ายเพื่อรับคะแนน")
