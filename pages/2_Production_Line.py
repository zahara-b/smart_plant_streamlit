import streamlit as st

if "user_role" not in st.session_state:
    st.error("برای دسترسی به این صفحه، لطفاً ابتدا از صفحه اصلی وارد شوید.")
    st.stop() # اجرای بقیه کد این صفحه را متوقف می‌کند

st.set_page_config(page_title="خط تولید", page_icon="🔧")
st.title("🔧 مانیتورینگ خط تولید")

if 'production_line' not in st.session_state:
    st.warning("لطفاً ابتدا از صفحه اصلی برنامه را اجرا کنید.")
    st.stop()

data = st.session_state.production_line

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("نرخ جریان", f"{data['flow_rate']:.1f} L/min")
with col2:
    st.metric("فشار خط", f"{data['pressure']:.1f} bar")
with col3:
    st.metric("تعداد بسته‌بندی شده", f"{data['units_packaged']} عدد")

if data['pressure'] > 2.0:
    st.success("وضعیت پمپ‌ها: نرمال")
else:
    st.error("وضعیت پمپ‌ها: فشار پایین!")