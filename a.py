import streamlit as st
import pandas as pd
import markdown
import html

# Cấu hình trang
st.set_page_config(
    page_title="Markdown Excel Converter (Local)",
    page_icon="📘",
    layout="centered"
)

st.title("📘 Markdown Excel Converter (Chạy Local)")

st.markdown("""
Ứng dụng giúp bạn:
1. Chọn file **Excel** có cột `content` chứa Markdown.  
2. Tự động chuyển Markdown → HTML có hyperlink.  
3. Xem trước từng bài viết.  
4. Nhấn **📋 Copy bài này** để copy nội dung ra clipboard.  
5. Sau đó dán vào **Google Sites (Rich Text)** để hiển thị đúng hyperlink.
---
""")

# Upload file Excel
uploaded_file = st.file_uploader("📂 Chọn file Excel", type=["xlsx", "xls"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file, dtype=str)
    except Exception as e:
        st.error(f"Không thể đọc file Excel: {e}")
        st.stop()

    if 'content' not in df.columns:
        st.error("❌ File Excel phải có cột 'content'.")
        st.stop()

    contents = df['content'].dropna().tolist()

    if not contents:
        st.warning("⚠️ Không có nội dung Markdown nào trong cột 'content'.")
        st.stop()

    st.success(f"✅ Đã tải {len(contents)} bài từ Excel.")

    # Chọn bài để xem
    index = st.number_input(
        "Chọn bài muốn xem:",
        min_value=1,
        max_value=len(contents),
        value=1,
        step=1
    )
    md_text = contents[index - 1]

    # Markdown -> HTML
    html_text = markdown.markdown(md_text, extensions=["extra", "sane_lists"])

    # Hiển thị bài viết
    st.markdown("### 🔍 Preview (giữ hyperlink)")
    st.markdown(html_text, unsafe_allow_html=True)

    # Hiển thị mã HTML nếu cần
    with st.expander("📂 Xem mã HTML gốc"):
        st.code(html_text, language="html")

    # Nút copy (JS trong trình duyệt)
    st.markdown("### 📋 Sao chép HTML bài viết này")
    escaped_html = html.escape(html_text).replace("\n", " ")
    copy_button = f"""
    <button onclick="navigator.clipboard.writeText(`{escaped_html}`);
    alert('✅ Đã copy bài này vào clipboard! Hãy dán (Ctrl + V) vào Google Sites (Rich Text).');"
    style="background-color:#4CAF50;color:white;padding:10px 20px;border:none;
    border-radius:5px;cursor:pointer;font-size:16px;">
    📋 Copy bài này
    </button>
    """
    st.components.v1.html(copy_button, height=100)

else:
    st.info("⬆️ Hãy chọn file Excel để bắt đầu.")
