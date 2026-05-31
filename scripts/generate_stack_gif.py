#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

import requests
from PIL import Image, ImageDraw, ImageFilter, ImageFont

try:
    import cairosvg
except ImportError:
    cairosvg = None


STACK_ITEMS = [
    {"label": "TypeScript", "slug": "typescript", "accent": "#3178C6"},
    {"label": "Python", "slug": "python", "accent": "#3776AB"},
    {"label": "React", "slug": "react", "accent": "#61DAFB"},
    {"label": "Next.js", "slug": "nextdotjs", "accent": "#111111"},
    {"label": "Node.js", "slug": "nodedotjs", "accent": "#5FA04E"},
    {"label": "Tailwind CSS", "slug": "tailwindcss", "accent": "#06B6D4"},
    {"label": "Compact", "slug": None, "accent": "#6D28D9", "short": "CP"},
    {"label": "GitHub", "slug": "github", "accent": "#24292F"},
    {"label": "Docker", "slug": "docker", "accent": "#2496ED"},
    {"label": "C++", "slug": "cplusplus", "accent": "#00599C"},
    {"label": "C", "slug": "c", "accent": "#A8B9CC"},
    {"label": "Midnight", "slug": None, "accent": "#0F172A", "short": "MN"},
    {"label": "Splunk", "slug": "splunk", "accent": "#65A637"},
    {"label": "Vercel", "slug": "vercel", "accent": "#000000"},
]
STACK_DATA_PATH = Path("data/stack_items.json")

BG_COLOR = "#FAF9F6"
CARD_COLOR = "#FFFFFF"
TEXT_COLOR = "#171717"
MUTED_BORDER = "#E7E3DA"
ICON_WELL = "#F3F1EB"
SHADOW_COLOR = (0, 0, 0, 20)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a light-theme sliding tech stack GIF."
    )
    parser.add_argument(
        "--output",
        default="assets/tech-stack-slider-light.gif",
        help="Output GIF path relative to the repository root.",
    )
    parser.add_argument("--width", type=int, default=1200, help="Canvas width.")
    parser.add_argument("--height", type=int, default=150, help="Canvas height.")
    parser.add_argument(
        "--seconds",
        type=float,
        default=18.0,
        help="Loop length. Higher is slower.",
    )
    parser.add_argument("--fps", type=int, default=24, help="Frames per second.")
    return parser.parse_args()


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
        if bold
        else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/SFNS.ttf",
        "/Library/Fonts/Arial Unicode.ttf",
    ]
    for candidate in candidates:
        path = Path(candidate)
        if path.exists():
            return ImageFont.truetype(str(path), size=size)
    return ImageFont.load_default()


def measure_text(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont) -> tuple[int, int]:
    box = draw.textbbox((0, 0), text, font=font)
    return box[2] - box[0], box[3] - box[1]


def draw_round_rect(
    image: Image.Image,
    box: tuple[int, int, int, int],
    radius: int,
    fill: str | tuple[int, int, int, int],
    outline: str | None = None,
    width: int = 1,
) -> None:
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def cache_dir() -> Path:
    path = repo_root() / ".cache" / "logo-slider"
    path.mkdir(parents=True, exist_ok=True)
    return path


def load_stack_items() -> list[dict[str, str | None]]:
    data_path = repo_root() / STACK_DATA_PATH
    if not data_path.exists():
        return STACK_ITEMS

    try:
        loaded = json.loads(data_path.read_text())
    except (json.JSONDecodeError, OSError):
        return STACK_ITEMS

    if isinstance(loaded, list) and loaded:
        return loaded
    return STACK_ITEMS


def download_svg(slug: str, dest: Path) -> bool:
    url = f"https://cdn.simpleicons.org/{slug}"
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
    except requests.RequestException:
        return False
    dest.write_bytes(response.content)
    return True


