import os
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

def find_index(i, matrix):
    return len(matrix[0])*i[0] + i[1]

def find_coordinate(i, matrix):
    return (i//len(matrix[0]),i%len(matrix[0]))

def adjacencylist(i, matrix):
    s = find_index(i,matrix)
    m = len(matrix[0])
    n = len(matrix)
    list = []
    for i in (s-m,s-1,s+1,s+m):
        if i >= 0 and i < m*n and matrix[i//m][i%m] != 'x':
            list.append(i)
    return list

def calculate_cost(u , start, previouspoint, matrix):
    count = 1
    i = find_index(u, matrix)
    while previouspoint[i] != start:
        count = count + 1
        i = find_index(previouspoint[i], matrix)
    return count

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

def DFS_Search(matrix, previouspoint, consider, start, end):
    consider[find_index(start,matrix)] = 0
    if consider[find_index(end,matrix)] == 0:
        return
    for u in adjacencylist(start, matrix):
        if consider[u]== 1:
            previouspoint[u] = start
            DFS_Search(matrix,previouspoint,consider, find_coordinate(u, matrix), end)

def find_startend(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j]=='S':
                start=(i,j)
            elif matrix[i][j]==' ':
                if (i==0) or (i==len(matrix)-1) or (j==0) or (j==len(matrix[0])-1):
                    end=(i,j)
    return start, end

def find_route(previouspoint, start, end, matrix):
    route = []
    j = find_index(end, matrix)
    while previouspoint[j]!= start:
        route.insert(0,previouspoint[j])
        j = find_index(previouspoint[j],matrix)
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
consider,previouspoint = init_variable(matrix)
start, end = find_startend(matrix)
DFS_Search(matrix,previouspoint,consider,start, end)
route = find_route(previouspoint,start,end, matrix)
visualize_maze(matrix,bonus_points,start,end,route)
print("Total cost:", calculate_cost(end , start, previouspoint, matrix))