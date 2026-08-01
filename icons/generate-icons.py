#!/usr/bin/env python3
"""
Generate GoStop app icons in all required sizes.
Run: python3 icons/generate-icons.py
"""

from __future__ import annotations

import math
import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageFilter

ICON_DIR = Path(__file__).parent
COLOR_GO = (52, 199, 89)       # #34C759
COLOR_STOP = (255, 59, 48)     # #FF3B30
COLOR_WHITE = (255, 255, 255)
COLOR_SHADOW = (0, 0, 0, 64)

SIZES = {
    "icon-1024.png": 1024,
    "icon-512.png": 512,
    "icon-512-maskable.png": 512,
    "icon-192.png": 192,
    "icon-180.png": 180,
    "apple-touch-icon.png": 180,
    "favicon-32.png": 32,
    "favicon-16.png": 16,
}


def rounded_rect_mask(size: int, radius: float) -> Image.Image:
    """Create an alpha mask for a rounded rectangle."""
    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, size - 1, size - 1), radius=radius, fill=255)
    return mask


def draw_curved_divider(
    draw: ImageDraw.ImageDraw,
    size: int,
    center_x: float,
    width: float,
) -> None:
    """Draw the white curved card-edge divider."""
    points_left = []
    points_right = []
    steps = 120

    for i in range(steps + 1):
        t = i / steps
        y = t * (size - 1)
        # S-curve bulge toward center
        bulge = math.sin(t * math.pi) * width * 0.35
        points_left.append((center_x - width * 0.5 + bulge, y))
        points_right.append((center_x + width * 0.5 + bulge, y))

    polygon = points_left + list(reversed(points_right))
    draw.polygon(polygon, fill=COLOR_WHITE)


def get_font(size: int, bold: bool = True) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    """Load system font with fallbacks."""
    candidates = [
        "/System/Library/Fonts/SFNSDisplay.ttf",
        "/System/Library/Fonts/SFNS.ttf",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/Library/Fonts/Arial Bold.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except OSError:
                continue
    return ImageFont.load_default()


def generate_icon(size: int) -> Image.Image:
    """Render a single icon at the given pixel size."""
    # Padding for shadow on larger icons
    pad = max(2, int(size * 0.04)) if size >= 64 else 0
    canvas_size = size + pad * 2

    img = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    radius = size * 0.195  # ~200/1024
    origin = pad

    # Drop shadow
    if pad > 0:
        shadow = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
        shadow_draw = ImageDraw.Draw(shadow)
        shadow_draw.rounded_rectangle(
            (origin + 2, origin + 4, origin + size - 1, origin + size - 1),
            radius=radius,
            fill=COLOR_SHADOW,
        )
        shadow = shadow.filter(ImageFilter.GaussianBlur(radius=max(2, size // 80)))
        img = Image.alpha_composite(img, shadow)
        draw = ImageDraw.Draw(img)

    # Base rounded square clipped to halves
    base = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    base_draw = ImageDraw.Draw(base)

    # Green left half
    base_draw.rectangle((0, 0, size // 2, size), fill=COLOR_GO)
    # Red right half
    base_draw.rectangle((size // 2, 0, size, size), fill=COLOR_STOP)

    # Curved divider
    divider_width = max(2, size * 0.025)
    draw_curved_divider(base_draw, size, size / 2, divider_width)

    # Apply rounded corner mask
    mask = rounded_rect_mask(size, radius)
    rounded = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    rounded.paste(base, (0, 0), mask)

    img.paste(rounded, (origin, origin), rounded)

    # Gloss overlay
    gloss = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    gloss_draw = ImageDraw.Draw(gloss)
    gloss_draw.rectangle((0, 0, size, int(size * 0.45)), fill=(255, 255, 255, 35))
    gloss_masked = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    gloss_masked.paste(gloss, (0, 0), mask)
    img.paste(gloss_masked, (origin, origin), gloss_masked)

    draw = ImageDraw.Draw(img)

    # Text
    go_font_size = int(size * 0.175)
    stop_font_size = int(size * 0.115)
    go_font = get_font(go_font_size)
    stop_font = get_font(stop_font_size)

    go_text = "GO"
    stop_text = "STOP"

    go_bbox = draw.textbbox((0, 0), go_text, font=go_font)
    go_w = go_bbox[2] - go_bbox[0]
    go_h = go_bbox[3] - go_bbox[1]
    go_x = origin + size * 0.28 - go_w / 2
    go_y = origin + size * 0.52 - go_h / 2

    stop_bbox = draw.textbbox((0, 0), stop_text, font=stop_font)
    stop_w = stop_bbox[2] - stop_bbox[0]
    stop_h = stop_bbox[3] - stop_bbox[1]
    stop_x = origin + size * 0.72 - stop_w / 2
    stop_y = origin + size * 0.52 - stop_h / 2

    draw.text((go_x, go_y), go_text, fill=COLOR_WHITE, font=go_font)
    draw.text((stop_x, stop_y), stop_text, fill=COLOR_WHITE, font=stop_font)

    # Crop to exact size (remove shadow pad for favicons)
    if pad > 0 and size >= 64:
        return img
    return img.crop((pad, pad, pad + size, pad + size)) if pad else img


def generate_maskable_icon(size: int) -> Image.Image:
    """Render a maskable icon with content inset within the 80% safe zone."""
    icon = generate_icon(size)
    safe = int(size * 0.80)
    offset = (size - safe) // 2
    canvas = Image.new("RGBA", (size, size), COLOR_GO)
    resized = icon.resize((safe, safe), Image.Resampling.LANCZOS)
    canvas.paste(resized, (offset, offset), resized)
    return canvas


def main() -> None:
    """Generate all icon files."""
    # Generate at 1024 first, then resize for efficiency
    master = generate_icon(1024)
    # Crop shadow for master if needed
    if master.size[0] > 1024:
        offset = (master.size[0] - 1024) // 2
        master = master.crop((offset, offset, offset + 1024, offset + 1024))

    for filename, size in SIZES.items():
        if filename == "icon-512-maskable.png":
            output = generate_maskable_icon(size)
        elif size == 1024:
            output = master
        else:
            output = master.resize((size, size), Image.Resampling.LANCZOS)

        path = ICON_DIR / filename
        output.save(path, "PNG", optimize=True)
        print(f"Created {path} ({size}x{size})")

    print("All icons generated successfully.")


if __name__ == "__main__":
    main()
