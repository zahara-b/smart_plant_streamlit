import streamlit as st
import pandas as pd
import datetime

# --- ۱. سیستم لاگین و احراز هویت ---
def check_password():
    """تابع برای نمایش فرم لاگین و بررسی رمز عبور."""
    if "user_role" in st.session_state:
        return True

    st.set_page_config(page_title="ورود به سیستم", layout="centered")
    st.title("🏭 ورود به سیستم مدیریت کارخانه")
    
    username = st.text_input("نام کاربری", key="username_input")
    password = st.text_input("رمز عبور", type="password", key="password_input")
    
    st.info("راهنمایی: `manager`/`123` یا `seller`/`456`")

    if st.button("ورود", key="login_button"):
        if username.lower() == "manager" and password == "123":
            st.session_state.user_role = "مدیر تولید"
            st.rerun()
        elif username.lower() == "seller" and password == "456":
            st.session_state.user_role = "مدیر فروش"
            st.rerun()
        else:
            st.error("نام کاربری یا رمز عبور اشتباه است.")
    
    return False

# اگر کاربر لاگین نکرده باشد، بقیه برنامه را متوقف کن
if not check_password():
    st.stop()

# --- ۲. تنظیمات صفحه و مقداردهی اولیه (بعد از لاگین موفق) ---
st.set_page_config(
    page_title="داشبورد اصلی",
    page_icon="🏭",
    layout="wide",
)

def initialize_state():
    """مقداردهی اولیه داده‌های برنامه در Session State."""
    if 'initialized' not in st.session_state:
        st.session_state.initialized = True
        st.session_state.tanks = {
            "مخزن ۱ (روغن خام)": {"level": 75.0, "temp": 45.0, "ffa": 0.8},
            "مخزن ۲ (روغن تصفیه شده)": {"level": 90.0, "temp": 55.0, "ffa": 0.1},
            "مخزن ۳ (افزودنی ویتامین)": {"level": 50.0, "temp": 25.0, "ffa": 0.0},
        }
        st.session_state.production_line = {
            "flow_rate": 120.0, "pressure": 3.5, "units_packaged": 1502
        }
        st.session_state.history = pd.DataFrame(columns=['timestamp', 'tank', 'metric', 'value'])
        st.session_state.alert_log = []

initialize_state()

# --- ۳. سیستم خبره و توابع کمکی ---
def run_expert_system():
    alerts = []
    for name, data in st.session_state.tanks.items():
        if data['level'] < 20: alerts.append(f" سطح موجودی '{name}' بسیار پایین است ({data['level']:.1f}%)!")
        if data['temp'] > 70: alerts.append(f" دمای '{name}' بیش از حد بالاست ({data['temp']:.1f}°C)!")
        if "خام" in name and data['ffa'] > 1.0: alerts.append(f" اسیدیته (FFA) در '{name}' بالاست ({data['ffa']:.2f})!")
    if st.session_state.production_line['pressure'] < 2.0: alerts.append(f" فشار خط تولید پایین است! پمپ‌ها را بررسی کنید.")
    return alerts

def log_history():
    ts = datetime.datetime.now()
    new_rows = []
    for name, data in st.session_state.tanks.items():
        new_rows.append({'timestamp': ts, 'tank': name, 'metric': 'level', 'value': data['level']})
        new_rows.append({'timestamp': ts, 'tank': name, 'metric': 'temp', 'value': data['temp']})
    st.session_state.history = pd.concat([st.session_state.history, pd.DataFrame(new_rows)], ignore_index=True)

