from PIL import Image, ImageDraw
import random
import math
import copy

# Настройки
width, height = 400, 400
center_x, center_y = width // 2, height // 2
num_stars = 200
max_frames = 192  # ← Изменено: столько же кадров, сколько в space.gif
z_speed = 0.02
return_threshold = 5  # допустимая погрешность в пикселях

# Создание звёзд в 3D-пространстве
stars = []
for _ in range(num_stars):
    stars.append({
        "x": random.uniform(-1, 1),
        "y": random.uniform(-1, 1),
        "z": random.uniform(0.1, 1.0)
    })

initial_stars = copy.deepcopy(stars)
initial_screen_positions = []

frames = []

# Генерация кадров
for frame_index in range(max_frames):
    img = Image.new("RGB", (width, height), "black")
    draw = ImageDraw.Draw(img)
    new_stars = []

    for i, star in enumerate(stars):
        star["z"] -= z_speed
        if star["z"] <= 0.05:
            star = {
                "x": initial_stars[i]["x"],
                "y": initial_stars[i]["y"],
                "z": 1.0
            }

        sx = int(center_x + (star["x"] / star["z"]) * center_x)
        sy = int(center_y + (star["y"] / star["z"]) * center_y)

        if frame_index == 0:
            initial_screen_positions.append((sx, sy))

        if 0 <= sx < width and 0 <= sy < height:
            size = max(1, int((1 - star["z"]) * 5))
            brightness = int((1 - star["z"]) * 255)
            color = (brightness, brightness, brightness)
            draw.ellipse((sx - size, sy - size, sx + size, sy + size), fill=color)

        new_stars.append(star)

    stars = new_stars
    frames.append(img)

# Сохраняем GIF
frames[0].save(
    "space_warp_loop.gif",
    save_all=True,
    append_images=frames[1:],
    duration=50,  # 50 мс на кадр → 192 * 0.05 = 9.6 секунд
    loop=0
)

print(f"GIF сохранён: {len(frames)} кадров → space_warp_loop.gif")
