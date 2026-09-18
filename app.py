import streamlit as st

# =========================
# 页面基础设置
# =========================
st.set_page_config(
    page_title="Shopee MY Listing Optimizer",
    page_icon="✨",
    layout="wide"
)

# =========================
# 页面样式
# =========================
st.markdown("""
<style>

/* 页面背景 */
.stApp {
    background-color: #F7F4EC;
}

/* 主页面最大宽度 */
.block-container {
    max-width: 1400px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* 顶部品牌 */
.brand {
    font-size: 14px;
    letter-spacing: 2px;
    color: #315F50;
    font-weight: 600;
    margin-bottom: 5px;
}

/* 主标题 */
.main-title {
    font-size: 42px;
    font-weight: 800;
    color: #174C3C;
    margin-bottom: 5px;
}

/* 副标题 */
.subtitle {
    color: #6E746F;
    font-size: 16px;
    margin-bottom: 25px;
}

/* 顶部横幅 */
.hero {
    background: #FFF0C8;
    border: 3px solid #245C4B;
    border-radius: 32px;
    padding: 35px 30px;
    text-align: center;
    margin-bottom: 30px;
    box-shadow: 0px 8px 0px rgba(36, 92, 75, 0.10);
}

.hero-title {
    color: #174C3C;
    font-size: 38px;
    font-weight: 800;
    margin: 0;
}

/* 区域标题 */
.section-title {
    font-size: 23px;
    font-weight: 750;
    color: #244F42;
    margin-bottom: 15px;
}

/* 输出区域 */
.output-box {
    background: #FFFFFF;
    border: 1px solid #E2DED4;
    border-radius: 18px;
    padding: 22px;
    min-height: 550px;
}

/* 等待生成状态 */
.empty-result {
    text-align: center;
    padding-top: 150px;
    color: #7C827E;
}

.empty-icon {
    font-size: 45px;
    margin-bottom: 12px;
}

.empty-title {
    font-size: 21px;
    font-weight: 700;
    color: #315F50;
}

/* 按钮 */
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
    border: none;
}

/* 输入框圆角 */
.stTextInput input,
.stTextArea textarea {
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)


# =========================
# 顶部
# =========================

st.markdown(
    '<div class="brand">MY AI COMMERCE · MALAYSIA</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="main-title">Shopee MY Listing Optimizer</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">中文输入，一键生成自然、清晰的英文商品内容</div>',
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
# 左右两栏
# =========================

left, right = st.columns([1, 1.1], gap="large")


# =========================
# 左侧：产品信息
# =========================

with left:

    st.markdown(
        '<div class="section-title">01 · 产品信息</div>',
        unsafe_allow_html=True
    )

    product_title = st.text_input(
        "中文商品标题 *",
        placeholder="例如：桌面手机充电线电源线整理收纳盒"
    )

    product_info = st.text_area(
        "中文产品描述 / 属性 *",
        placeholder="""例如：

材质：PP
颜色：奶油白
尺寸：小号 / 大号
用途：桌面电线收纳
特点：防尘、隐藏插排、多孔出线""",
        height=190
    )

    store_template = st.text_area(
        "英文店铺基础模板",
        value="""✨ WELCOME TO OUR STORE ✨

Discover practical and stylish products designed to make everyday life easier, tidier, and more comfortable.

🌿 Thoughtful Designs
🌿 Quality You Can Trust
🌿 Style for Every Space

Thank you for supporting our store.""",
        height=190
    )

    platform = st.selectbox(
        "目标平台",
        [
            "Shopee Malaysia",
            "TikTok Shop Malaysia"
        ]
    )

    style = st.selectbox(
        "Listing 风格",
        [
            "SEO关键词优先",
            "自然简洁",
            "卖点突出"
        ]
    )

    uploaded_images = st.file_uploader(
        "上传商品图片（后续加入AI图片英文化）",
        type=["jpg", "jpeg", "png", "webp"],
        accept_multiple_files=True
    )

    generate = st.button(
        "✨ 生成优化结果",
        use_container_width=True
    )


# =========================
# 右侧：优化结果
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
                <div class="empty-icon">✦</div>
                <div class="empty-title">
                    准备好优化您的 Listing
                </div>
                <p>
                    填写左侧产品信息，AI 将生成英文标题、
                    关键词、卖点与完整商品描述。
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    else:

        if not product_title or not product_info:

            st.warning(
                "请先填写中文商品标题和产品描述 / 属性。"
            )

        else:

            st.success("页面运行成功！下一步我们接入 AI。")

            st.subheader("English Product Title")
            st.info(
                "AI 接入后，这里会自动生成 Shopee / TikTok 英文标题。"
            )

            st.subheader("Core Keywords")
            st.write(
                "Keyword 1 · Keyword 2 · Keyword 3 · Keyword 4"
            )

            st.subheader("Selling Points")
            st.write("""
• Selling Point 1  
• Selling Point 2  
• Selling Point 3  
• Selling Point 4
""")

            st.subheader("Product Description")
            st.write(
                "AI 接入后，这里会根据你的中文商品资料自动生成完整英文详情。"
            )

            st.subheader("Specifications")
            st.write(
                "Material / Size / Colour / Package / Usage"
            )

            st.subheader("Variations")
            st.write(
                "AI 将根据商品信息自动整理规格名称。"
            )


# =========================
# 页脚
# =========================

st.markdown("---")

st.caption(
    "AI Listing Optimizer · Shopee MY / TikTok Shop MY"
)
