import streamlit as st
from google import genai

st.set_page_config(
    page_title="Shopee MY Listing Optimizer",
    page_icon="✨",
    layout="wide"
)

# =========================
# Gemini
# =========================

client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# =========================
# CSS
# =========================

st.markdown("""
<style>

.stApp {
    background-color: #F7F4EC;
}

.block-container {
    max-width: 1400px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

.brand {
    font-size: 14px;
    letter-spacing: 2px;
    color: #315F50;
    font-weight: 600;
}

.main-title {
    font-size: 42px;
    font-weight: 800;
    color: #174C3C;
    margin-bottom: 3px;
}

.subtitle {
    color: #6E746F;
    font-size: 16px;
    margin-bottom: 25px;
}

.hero {
    background: #FFF0C8;
    border: 3px solid #245C4B;
    border-radius: 32px;
    padding: 35px 30px;
    text-align: center;
    margin-bottom: 30px;
    box-shadow: 0px 8px 0px rgba(36,92,75,0.10);
}

.hero-title {
    color: #174C3C;
    font-size: 38px;
    font-weight: 800;
}

.section-title {
    font-size: 23px;
    font-weight: 750;
    color: #244F42;
    margin-bottom: 15px;
}

.output-box {
    background: white;
    border: 1px solid #E2DED4;
    border-radius: 18px;
    padding: 25px;
    min-height: 600px;
}

.empty-result {
    text-align: center;
    padding-top: 180px;
    color: #7C827E;
}

.empty-title {
    font-size: 21px;
    font-weight: 700;
    color: #315F50;
}

.stButton > button {
    width: 100%;
    border-radius: 12px;
    height: 48px;
    background-color: #3E8C70;
    color: white;
    font-weight: 700;
    border: none;
}

.stButton > button:hover {
    background-color: #32745D;
    color: white;
}

</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================

st.markdown(
    '<div class="brand">AI COMMERCE · MALAYSIA</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="main-title">Shopee MY Listing Optimizer</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">中文输入，快速生成适合马来西亚市场的英文商品内容</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="hero">
<div class="hero-title">
AI 商品上架助手 ✨
</div>
</div>
""", unsafe_allow_html=True)

# =========================
# 页面布局
# =========================

left, right = st.columns([1, 1.1], gap="large")

with left:

    st.markdown(
        '<div class="section-title">01 · 产品信息</div>',
        unsafe_allow_html=True
    )

    product_title = st.text_input(
        "中文商品标题 *",
        placeholder="直接复制1688商品标题"
    )

    product_info = st.text_area(
        "中文产品描述 / 属性 *",
        placeholder="""例如：

产品名称：
材质：
尺寸：
颜色：
功能：
包装数量：
适用场景：
其他卖点：""",
        height=220
    )

    store_template = st.text_area(
        "英文店铺基础模板",
        value="""✨ WELCOME TO OUR STORE ✨

Discover practical and stylish products designed to make everyday life easier.

🌿 Thoughtful Designs
🌿 Quality You Can Trust
🌿 Style for Every Space

Thank you for supporting our store.""",
        height=180
    )

    platform = st.selectbox(
        "目标平台",
        [
            "Shopee Malaysia",
            "TikTok Shop Malaysia"
        ]
    )

    listing_style = st.selectbox(
        "Listing 风格",
        [
            "SEO关键词优先",
            "自然简洁",
            "卖点突出"
        ]
    )

    uploaded_images = st.file_uploader(
        "上传商品图片",
        type=["jpg", "jpeg", "png", "webp"],
        accept_multiple_files=True,
        help="图片AI处理功能下一阶段加入"
    )

    generate = st.button(
        "✨ 生成优化结果",
        use_container_width=True
    )


# =========================
# 右侧
# =========================

with right:

    st.markdown(
        '<div class="section-title">02 · 优化结果</div>',
        unsafe_allow_html=True
    )

    if not generate:

        st.markdown("""
        <div class="output-box">
            <div class="empty-result">
                <div style="font-size:45px;">✦</div>
                <div class="empty-title">
                准备好优化您的 Listing
                </div>
                <p>
                填写左侧商品信息，AI 将生成标题、关键词、
                卖点与完整英文商品描述。
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    else:

        if not product_title or not product_info:

            st.warning("请填写商品标题和产品描述 / 属性。")

        else:

            prompt = f"""
You are an experienced Southeast Asian e-commerce listing specialist.

Your task is to create a high-quality English product listing for:

Platform: {platform}
Market: Malaysia
Listing style: {listing_style}

SOURCE PRODUCT TITLE:
{product_title}

SOURCE PRODUCT INFORMATION:
{product_info}

STORE TEMPLATE:
{store_template}

IMPORTANT RULES:

1. Never invent product specifications, materials, dimensions,
   functions, certifications, quantities or features.

2. If information is missing, omit it or mark it as
   [Need Confirmation].

3. Translate naturally rather than word-for-word.

4. Use English search terminology that Malaysian shoppers
   are likely to understand.

5. Prioritize high-intent product keywords.

6. Do not use misleading or exaggerated claims such as:
   "No.1", "Best", "100% guaranteed", "perfect",
   unless explicitly supported by the source information.

7. Keep the title readable.
   Do not spam or repeat keywords unnecessarily.

8. Preserve important product attributes such as:
   product type, material, size, colour, quantity,
   application and compatibility.

9. Do not fabricate information based on assumptions.

OUTPUT EXACTLY USING THIS STRUCTURE:

### English Product Title

[Optimized English title]

### Core Search Keywords

- keyword
- keyword
- keyword
- keyword
- keyword

### Selling Points

- selling point
- selling point
- selling point
- selling point
- selling point

### Product Description

[Complete natural English description]

### Specifications

Product Name:
Material:
Colour:
Size:
Quantity:
Application:

Only include specifications supported by the source.

### Variations

[List recommended variation names based only on supplied information]

### Information To Confirm

[List any important missing or ambiguous information that should be
confirmed before publishing.]

### Store Message

{store_template}
"""

            try:

                with st.spinner(
                    "AI 正在分析商品并生成 Listing..."
                ):

                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=prompt
                    )

                st.success("Listing 生成完成 ✨")

                st.markdown(
                    '<div class="output-box">',
                    unsafe_allow_html=True
                )

                st.markdown(response.text)

                st.markdown(
                    '</div>',
                    unsafe_allow_html=True
                )

            except Exception as e:

                st.error("生成失败。")

                st.code(str(e))

                st.info(
                    "如果出现错误，把这里显示的错误内容截图给我。"
                )


st.markdown("---")

st.caption(
    "AI Listing Optimizer · Shopee MY / TikTok Shop MY"
)
