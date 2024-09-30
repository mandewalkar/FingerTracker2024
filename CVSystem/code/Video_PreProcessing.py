
import cv2
import numpy as np
import os
import shutil
import sys
import math

def main(video_name, fps):
    # Define the path to the input video file here:
    current_directory = os.getcwd()
    video_file_name = os.path.join(current_directory, 'data', video_name)
    #video_file_name = os.path.join(r'C:\Users\parni\Desktop\Research\FingerTracker24\CVSystem\data', video_name)
    print(video_file_name)

    # Mouse callback function to capture corner points
    def mouse_callback(event, x, y, flags, params):
        if event == cv2.EVENT_LBUTTONDOWN:
            if len(params['points']) < 4:
                params['points'].append((x, y))
                cv2.circle(params['img'], (x, y), 5, (0, 255, 0), -1)
                cv2.imshow('Select Corners', params['img'])
    
    #function to extend frame for better hand detection
    def extend_frame(points, extender):
        #extend left boundary up calculate its line
        m1 = (points[2][1] - points[0][1]) / (points[2][0] - points[0][0])
        b1 = points[2][1] - m1 * points[2][0]
        new_x0 = points[0][0] + extender
        new_y0 = new_x0 * m1 + b1
        #calculate distance of new point from old point
        dist = new_y0 - points[0][1]
        #calculate top extended line
        m5 = (points[1][1] - points[0][1]) / (points[1][0] - points[0][0])
        b5 = (points[1][1] - m5 * points[1][0]) + dist
        #calculate right line
        m3 = (points[3][1] - points[1][1]) / (points[3][0] - points[1][0])
        b3 = (points[3][1] - m3 * points[3][0])
        #calculate intersection of line 5 and line 3
        new_x1 = (b5 - b3) / (m3 - m5)
        new_y1 = m3 * new_x1 + b3
        return [(new_x0,new_y0),(new_x1,new_y1),points[2],points[3]]
    
    # Read input video
    cap = cv2.VideoCapture(video_file_name)

    # Get first frame to select corners
    ret, frame = cap.read()
    if not ret:
        print('Error reading video file')
        exit()

    # Display the first frame for corner selection
    cv2.namedWindow('Select Corners', cv2.WINDOW_NORMAL)
    cv2.imshow('Select Corners', frame)
    corner_points = []
    cv2.setMouseCallback('Select Corners', mouse_callback, {'img': frame, 'points': corner_points})
    cv2.waitKey(0)

    # Close the window after corner selection
    cv2.destroyAllWindows()

    # Define source and destination points for the perspective transform
    print(corner_points)
    new_pts = extend_frame(corner_points, 50)
    print(new_pts)
    src = np.float32(new_pts)
    #dst = np.float32([[0, 0], [1024, 0], [0, 768], [1024, 768]])
    dst = np.float32([[0, 0], [1024, 0], [0, 868], [1024, 868]])

    # Compute perspective transform matrix
    M = cv2.getPerspectiveTransform(src, dst)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    #out = cv2.VideoWriter('./transformed_video.mp4', fourcc, fps, (1024,768))
    out = cv2.VideoWriter('./transformed_video.mp4', fourcc, fps, (1024,868))  


    # Loop through all frames of the video
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Apply the perspective transform to the current frame
        transformed_frame = cv2.warpPerspective(frame, M, (1024, 868))
        # transformed_frame = cv2.warpPerspective(frame, M, (1024, 768))
        transformed_frame = cv2.flip(transformed_frame,1)
        out.write(transformed_frame)

        # Display the transformed frame
        cv2.imshow('Transformed Video', transformed_frame)
        #print("writing transformed video")
    

        # Exit if 'q' is pressed
        if cv2.waitKey(1) == ord('q'):
            break

    # Release resources
    cap.release()
    out.release()
    cv2.destroyAllWindows()

    #move file
    current_directory = os.getcwd()
    destination_path = os.path.join(current_directory, 'output_logs')

    if not os.path.exists(destination_path):
        os.makedirs(destination_path)

    shutil.move('transformed_video.mp4', os.path.join(destination_path, 'transformed_video.mp4'))



if __name__ == '__main__':
    command_line_arguments = sys.argv[1:] #argument 0 is video file name and argument 1 is fps and arg 2 is touchscreen file name
    main(command_line_arguments[0], 30)
