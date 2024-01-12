#Vasileios Valeras 4031

# create a dictionary to store linestrings id's for each cell
cell_dict = {}

# Create a set to store the unique linestring ids
linestring_ids = set()

# Create a list to store the linestrings
linestrings = []


# read grid.dir
with open('grid.dir') as dir, open ('grid.grd') as grd:
    # read min and max x and y values
    first_line = dir.readline().split()
    grid_min_x = float(first_line[1])
    grid_max_x = float(first_line[2])
    grid_min_y = float(first_line[3])
    grid_max_y = float(first_line[4])

    # iterate through each line in the file
    for line in dir:
        # split the line into its parts
        parts = line.split()
        # get the cell key (convert to integers)
        cell_key = (int(parts[1]), int(parts[2]))
        # get the number of linestrings in this cell
        num_linestrings = int(parts[3])
        if num_linestrings > 0:
            # read num_linestrings lines from grid.grd
            linestring_data = (grd.readline().split(',') for _ in range(num_linestrings))
            for linestring_parts in linestring_data:
                # add the linestring id to the cell dictionary as an integer
                linestring_id = int(linestring_parts[0])
                if linestring_id not in linestring_ids:
                    # add the linestring id to the set of unique ids
                    linestring_ids.add(linestring_id)
                    # parse the linestring data
                    minMBR = list(map(float, linestring_parts[1].split()))
                    maxMBR = list(map(float, linestring_parts[2].split()))
                    coords = [[float(x), float(y)] for x, y in (c.split() for c in linestring_parts[3:])]
                    # add the linestring information to the linestrings list
                    linestrings.append([linestring_id, [minMBR, maxMBR], coords])
                # add the linestring id to the cell dictionary
                if cell_key not in cell_dict:
                    cell_dict[cell_key] = [linestring_id]
                else:
                    cell_dict[cell_key].append(linestring_id)
        else:
            cell_dict[cell_key] = []


# Create a 10x10 grid
x_interval = (grid_max_x - grid_min_x) / 10
y_interval = (grid_max_y - grid_min_y) / 10
grid = [((i, j), [grid_min_x + i * x_interval, grid_min_y + j * y_interval, grid_min_x + (i+1) * x_interval,
                  grid_min_y + (j+1) * y_interval]) for j in range(9, -1, -1) for i in range(10)]


def check_intersection(x1, y1, x2, y2, x3, y3, x4, y4):
    # Calculate the values of t and u
    denominator = (x1-x2)*(y3-y4) - (y1-y2)*(x3-x4)
    if denominator == 0:
        # The lines are parallel, so there is no intersection
        return False
    t = ((x1-x3)*(y3-y4) - (y1-y3)*(x3-x4)) / denominator
    u = -((x1-x2)*(y1-y3) - (y1-y2)*(x1-x3)) / denominator

    # Calculate the intersection point
    px = x1 + t*(x2-x1)
    py = y1 + t*(y2-y1)

    # Check if the intersection point falls within both line segments
    if 0 <= t <= 1 and 0 <= u <= 1:
        return True
    else:
        return False

f = input("Please provide me the .txt file with the window queries: ")

with open(f) as queries:
    query = 1
    for line in queries:
        parts = line.split(',')
        window = [float(x) for x in parts[1].split()]
        intersect_cells = 0
        records = []
        counter = 0
        outputs = []
        actual_outputs = []
        for cell in grid:
            if (window[0] <= cell[1][2] and window[1] >= cell[1][0] and
                    window[2] <= cell[1][3] and window[3] >= cell[1][1]):
                cell_id = cell[0]
                cell_linestrings = cell_dict[cell_id]
                if cell_linestrings:
                    intersect_cells += 1
                    records.append((cell_linestrings, cell))

        for record,cell in records:
            for ls_id in record:
                for linestring in linestrings:
                    if linestring[0] == ls_id:
                        # compute the reference point for this linestring and cell
                        ref_point = [max(linestring[1][0][0], window[0]), max(linestring[1][0][1], window[2])]
                        if (window[0] <= linestring[1][1][0] and window[1] >= linestring[1][0][0] and
                                window[2] <= linestring[1][1][1] and window[3] >= linestring[1][0][1]):
                            if cell[1][0] <= ref_point[0] <= cell[1][2] and cell[1][1] <= ref_point[1] <= cell[1][3]:
                                outputs.append(ls_id)
                                #counter += 1

        vertices = [(window[0], window[2]), (window[1], window[2]), (window[1], window[3]), (window[0], window[3])]

        for output in outputs:
            for linestring in linestrings:
                if linestring[0] == output:
                    if ((window[0] <= linestring[1][0][0] <= window[1]) and (window[0] <= linestring[1][1][0] <= window[1])) or (window[2] <= linestring[1][0][1] <= window[3])  and (window[2] <= linestring[1][1][1] <= window[3]):
                        actual_outputs.append(output)
                        counter += 1
                    else:
                        coordinates = linestring[2]
                        for i in range (1,len(coordinates)):
                            x1,y1 = coordinates[i-1]
                            x2,y2 = coordinates[i]
                            for i in range(len(vertices)):
                                j = (i + 1) % len(vertices)
                                wx1, wy1 = vertices[i]
                                wx2, wy2 = vertices[j]

                                if check_intersection(x1, y1, x2, y2, wx1, wy1, wx2, wy2):
                                    if output not in actual_outputs:
                                        actual_outputs.append(output)
                                        counter += 1

        actual_outputs = sorted(actual_outputs)
        print("Query " + str(query) + " results:")
        for out in actual_outputs:
            print(str(out), end=' ')
        print("")
        print("Cells: " + str(intersect_cells))
        print("Results: " + str(counter))
        print("----------")
        query += 1

