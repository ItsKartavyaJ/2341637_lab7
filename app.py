import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import colorsys
import io

st.set_page_config(page_title="🎨 Color Palette Generator", page_icon="🎨", layout="centered")

st.title("🎨 Color Palette Generator")
st.markdown("Generate beautiful color palettes based on color theory.")

# Helper to convert HEX to RGB
def hex_to_rgb(hex_code):
    hex_code = hex_code.lstrip('#')
    return tuple(int(hex_code[i:i+2], 16) for i in (0, 2 ,4))

# Helper to convert RGB to HEX
def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(*rgb)

# Generate palette colors based on scheme type
def generate_palette(base_color, scheme):
    # Convert base_color to HLS
    r, g, b = [x/255.0 for x in base_color]
    h, l, s = colorsys.rgb_to_hls(r, g, b)

    palette = []

    if scheme == "Complementary":
        # Base + complementary (hue + 0.5)
        palette.append(base_color)
        comp_h = (h + 0.5) % 1.0
        r2, g2, b2 = colorsys.hls_to_rgb(comp_h, l, s)
        palette.append(tuple(int(x*255) for x in (r2, g2, b2)))

    elif scheme == "Analogous":
        # Base + two adjacent hues (+/- 30 degrees = 1/12)
        offsets = [-1/12, 0, 1/12]
        for offset in offsets:
            new_h = (h + offset) % 1.0
            r2, g2, b2 = colorsys.hls_to_rgb(new_h, l, s)
            palette.append(tuple(int(x*255) for x in (r2, g2, b2)))

    elif scheme == "Triadic":
        # Base + 2 others spaced by 120 degrees (1/3)
        palette.append(base_color)
        for i in [1/3, 2/3]:
            new_h = (h + i) % 1.0
            r2, g2, b2 = colorsys.hls_to_rgb(new_h, l, s)
            palette.append(tuple(int(x*255) for x in (r2, g2, b2)))

    elif scheme == "Tetradic":
        # Base + 3 others spaced by 90 degrees (1/4)
        palette.append(base_color)
        for i in [1/4, 1/2, 3/4]:
            new_h = (h + i) % 1.0
            r2, g2, b2 = colorsys.hls_to_rgb(new_h, l, s)
            palette.append(tuple(int(x*255) for x in (r2, g2, b2)))

    return palette

# Render color swatches with HEX codes
def show_palette(palette):
    cols = st.columns(len(palette))
    for idx, color in enumerate(palette):
        hex_code = rgb_to_hex(color)
        with cols[idx]:
            st.markdown(f'<div style="background-color:{hex_code}; padding:40px; border-radius:8px;"></div>', unsafe_allow_html=True)
            st.caption(hex_code.upper())

# Generate downloadable palette image
def create_palette_image(palette):
    width = 200 * len(palette)
    height = 200
    image = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(image)

    for i, color in enumerate(palette):
        x0 = i * 200
        x1 = x0 + 200
        draw.rectangle([x0, 0, x1, height], fill=color)
        # Add HEX text
        hex_code = rgb_to_hex(color).upper()
        try:
            font = ImageFont.truetype("arial.ttf", 30)
        except:
            font = ImageFont.load_default()
        bbox = draw.textbbox((0, 0), hex_code, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]

        draw.text((x0 + (200 - text_w)/2, height/2 - text_h/2), hex_code, fill="white", font=font)

    return image

# === Streamlit UI ===
base_color = st.color_picker("Pick a base color", "#3f51b5")
scheme = st.selectbox("Select a color scheme", ["Complementary", "Analogous", "Triadic", "Tetradic"])

rgb_color = hex_to_rgb(base_color)
palette = generate_palette(rgb_color, scheme)

st.subheader("Generated Palette")
show_palette(palette)

img = create_palette_image(palette)
buf = io.BytesIO()
img.save(buf, format="PNG")
byte_im = buf.getvalue()

st.download_button(
    label="Download Palette as PNG",
    data=byte_im,
    file_name=f"{scheme}_palette.png",
    mime="image/png"
)

st.markdown("---")
st.markdown("Made with ❤️ by Kartavya Jain | Powered by Streamlit")

