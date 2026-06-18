import streamlit as st
import sys
from io import StringIO
import contextlib
import re

# ตั้งค่าหน้าเว็บให้แสดงผลแบบกว้าง (Wide mode)
st.set_page_config(page_title="Tkinter Calculator Challenge & Sandbox", layout="wide")

st.title("🧮 บทเรียน: สร้างเครื่องคิดเลขด้วย Tkinter (พร้อมระบบรันโค้ด)")
st.write("ให้นักเรียนฝึกเขียนโค้ดสร้างโปรแกรมเครื่องคิดเลขตามโจทย์ สามารถกดรันเพื่อดูผลลัพธ์ลอจิก หรือกดส่งคำตอบเพื่อตรวจคะแนน")

# แบ่งหน้าจอเป็น 2 ฝั่ง (ซ้าย: โจทย์และช่องพิมพ์โค้ด | ขวา: ระบบตรวจคำตอบและรันผลลัพธ์)
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
    
    # โค้ดเริ่มต้น
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
    
    # ช่องพิมพ์โค้ด
    user_code = st.text_area("✍️ พิมพ์โค้ด Python ของคุณที่นี่:", value=default_code, height=500)
    
    # ปุ่มกดควบคุมแบบแยกหน้าที่
    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        run_button = st.button("▶️ รันโค้ดเพื่อทดสอบลอจิก (Run Code)")
    with btn_col2:
        check_button = st.button("🚀 ส่งคำตอบ / ตรวจสอบโครงสร้างโค้ด")

