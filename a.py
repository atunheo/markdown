import streamlit as st
import pandas as pd
import markdown
import html
from io import BytesIO

st.set_page_config(page_title="Markdown Excel Converter", page_icon="📘", layout="centered")

st.title("📘 Markdown Excel Converter (Giữ hyperlink)")

st.write("""chỉ có heo lười ở đây""")

uploaded_file = st.file_uploader("📂 Chọn file Excel", type=["xlsx", "xls"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file, dtype=str)
    if 'content' not in df.columns:
        st.error("❌ File Excel phải có cột 'content'.")
    else:
        contents = df['content'].dropna().tolist()
        st.success(f"✅ Đã tải {len(contents)} bài từ Excel.")

        # Chọn bài cần xem
        index = st.number_input("Chọn bài", min_value=1, max_value=len(contents), value=1, step=1)
        md_text = contents[index - 1]

        # Chuyển Markdown → HTML
        html_text = markdown.markdown(md_text, extensions=['extra', 'sane_lists'])

        # Hiển thị preview
        st.markdown("### 🔍 Preview (có hyperlink)")
        st.markdown(html_text, unsafe_allow_html=True)

        # Hiển thị mã HTML (ẩn trong expander)
        with st.expander("Xem mã HTML gốc"):
            st.code(html_text, language="html")

        # Nút copy HTML (trình duyệt)
        copy_script = f"""
        <script>
        function copyToClipboard() {{
            navigator.clipboard.writeText(`{html.escape(html_text)}`);
            alert("✅ Đã copy HTML vào clipboard! Dán vào Google Sites (Rich Text) để hiển thị hyperlink.");
        }}
        </script>
        <button onclick="copyToClipboard()" style="
            background-color:#4CAF50;color:white;padding:10px 20px;
            border:none;border-radius:5px;cursor:pointer;">
            📋 Copy bài này
        </button>
        """
        st.components.v1.html(copy_script, height=80)

else:
    st.info("⬆️ Hãy tải file Excel để bắt đầu.")
