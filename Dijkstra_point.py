import numpy as np
import cv2
import math
import obstacle_map

def load_map(fname = None):
    if fname is not None :
        map_ = cv2.imread(fname)
        return map_
    world= 255*np.ones((200,300,3))
    rc=0
    obstacle_map.obstacle_circle(world)
    obstacle_map.obstacle_ellipse(world)
    obstacle_map.obstacle_rhombus(world)
    obstacle_map.obstacle_rectangle(world)
    obstacle_map.obstacle_polygon(world)

    cv2.imwrite('./map.jpg',world)
    return world

def isValidNode(map_,x,y):
    rows,cols = map_.shape[:2]
    if 0 <= x < rows and 0 <= y < cols and (map_[x][y]==(255,255,255)).all():
        return True
    else :
        return False

def getStartNode(map_):
    print("Enter the start co-ordinates")
    rows, cols= map_.shape[:2]
    while True :
        ## Cartesian Form
        x = int(input("x_intial is: "))
        y = int(input("y_intial is: "))
        ## image coordinates
        row = rows-y-1 ; col = x
        if not isValidNode(map_, row, col):
            print('Input Node not within available map range. Please enter again!')
        else:
            break;
    return (row, col)

def getGoalNode(map_):
    print("Enter the goal co-ordinates")
    rows, cols= map_.shape[:2]
    while True:
        ## Cartesian Form
        x = int(input("x_goal is: "))
        y = int(input("y_goal is: "))
        ## image coordinates
        row = rows-y-1 ; col = x
        if not isValidNode(map_, row, col):
            print('Input Node not within available map range. Please enter again! ')
        else:
            break;
    return (row, col)

# A node structure for our search tree
class Node:
    # A utility function to create a new node
    # visited : flag to identify visited nodes
    # parent : coordinate location of the parent
    # cost : cost of reaching current node from start node
    def __init__(self, visited=False,parent=None, cost = math.inf ):
        self.visited = visited
        self.parent = parent
        self.cost = cost

def updateNeighbours(arr, map_, curr_node):
    x,y = curr_node
    ## top node
    if isValidNode(map_,x-1,y):
        if (arr[x][y].cost + 1 < arr[x-1][y].cost):
            arr[x-1][y].cost = arr[x][y].cost + 1
            arr[x-1][y].parent = curr_node

    ## top-left node
    if isValidNode(map_,x-1,y-1):
        if (arr[x][y].cost + 1.41 < arr[x-1][y-1].cost):
            arr[x-1][y-1].cost = arr[x][y].cost + 1.41
            arr[x-1][y-1].parent = curr_node

    ## left node
    if isValidNode(map_,x,y-1):
        if (arr[x][y].cost + 1 < arr[x][y-1].cost):
            arr[x][y-1].cost = arr[x][y].cost + 1
            arr[x][y-1].parent = curr_node

    ## bottom-left node
    if isValidNode(map_,x+1,y-1):
        if (arr[x][y].cost + 1.41 < arr[x+1][y-1].cost):
            arr[x+1][y-1].cost = arr[x][y].cost + 1.41
            arr[x+1][y-1].parent = curr_node

    ## bottom_node
    if isValidNode(map_,x+1,y):
        if (arr[x][y].cost + 1 < arr[x+1][y].cost):
            arr[x+1][y].cost = arr[x][y].cost + 1
            arr[x+1][y].parent = curr_node

    ## bottom-right node
    if isValidNode(map_,x+1,y+1):
        if (arr[x][y].cost + 1.41 < arr[x+1][y+1].cost):
            arr[x+1][y+1].cost = arr[x][y].cost + 1.41
            arr[x+1][y+1].parent = curr_node

    ## right node
    if isValidNode(map_,x,y+1):
        if (arr[x][y].cost + 1 < arr[x][y+1].cost):
            arr[x][y+1].cost = arr[x][y].cost + 1
            arr[x][y+1].parent = curr_node

    ## top-right node
    if isValidNode(map_,x-1,y+1):
        if (arr[x][y].cost + 1.41 < arr[x-1][y+1].cost):
            arr[x-1][y+1].cost = arr[x][y].cost + 1.41
            arr[x-1][y+1].parent = curr_node

    return arr

def findMinCost(arr):
    curr_node = (-1,-1)
    min_cost = math.inf
    for row in range(len(arr)):
        for col in range(len(arr[row])):
            if arr[row][col].cost < min_cost and not arr[row][col].visited:
                curr_node = (row,col)
                min_cost = arr[row][col].cost
    return curr_node

def tracePath(arr,map_,goal_node):
    images= []
    output = './output.avi'
    curr_node = goal_node
    while curr_node is not None:
        img = map_.copy()
        img[curr_node[0]][curr_node[1]] = (0,0,255)
        images.append(img)
        curr_node = arr[curr_node[0]][curr_node[1]].parent

    images = images[::-1]
    saveVideo(images,output)

def saveVideo(images,output='path.avi'):
    h,w = images[0].shape[:2]
    out = cv2.VideoWriter(output,cv2.VideoWriter_fourcc('M','J','P','G'), 1, (w,h))
    images= np.uint8(images)
    for img in images:
        cv2.imshow('img',img)
        cv2.waitKey(0);cv2.destroyAllWindows()
        out.write(img)
    out.release()

def visitedAll(arr):
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            if not arr[i][j].visited:
                return False
    return True

def main():
    map_ = load_map()
    start_node = getStartNode(map_)
    goal_node = getGoalNode(map_)
    rows, cols = map_.shape[:2]
    arr = [[Node() for j in range(cols)] for i in range(rows)]
    arr[start_node[0]][start_node[1]].visited = True
    arr[start_node[0]][start_node[1]].cost = 0
    curr_node = start_node
    while not visitedAll(arr):
        if (curr_node == goal_node):
            print('found Goal at cost {}!!'.format(arr[goal_node[0]][goal_node[1]].cost))
            tracePath(arr,map_,goal_node)
            break
        arr[curr_node[0]][curr_node[1]].visited = True
        arr = updateNeighbours(arr, map_, curr_node)
        curr_node = findMinCost(arr)

if __name__=='__main__':
    main()
    ## TODO: take input in cartesian coordinates and convert them to image coordinates before using the rest of the code
    ## TODO: publish video to show visited nodes  and an image for found path
