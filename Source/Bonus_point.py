import os
import math
import matplotlib.pyplot as plt

def read_file(file_name):
    f=open(file_name,'r')
    n_bonus_points = int(next(f)[:-1])
    bonus_points = []
    for i in range(n_bonus_points):
        x, y, reward = map(int, next(f)[:-1].split(' '))
        bonus_points.append((x, y, reward))

    text=f.read()
    matrix=[list(i) for i in text.splitlines()]
    f.close()
    return bonus_points, matrix

def init_variable(matrix):
    consider = []
    previouspoint = []
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == 'x':
                consider.append(0)
            else:
                consider.append(1)
            previouspoint.append((0,0))
    return consider, previouspoint

def find_index(i, matrix):
    return len(matrix[0])*i[0] + i[1]

def find_coordinate(i, matrix):
    return (i//len(matrix[0]),i%len(matrix[0]))

def calculate_cost(u , start, previouspoint, matrix):
    count = 1
    i = find_index(u, matrix)
    while previouspoint[i] != start:
        check = 0
        for j in range(0, len(bonus_points)):
            if i == find_index(bonus_points[j], matrix):
                count = count + bonus_points[j][2]
                check = 1
        if check == 0:
            count = count + 1
        i = find_index(previouspoint[i], matrix)
    return count

def calculate_distance(i, j):
    return math.sqrt(pow((i[0] - j[0]),2) + pow((i[1] - j[1]),2))

def adjacencylist(u, matrix):
    s = find_index(u, matrix)
    m = len(matrix[0])
    n = len(matrix)
    list = []
    for i in (s-m,s-1,s+1,s+m):
        if i >= 0 and i <= m*n and matrix[i//m][i%m] != "x":
            list.append(i)
    return list

def nearest_bonuspoint(u, bonus_points, consider):
    for i in range(0, len(bonus_points)):
        temp = adjacencylist(bonus_points[i], matrix)
        if len(temp) == 1:
            consider[find_index(bonus_points[i], matrix)] = 0
    nearest = 0
    for i in range(1, len(bonus_points)):
        if (calculate_distance(u,bonus_points[i]) <  calculate_distance(u,bonus_points[nearest])) and consider[find_index(bonus_points[i], matrix)] == 1:
            nearest = i
    if consider[find_index(bonus_points[nearest], matrix)] == 1:
        return nearest
    return -1
        
def best_way(u, bonus_points,consider, end):
    nearest = nearest_bonuspoint(u, bonus_points, consider)
    if nearest == -1:
        return end
    else:
        if (bonus_points[nearest][2] + calculate_distance(bonus_points[nearest],u) + calculate_distance(bonus_points[nearest],end) ) > (calculate_distance(u,end)):
            return end
        else:
            x = (bonus_points[nearest][0],bonus_points[nearest][1])
            return x
    
def sort_adjacencylist(list, previouspoint, bonus_points, consider, end):
    for i in range(0, len(list) ):
        way1 = best_way(find_coordinate(list[i],matrix),bonus_points,consider, end)
        for j in range(i + 1, len(list)):
            way2 = best_way(find_coordinate(list[j],matrix),bonus_points,consider, end)
            if (calculate_distance(find_coordinate(list[i], matrix), way1)) > calculate_distance(find_coordinate(list[j], matrix), way2):
                list[i], list[j] = list[j], list[i]
            

def Bonuspoint_Search(matrix, previouspoint, consider, start, end):
    consider[find_index(start,matrix)] = 0
    if consider[find_index(end,matrix)] == 0:
        return
    list = adjacencylist(start, matrix)
    sort_adjacencylist(list, previouspoint, bonus_points, consider, end)
    for u in list:
        if consider[u]== 1:
            previouspoint[u] = start
            Bonuspoint_Search(matrix,previouspoint,consider, find_coordinate(u, matrix), end)
    
def find_startend(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j]=='S':
                start=(i,j)
            elif matrix[i][j]==' ':
                if (i==0) or (i==len(matrix)-1) or (j==0) or (j==len(matrix[0])-1):
                    end=(i,j)
            else:
                pass
    return start, end

def find_route(previouspoint, start, end, matrix):
    route = []
    j = find_index(end, matrix)
    while previouspoint[j]!= start:
        route.insert(0,previouspoint[j])
        j = find_index(previouspoint[j], matrix)
    route.insert(0,start)
    route.append(end)
    return route
                
def visualize_maze(matrix, bonus, start, end, route):
    """
    Args:
      1. matrix: The matrix read from the input file,
      2. bonus: The array of bonus points,
      3. start, end: The starting and ending points,
      4. route: The route from the starting point to the ending one, defined by an array of (x, y), e.g. route = [(1, 2), (1, 3), (1, 4)]
    """
    #1. Define walls and array of direction based on the route
    walls=[(i,j) for i in range(len(matrix)) for j in range(len(matrix[0])) if matrix[i][j]=='x']

    if route:
        direction=[]
        for i in range(1,len(route)):
            if route[i][0]-route[i-1][0]>0:
                direction.append('v') #^
            elif route[i][0]-route[i-1][0]<0:
                direction.append('^') #v        
            elif route[i][1]-route[i-1][1]>0:
                direction.append('>')
            else:
                direction.append('<')

        direction.pop(0)

    #2. Drawing the map
    ax=plt.figure(dpi=100).add_subplot(111)

    for i in ['top','bottom','right','left']:
        ax.spines[i].set_visible(False)

    plt.scatter([i[1] for i in walls],[-i[0] for i in walls],
                marker='X',s=100,color='black')
    
    plt.scatter([i[1] for i in bonus],[-i[0] for i in bonus],
                marker='P',s=100,color='green')

    plt.scatter(start[1],-start[0],marker='*',
                s=100,color='gold')

    if route:
        for i in range(len(route)-2):
            plt.scatter(route[i+1][1],-route[i+1][0],
                        marker=direction[i],color='red')

    plt.text(end[1],-end[0],'EXIT',color='red',
         horizontalalignment='center',
         verticalalignment='center')
    plt.xticks([])
    plt.yticks([])
    plt.show()

    print(f'Starting point (x, y) = {start[0], start[1]}')
    print(f'Ending point (x, y) = {end[0], end[1]}')
    
    for _, point in enumerate(bonus):
        print(f'Bonus point at position (x, y) = {point[0], point[1]} with point {point[2]}')
bonus_points, matrix = read_file('maze_map.txt')
print(f'The height of the matrix: {len(matrix)}')
print(f'The width of the matrix: {len(matrix[0])}')
start, end = find_startend(matrix)
consider, previouspoint = init_variable(matrix)
Bonuspoint_Search(matrix, previouspoint, consider, start, end)
route = find_route(previouspoint, start, end, matrix)
visualize_maze(matrix,bonus_points,start,end,route)
print("Total cost:", calculate_cost(end , start, previouspoint, matrix))