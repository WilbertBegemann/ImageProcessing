from PIL import Image
import numpy as np
import multiprocessing
import concurrent.futures
from timeit import default_timer as timer   
def normal_dist(x, mean, std):
    return (1 / (std * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mean) / std) ** 2)
def forloop_image(img,empty_image,x,height,width,radius):
    widthpixels = []
    for y in range(height):
            sum_r = 0
            sum_g = 0
            sum_b = 0
            std_r = []
            std_g = []
            std_b = []
            av_count = 0
            for i in range(-radius, radius + 1):
                for j in range(-radius, radius + 1):
                    if x + i >= 0 and x + i < width and y + j >= 0 and y + j < height:
                        av_count += 1
                        sum_r += img.getpixel((x + i, y + j))[0]/255
                        sum_g += img.getpixel((x + i, y + j))[1]/255
                        sum_b += img.getpixel((x + i, y + j))[2]/255
                        std_r.append(img.getpixel((x + i, y + j))[0]/255)
                        std_g.append(img.getpixel((x + i, y + j))[1]/255)
                        std_b.append(img.getpixel((x + i, y + j))[2]/255)
            sum_r = int(sum_r/(av_count*av_count))
            sum_g = int(sum_g/(av_count*av_count))
            sum_b = int(sum_b/(av_count*av_count))
            mean_r = img.getpixel((x, y))[0]/255
            mean_g = img.getpixel((x, y))[1]/255
            mean_b = img.getpixel((x, y))[2]/255
            change = 0.000005
            s_r = np.std(std_r)
            s_g = np.std(std_g)
            s_b = np.std(std_b)
            if s_r != 0 and np.std(std_g) != 0 and np.std(std_b) != 0:
                
                if normal_dist(sum_r, mean_r, s_r) > s_r:
                    sum_r = 0
                else:
                    sum_r = 255
                if normal_dist(sum_g, mean_g, s_g) > s_g:
                    sum_g = 0
                else:
                    sum_g = 255
                if normal_dist(sum_b, mean_b, s_b) > s_b:
                    sum_b = 0
                else:
                    sum_b = 255
            widthpixels.append([sum_r, sum_g, sum_b])
    return widthpixels

def distance_image(image_path:str)->None:
    start = timer()
    radius:int = 1
    scale = 1
    img = Image.open(image_path)
    std = 0.05
    width, height = img.size
    img=img.resize((int(width/scale),int(height/scale)))
    width, height = img.size
    print(f"Image size: {width}x{height}")
    img = img.convert("RGB")
    print(f"Image mode: {img}")
    empty_image = Image.new("RGB", (width, height), "white")
    pixels:list = np.zeros((width, height, 3))
    
    
    
    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = []
        results = []
        for x in range(width):
            future = executor.submit(forloop_image, img, empty_image, x, height, width, radius)
            results.append([x, future])
            futures.append(future)
            print(f"progress: {x}/{width}")

        # Wait for all the futures to complete
        concurrent.futures.wait(futures)
        for result in results:
            x = result[0]
            for y in range(height):
                empty_image.putpixel((x, y), (result[1].result()[y][0], result[1].result()[y][1], result[1].result()[y][2]))
    print(timer()-start)
    empty_image.save("output.jpg")

if __name__ == "__main__":
    multiprocessing.freeze_support()
    distance_image("noise.jpg")
    

