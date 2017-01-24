from PIL import Image

img = Image.open("dolphin-05.jpg")

def pixel_diff(p1, p2):
    # Sum of sq differences
    return pow(p1[0] - p2[0], 2) + pow(p1[1] - p2[1], 2) + pow(p1[2] - p2[2], 2)

def normalize_grid(grid):
    # http://stats.stackexchange.com/questions/70801/how-to-normalize-data-to-0-1-range
    # Must have some values
    min_val = min([min(line) for line in grid])
    max_val = max([max(line) for line in grid])
    width = len(grid[0])
    height = len(grid)
    normalized = [["" for _ in range(width)] for _ in range(height)]
    for y in range(height):
        for x in range(width):
            # TODO REMOVE SCALE
            normalized[y][x] = 255*(float(grid[y][x] - min_val) / (max_val - min_val))
    return normalized

def greyscale(grid):
    width = len(grid[0])
    height = len(grid)
    image = Image.new("RGB", (width, height))
    for y in range(height):
        for x in range(width):
            val = int(grid[y][x])
            image.putpixel((x,y), (val,val,val))
    return image

def partial_derivative_x(image):
    width, height = image.size
    dx_grid = [[-1 for _ in range(width)] for _ in range(height)]
    for y in range(height):
        for x in range(width):
            # print(x,y)
            if x == 0:
                current = image.getpixel((x,y))
                compare = image.getpixel((x+1,y))
            else:
                current = image.getpixel((x,y))
                compare = image.getpixel((x-1,y))

            dx = pixel_diff(current, compare)
            dx_grid[y][x] = dx
    return dx_grid

def partial_derivative_y(image):
    width, height = image.size
    dx_grid = [[-1 for _ in range(width)] for _ in range(height)]
    for y in range(height):
        for x in range(width):
            if y == 0:
                current = image.getpixel((x,y))
                compare = image.getpixel((x,y+1))
            else:
                current = image.getpixel((x,y))
                compare = image.getpixel((x,y-1))

            dx = pixel_diff(current, compare)
            dx_grid[y][x] = dx
    return dx_grid
