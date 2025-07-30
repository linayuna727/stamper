# Stamper
 
A Python script to add timestamps to photos, reminiscent of old digital cameras from the early 2010's. It extracts date and time information from image EXIF data or file metadata.
 
## Features
 
- Extracts `DateTimeOriginal` from image EXIF data.
- Falls back to file modification time if EXIF data is unavailable.
- Customizable text and outline colors via presets or hexadecimal codes.
- Utilizes a bold sans-serif font for a clear, authentic digital camera aesthetic.
- Adjustable timestamp size and position. Padding is automatically managed.
- Processes individual image files or all images within a specified directory.
- Creates a `stamped` directory for output images.
 
## Installation
 
1.  **Obtain the Project:** Clone this repository or download the project files.
     ```bash
     git clone https://github.com/linayuna727/stamper
     ```
 
2.  **Install Dependencies:** The `Pillow` library is required for image processing.
 
     ```bash
     pip install pillow
     ```

> [!WARNING]
> Major Linux distributions (like Debian, Fedora and archlinux) don't allow installing Python modules this way. For instance, on Debian, you'll have to install it via `apt` (`sudo apt install pillow`) instead.
>
> If your distribution doesn't have a package for `pillow`, you can always create a virtual environment (`python3 -m venv venv`) and use that (`source venv/bin/activate`) to install Python packages. Remember that doing it this way will require you to enter that virtual environment every time you want to use the script.

## Usage
 
Execute the script from your terminal.
 
### Basic Usage
 
To process all images in the current directory with default settings (orange text with black outline, bottom-right position, and default scaling):
 ```bash
 python timestamper.py .
 ```
 
To process a specific image file:
 ```bash
 python timestamper.py /path/to/your/image.jpg
 ```
 
 ### Customizing Colors
 
 You can customize the timestamp's appearance using predefined color presets or by providing custom hexadecimal color codes.
 
 **Using a Color Preset:**
 ```bash
 python timestamper.py . --preset purple
 ```
 **Available Color Presets:** `orange`, `yellow`, `purple`, `green`, `blue`, `white`, `black`
 
 **Using Custom Hexadecimal Colors:**
 ```bash
 python timestamper.py . --color "#FF00FF" --outline-color "#330033"
 ```
 *Note: If a custom `--color` is specified, you can also provide `--outline-color`. If no `--outline-color` is provided, a black outline will be used by default.*
 
 ### Customizing Size and Position
 
 You can adjust the size and position of the timestamp. Padding is handled automatically based on font size and image dimensions.
 
 **Adjusting Size:**
 ```bash
 python timestamper.py . --size 60
 ```
 *`--size` controls the inverse ratio of the font size to the image width. A smaller numerical value results in larger text (default: 50).*
 
 **Changing Position:**
 ```bash
 python timestamper.py . --position top-left
 ```
 **Available Positions:** `bottom-right` (default), `bottom-left`, `top-right`, `top-left`
 
 ### Customizing the Timestamp Format
 
 You can control the information displayed in the timestamp.
 
 **Using a Format Preset:**
 ```bash
 python timestamper.py . --format date
 ```
 **Available Formats:**
 - `both` (default): Displays both date and time (e.g., `27.10.2023 14:30`)
 - `date`: Displays only the date (e.g., `27.10.2023`)
 - `time`: Displays only the time (e.g., `14:30`)
