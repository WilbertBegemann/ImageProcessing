# What is this project about
This project is for me to learn about image processing, although it is not optimized for the GPU, it can run on multiple cores on the CPU.


# What do you need to run
- python 3
- pip install pillow
- pip install numpy

# How to run
```
    python3 gaussian.py
```
or
```
    python3 sobel.py
```
or
```
    python3 atan2sobel.py
```
# estimated run time
+-4 seconds with Black_Circle.jpg
# Results
## Input Image
![alt text](https://github.com/WilbertBegemann/ImageProcessing/blob/main/Black_Circle.jpg?raw=true)
## atan2sobel.py result
![alt text](https://github.com/WilbertBegemann/ImageProcessing/blob/main/atan2sobel.jpg?raw=true)
## sobel.py result
![alt text](https://github.com/WilbertBegemann/ImageProcessing/blob/main/sobel.jpg?raw=true)
## gaussian.py result
![alt text](https://github.com/WilbertBegemann/ImageProcessing/blob/main/gaussian.jpg?raw=true)
## ascii.py result
![alt text](https://github.com/WilbertBegemann/ImageProcessing/blob/main/ascii.png?raw=true)
```
/------------------------------\
|                              |
|                              |
|           ///--\\\           |
|        ///////-\\\\\\        |
|       ///////--\\\\\\\       |
|      //////      \\\\\\      |
|     /////          \\\\\     |
|    /////            \\\\\    |
|   /////              \\\\\   |
|   ////                \\\\   |
|   ///                  \\\   |
|  ////                  \\\\  |
|  ///|                   \\\  |
|  |//                    \\\  |
|  |||                    |||  |
|  |\\                    ///  |
|  \\\\                   ///  |
|  \\\\                  ////  |
|   \\\                  ///   |
|   \\\\                ////   |
|    \\\\              /////   |
|    \\\\\            /////    |
|     \\\\\          /////     |
|      \\\\\\-     //////      |
|       \\\\\\\--///////       |
|         \\\\\\///////        |
|           \\\--///           |
|                              |
|                              |
\------------------------------/
```