with col2:
    # ==========================================
    # ส่วนที่ 1: การรันผลลัพธ์ (Run & Mock Execution)
    # ==========================================
    st.subheader("🖥️ ผลลัพธ์การรันโปรแกรม (Execution Sandbox)")
    
    # เก็บข้อมูลสถานะใน Session State เพื่อให้กดปุ่มทดสอบจำลองแล้วค่าไม่หาย
    if "calc_expression" not in st.session_state:
        st.session_state.calc_expression = ""
    if "calc_display" not in st.session_state:
        st.session_state.calc_display = "0"

    if run_button:
        st.info("กำลังรันโค้ดและคอมไพล์ระบบอินเทอร์เฟซ...")
        
        # คลาสและ Object จำลองทดแทนตัวแปรของ Tkinter ไม่ให้เกิดบั๊กบนเซิร์ฟเวอร์
        class MockStringVar:
            def __init__(self): pass
            def set(self, v): st.session_state.calc_display = str(v)
            def get(self): return st.session_state.calc_display

        # โครงสร้างตัวแปรสภาพแวดล้อมเสมือน
        mock_globals = {
            'Tk': lambda: type('MockTk', (), {'title': lambda s, t: None, 'option_add': lambda s, a, b: None, 'mainloop': lambda s: None})(),
            'StringVar': MockStringVar,
            'Label': lambda *args, **kwargs: type('MockLabel', (), {'grid': lambda **k: None})(),
            'Button': lambda *args, **kwargs: type('MockButton', (), {'grid': lambda **k: None})(),
            'expression': st.session_state.calc_expression,
            'lable_show_cal': MockStringVar()
        }
        
        try:
            # ปิดคำสั่งวนลูปอินฟินิตี้ชั่วคราวเพื่อรันเอาลอจิกฟังก์ชันมาใช้
            exec_code = user_code.replace("m.mainloop()", "# m.mainloop()")
            exec(exec_code, mock_globals)
            
            # บันทึกฟังก์ชันที่แปลงได้ลง Session เพื่อให้ปุ่มจำลองนำไปกดเรียกต่อได้
            st.session_state.mock_globals = mock_globals
            st.success("🤖 รันโค้ดลอจิกสำเร็จ! ตรวจสอบกล่องจำลองเครื่องคิดเลขด้านล่างนี้:")
            
        except Exception as e:
            st.error(f"⚠️ เกิดข้อผิดพลาดใน Syntax หรือโค้ดของคุณ: {e}")

    # แสดงผล UI เครื่องคิดเลขจำลอง (ถ้าผู้เรียนเคยผ่านการกด Run อย่างน้อย 1 ครั้ง)
    if "mock_globals" in st.session_state:
        st.markdown("### 🎛️ เครื่องคิดเลขจำลองจากโค้ดของคุณ")
        
        # อัปเดตการแสดงผลหน้าจอ
        st.code(f" [ {st.session_state.calc_display} ] ", language="text")
        
        # สร้างปุ่มกด Interactive เชื่อมต่อฟังก์ชันของผู้เรียน
        mg = st.session_state.mock_globals
        
        if 'press' in mg and 'clear' in mg and 'equal' in mg:
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                if st.button("ปุ่ม [ 7 ]"):
                    # จำลองการกดยิงคำสั่งเข้าฟังก์ชันในโค้ดผู้เรียน
                    # อิงตามการดึงตัวแปร Global
                    mg['expression'] = st.session_state.calc_expression = st.session_state.calc_expression + "7"
                    mg['lable_show_cal'].set(mg['expression'])
                    st.rerun()
            with c2:
                if st.button("ปุ่ม [ + ]"):
                    mg['expression'] = st.session_state.calc_expression = st.session_state.calc_expression + "+"
                    mg['lable_show_cal'].set(mg['expression'])
                    st.rerun()
            with c3:
                if st.button("ปุ่ม [ = ]"):
                    # ลองจำลองรันฟังก์ชัน equal() ที่ผู้เรียนเขียน
                    try:
                        # สร้าง context สำหรับทำงานกับฟังก์ชันผู้เรียน
                        globals_env = {'expression': st.session_state.calc_expression, 'lable_show_cal': mg['lable_show_cal'], 'eval': eval, 'str': str}
                        exec("def equal():\n    try:\n        global expression\n        global lable_show_cal\n        result = str(eval(expression))\n        lable_show_cal.set(result)\n    except:\n        result = 'error'\n    lable_show_cal.set(result)\n\nequal()", globals_env)
                    except:
                        st.session_state.calc_display = "error"
                    st.rerun()
            with c4:
                if st.button("ปุ่ม [ Clear ]", type="primary"):
                    st.session_state.calc_expression = ""
                    st.session_state.calc_display = "0"
                    st.rerun()
        st.caption("ℹ️ ระบบด้านบนเป็นการดึงฟังก์ชัน `press`, `clear`, `equal` จากโค้ดคุณมาทดลองทดสอบการประมวลผลจริง")

    # ==========================================
    # ส่วนที่ 2: ระบบตรวจคะแนน (Auto Grader)
    # ==========================================
    st.write("---")
    st.subheader("🎯 ผลการตรวจโครงสร้างโค้ด")
    
    if check_button:
        score = 0
        total_checks = 6
        feedback = []
        
        clean_code = user_code.replace(" ", "").replace("'", '"')
        
        if "defclear()" in clean_code and "defpress(number):" in clean_code and "defequal():" in clean_code:
            feedback.append("✅ โครงสร้างฟังก์ชันลอจิก `clear`, `press`, และ `equal` ครบถ้วน")
            score += 1
        else:
            feedback.append("❌ ฟังก์ชันลอจิกไม่ครบถ้วน (ต้องมี clear(), press(number) และ equal())")
            
        if "eval(expression)" in clean_code and "except:" in clean_code:
            feedback.append("✅ มีการใช้ `eval()` และระบบ `try-except` ดักจับ Error ได้ถูกต้อง")
            score += 1
        else:
            feedback.append("❌ ฟังก์ชัน equal() ควรมีระบบ `try-except` และใช้ `eval(expression)`")
            
        if "m=Tk()" in clean_code and 'm.title("Calculatorfrompython")' in clean_code:
            feedback.append("✅ สร้างหน้าต่าง `m` และตั้งชื่อ Title ถูกต้อง")
            score += 1
        else:
            feedback.append("❌ หน้าต่างหลัก `Tk()` หรือชื่อ Title ไม่ถูกต้อง")
            
        if "Label(m,textvariable=lable_show_cal).grid" in clean_code:
            feedback.append("✅ สร้างหน้าจอแสดงผล `Label` และผูกกับ `lable_show_cal` ถูกต้อง")
            score += 1
        else:
            feedback.append("❌ ไม่พบการสร้าง `Label` ที่ผูกกับ `textvariable=lable_show_cal`")

        has_buttons = True
        if 'text="clear",command=clear' not in clean_code: has_buttons = False
        if 'text="7",command=lambda:press("7")' not in clean_code: has_buttons = False
        if 'text="+",command=lambda:press("+")' not in clean_code: has_buttons = False
        if 'text="=",command=equal' not in clean_code: has_buttons = False
            
        if has_buttons:
            feedback.append("✅ ปุ่มตัวเลข ปุ่มเครื่องหมายสำคัญ และการใช้ Lambda ถูกต้องครบบริบูรณ์")
            score += 1
        else:
            feedback.append("❌ ปุ่มกดบางปุ่มหรือการตั้งค่า `command=lambda: press(...)` ยังไม่ถูกต้องตามรูปแบบ")

        if "m.mainloop()" in clean_code:
            feedback.append("✅ มีการสั่งรันโปรแกรมปิดท้ายด้วย `m.mainloop()`")
            score += 1
        else:
            feedback.append("❌ อย่าลืมใส่ `m.mainloop()` ที่บรรทัดสุดท้ายเพื่อสั่งให้ GUI ทำงาน")
            
        if score == total_checks:
            st.success(f"🎉 ยอดเยี่ยมมาก! โค้ดถูกต้องสมบูรณ์ ได้ {score}/{total_checks} คะแนน")
            st.balloons()
        else:
            st.warning(f"💡 คะแนนการเขียนโครงสร้างของคุณคือ: {score}/{total_checks}")
            
        for item in feedback:
            st.write(item)