# --- ۴. طراحی رابط کاربری (UI) ---
with st.sidebar:
    st.success(f"خوش آمدید، **{st.session_state.user_role}**!")
    st.header("🕹️ شبیه‌ساز")
    
    st.subheader("کنترل مخازن")
    selected_tank = st.selectbox("انتخاب مخزن برای تغییر", options=list(st.session_state.tanks.keys()))
    tank_data = st.session_state.tanks[selected_tank]
    tank_data['level'] = st.slider("سطح مواد (%)", 0.0, 100.0, tank_data['level'], key=f"level_{selected_tank}")
    tank_data['temp'] = st.slider("دما (°C)", 20.0, 100.0, tank_data['temp'], key=f"temp_{selected_tank}")
    if "خام" in selected_tank:
        tank_data['ffa'] = st.slider("اسیدیته (FFA)", 0.0, 2.0, tank_data['ffa'], key=f"ffa_{selected_tank}")

    st.markdown("---")
    st.subheader("کنترل خط تولید")
    prod_data = st.session_state.production_line
    prod_data['pressure'] = st.slider("فشار خط (bar)", 0.0, 5.0, prod_data['pressure'], key="pressure_slider")
    prod_data['flow_rate'] = st.slider("نرخ جریان (L/min)", 50.0, 200.0, prod_data['flow_rate'], key="flow_rate_slider")
    
    if st.button("ثبت داده‌ها در تاریخچه"):
        log_history()
        st.toast("داده‌ها با موفقیت ثبت شدند!")

# --- داشبورد اصلی ---
current_alerts = run_expert_system()

if st.session_state.user_role == "مدیر تولید":
    st.title("🏭 داشبورد فنی مدیر تولید")
    if current_alerts:
        st.error(f"🚨 **{len(current_alerts)} هشدار فنی فعال وجود دارد!**")
        ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for alert in current_alerts:
            st.write(f"- {alert}")
            new_alert_log_entry = f"[{ts}] {alert}"
            if new_alert_log_entry not in st.session_state.alert_log:
                st.session_state.alert_log.insert(0, new_alert_log_entry)
    else:
        st.success("✅ وضعیت فنی مطلوب است.")
    
    st.markdown("---")
    st.subheader("KPI های فنی کلیدی")
    col1, col2, col3 = st.columns(3)
    prod_data = st.session_state.production_line
    col1.metric("فشار خط تولید", f"{prod_data['pressure']:.1f} bar", delta=f"{prod_data['pressure'] - 3.5:.1f} bar vs. Target")
    col2.metric("نرخ جریان", f"{prod_data['flow_rate']:.1f} L/min")
    col3.metric("اسیدیته روغن خام", f"{st.session_state.tanks['مخزن ۱ (روغن خام)']['ffa']:.2f} FFA")
    
    st.subheader("نمودار تاریخچه دما (آخرین ۱۰۰ رکورد)")
    if not st.session_state.history.empty:
        temp_history = st.session_state.history[st.session_state.history['metric'] == 'temp']
        chart_data = temp_history.pivot(index='timestamp', columns='tank', values='value').tail(100)
        st.line_chart(chart_data)

elif st.session_state.user_role == "مدیر فروش":
    st.title("📈 داشبورد مدیریتی مدیر فروش")
    st.info(f"تعداد هشدارهای فنی فعال در خط تولید: {len(current_alerts)}")
    
    st.markdown("---")
    finished_tank = st.session_state.tanks["مخزن ۲ (روغن تصفیه شده)"]
    total_capacity_liters = 5000 
    available_liters = finished_tank['level'] * total_capacity_liters / 100
    
    st.subheader("KPI های فروش و موجودی")
    col1, col2, col3 = st.columns(3)
    col1.metric("موجودی قابل فروش", f"{available_liters:,.0f} لیتر")
    col2.metric("محصول بسته‌بندی شده (امروز)", f"{st.session_state.production_line['units_packaged']} واحد")
    col3.metric("ظرفیت خالی انبار", f"{100 - finished_tank['level']:.1f} %")
    
    st.subheader("وضعیت کلی موجودی انبارها")
    for name, data in st.session_state.tanks.items():
        st.progress(int(data['level']), text=f"{name}: {data['level']:.1f}%")