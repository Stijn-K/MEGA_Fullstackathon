import time
from picamera2 import Picamera2 # apt install python3-picamera2


def ascii_image(image_array, width=80):
    """
    Convert an RGBA image array to ASCII art for terminal display
    """
    # Get dimensions of the image array
    height, img_width, channels = image_array.shape

    # Calculate aspect ratio and target height
    aspect_ratio = height / img_width
    target_height = int(width * aspect_ratio)
    if target_height > 100:  # Limit height for terminal display
        target_height = 100

    # Characters from dark to light
    chars = ' .:-=+*#%@'
    ascii_data = ''

    # Resize and convert to ASCII
    for y in range(target_height):
        # Map to source y coordinate
        source_y = min(int(y * height / target_height), height - 1)

        line = ''
        for x in range(width):
            # Map to source x coordinate
            source_x = min(int(x * img_width / width), img_width - 1)

            # Get RGB values (ignore alpha channel)
            r = int(image_array[source_y, source_x, 0])
            g = int(image_array[source_y, source_x, 1])
            b = int(image_array[source_y, source_x, 2])

            # Calculate brightness using standard luminance formula
            brightness = 0.299 * r + 0.587 * g + 0.114 * b

            # Map brightness to character
            char_idx = int(brightness / 255 * (len(chars) - 1))
            char_idx = max(0, min(char_idx, len(chars) - 1))  # Ensure valid index
            line += chars[char_idx]

        ascii_data += line + '\n'

    return ascii_data


def main():
    print("Initializing camera...")

    # Initialize the camera
    picam2 = Picamera2()
    config = picam2.create_preview_configuration(main={"size": (320, 240)})
    picam2.configure(config)
    picam2.start()

    # Give camera time to initialize
    time.sleep(2)

    try:
        print("Camera ready! Press Ctrl+C to exit.")

        while True:
            # Capture image
            image_data = picam2.capture_array()

            # Get terminal width
            term_width = 80

            # Convert to ASCII and display
            ascii_art = ascii_image(image_data, term_width)

            # Clear screen and display
            print("\033[2J\033[H")  # ANSI escape sequence to clear screen
            print(ascii_art)

            time.sleep(0.5)

    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        picam2.stop()
        print("Camera stopped.")


if __name__ == "__main__":
    main()