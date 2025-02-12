import cv2
import cv2.aruco as aruco

# Initialize the video capture from the default camera
cap = cv2.VideoCapture(0)

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

# Specify the dictionary
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_APRILTAG_36h11)  # Adjust dictionary as needed
parameters = aruco.DetectorParameters()

# Flag to indicate detection
tag_detected = False

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect the markers in the image
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

    if ids is not None:
        tag_detected = True  # Set the flag
        for i, corner in zip(ids, corners):
            # Flatten the corner points array
            corner = corner.reshape((4, 2))
            # Convert to integers
            corner = corner.astype(int)

            # Draw the bounding box around the detected AprilTag
            cv2.polylines(frame, [corner], True, (0, 255, 0), 5)

            # Optionally, draw the ID of the tag
            cv2.putText(frame, str(i[0]), (corner[0][0], corner[0][1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # Print the ID and the coordinates of the corners of the AprilTag
            print(f"ID: {i[0]}, Corner Coordinates: {corner.tolist()}")

    # Display the result
    cv2.imshow('Real-time AprilTags Detection', frame)

    # Break the loop when 'q' is pressed or an AprilTag is detected
    if cv2.waitKey(1) & 0xFF == ord('q') or tag_detected:
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
