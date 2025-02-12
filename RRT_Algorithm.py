# RRT Conncect Testing
import numpy as np
import cv2 as cv2
import math
import time

STEP = 75
EDGECOLOR = (125, 125, 125)
POINTCOLOR = (125, 125, 125)
INCLUDESURRCOLISION = True
SURROUNDING = 80 # 80 
START_POINT = (0, 0)

Image_number = 3 # 1 (Testing Map), 2(Final Map Shape - DO NOT USE), 3 (FINAL MAP), 4


Goal_config = None
map = None
img = None

if Image_number == 1:
    Starting_config = (1315, 1160)
    Goal_config = (950, 900) # (40, 100) # 
    map = cv2.imread('./Maps/map_1/map_adj_scaled.png', 0) # 0 for grayscale, all numbers are 0 or 255
    img = cv2.imread('./Maps/map_1/map_adj_scaled.png')

if Image_number == 2:
    Starting_config = (1315, 1360)
    Goal_config = (950, 900) # (40, 100) # 
    map = cv2.imread('./Maps/map_2/map2_adj_scaled.png', 0) # 0 for grayscale, all numbers are 0 or 255
    img = cv2.imread('./Maps/map_2/map2_adj_scaled.png')


if Image_number == 3:
    Starting_config = (300, 300) # (x, y) BLUE
    START_POINT = Starting_config
    Goal_config = (500, 85) # (x, y) Red
    map = cv2.imread('./Maps/map_3/map3.png', 0) # 0 for grayscale, all numbers are 0 or 255
    img = cv2.imread('./Maps/map_3/map3.png')
    

if Image_number == 4:
    Starting_config = (57, 170) # (275, 30) #
    Goal_config = (1150, 1100) # (40, 100) #
    map = cv2.imread('maze4_adj.png', 0) # 0 for grayscale, all numbers are 0 or 255
    img = cv2.imread('maze4_adj.png')


def show_image(image, wait_time=0):
    image = cv2.resize(image, [500, 500])
    cv2.imshow('image', image)
    cv2.waitKey(wait_time)


class Node:
    def __init__(self, point, parent=None):
        self.point = point
        self.parent = parent

class RRT_connect_tree:
    def __init__(self, start):
        self.start = Node(start)
        self.nodes = [self.start]
        self.edges = []
        self.path = []
        self.newest_index = 0
    
    def add_node(self, point, parent):
        self.nodes.append(Node(point, parent))
        self.edges.append((parent.point, point))
        self.newest_index = len(self.nodes) - 1
        cv2.line(img, parent.point, point, EDGECOLOR, 1)
        show_image(img, 1)
    
    def get_nearest_node(self, point):
        min_dist = float('inf')
        nearest_node = None
        for node in self.nodes:
            dist = math.sqrt((point[0] - node.point[0])**2 + (point[1] - node.point[1])**2)
            if dist < min_dist:
                min_dist = dist
                nearest_node = node
        return nearest_node
    

def new_config(node1, node2):
    angle = math.atan2(node2.point[1] - node1.point[1], node2.point[0] - node1.point[0])
    x = round(node1.point[0] + STEP * math.cos(angle))
    y = round(node1.point[1] + STEP * math.sin(angle))
    

    # print("X: ", x, "Y: ", y)
    dist = math.sqrt((node2.point[0] - x)**2 + (node2.point[1] - y)**2)
    if dist < STEP and not test_collision(node2):
        return Node(node2.point, node1)
    else:
        return Node((x, y), node1)
    

def test_collision(node): # Returns false for no collision, true for collision
    if not INCLUDESURRCOLISION:
        if map[node.point[1], node.point[0]] == 255:
            return False
        else:
            return True
    elif INCLUDESURRCOLISION:
        for i in range(-SURROUNDING, SURROUNDING +1):
            for j in range(-SURROUNDING, SURROUNDING +1):
                if map[node.point[1] + i, node.point[0] + j] == 0:
                    return True
        return False 


def rrt_extend_tree(tree, node):
    nearest_node = tree.get_nearest_node(node.point)
    new_node = new_config(nearest_node, node)
    if test_collision(new_node):
        # print("New node is in collision: ", new_node.point)
        return "failed"
    elif new_node.point == node.point: #and test_collision(new_node):
        tree.add_node(new_node.point, nearest_node)
        # print("New node is the same as the goal")
        return "reached"
    else:
        tree.add_node(new_node.point, nearest_node)
        return "extended"

def connect(tree,  q):
    s = 'extended'
    while s == 'extended':
        s = rrt_extend_tree(tree, q)
    return s

