# Define function to draw keypoints and connections

import cv2
import mediapipe as mp
mp_pose = mp.solutions.pose

def draw_keypoints_and_connections(image, landmarks, mode):
    # Get image dimensions
    height, width, _ = image.shape
    # Initialize list to the landmarks pixel coordinates
    landmark_points = []
    for landmark in landmarks:
        landmark_point = (int(landmark.x * width), int(landmark.y * height))
        landmark_points.append(landmark_point)

    # Define connections for 'all' mode, excluding face and hand landmarks
    connections_all = []
    for conn in mp_pose.POSE_CONNECTIONS:
        exclude = False
        for lm in conn:
            if lm in range(0, 11) or lm in range(17, 23):
                exclude = True
                break
        if not exclude:
            connections_all.append(conn)

  
    # Define connections for 'right' mode
    connections_right = [
        (mp_pose.PoseLandmark.RIGHT_SHOULDER, mp_pose.PoseLandmark.RIGHT_HIP),
        (mp_pose.PoseLandmark.RIGHT_HIP, mp_pose.PoseLandmark.RIGHT_KNEE),
        (mp_pose.PoseLandmark.RIGHT_KNEE, mp_pose.PoseLandmark.RIGHT_HEEL),
        (mp_pose.PoseLandmark.RIGHT_HEEL, mp_pose.PoseLandmark.RIGHT_FOOT_INDEX)
    ]
    # Define connections for 'left' mode
    connections_left = [
        (mp_pose.PoseLandmark.LEFT_SHOULDER, mp_pose.PoseLandmark.LEFT_HIP),
        (mp_pose.PoseLandmark.LEFT_HIP, mp_pose.PoseLandmark.LEFT_KNEE),
        (mp_pose.PoseLandmark.LEFT_KNEE, mp_pose.PoseLandmark.LEFT_HEEL),
        (mp_pose.PoseLandmark.LEFT_HEEL, mp_pose.PoseLandmark.LEFT_FOOT_INDEX)
    ]

    # Determine which keypoints and connections to draw
    keypoints_to_draw = set()
    connections_to_draw = []

    # Add keypoints and connections to draw based on the mode
    if mode == 'all':
        for idx in range(11, 17):
            keypoints_to_draw.add(idx)
        for idx in range(23, 33):
            keypoints_to_draw.add(idx)
        connections_to_draw = connections_all

    elif mode == 'right':
        for connection in connections_right:
            keypoints_to_draw.add(connection[0])
            keypoints_to_draw.add(connection[1])
        connections_to_draw = connections_right

    elif mode == 'left':
        for connection in connections_left:
            keypoints_to_draw.add(connection[0])
            keypoints_to_draw.add(connection[1])
        connections_to_draw = connections_left

    # Draw the connections
    for connection in connections_to_draw:
        start_point = landmark_points[connection[0]]
        end_point = landmark_points[connection[1]]
        cv2.line(image, start_point, end_point, (245,117,66), 2)

    # Draw the keypoints
    for idx in keypoints_to_draw:
        point = landmark_points[idx]
        cv2.circle(image, point, 2, (245,66,230), thickness=-1)