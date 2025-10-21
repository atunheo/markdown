import streamlit as st
import pandas as pd
import markdown
import html

st.set_page_config(
    page_title="Markdown Excel Converter",
    page_icon="📘",
    layout="centered"
)

st.title("📘 Markdown Excel Converter (Giữ hyperlink)")

st.markdown("""
Ứng dụng này giúp bạn:
1. Tải file **Excel** (1 cột **content** chứa Markdown).  
2. Chuyển Markdown → HTML có hyperlink (giống Markdown Live Preview).  
3. Xem trước từng bài, nhấn **📋 Copy bài này** để sao chép vào clipboard.  
4. Dán (Ctrl + V) vào **Google Sites** ở chế độ *Rich Text* để giữ hyperlink.
---
""")

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
        st.warning("⚠️ Không tìm thấy nội dung Markdown nào trong cột 'content'.")
        st.stop()

    st.success(f"✅ Đã tải {len(contents)} bài từ Excel.")

    # Chọn bài muốn xem
    index = st.number_input(
        "Chọn bài cần xem",
        min_value=1,
        max_value=len(contents),
        value=1,
        step=1
    )
    md_text = contents[index - 1]

    # Chuyển Markdown → HTML
    html_text = markdown.markdown(md_text, extensions=["extra", "sane_lists"])

    # Hiển thị preview (HTML thực)
    st.markdown("### 🔍 Preview (giữ hyperlink)")
    st.markdown(html_text, unsafe_allow_html=True)

    # Mã HTML (ẩn trong expander)
    with st.expander("Xem mã HTML"):
        st.code(html_text, language="html")

    # Nút Copy
    st.markdown("### 📋 Sao chép bài viết này")
    escaped_html = html.escape(html_text).replace("\n", " ")
    copy_button = f"""
    <button onclick="navigator.clipboard.writeText(`{escaped_html}`);
    alert('✅ Đã copy bài này! Dán (Ctrl + V) vào Google Sites ở chế độ Rich Text.');"
    style="background-color:#4CAF50;color:white;padding:10px 20px;border:none;
    border-radius:5px;cursor:pointer;font-size:16px;">
    📋 Copy bài này
    </button>
    """
    st.components.v1.html(copy_button, height=100)

else:
    st.info("⬆️ Hãy tải file Excel để bắt đầu.")
