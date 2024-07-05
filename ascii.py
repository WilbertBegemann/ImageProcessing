
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import math as m
import multiprocessing
import concurrent.futures
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import math as m
import concurrent.futures
from timeit import default_timer as timer   

def normal_dist(x, mean, std):
    return (1 / (std * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mean) / std) ** 2)

def forloop_image(img, empty_image, y, height, width, radius):
    widthpixels = []
    G_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    G_y = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]])
    
    for x in range(width):
        gx_r = gx_b = gx_g = gy_r = gy_b = gy_g = 0
        
        for i in range(-1, 2):
            for j in range(-1, 2):
                if 0 <= x + i < width and 0 <= y + j < height:
                    pixel = img.getpixel((x + i, y + j))
                    gx_r += G_x[i + 1][j + 1] * pixel[0]
                    gx_g += G_x[i + 1][j + 1] * pixel[1]
                    gx_b += G_x[i + 1][j + 1] * pixel[2]
                    gy_r += G_y[i + 1][j + 1] * pixel[0]
                    gy_g += G_y[i + 1][j + 1] * pixel[1]
                    gy_b += G_y[i + 1][j + 1] * pixel[2]
        
        x_a = (gx_r / 255 + gx_g / 255 + gx_b / 255) / 3
        y_a = (gy_r / 255 + gy_g / 255 + gy_b / 255) / 3
        grace = 0.15
        if abs(x_a) < grace and abs(y_a) < grace:
            widthpixels.append(" ")
        elif abs(x_a) < grace and abs(y_a) > grace:
            widthpixels.append("|")
        elif abs(y_a) < grace and abs(x_a) > grace:
            widthpixels.append("-")
        elif x_a > 0 and y_a > 0:
            widthpixels.append("\\")
        elif x_a < 0 and y_a < 0:
            widthpixels.append("\\")
        elif x_a > 0 and y_a < 0:
            widthpixels.append("/")
        elif x_a < 0 and y_a > 0:
            widthpixels.append("/")
        else:
            widthpixels.append(" ")
    
    return "".join(widthpixels)

def distance_image(image_path: str,character_amount:int,output:str) -> None:
    start = timer()
    
    radius = 1
    img = Image.open(image_path)
    std = 0.05
    oldwidth, oldheight = img.size
    scale = oldwidth / character_amount
    img = img.resize((int(oldwidth / scale), int(oldheight / scale)))
    width, height = img.size
    img = img.convert("RGB")
    empty_image = Image.new("RGB", (width, height), "white")
    
    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = {executor.submit(forloop_image, img, empty_image, y, height, width, radius): y for y in range(height)}
        
        results = {}
        for future in concurrent.futures.as_completed(futures):
            y = futures[future]
            results[y] = future.result()
    
    sorted_results = [results[x] for x in sorted(results.keys())]
    
    with open(f"{output}.txt", "w") as file:
        for line in sorted_results:
            file.write(line + "\n")
    
    empty_image = Image.new("RGB", (oldwidth, oldheight), "white")
    draw = ImageDraw.Draw(empty_image)
    font = ImageFont.truetype('GrescoTrial-Black.ttf', 8)
    placed = (-1, -1)
    for y in range(height):
        for x in range(width):
            if (x, y) != placed:
                draw.text((int(x*oldwidth/width), int(y*oldheight/height)), sorted_results[y][x], fill=(0, 0, 0), font=font)
                placed = (x, y)
    
    empty_image.save(f"{output}.jpg")
    
    print(timer() - start)

if __name__ == "__main__":
    multiprocessing.freeze_support()
    
    image_path = input("Enter the path to the image: ")
    character_amount = int(input("Amount of characters per width: "))
    output = input("Enter the output file name(don't add extentions): ")
    distance_image(image_path,character_amount,output)