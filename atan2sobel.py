
from PIL import Image
import numpy as np
import math as m
import multiprocessing
import concurrent.futures
from timeit import default_timer as timer   
def normal_dist(x, mean, std):
    return (1 / (std * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mean) / std) ** 2)
def forloop_image(img,empty_image,x,height,width,radius):
    widthpixels = []
    G_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    G_y = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]])
    gx_r=0
    gx_b=0
    gx_g=0
    gy_r=0
    gy_b=0
    gy_g=0
    g_r=0.0
    g_b=0.0
    g_g=0.0
    for y in range(height):
        gx_r=0
        gx_b=0
        gx_g=0
        gy_r=0
        gy_b=0
        gy_g=0
        a=0
        b=0
        c=0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if x + i >= 0 and x + i < width and y + j >= 0 and y + j < height:
                    gx_r += G_x[2-(i+1)][2-(j+1)]*img.getpixel((x + i, y + j))[0]
                    gx_g += G_x[2-(i+1)][2-(j+1)]*img.getpixel((x + i, y + j))[1]
                    gx_b += G_x[2-(i+1)][2-(j+1)]*img.getpixel((x + i, y + j))[2]
                    gy_r += G_y[2-(i+1)][2-(j+1)]*img.getpixel((x + i, y + j))[0]
                    gy_g += G_y[2-(i+1)][2-(j+1)]*img.getpixel((x + i, y + j))[1]
                    gy_b += G_y[2-(i+1)][2-(j+1)]*img.getpixel((x + i, y + j))[2]
                    
                    a = m.sqrt(gx_r**2 + gy_r**2)
                    b = m.sqrt(gx_g**2 + gy_g**2)
                    c = m.sqrt(gx_b**2 + gy_b**2)
        widthpixels.append([int(m.atan2(gx_r,gy_r)*255), int(m.atan2(gx_g,gy_g)*255), int(m.atan2(gx_b,gy_b)*255)])
    return widthpixels

def distance_image(image_path:str,scale:int=1,output:str = "output")->None:
    """This function takes in an image path, scale and output file name and returns a new image with the sobel filter applied to it."""
    start = timer()
    scale = 1
    radius = 1
    img = Image.open(image_path)
    width, height = img.size
    img=img.resize((int(width/scale),int(height/scale)))
    width, height = img.size
    
    img = img.convert("RGB")
    
    empty_image = Image.new("RGB", (width, height), "white")
    pixels:list = np.zeros((width, height, 3))
    
    
    
    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = []
        results = []
        for x in range(width):
            future = executor.submit(forloop_image, img, empty_image, x, height, width, radius)
            results.append([x, future])
            futures.append(future)
            

        # Wait for all the futures to complete
        concurrent.futures.wait(futures)
        for result in results:
            x = result[0]
            for y in range(height):
                empty_image.putpixel((x, y), (result[1].result()[y][0], result[1].result()[y][1], result[1].result()[y][2]))
    print("calculation time:",timer()-start)
    empty_image.save(output)

if __name__ == "__main__":
    multiprocessing.freeze_support()
    image_path = input("Enter the path to the image: ")
    scale = int(input("Enter the scale: "))
    output = input("Enter the output file name: ")

    distance_image(image_path, scale, output)
    

