import streamlit as st
import pandas as pd

# بررسی لاگین بودن کاربر
if "user_role" not in st.session_state:
    st.error("برای دسترسی به این صفحه، لطفاً ابتدا از صفحه اصلی وارد شوید.")
    st.stop()

st.set_page_config(page_title="تاریخچه هشدارها", page_icon="📜", layout="wide")
st.title("📜 تاریخچه و لاگ هشدارها")

if not st.session_state.alert_log:
    st.info("تاکنون هیچ هشداری ثبت نشده است.")
else:
    st.write("آخرین هشدارها در بالای لیست قرار دارند.")
    # تبدیل لیست به دیتافریم برای نمایش بهتر
    # **این خط اصلاح شد**
    log_df = pd.DataFrame(st.session_state.alert_log, columns=["پیام هشدار"])
    st.dataframe(log_df, use_container_width=True)