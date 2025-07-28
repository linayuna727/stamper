import os
import argparse
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont, ExifTags

# Configuration
COLOR_PRESETS = {
    # "preset_name": (text_color, outline_color)
    "orange": ("#FFA500", "#000000"), # Orange text with black outline
    "yellow": ("#FFFF00", "#000000"), # Yellow text with black outline
    "purple": ("#E0B0FF", "#4D0082"), # Lighter purple with dark purple outline
    "green": ("#B0FFB0", "#005000"),  # Light green with dark green outline
    "blue": ("#B0E0FF", "#000082"),   # Light blue with dark blue outline
    "white": ("#FFFFFF", "#000000"),  # White text with black outline
    "black": ("#000000", "#FFFFFF"),  # Black text with white outline
}
DEFAULT_COLOR_PRESET = "orange"
OUTPUT_DIR = "stamped"
FONT_FILE = "fonts/OpenSans-Bold.ttf"

def get_image_timestamp(image_path, stamp_format='both'):
    """Extracts and formats the timestamp from image EXIF data or file metadata."""
    dt = None
    try:
        with Image.open(image_path) as img:
            exif_data = img.getexif()
            if exif_data:
                for tag, value in exif_data.items():
                    tag_name = ExifTags.TAGS.get(tag, tag)
                    if tag_name == 'DateTimeOriginal':
                        dt = datetime.strptime(value, '%Y:%m:%d %H:%M:%S')
                        break
    except Exception:
        pass  # Fallback to file modification time

    if not dt:
        try:
            mtime = os.path.getmtime(image_path)
            dt = datetime.fromtimestamp(mtime)
        except Exception:
            return "No timestamp"

    formats = {
        'date': '%d.%m.%Y',
        'time': '%H:%M',
        'both': '%d.%m.%Y %H:%M'
    }
    return dt.strftime(formats.get(stamp_format, 'both'))


def add_timestamp_to_image(image_path, color, outline_color, stamp_format, font_size_ratio, position):
    """Adds a timestamp to a single image."""
    timestamp_text = get_image_timestamp(image_path, stamp_format)
    print(f"Processing {os.path.basename(image_path)} -> Stamp: {timestamp_text}")

    try:
        with Image.open(image_path).convert("RGBA") as base:
            txt = Image.new("RGBA", base.size, (255, 255, 255, 0))

            W, H = base.size
            font_size = int(W / font_size_ratio)
            stroke_width = int(W / 800)
            
            # Adjusted padding calculation to move text higher
            # Base padding from the edge, then additional lift
            base_padding = int(W / 30) # A consistent base padding
            vertical_lift = int(font_size * 0.25) # Lift by 25% of font height
            padding = base_padding + vertical_lift

            try:
                font = ImageFont.truetype(FONT_FILE, font_size)
            except IOError:
                print(f"Warning: Font not found at {FONT_FILE}. Using default font.")
                font = ImageFont.load_default()

            draw = ImageDraw.Draw(txt)

            # Determine position
            x, y, anchor = 0, 0, ""
            if position == 'bottom-right':
                x, y, anchor = W - padding, H - padding, "rs"
            elif position == 'bottom-left':
                x, y, anchor = padding, H - padding, "ls"
            elif position == 'top-right':
                x, y, anchor = W - padding, padding, "ra"
            elif position == 'top-left':
                x, y, anchor = padding, padding, "la"

            # Draw outline
            if outline_color:
                draw.text((x, y), timestamp_text, font=font, fill=outline_color, stroke_width=stroke_width, anchor=anchor)
            # Draw main text
            draw.text((x, y), timestamp_text, font=font, fill=color, anchor=anchor)

            out = Image.alpha_composite(base, txt)

            output_filename = os.path.join(OUTPUT_DIR, os.path.basename(image_path))
            out.convert("RGB").save(output_filename)

    except Exception as e:
        print(f"Error processing {image_path}: {e}")


def main():
    parser = argparse.ArgumentParser(description="Add a timestamp to photos.")
    parser.add_argument("path", help="Path to an image file or a directory of images.")
    parser.add_argument("--preset", help=f"Color preset to use. Available: {', '.join(COLOR_PRESETS.keys())} (default: {DEFAULT_COLOR_PRESET}).", default=DEFAULT_COLOR_PRESET, type=str.lower)
    parser.add_argument("--color", help="Custom text color (hex code, e.g., '#FF0000'). Overrides preset. (default: None)", default=None)
    parser.add_argument("--outline-color", help="Custom outline color (hex code). Overrides preset. (default: None)", default=None)
    parser.add_argument("--format", help=f"Timestamp format. Choices: {', '.join(['both', 'date', 'time'])} (default: both).", choices=['both', 'date', 'time'], default='both', type=str.lower)
    parser.add_argument("--size", help=f"Text size (ratio to image width, e.g., 50 for 1/50th). A smaller number means larger text. (default: 50).", type=int, default=50)
    parser.add_argument("--position", help=f"Timestamp position. Choices: {', '.join(['bottom-right', 'bottom-left', 'top-right', 'top-left'])} (default: bottom-right).", choices=['bottom-right', 'bottom-left', 'top-right', 'top-left'], default='bottom-right', type=str.lower)

    args = parser.parse_args()

    # Determine colors
    final_color = args.color
    final_outline_color = args.outline_color

    if not final_color: # If no custom color, use preset
        if args.preset not in COLOR_PRESETS:
            print(f"Error: Color preset '{args.preset}' not found. Using default.")
            args.preset = DEFAULT_COLOR_PRESET
        final_color, final_outline_color = COLOR_PRESETS[args.preset]

    # Custom outline color overrides preset or default
    if args.outline_color:
        final_outline_color = args.outline_color

    # Create output directory
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"Created directory: {OUTPUT_DIR}")

    if os.path.isdir(args.path):
        print(f"Processing all images in directory: {args.path}")
        for filename in os.listdir(args.path):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                image_path = os.path.join(args.path, filename)
                add_timestamp_to_image(image_path, final_color, final_outline_color, args.format, args.size, args.position)
    elif os.path.isfile(args.path):
        add_timestamp_to_image(args.path, final_color, final_outline_color, args.format, args.size, args.position)
    else:
        print(f"Error: Path not found - {args.path}")

    print("\nComplete!")

if __name__ == "__main__":
    main()
