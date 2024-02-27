# Kopernikus_data_cleanup_task

## Question and Answers

1. What did you learn after looking on our dataset?
--> The dataset consists of set of images from a parking garage taken from different cameras at different time of the day. The pictures seem to be taken at a resolution of 1080p (1920x1080), although the pictures from the camera c10 have been downsized to 640x480 (except for one). There is a mismatch of resolution among the images. This makes some form of pre processing necessary to be able to work with this dataset.

2. How does you program work?
--> This program loads images from a folder, preprocesses them by converting to grayscale and resizing, and then compares each image with the previous one. If the images are too similar based on a predefined threshold, the program removes the current image. If not, it updates the reference image for the next comparison. Finally, it returns a list of removed image filenames.

3. What values did you decide to use for input parameters and how did you find these values?
--> Minimum contour area was one of the parameters that was used in the compare_frames_change_detection function. I set it to value of 900, as I thought a contours size of 30x30 pixels would make sense to measure the changes in the image of size 640x480. One more parameter was added in the program that can be passed as an argument, and that is the threshold for similarity score between the images. Some images were tesetd based on how they looked and based on similarity a threshold of 10000 was chosen, which meant that similar looking images had score of less than  10000 and were deleted from the folder.

4. What you would suggest to implement to improve data collection of unique cases in future?
--> One improvement that I can think of is to program the data collection pipelines in a manner that we don't capture the data at 30 frames per second, or if we do then intentionally drop some frames, because these consecutive frames would look mostly identical and won't have much learning potential for the network. Getting rid of these frames during data genration would make the entire data processing pipline more efficient.
