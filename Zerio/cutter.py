from PIL import Image

# Загружаем изображение игрока
input_path = "/mnt/data/player.png"
output_path = "/mnt/data/player_trimmed.png"

# Открываем изображение
image = Image.open(input_path)

# Автоматическая обрезка холста
trimmed_image = image.crop(image.getbbox())

# Сохраняем результат
trimmed_image.save(output_path)
print("Готово! Изображение сохранено в:", output_path)