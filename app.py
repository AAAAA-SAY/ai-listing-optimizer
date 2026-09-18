import streamlit as st
from google import genai
from google.genai import types

# =========================================================
# 页面设置
# =========================================================

st.set_page_config(
    page_title="Shopee MY Listing Optimizer",
    page_icon="✨",
    layout="wide"
)

# =========================================================
# Gemini API
# =========================================================

client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)

# =========================================================
# CSS 页面样式
# =========================================================

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
    margin-bottom: 5px;
}

.main-title {
    font-size: 42px;
    font-weight: 800;
    color: #174C3C;
    margin-bottom: 5px;
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
    box-shadow: 0px 8px 0px rgba(36, 92, 75, 0.10);
}

.hero-title {
    color: #174C3C;
    font-size: 38px;
    font-weight: 800;
    margin: 0;
}

.section-title {
    font-size: 23px;
    font-weight: 750;
    color: #244F42;
    margin-bottom: 15px;
}

.output-box {
    background: #FFFFFF;
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
    margin-top: 10px;
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
    border: none;
}

.stTextInput input,
.stTextArea textarea {
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# 页面顶部
# =========================================================

st.markdown(
    '<div class="brand">AI COMMERCE · MALAYSIA</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="main-title">Shopee MY Listing Optimizer</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">中文资料 / 商品图片输入，快速生成马来西亚站英文 Listing</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="hero">
    <div class="hero-title">
        AI 商品上架助手 ✨
    </div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# 左右布局
# =========================================================

left, right = st.columns(
    [1, 1.1],
    gap="large"
)

# =========================================================
# 左侧：商品输入
# =========================================================

with left:

    st.markdown(
        '<div class="section-title">01 · 产品信息</div>',
        unsafe_allow_html=True
    )

    product_title = st.text_input(
        "中文商品标题（可选）",
        placeholder="可直接复制 1688 商品标题"
    )

    product_info = st.text_area(
        "中文产品描述 / 属性（可选）",
        placeholder="""如果供应商有资料，可以直接复制进来。

例如：

产品名称：
材质：
尺寸：
颜色：
功能：
包装数量：
适用场景：
其他卖点：

如果没有文字资料，可以留空，直接上传商品图片。""",
        height=240
    )

    uploaded_images = st.file_uploader(
        "上传商品图片",
        type=[
            "jpg",
            "jpeg",
            "png",
            "webp"
        ],
        accept_multiple_files=True,
        help="支持上传1688主图、详情图、参数图等"
    )

    # 图片预览
    if uploaded_images:

        st.caption(
            f"已上传 {len(uploaded_images)} 张图片"
        )

        preview_columns = st.columns(3)

        for index, uploaded_file in enumerate(uploaded_images):

            with preview_columns[index % 3]:

                st.image(
                    uploaded_file,
                    use_container_width=True
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

    store_template = st.text_area(
        "英文店铺基础模板",
        value="""✨ WELCOME TO OUR STORE ✨

Discover practical and stylish products designed to make everyday life easier, tidier, and more comfortable.

🌿 Thoughtful Designs
🌿 Quality You Can Trust
🌿 Style for Every Space

Thank you for supporting our store.""",
        height=180
    )

    generate = st.button(
        "✨ 生成优化结果",
        use_container_width=True
    )

# =========================================================
# 右侧：AI 输出
# =========================================================

with right:

    st.markdown(
        '<div class="section-title">02 · 优化结果</div>',
        unsafe_allow_html=True
    )

    if not generate:

        st.markdown("""
        <div class="output-box">
            <div class="empty-result">

                <div style="font-size:45px;">
                    ✦
                </div>

                <div class="empty-title">
                    准备好优化您的 Listing
                </div>

                <p>
                    输入商品资料或上传商品图片，
                    AI 将自动分析并生成英文 Listing。
                </p>

            </div>
        </div>
        """, unsafe_allow_html=True)

    else:

        # 至少需要一种商品信息
        if (
            not product_title
            and not product_info
            and not uploaded_images
        ):

            st.warning(
                "请至少填写商品标题、商品资料，或上传一张商品图片。"
            )

        else:

            # =================================================
            # Prompt
            # =================================================

            prompt = f"""
You are an experienced Southeast Asian e-commerce listing specialist.

Your task is to analyze the supplied product information and product
images, then create a high-quality English product listing.

TARGET PLATFORM:
{platform}

TARGET MARKET:
Malaysia

LISTING STYLE:
{listing_style}

SOURCE PRODUCT TITLE:
{product_title if product_title else "No written title provided."}

SOURCE PRODUCT INFORMATION:
{product_info if product_info else "No written product description provided. Analyze the uploaded images."}


==================================================
IMAGE ANALYSIS INSTRUCTIONS
==================================================

The user may provide multiple supplier product images.

Carefully analyze ALL uploaded images.

Read and understand visible Chinese or English text in the images.

Use information explicitly shown in the images to identify:

- Product type
- Product purpose
- Visible structure
- Visible functions
- Usage scenarios
- Colour
- Quantity
- Dimensions, ONLY when explicitly written
- Material, ONLY when explicitly written
- Compatibility, ONLY when explicitly written
- Included accessories, ONLY when clearly shown or written
- Product features
- Product selling points

If written product information is missing, build the listing primarily
from information that can be reliably confirmed from the images.

You may develop marketing selling points from clearly observable
product features.

For example:

If the image clearly shows multiple storage compartments,
you may describe the product as providing organised storage.

If the image clearly shows an adjustable shelf,
you may describe the adjustable shelf as a selling point.


==================================================
STRICT ANTI-HALLUCINATION RULES
==================================================

NEVER guess or invent:

- Material
- Dimensions
- Weight
- Load capacity
- Certification
- Product quantity
- Technical specifications
- Compatibility
- Waterproof rating
- Heat resistance
- Safety certification
- Country of manufacture
- Warranty
- Performance data

Do NOT infer material purely from appearance.

Example:

If the product looks metallic but neither the text nor image explicitly
confirms stainless steel, DO NOT write "stainless steel".

Do NOT infer dimensions based on visual proportions.

Do NOT invent functions simply because similar products normally have
those functions.

When important information cannot be confirmed, place it under:

[Need Confirmation]


==================================================
TRANSLATION RULES
==================================================

Translate Chinese naturally into commercial English.

Do NOT perform rigid word-for-word translation.

Use clear English terminology understandable to Malaysian shoppers.

Preserve the original meaning.

Do not exaggerate supplier claims.

Avoid unsupported terms such as:

- Best
- No.1
- Perfect
- Premium Quality
- 100% Guaranteed
- Lifetime
- Professional Grade

unless explicitly supported by the supplied information.


==================================================
SEO RULES
==================================================

Create a readable, search-friendly product title.

Prioritize:

1. Product type
2. Core search keyword
3. Important function
4. Important specification
5. Usage scenario

Do not repeat keywords unnecessarily.

Do not keyword spam.

Use commercially relevant English search terms.


==================================================
OUTPUT FORMAT
==================================================

Output EXACTLY using the following structure:


### English Product Title

Create one optimized English title.


### Core Search Keywords

Provide 5-10 relevant search keywords.

Use bullet points.


### Selling Points

Provide 4-6 useful selling points.

Selling points must be based on supplied information or clearly
observable product features.


### Product Description

Write a clear and natural English product description suitable for
{platform}.

Explain:

- What the product is
- What it is used for
- Important features
- Suitable usage scenarios

Keep the description readable and practical.


### Specifications

Only include confirmed information.

Use this structure when information is available:

Product Name:
Material:
Colour:
Size:
Quantity:
Style:
Application:
Package Includes:

If information is unavailable, do not invent it.


### Variations

Recommend clear variation names based ONLY on supplied information.

If variations cannot be determined, write:

[Need Confirmation]


### Information To Confirm

List important information that cannot be reliably determined from the
provided text or images.


### Image Text Translation

If Chinese text is visible in uploaded images:

List the important Chinese text and provide natural English translations.

Use this format:

Chinese:
English:

If no readable Chinese text is found, write:

No readable Chinese product text detected.


### Store Message

{store_template}
"""

            # =================================================
            # 发送给 Gemini 的内容
            # =================================================

            contents = [prompt]

            if uploaded_images:

                for uploaded_file in uploaded_images:

                    image_bytes = uploaded_file.getvalue()

                    image_part = types.Part.from_bytes(
                        data=image_bytes,
                        mime_type=uploaded_file.type
                    )

                    contents.append(image_part)

            # =================================================
            # 调用 Gemini
            # =================================================

            try:

                with st.spinner(
                    "AI 正在读取商品资料和图片..."
                ):

                    response = client.models.generate_content(
                        model="gemini-3.5-flash",
                        contents=contents
                    )

                st.success(
                    "Listing 生成完成 ✨"
                )

                st.markdown(
                    '<div class="output-box">',
                    unsafe_allow_html=True
                )

                st.markdown(
                    response.text
                )

                st.markdown(
                    '</div>',
                    unsafe_allow_html=True
                )

            except Exception as e:

                st.error(
                    "生成失败"
                )

                st.code(
                    str(e)
                )

                st.info(
                    "如果再次报错，把上面的错误内容截图给我。"
                )

# =========================================================
# Footer
# =========================================================

st.markdown("---")

st.caption(
    "AI Listing Optimizer · Shopee MY / TikTok Shop MY"
)
