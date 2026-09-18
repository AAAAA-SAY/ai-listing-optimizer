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
    min-height: 500px;
}

.empty-result {
    text-align: center;
    padding-top: 150px;
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
        placeholder="""有供应商资料可以直接复制。

例如：

产品名称：
材质：
尺寸：
颜色：
功能：
包装数量：
适用场景：
其他卖点：

没有文字资料可以留空，直接上传商品图片。""",
        height=220
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
        help="支持1688主图、详情图、规格图、参数图等"
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
                    AI 将自动生成英文商品内容。
                </p>

            </div>
        </div>
        """, unsafe_allow_html=True)

    else:

        # 至少提供一种信息
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
You are a professional e-commerce listing assistant specialising in
Shopee Malaysia and TikTok Shop Malaysia.

Your task is NOT to write creative advertising copy.

Your task is to convert supplier information and product images into a
concise, accurate and ready-to-publish English product listing.


TARGET PLATFORM:
{platform}

TARGET MARKET:
Malaysia

LISTING STYLE:
{listing_style}


SOURCE PRODUCT TITLE:
{product_title if product_title else "No written title provided."}


SOURCE PRODUCT INFORMATION:
{product_info if product_info else "No written product information provided."}


==================================================
SOURCE PRIORITY
==================================================

Use information in this priority order:

1. Explicit written product specifications supplied by the user
2. Explicit readable text appearing in uploaded product images
3. Features that are directly and clearly visible in product images

Never replace explicit supplier information with your own assumptions.

If text and image information conflict, do NOT decide which one is
correct.

Use [Need Confirmation] for the conflicting information.


==================================================
IMAGE ANALYSIS RULES
==================================================

Analyze all uploaded product images carefully.

You may use the images to identify:

- Product type
- Visible colour
- Visible structure
- Visible design
- Visible components
- Visible usage scenario
- Explicitly written dimensions
- Explicitly written materials
- Explicitly written quantities
- Explicitly written functions
- Explicitly written compatibility
- Explicitly shown package contents

If there is no written description, you may create a basic listing from
features that are clearly visible in the images.

However, visual appearance alone is NOT evidence for technical
specifications.


==================================================
STRICT NO-GUESSING RULE
==================================================

Do NOT invent, assume or infer unsupported product facts.

Never guess:

- Material
- Exact colour name when uncertain
- Dimensions
- Weight
- Quantity
- Piece count
- Load capacity
- Waterproof ability
- Heat resistance
- Durability
- Certification
- Safety standard
- Age suitability
- Compatibility
- Country of manufacture
- Warranty
- Package contents
- Technical performance

Example:

A product looking metallic does NOT mean it is stainless steel.

A building block product does NOT automatically mean it is made from ABS.

A toy does NOT automatically mean it is educational.

A product containing small parts does NOT allow you to invent an age
recommendation.

Do not infer information simply because similar products commonly have
that feature.


==================================================
SELLING POINT RULES
==================================================

Selling points must come from:

1. Explicit supplier information
OR
2. Directly observable product features

You may describe the practical benefit of an observable feature when
the relationship is obvious and non-technical.

Allowed example:

Visible multiple compartments
→ Helps organise different items.

Visible compact structure
→ Suitable for desktop placement.

Visible decorative miniature design
→ Can also be used as desktop decoration.

NOT allowed:

Building blocks
→ Improves intelligence.

DIY toy
→ Improves fine motor skills.

Metal appearance
→ Rust-resistant.

Thick-looking panel
→ Heavy-duty.

Do NOT invent health, educational, developmental, safety or performance
benefits.


==================================================
LANGUAGE & TRANSLATION RULES
==================================================

Translate Chinese naturally into clear commercial English.

Do not translate word-for-word when the result sounds unnatural.

Keep the original product meaning.

Use English terminology understandable to Malaysian shoppers.

Do NOT exaggerate the supplier's claims.

Avoid unsupported promotional words such as:

- Best
- No.1
- Perfect
- Premium Quality
- Guaranteed
- Professional Grade
- Must-Have
- Ultimate

Keep the tone factual, natural and commercially useful.


==================================================
TITLE RULES
==================================================

Create ONE English product title.

The title should prioritise:

Product Type
+ Core Keyword
+ Important Confirmed Feature
+ Important Confirmed Specification
+ Usage

Only include information supported by the source.

Do not keyword spam.

Do not repeat the same keyword unnecessarily.

Do not insert unconfirmed specifications.

Keep the title readable and suitable for search.


==================================================
OUTPUT LENGTH
==================================================

Keep the entire response concise.

This is an e-commerce listing, NOT an analysis report.

Do NOT explain your reasoning.

Do NOT explain why information is missing.

Do NOT provide marketing strategy.

Do NOT provide keyword analysis.

Do NOT provide recommendations to the seller.

Do NOT create information simply to make the listing look complete.


==================================================
OUTPUT FORMAT
==================================================

Output EXACTLY using the following structure:


### English Product Title

Write ONE concise, natural and search-friendly English title.


### Selling Points

Write ONLY 4 selling points.

Each selling point must be ONE short sentence.

Format:

• Feature Name – Short practical description.

Do not exceed approximately 20 words per selling point.


### Product Description

Write ONE concise product description.

Maximum 80 words.

Include only:

- What the product is
- Main confirmed or clearly visible features
- Main usage

Do not repeat all selling points.

Do not add unsupported benefits.


### Specifications

Only include information that can be confirmed from the supplied text
or images.

Use:

Product Name:
Material:
Colour:
Size:
Quantity:
Style:
Package Includes:

For any important attribute that cannot be confirmed, write only:

[Need Confirmation]

Do NOT explain why.


### Image Translation

Only create this section when readable Chinese product text appears in
uploaded images.

Translate ONLY important product information.

Do not translate decorative slogans unless they contain useful product
information.

Format:

Chinese → English

Keep translations short.

If there is no useful readable Chinese product text, omit the entire
Image Translation section.


==================================================
FINAL CHECK
==================================================

Before answering, silently check:

- Did I invent any specification?
- Did I infer material from appearance?
- Did I invent educational, health or safety benefits?
- Did I invent package contents?
- Did I invent variations?
- Did I repeat information unnecessarily?
- Is the description under 80 words?
- Are there exactly 4 selling points?

If any unsupported claim exists, remove it before producing the final
listing.
"""

            # =================================================
            # 构建发送给 Gemini 的内容
            # =================================================

            contents = [prompt]

            if uploaded_images:

                for uploaded_file in uploaded_images:

                    image_bytes = uploaded_file.getvalue()

                    image_part = types.Part.from_bytes(
                        data=image_bytes,
                        mime_type=uploaded_file.type
                    )

                    contents.append(
                        image_part
                    )


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
