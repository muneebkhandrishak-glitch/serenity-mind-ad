# Serenity Mind – Free No-GPU Ad Video Generator

**Short promotional video for a digital mental-peace product**  
Completely free • No GPU required • Runs on CPU only

This project creates a clean 20–30 second vertical (9:16) or landscape ad video using:
- Free Microsoft Edge TTS (natural voice)
- Free stock images (or solid calm backgrounds)
- FFmpeg + MoviePy for assembly
- Auto captions + soft music bed (optional)

Perfect for promoting digital products like meditation apps, calm journals, guided audio packs, or mindfulness courses.

---

## Product Concept

**Serenity Mind** – A simple digital sanctuary for mental peace.  
Daily 5-minute resets, guided breathing, journaling prompts, and calming soundscapes.  
Available as app / digital download.

---

## Features

- Zero GPU needed
- 100% free (Edge TTS is free, no API key)
- Vertical Shorts/Reels ready (1080×1920)
- Auto voiceover + burned-in captions
- Soft Ken-Burns zoom on calm images
- Easy to customize script, voice, colors

---

## Quick Install (Linux / macOS / Windows)

### 1. Prerequisites
```bash
# Python 3.10+
python3 --version

# FFmpeg (required)
# Ubuntu/Debian:
sudo apt update && sudo apt install -y ffmpeg
# macOS:
brew install ffmpeg
# Windows: download from https://ffmpeg.org and add to PATH
```

### 2. Clone & Setup
```bash
git clone https://github.com/muneebkhandrishak-glitch/serenity-mind-ad.git
cd serenity-mind-ad

python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### 3. Generate the Ad (one command)
```bash
python scripts/generate_ad.py
```

The finished video appears in `output/serenity_mind_ad.mp4`

---

## Customization

Edit these in `scripts/generate_ad.py`:

| Setting            | What it does                          |
|--------------------|---------------------------------------|
| `SCRIPT_SEGMENTS`  | The spoken + caption text             |
| `VOICE`            | Edge TTS voice (e.g. en-US-JennyNeural) |
| `PRODUCT_NAME`     | Brand name on screen                  |
| `BG_COLOR`         | Background color (calm blue/green)    |

You can also drop your own calm images into `assets/images/` (jpg/png).  
If none are present the script uses elegant solid-color + text scenes.

---

## Optional: Free Stock Images

1. Get a free Pexels API key → https://www.pexels.com/api/
2. Put it in `.env`:
   ```
   PEXELS_API_KEY=your_key_here
   ```

---

## Voices you can try (Edge TTS – free)

```
en-US-JennyNeural          # calm female (recommended)
en-US-GuyNeural            # warm male
en-GB-SoniaNeural          # soft British
en-US-AriaNeural           # gentle
```

Change `VOICE = "en-US-JennyNeural"` in the script.

---

## File Structure

```
serenity-mind-ad/
├── README.md
├── requirements.txt
├── scripts/
│   └── generate_ad.py      # main generator
├── assets/
│   ├── images/             # optional calm images
│   └── audio/              # generated voiceovers
└── output/                 # final videos go here
```

---

## License

MIT – free for personal and commercial use.  
You can sell the digital product this ad promotes.  
Attribution appreciated but not required.

---

Made with ❤️ for creators who want free, private, no-GPU video tools.
