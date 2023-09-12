import random
import math
from PIL import Image, ImageDraw

points_per_area = 70
chunk_in_canvas = 7
canvas_points_radius = 70
chunk_radius = 60
node_radius = 5
big_node_radius = 10

width = 512
height = 512
canvas = Image.new('RGB', (width, height), (255, 255, 255))
draw = ImageDraw.Draw(canvas)

def overlap_check(points, cur_point, radius):
    for point in points:
        x1, y1, x2, y2 = point[0], point[1], cur_point[0], cur_point[1]
        dist = math.dist([x1,y1], [x2,y2])
        #print(dist)
        r = radius * 2
        #print(dist, r)
        if dist < r:
            return True
    return False

def generate_points_in_circle_area(start, end):
    x1, y1, x2, y2 = start[0], start[1], end[0], end[1]
    points = []
    cnt = 0
    #middle points as pivot for the circular distribution
    xc = (x1 + x2) // 2
    yc = (y1 + y2) // 2
    
    while cnt < points_per_area:
        print(x1, x2, y1, y2)
        if x1 > x2:
            xa, ya = x1, y1
            x1, y1 = x2, y2
            x2, y2 = xa, ya
        x = random.randint(x1, x2)
        y = random.randint(y1, y2)
        #Check if the points overlap each other and make sure that have circular distribution
        if overlap_check(points, (x, y), node_radius) == False and is_inside_circle((x,y), (xc, yc)):
            print(x,y)
            points.append((x, y))
            #draw.ellipse((x - node_radius, y - node_radius, x + node_radius, y + node_radius), fill=(255, 0, 0), outline="black")
            cnt+=1
    return points


def draw_point(x, y, radius):
    r = random.randint(0,6)
    draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=(
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255)
    ), outline="white")

def is_inside_circle(point, center):
    x, y, xc, yc = point[0], point[1], center[0], center[1]
    z = (x - xc)**2 + (y - yc)**2
    z = math.sqrt(z)
    if z < chunk_radius:
        return True
    return False

def generate_points_in_canvas(start, end):
    x1, y1, x2, y2 = start[0], start[1], end[0], end[1]
    points = []
    cnt = 0
    
    while cnt < chunk_in_canvas:
        x = random.randint(x1, x2)
        y = random.randint(y1, y2)
        print(x,y)
        #Check if the points overlap each other and make sure that have circular distribution
        #print(x,y)
        if overlap_check(points, (x, y), canvas_points_radius) == False:
            points.append((x, y))
            cnt+=1
    return points

def classify_points_and_areas(canvas_points):
    points = []
    areas = []
    for point in canvas_points:
        r = random.randint(0,1)
        x, y = point[0], point[ 1]
        if r == 0:
            points.append((x, y))
        else:
            areas.append((x, y))
    return [points, areas]

def generate_areas(points):
    areas = []
    for point in points:
        x, y = point[0], point[1]
        x1 = x + chunk_radius
        y1 = y + chunk_radius
        x2 = x - chunk_radius
        y2 = y - chunk_radius
        areas.append([(x1, y1),(x2, y2)])
    return  areas

def draw_lines_between_points_and_chunk(points_area, big_points):
    print("hddd")
    print(big_points)
    for area_point in points_area:
        
        for point in area_point:
        
            for big_point in big_points:
                start = (point[0], point[1])
                end = (big_point[0], big_point[1])
                draw.line([start, end], fill=(0, 0, 0), width=1)
#generate points inside canvas
canvas_points = generate_points_in_canvas((chunk_radius, chunk_radius), (width - chunk_radius, height - chunk_radius))
print(canvas_points)
points, areas_p = classify_points_and_areas(canvas_points)
print(points, areas_p)
areas = generate_areas(areas_p)

points_area = []
big_points = []

for area in areas:
    start = area[0]
    end = area[1]
    print(start, end)
    points_area.append(generate_points_in_circle_area(start, end))

for point in points:
    x, y = point[0], point[1]
    #draw_point(x, y, big_node_radius)
    big_points.append((x,y))

draw_lines_between_points_and_chunk(points_area, big_points)

for point in points:
    x, y = point[0], point[1]
    draw_point(x, y, big_node_radius)
  
for area_point in points_area:
        for point in area_point:
            x, y = point[0], point[1]
            draw_point(x, y, node_radius)

#draw_points_in_circle_area((0,0),(300,300))
# Save the graph as a PPM image
canvas.save('random_art.ppm', 'PPM')
print("Random art image (512x512) saved as 'graph_network.ppm'")
#if __name__ == "__main__":
    
