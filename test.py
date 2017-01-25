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

def seam_tester(image, direction_grid):
    width, height = image.size
    for x in range(1, width, 3):
        y = height-1
        draw_seam(image, (x, y), direction_grid)

def draw_seam(image, start_point, direction_grid):
    cur_point = start_point
    while direction_grid[cur_point[1]][cur_point[0]] != 0:
        image.putpixel(cur_point, (255,0,0))

        if direction_grid[cur_point[1]][cur_point[0]] == 1:
            cur_point = (cur_point[0]-1, cur_point[1]-1)
        elif direction_grid[cur_point[1]][cur_point[0]] == 2:
            cur_point = (cur_point[0], cur_point[1]-1)
        else: # 3
            cur_point = (cur_point[0]+1, cur_point[1]-1)
    return image

def seam_search_vertical(partial_grid):

    width = len(partial_grid[0])
    height = len(partial_grid)
    cost_grid = [[None for _ in range(width)] for _ in range(height)]
    direction_grid = [[0 for _ in range(width)] for _ in range(height)]

    # Populate first row
    for x in range(width):
        y = 0
        cost_grid[y][x] = partial_grid[y][x]
        direction_grid[y][x] = 0 # END OF PATH

    for y in range(1, height):
        for x in range(width):
            if x == 0:
                min_parent = 2
                min_cost = cost_grid[y-1][x]
                if cost_grid[y-1][x+1] < min_cost:
                    min_parent = 3
                    min_cost = cost_grid[y-1][x+1]
            elif x == width - 1:
                min_parent = 1
                min_cost = cost_grid[y-1][x-1]
                if cost_grid[y-1][x] < min_cost:
                    min_parent = 2
                    min_cost = cost_grid[y-1][x]
            else:
                min_parent = 1
                min_cost = cost_grid[y-1][x-1]
                if cost_grid[y-1][x] < min_cost:
                    min_parent = 2
                    min_cost = cost_grid[y-1][x]
                if cost_grid[y-1][x+1] < min_cost:
                    min_parent = 3
                    min_cost = cost_grid[y-1][x+1]

            cost_grid[y][x] = partial_grid[y][x] + min_cost
            direction_grid[y][x] = min_parent

    return cost_grid, direction_grid
    # for x in range(width):
        # y = height - 1
        # if cost_grid[y][x] < cur_min
            # min_index = x