def random_config():
    x = np.random.randint(0, img.shape[1])
    y = np.random.randint(0, img.shape[0])
    return (x,y)


def run_RRT_algorithm(start_config, goal_config, highlight=True):
    tree1 = RRT_connect_tree(start_config)
    tree2 = RRT_connect_tree(goal_config)
    while True:
        qrand = random_config()
        rand_node = Node(qrand)
        if not rrt_extend_tree(tree1, rand_node) == "failed":
            if connect(tree2, tree1.nodes[tree1.newest_index]) == 'reached':
                # print("Path found")
                if highlight:
                    path = highlight_path(tree1, tree2)
                    return path
                else:
                    return tree1

        tree1, tree2 = tree2, tree1

def highlight_path(tree1, tree2):
    path_a = []
    path_b = []
    
    node = tree1.nodes[tree1.newest_index]
    while node.parent is not None:
        path_a.append(node.point)
        node = node.parent
    node = tree2.nodes[tree2.newest_index]
    while node.parent is not None:
        path_b.append(node.point)
        node = node.parent

    path_a.append(tree1.nodes[0].point)
    path_b.append(tree2.nodes[0].point)
    return_path = []
    if START_POINT in path_a:
        path_a.reverse()
        return_path = path_a[:-1] + path_b
    else :
        path_b.reverse()
        return_path = path_b[:-1] + path_a

    # print("Path A: ", path_a)
    # print("Path B: ", path_b)
    # print("Return Path: ", return_path)

    for i in range(len(path_a) - 1):
        cv2.line(img, path_a[i], path_a[i + 1], (0, 255, 0), 3)
        # time.sleep(0.1)
    for i in range(len(path_b) - 1):
        cv2.line(img, path_b[i], path_b[i + 1], (0, 255, 0), 3)
    
    # save the image
    # cv2.imwrite('path_clean.png', img)

    for i in range(len(path_a) - 1):
        cv2.circle(img, path_a[i], 5, (0, 0, 0), -1)

    for i in range(len(path_b) - 1):
        cv2.circle(img, path_b[i], 5, (0, 0, 0), -1)

    # cv2.imwrite('path_clean_points.png', img)
    
    return return_path

# def collision_feasible(node1_point, node2_point):
#     # Check if the line segment between node1 and node2 is collision-free
#     # If the line segment is collision-free, return True
#     # Otherwise, return False
    
#     # Finding the path of nodes from the start to the end
#     STEP = 5
#     path = run_RRT_algorithm(node1_point, node2_point, highlight=True)




# def smooth_path(path):
#     smoothed_path = [path[0]]  # Start with the first point in the path
#     current_point = path[0]

#     for next_point in path[1:]:
#         # Check if the line segment between current_point and next_point is collision-free
#         if collision_feasible(current_point, next_point):
#             # If collision-free, update current_point to next_point
#             current_point = next_point
#             # Add next_point to the smoothed path
#             smoothed_path.append(next_point)

#     return smoothed_path


def convert_path_to_robot_coords(path):
    return_path = []
    for i in range(len(path)):
        x = path[i][0] # original image was scaled by 20
        y = path[i][1] # original image was scaled by 20

        # starting location in robot coordinates is (200, 200)
        # need to translate coords to robot coordinates
        x = (600 - x) * 0.92 / 200
        y = (600 - y) * 0.92 / 200
        angle = 0
        if i < len(path) - 1:
            angle = math.atan2(path[i+1][1] - path[i][1], path[i+1][0] - path[i][0])
            angle = math.degrees(angle)

        return_path.append((round(x, 2), round(y, 2), round(angle, 3)))

    return return_path

def write_path_to_file(path):
    with open('path.sh', 'w') as f:
        for i in range(len(path)):
            # f.write("rosrun real_robot_challenge nav_goal_client.py " + str(path[i][0]) + " " + str(path[i][1]) + " " + str(path[i][2]) + "\n")
            # X: Y: angle_deg:
            f.write(str(path[i][0]) + " " + str(path[i][1]) + " " + str(path[i][2]) + "\n")

    return path

cv2.circle(img, Starting_config, 15, (255, 0, 0), -1)
cv2.circle(img, Goal_config, 15, (0, 0, 255), -1)


path = run_RRT_algorithm(Starting_config, Goal_config)
# print(path)

# Converting the pixel coordinates to world/map coordinates
path_for_robot = convert_path_to_robot_coords(path)

# Writing the path to a .sh script so the robot can run
write_path = write_path_to_file(path_for_robot)

show_image(img, 0)
cv2.destroyAllWindows()
