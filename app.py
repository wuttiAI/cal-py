import streamlit as st
import re

# ตั้งค่าหน้าเว็บให้แสดงผลแบบกว้าง (Wide mode)
st.set_page_config(page_title="Tkinter Coding Challenge", layout="wide")

st.title("🖥️ บทเรียนฝึกเขียนโค้ด: Tkinter GUI เบื้องต้น")
st.write("ให้นักเรียนศึกษาโค้ดจากภาพตัวอย่าง แล้วพิมพ์ซี้อโค้ดให้ถูกต้องเพื่อผ่านภารกิจ")

# แบ่งหน้าจอเป็น 2 ฝั่ง (ซ้าย: โจทย์และช่องพิมพ์โค้ด | ขวา: ผลลัพธ์และการตรวจคำตอบ)
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📝 โจทย์และภาพตัวอย่าง")
    # แนะนำให้ผู้อ่านนำภาพตัวอย่างไปใส่ใน GitHub repo เดียวกัน แล้วเปลี่ยนชื่อไฟล์ตรงนี้
    # หรือจะใช้คำอธิบายโค้ดด้านล่างนี้แทนก็ได้ครับ
    st.markdown("""
    **คำสั่ง:** จงเติมโค้ดสร้างหน้าต่าง GUI ด้วย `tkinter` ที่มีคุณสมบัติดังนี้:
    1. มีฟังก์ชัน `press(n)` เพื่อเพิ่มตัวเลขและแสดงผลบน Label
    2. มีหน้าต่างหลักชื่อ `m` พร้อมหัวข้อ `'Main window'`
    3. มีปุ่มเลข `1`, `2`, `3`, `4` และปุ่ม `Stop` สำหรับปิดโปรแกรม
    """)
    
    # โค้ดตั้งต้น (หรือจะปล่อยว่างไว้ให้เติมเองทั้งหมดก็ได้)
    default_code = """import tkinter as tk

def press(n):
    global expression
    global labellText
    expression = expression + n
    labellText.set(expression)

m = tk.Tk()
m.title('Main window')

expression = ''
labellText = tk.StringVar()
labellText.set(expression)

# ---- เริ่มเขียนโค้ดสร้าง Label และ Button ต่อจากตรงนี้ ----

"""
    
    # ช่องสำหรับให้ผู้เรียนพิมพ์โค้ด
    user_code = st.text_area("✍️ พิมพ์โค้ด Python ของคุณที่นี่:", value=default_code, height=450)
    check_button = st.button("🚀 ส่งคำตอบ / ตรวจสอบโค้ด")

with col2:
    st.subheader("🎯 สถานะการตรวจคำตอบ (Grader Output)")
    
    if check_button:
        # ระบบตรวจคำตอบอัตโนมัติโดยการเช็ค Keyword และโครงสร้างโค้ด (Code Linting)
        score = 0
        total_checks = 5
        feedback = []
        
        # 1. ตรวจสอบการสร้าง Label
        if "tk.Label" in user_code and "textvariable=labellText" in user_code:
            feedback.append("✅ สร้าง `labell` พร้อมผูก `textvariable` ถูกต้อง")
            score += 1
        else:
            feedback.append("❌ ไม่พบการสร้าง `tk.Label` หรือลืมใส่ `textvariable=labellText`")
            
        # 2. ตรวจสอบการจัดวาง Grid ของ Label
        if re.search(r"labell\.grid\(.*row=0.*columnspan=2.*\)", user_code.replace(" ", "")):
            feedback.append("✅ จัดวางตำแหน่ง `labell.grid` แถวที่ 0 และควบ 2 คอลัมน์ถูกต้อง")
            score += 1
        else:
            feedback.append("❌ การตั้งค่า `labell.grid(row=0, columnspan=2)` ยังไม่ถูกต้อง")
            
        # 3. ตรวจสอบปุ่มกด (ตัวอย่างเช็คปุ่ม 1 และปุ่ม Stop)
        if "text='1'" in user_code and "command=lambda:press('1')" in user_code.replace(" ", ""):
            feedback.append("✅ สร้างปุ่ม Button 1 พร้อมระบบส่งค่า Lambda ถูกต้อง")
            score += 1
        else:
            feedback.append("❌ ปุ่ม Button 1 หรือคำสั่ง `command=lambda: press('1')` ยังไม่ถูกต้อง")
            
        if "text='Stop'" in user_code and "m.destroy" in user_code:
            feedback.append("✅ สร้างปุ่ม Stop และคำสั่งปิดหน้าต่าง (`m.destroy()`) ถูกต้อง")
            score += 1
        else:
            feedback.append("❌ ไม่พบปุ่ม 'Stop' หรือคำสั่งปิดหน้าต่าง `m.destroy()`")
            
        # 4. ตรวจสอบการสั่ง Run Mainloop
        if "m.mainloop()" in user_code.replace(" ", ""):
            feedback.append("✅ มีการปิดท้ายด้วย `m.mainloop()` เพื่อรันโปรแกรม")
            score += 1
        else:
            feedback.append("❌ อย่าลืมใส่คำสั่ง `m.mainloop()` ที่บรรทัดสุดท้าย")
            
        # แสดงผลสรุปคะแนน
        st.write("---")
        if score == total_checks:
            st.success(f"🎉 ยอดเยี่ยมมาก! คุณทำคะแนนได้ {score}/{total_checks} คะแนน โค้ดถูกต้องสมบูรณ์")
            st.balloons()
        else:
            st.warning(f"💡 พยายามอีกนิด! คะแนนของคุณ: {score}/{total_checks}")
            
        # แสดงรายละเอียดผลการตรวจ
        for item in feedback:
            st.write(item)
            
    else:
        st.info("ℹ️ เมื่อพิมพ์โค้ดเสร็จแล้ว ให้กดปุ่ม 'ส่งคำตอบ' ด้านล่างซ้ายเพื่อตรวจคะแนน")
