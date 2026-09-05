import random
from PIL import Image, ImageDraw, ImageFilter, ImageFont

def merge(c1, c2):
    return tuple(round((a + b) / 2) for a, b in zip(c1, c2))

def nudge(c1, amount):
    return tuple(min(255, max(0, a + int((random.random() - 0.5) * 2 * amount))) for a in c1)

START_COLOR = (80, 0, 120)
WIDTH, HEIGHT = 1024, 1024
SQUARE_WIDTH = 4
NUDGE_AMOUNT = 12

def main() -> None:
    seed_input = input("Enter seed (or leave blank for random): ")
    seed = int(seed_input) if seed_input else random.randint(0, 2**32 - 1)
    random.seed(seed)

    image = Image.new("RGBA", (WIDTH, HEIGHT), (255, 255, 255, 255))
    draw = ImageDraw.Draw(image)

    squares = []

    for i in range(0, WIDTH // SQUARE_WIDTH):
        row = []
        for j in range(0, HEIGHT // SQUARE_WIDTH):
            left_color = nudge(START_COLOR, NUDGE_AMOUNT) if i == 0 else squares[i - 1][j]
            top_color = nudge(START_COLOR, NUDGE_AMOUNT) if j == 0 else row[j - 1]
            new_color = merge(left_color, top_color)
            new_color = nudge(new_color, NUDGE_AMOUNT)
            row.append(new_color)
        squares.append(row)

    for i in range(0, WIDTH // SQUARE_WIDTH):
        for j in range(0, HEIGHT // SQUARE_WIDTH):
            color = squares[i][j]
            bounds = [i * SQUARE_WIDTH, j * SQUARE_WIDTH, (i + 1) * SQUARE_WIDTH, (j + 1) * SQUARE_WIDTH]
            draw.rectangle(bounds, fill=color)

    image.save("pfp.png")
    print("Image saved as pfp.png. Seed used:", seed)
