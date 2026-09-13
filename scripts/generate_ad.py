#!/usr/bin/env python3
"""
Serenity Mind – Free No-GPU Short Ad Generator
Creates a calm 20-30s promotional video for a digital mental-peace product.
No GPU required. Uses Edge-TTS + MoviePy + FFmpeg.
"""

import os
import asyncio
import textwrap
from pathlib import Path
from typing import List, Tuple

# Third-party
try:
    import edge_tts
    from moviepy.editor import (
        ImageClip, TextClip, CompositeVideoClip, AudioFileClip,
        concatenate_videoclips, ColorClip
    )
    from moviepy.video.fx.all import fadein, fadeout
    from PIL import Image, ImageDraw, ImageFont
    import numpy as np
except ImportError as e:
    print("Missing packages. Run: pip install -r requirements.txt")
    raise e

# ====================== CONFIG ======================
PRODUCT_NAME = "Serenity Mind"
TAGLINE = "Your digital sanctuary for mental peace"
CTA_TEXT = "Start your free calm journey today"
CTA_SUB = "Available now • Link in bio"

# Calm, short ad script (spoken + captions)
SCRIPT_SEGMENTS = [
    "Feeling overwhelmed by the noise of everyday life?",
    "Racing thoughts. Constant stress. No time to breathe.",
    "Introducing Serenity Mind.",
    "A simple digital guide to mental peace.",
    "Five-minute guided resets. Soft breathing exercises. Journaling prompts that actually help.",
    "No pressure. No perfection. Just presence.",
    "Download Serenity Mind and reclaim your calm.",
]

VOICE = "en-US-JennyNeural"          # calm female voice (free)
BG_COLOR = (30, 58, 95)              # deep calm blue
ACCENT_COLOR = (167, 199, 231)       # soft sky blue
TEXT_COLOR = (255, 255, 255)
OUTPUT_DIR = Path(__file__).parent.parent / "output"
ASSETS_DIR = Path(__file__).parent.parent / "assets"
WIDTH, HEIGHT = 1080, 1920           # vertical Shorts / Reels
FPS = 24
# ====================================================


def ensure_dirs():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (ASSETS_DIR / "images").mkdir(parents=True, exist_ok=True)
    (ASSETS_DIR / "audio").mkdir(parents=True, exist_ok=True)


async def generate_voiceover(text: str, output_path: Path, voice: str = VOICE) -> Path:
    """Generate natural voice using free Edge TTS."""
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(str(output_path))
    return output_path


def create_text_image(
    text: str,
    size: Tuple[int, int] = (WIDTH, HEIGHT),
    bg_color: Tuple[int, int, int] = BG_COLOR,
    text_color: Tuple[int, int, int] = TEXT_COLOR,
    font_size: int = 64,
    y_offset: int = 0,
) -> np.ndarray:
    """Create a clean image with centered text using Pillow (no external fonts needed)."""
    img = Image.new("RGB", size, bg_color)
    draw = ImageDraw.Draw(img)

    # Try nice fonts, fall back to default
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
        small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 36)
    except Exception:
        font = ImageFont.load_default()
        small_font = font

    # Word wrap
    max_width = size[0] - 120
    lines = []
    for paragraph in text.split("\n"):
        wrapped = textwrap.fill(paragraph, width=28)
        lines.extend(wrapped.split("\n"))

    # Calculate total text height
    line_heights = []
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        line_heights.append(bbox[3] - bbox[1] + 18)
    total_h = sum(line_heights)

    y = (size[1] - total_h) // 2 + y_offset
    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=font)
        w = bbox[2] - bbox[0]
        x = (size[0] - w) // 2
        # Soft shadow
        draw.text((x + 3, y + 3), line, font=font, fill=(0, 0, 0))
        draw.text((x, y), line, font=font, fill=text_color)
        y += line_heights[i]

    return np.array(img)


def make_scene(
    text: str,
    duration: float,
    bg_color: Tuple[int, int, int] = BG_COLOR,
    font_size: int = 58,
) -> ImageClip:
    """Create a single scene with gentle zoom (Ken Burns-ish)."""
    img_array = create_text_image(text, bg_color=bg_color, font_size=font_size)
    clip = ImageClip(img_array).set_duration(duration)

    # Gentle zoom in
    def zoom(t):
        # start at 1.0, end at 1.08
        return 1.0 + 0.08 * (t / duration)

    clip = clip.resize(lambda t: zoom(t))
    # Center crop to original size after zoom
    clip = clip.set_position("center")
    return clip


def build_video(audio_path: Path, segments: List[str]) -> Path:
    """Assemble the full ad video."""
    # Get audio duration
    audio = AudioFileClip(str(audio_path))
    total_duration = audio.duration

    # Distribute time across segments (with slight extra on key lines)
    weights = [1.1, 1.2, 1.4, 1.3, 1.5, 1.2, 1.3]  # emphasize product intro & CTA
    weight_sum = sum(weights[: len(segments)])
    durations = [total_duration * (w / weight_sum) for w in weights[: len(segments)]]

    clips = []
    for i, (seg, dur) in enumerate(zip(segments, durations)):
        # Alternate subtle color tones for visual interest
        if i in (2, 3):  # product name scenes
            color = (25, 75, 110)
            size = 72
        elif i == len(segments) - 1:  # CTA
            color = (20, 90, 70)
            size = 56
        else:
            color = BG_COLOR
            size = 56

        scene = make_scene(seg, duration=dur, bg_color=color, font_size=size)
        scene = fadein(scene, 0.4).fadeout(0.4)
        clips.append(scene)

    video = concatenate_videoclips(clips, method="compose")
    video = video.set_audio(audio)
    video = video.set_fps(FPS)

    # Final branding bar at bottom
    brand = TextClip(
        f"{PRODUCT_NAME}  •  {TAGLINE}",
        fontsize=28,
        color="white",
        font="DejaVu-Sans",
        method="caption",
        size=(WIDTH - 80, None),
    ).set_duration(total_duration).set_position(("center", HEIGHT - 90))

    final = CompositeVideoClip([video, brand])

    out_path = OUTPUT_DIR / "serenity_mind_ad.mp4"
    final.write_videofile(
        str(out_path),
        fps=FPS,
        codec="libx264",
        audio_codec="aac",
        preset="medium",
        threads=4,
        logger=None,
    )
    return out_path


async def main():
    print("🌿 Serenity Mind – Free No-GPU Ad Generator")
    print("=" * 50)
    ensure_dirs()

    full_script = " ".join(SCRIPT_SEGMENTS)
    print(f"Script length: {len(full_script)} chars")
    print(f"Voice: {VOICE}")

    # 1. Generate voiceover
    audio_path = ASSETS_DIR / "audio" / "voiceover.mp3"
    print("🎤 Generating free Edge-TTS voiceover...")
    await generate_voiceover(full_script, audio_path)
    print(f"   → {audio_path}")

    # 2. Build video
    print("🎬 Assembling calm ad video (this takes 30-90 seconds on CPU)...")
    out = build_video(audio_path, SCRIPT_SEGMENTS)
    print("=" * 50)
    print(f"✅ Done! Video saved to:\n   {out}")
    print("\nYou can now post it as a YouTube Short / Instagram Reel / TikTok.")
    print("Customize the script, colors, or voice in scripts/generate_ad.py")


if __name__ == "__main__":
    asyncio.run(main())
