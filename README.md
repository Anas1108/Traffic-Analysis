# Traffic Analysis in a Video

## Introduction
This project aims to develop a program that can accurately count the number of vehicles moving on a road in a given video and classify the traffic as high, low, or medium based on the count. 

## Requirements
To run this program, the following software and packages are required:
* Python 3.x
* OpenCV
* Numpy
* Matplotlib

## Usage
1. Clone the repository
- git clone https://github.com/Anas1108/Traffic-Analysis.git

2. Install required packages
- pip install opencv-python numpy matplotlib

3. Run the program
- python main.py --video path/to/video.mp4
Replace `path/to/video.mp4` with the actual path to the video file.

4. Results
The program will display the total number of vehicles in the video and classify the traffic as high, low, or medium. The classification criteria are as follows:
- High Traffic: Total vehicle count greater than or equal to 100
- Medium Traffic: Total vehicle count between 50 and 99
- Low Traffic: Total vehicle count less than 50

## Conclusion
This program can be useful in analyzing traffic patterns in busy areas and providing insights for traffic management. Further improvements can be made to increase accuracy and add more sophisticated traffic analysis features.