def rasterize_svg(svg_path: Path, png_path: Path) -> bool:
    if cairosvg is not None:
        try:
            cairosvg.svg2png(url=str(svg_path), write_to=str(png_path))
            return png_path.exists()
        except Exception:
            pass

    try:
        subprocess.run(
            [
                "sips",
                "-s",
                "format",
                "png",
                str(svg_path),
                "--out",
                str(png_path),
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False
    return png_path.exists()


def fetch_logo(item: dict[str, str | None], size: int) -> Image.Image | None:
    slug = item.get("slug")
    if not slug:
        return None

    cache = cache_dir()
    svg_path = cache / f"{slug}.svg"
    png_path = cache / f"{slug}.png"

    if not svg_path.exists() and not download_svg(slug, svg_path):
        return None
    if not png_path.exists() and not rasterize_svg(svg_path, png_path):
        return None

    try:
        image = Image.open(png_path).convert("RGBA")
    except OSError:
        return None

    image.thumbnail((size, size), Image.Resampling.LANCZOS)
    return image


def build_fallback_mark(short: str, accent: str, size: int, font: ImageFont.ImageFont) -> Image.Image:
    tile = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(tile)
    draw.ellipse((0, 0, size - 1, size - 1), fill=accent)
    short_w, short_h = measure_text(draw, short, font)
    draw.text(
        ((size - short_w) / 2, (size - short_h) / 2 - 1),
        short,
        fill="#FFFFFF",
        font=font,
    )
    return tile


def build_logo_tile(item: dict[str, str | None], icon_size: int, short_font: ImageFont.ImageFont) -> Image.Image:
    tile_size = 44
    tile = Image.new("RGBA", (tile_size, tile_size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(tile)
    draw.rounded_rectangle((0, 0, tile_size - 1, tile_size - 1), radius=14, fill=ICON_WELL)

    logo = fetch_logo(item, icon_size)
    if logo is None:
        short = str(item.get("short") or item["label"][:2]).upper()
        logo = build_fallback_mark(short, str(item["accent"]), icon_size, short_font)

    x = (tile_size - logo.width) // 2
    y = (tile_size - logo.height) // 2
    tile.alpha_composite(logo, (x, y))
    return tile


def build_card(
    item: dict[str, str | None],
    label_font: ImageFont.ImageFont,
    short_font: ImageFont.ImageFont,
) -> Image.Image:
    label = str(item["label"])
    dummy = Image.new("RGBA", (10, 10), (0, 0, 0, 0))
    draw = ImageDraw.Draw(dummy)

    label_w, label_h = measure_text(draw, label, label_font)

    icon_tile = build_logo_tile(item, 24, short_font)

    padding_x = 18
    gap = 14
    card_h = 74
    text_block_w = label_w
    card_w = padding_x * 2 + icon_tile.width + gap + text_block_w

    shadow = Image.new("RGBA", (card_w + 20, card_h + 20), (0, 0, 0, 0))
    shadow_box = (10, 10, 10 + card_w, 10 + card_h)
    draw_round_rect(shadow, shadow_box, 24, SHADOW_COLOR)
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=7))

    card = Image.new("RGBA", shadow.size, (0, 0, 0, 0))
    card.alpha_composite(shadow)
    draw_round_rect(card, shadow_box, 24, CARD_COLOR, outline=MUTED_BORDER, width=1)

    draw = ImageDraw.Draw(card)
    icon_x = shadow_box[0] + padding_x
    icon_y = shadow_box[1] + (card_h - icon_tile.height) // 2
    card.alpha_composite(icon_tile, (icon_x, icon_y))

    label_x = icon_x + icon_tile.width + gap
    label_y = shadow_box[1] + (card_h - label_h) // 2 - 2
    draw.text((label_x, label_y), label, fill=TEXT_COLOR, font=label_font)
    return card


def build_strip() -> tuple[Image.Image, int]:
    label_font = load_font(22, bold=True)
    short_font = load_font(15, bold=True)
    gap = 18

    cards = [build_card(item, label_font, short_font) for item in load_stack_items()]
    total_width = sum(card.width for card in cards) + gap * (len(cards) - 1)
    strip_h = max(card.height for card in cards)
    strip = Image.new("RGBA", (total_width, strip_h), (0, 0, 0, 0))

    x = 0
    for card in cards:
        y = (strip_h - card.height) // 2
        strip.alpha_composite(card, (x, y))
        x += card.width + gap
    return strip, total_width


def add_edge_fade(image: Image.Image, fade_width: int = 58) -> Image.Image:
    width, height = image.size
    mask = Image.new("L", (width, height), 255)
    draw = ImageDraw.Draw(mask)

    for i in range(fade_width):
        alpha = int(255 * (i / fade_width))
        draw.line((i, 0, i, height), fill=alpha)
        draw.line((width - 1 - i, 0, width - 1 - i, height), fill=alpha)

    background = Image.new("RGBA", image.size, BG_COLOR)
    return Image.composite(image, background, mask)


def build_rgba_frames(width: int, height: int, seconds: float, fps: int) -> list[Image.Image]:
    strip, strip_width = build_strip()
    repeated = Image.new("RGBA", (strip_width * 2, strip.height), (0, 0, 0, 0))
    repeated.alpha_composite(strip, (0, 0))
    repeated.alpha_composite(strip, (strip_width, 0))

    frame_count = max(1, int(seconds * fps))
    frames: list[Image.Image] = []
    top = (height - strip.height) // 2

    for frame_index in range(frame_count):
        progress = frame_index / frame_count
        offset = int(progress * strip_width)

        frame = Image.new("RGBA", (width, height), BG_COLOR)
        frame.alpha_composite(repeated, (-offset, top))
        frame.alpha_composite(repeated, (strip_width - offset, top))
        frames.append(add_edge_fade(frame))

    return frames


def save_with_ffmpeg(frames: list[Image.Image], output_path: Path, fps: int) -> bool:
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        return False

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        for index, frame in enumerate(frames):
            frame.save(tmp_path / f"frame_{index:04d}.png")

        palette_path = tmp_path / "palette.png"
        input_pattern = str(tmp_path / "frame_%04d.png")

        try:
            subprocess.run(
                [
                    ffmpeg,
                    "-y",
                    "-framerate",
                    str(fps),
                    "-i",
                    input_pattern,
                    "-vf",
                    "palettegen=max_colors=128:reserve_transparent=0",
                    str(palette_path),
                ],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            subprocess.run(
                [
                    ffmpeg,
                    "-y",
                    "-framerate",
                    str(fps),
                    "-i",
                    input_pattern,
                    "-i",
                    str(palette_path),
                    "-lavfi",
                    "paletteuse=dither=bayer:bayer_scale=3",
                    "-loop",
                    "0",
                    str(output_path),
                ],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except subprocess.CalledProcessError:
            return False

    return output_path.exists()


def save_with_pillow(frames: list[Image.Image], output_path: Path, fps: int) -> None:
    duration = int(1000 / fps)
    palette_frames = [frame.convert("P", palette=Image.Palette.ADAPTIVE) for frame in frames]
    palette_frames[0].save(
        output_path,
        save_all=True,
        append_images=palette_frames[1:],
        duration=duration,
        loop=0,
        optimize=False,
        disposal=2,
    )


def main() -> None:
    args = parse_args()
    output_path = repo_root() / args.output
    output_path.parent.mkdir(parents=True, exist_ok=True)

    frames = build_rgba_frames(args.width, args.height, args.seconds, args.fps)
    if not save_with_ffmpeg(frames, output_path, args.fps):
        save_with_pillow(frames, output_path, args.fps)

    print(f"Saved {output_path}")


if __name__ == "__main__":
    main()
