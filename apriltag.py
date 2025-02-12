import cv2
import cv2.aruco as aruco

# Load the image
image = cv2.imread('Apriltag.png')

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Specify the dictionary
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_APRILTAG_36h11)  # Adjust dictionary as needed

# Initialize the detector parameters using default values
parameters = aruco.DetectorParameters()

# Detect the markers in the image
corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

if ids is not None:
    for i, corner in zip(ids, corners):
        # Flatten the corner points array
        corner = corner.reshape((4, 2))
        # Convert to integers
        corner = corner.astype(int)
        
        # Draw the bounding box around the detected AprilTag
        cv2.polylines(image, [corner], True, (0, 255, 0), 5)
        
        # Optionally, draw the ID of the tag
        cv2.putText(image, str(i[0]), (corner[0][0], corner[0][1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        # Print the ID and the coordinates of the corners of the AprilTag
        print(f"ID: {i[0]}, Corner Coordinates: {corner.tolist()}")

    # Display the result
    cv2.imshow('Detected AprilTags', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("No AprilTags were detected in the image.")
