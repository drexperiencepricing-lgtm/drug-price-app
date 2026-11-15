import pandas as pd
import streamlit as st

st.set_page_config(page_title="برنامج فرز وبحث أسعار الوكلاء", layout="wide")

st.title("📊 برنامج فرز وبحث أسعار الوكلاء والأصناف")
st.write(
    "قم باختيار الوكيل لعرض أصنافه، ثم أدخل السعر اليدوي لمقارنته بنسبة الارتفاع"
    " أو الانخفاض."
)


@st.cache_data
def load_data():
  return pd.read_excel(
      "المسجلة_والمدرحة_المرسلة_من_اداراة_الكمبوتر_نسخة_د_امين_ج.xlsx"
  )


try:
  df = load_data()
  agents = df["الوكيل"].dropna().unique()
  selected_agent = st.selectbox("اختر اسم الوكيل:", agents)

  filtered_df = df[df["الوكيل"] == selected_agent].copy()

  if not filtered_df.empty:
    st.success(f"تم العثور على {len(filtered_df)} صنف للوكيل: {selected_agent}")

    for index, row in filtered_df.iterrows():
      with st.container():
        col1, col2, col3 = st.columns([3, 2, 2])

        with col1:
          st.markdown(
              f"**الصنف:** {row.get('الاسم التجاري', 'غير متوفر')} |"
              f" **التركيز:** {row.get('التركيز', '')}"
          )
          st.markdown(
              f"<small>الكود: {row.get('الكود', '')} | العبوة:"
              f" {row.get('العبوة', '')}</small>",
              unsafe_allow_html=True,
          )

        with col2:
          raw_price = str(row.get("سعر الاستيراد", "0"))
          try:
            original_price = float(
                "".join([c for c in raw_price if c.isdigit() or c == "."])
            )
          except:
            original_price = 0.0

          st.text(f"سعر الاكسل: {raw_price}")
          manual_price = st.number_input(
              "السعر اليدوي الجديد",
              min_value=0.0,
              value=0.0,
              step=0.1,
              key=f"manual_{index}",
          )

        with col3:
          if manual_price > 0 and original_price > 0:
            diff = manual_price - original_price
            pct = (diff / original_price) * 100
            if pct > 0:
              st.error(f"🔺 ارتفاع: {pct:.2f}% (+{diff:.2f})")
            elif pct < 0:
              st.success(f"🔻 انخفاض: {abs(pct):.2f}% ({diff:.2f})")
            else:
              st.info("➖ السعر مطابق تماماً")
          else:
            st.write("أدخل السعر للمقارنة")

        st.markdown("---")

    if st.button("🖨️ طباعة الصفحة / حفظ كملف PDF"):
      st.markdown(
          "<script>window.print();</script>", unsafe_allow_html=True
      )

  else:
    st.warning("لا توجد أصناف مسجلة لهذا الوكيل.")

except Exception as e:
  st.error(
      f"حدث خطأ في تحميل الملف. تأكد من وجود ملف الاكسل في نفس المجلد. الخطأ:"
      f" {e}"
  )
