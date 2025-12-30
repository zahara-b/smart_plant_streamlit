import streamlit as st

# بررسی لاگین بودن کاربر
if "user_role" not in st.session_state:
    st.error("برای دسترسی به این صفحه، لطفاً ابتدا از صفحه اصلی وارد شوید.")
    st.stop()

st.set_page_config(page_title="جزئیات مخازن", page_icon="🛢️", layout="wide")
st.title("🛢️ جزئیات دقیق مخازن")

selected_tank = st.selectbox("یک مخزن را برای مشاهده جزئیات انتخاب کنید", options=list(st.session_state.tanks.keys()))
data = st.session_state.tanks[selected_tank]

st.header(f"وضعیت فعلی '{selected_tank}'")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("سطح مواد", f"{data['level']:.1f} %")
with col2:
    st.metric("دما", f"{data['temp']:.1f} °C")
with col3:
    if 'ffa' in data:
        st.metric("اسیدیته (FFA)", f"{data['ffa']:.2f}")
    else:
        st.info("پارامتر FFA برای این مخزن تعریف نشده.")

st.progress(int(data['level']))

st.subheader("نمودار تاریخچه این مخزن")
if not st.session_state.history.empty:
    tank_history = st.session_state.history[st.session_state.history['tank'] == selected_tank]
    if not tank_history.empty:
        chart_data = tank_history.pivot(index='timestamp', columns='metric', values='value').tail(100)
        st.line_chart(chart_data)
    else:
        st.info("هنوز داده‌ای برای این مخزن در تاریخچه ثبت نشده است.")
else:
    st.info("داده‌ای در تاریخچه وجود ندارد. لطفاً از سایدبار داده‌ها را ثبت کنید.")



### **۳. کد کامل فایل `pages/2_Production_Line.py`**


import streamlit as st

# بررسی لاگین بودن کاربر
if "user_role" not in st.session_state:
    st.error("برای دسترسی به این صفحه، لطفاً ابتدا از صفحه اصلی وارد شوید.")
    st.stop()

st.set_page_config(page_title="خط تولید", page_icon="🔧", layout="wide")
st.title("🔧 مانیتورینگ خط تولید")

data = st.session_state.production_line

st.header("وضعیت لحظه‌ای تجهیزات")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("نرخ جریان", f"{data['flow_rate']:.1f} L/min")
with col2:
    st.metric("فشار خط", f"{data['pressure']:.1f} bar", delta=f"{data['pressure'] - 3.5:.1f}")
with col3:
    st.metric("تعداد بسته‌بندی شده", f"{data['units_packaged']} عدد")

if data['pressure'] > 2.0:
    st.success("وضعیت پمپ‌ها: نرمال")
else:
    st.error("وضعیت پمپ‌ها: فشار پایین! نیاز به بازبینی دارد.")