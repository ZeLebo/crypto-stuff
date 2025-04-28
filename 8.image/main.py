from PIL import Image

def pixel_embed(pixel, binary_message, idx):
    r, g, b = pixel

    if idx < len(binary_message):
        r = (r & ~1) | int(binary_message[idx])
        idx += 1
    if idx < len(binary_message):
        g = (g & ~1) | int(binary_message[idx])
        idx += 1
    if idx < len(binary_message):
        b = (b & ~1) | int(binary_message[idx])
        idx += 1

    return (r, g, b), idx

def embed_message(image_path, text, output_path):
    img = Image.open(image_path).convert('RGB')
    pixels = img.load()

    binary_message = ''.join(f'{ord(c):08b}' for c in text)
    binary_message += '00000000'  # null-byte

    width, height = img.size
    total_pixels = width * height

    if len(binary_message) > total_pixels * 3:
        raise ValueError("Сообщение слишком длинное для этого изображения.")

    idx = 0
    for x, y in ((x, y) for y in range(height) for x in range(width)):
        if idx >= len(binary_message):
            break
        pixels[x, y], idx = pixel_embed(pixels[x, y], binary_message, idx)

    img.save(output_path, format='PNG')

def extract_message(image_path):
    img = Image.open(image_path)
    img = img.convert('RGB')
    pixels = img.load()

    width, height = img.size

    bits = ''
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            bits += str(r & 1)
            bits += str(g & 1)
            bits += str(b & 1)

    chars = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        if len(byte) < 8:
            break
        ascii_code = int(byte, 2)
        if ascii_code == 0:
            break
        chars.append(chr(ascii_code))

    return ''.join(chars)

input_path = '8.image/blank.png'
output_path = '8.image/output.png'
message = 'Super secret message'

embed_message(input_path, message, output_path)
extracted = extract_message(output_path)
assert extracted == message, "Messages are different"
print(extracted)

try:
    embed_message(input_path, message * 100_000, output_path)
except ValueError as e:
    print(e)