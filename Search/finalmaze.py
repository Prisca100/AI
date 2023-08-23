class Frontierr():
    def __init__(self, type="stack"):
        self.frontier = []
        self.type = type

    def add(self, node):
        if not self.contains_state(node.state):
            self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def isEmpty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.type == "stack":
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node

        elif self.type == "queue":
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node
        else:
            raise Exception("We do not suport that data Structure")


class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action


class Maze():
    def __init__(self, filename, type, grid_size=50, border=2, mode="file"):
        self.type = type
        self.mode = mode
        self.filename = filename
        self.grid_size = grid_size
        self.border = border

    def process_image(self):
        from PIL import Image
        import collections
        img = Image.open(self.filename)
        img = img.convert('RGB')
        self.height = int(img.height/self.grid_size)
        self.width = int(img.width/self.grid_size)
        self.walls = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                left = j * self.grid_size + self.border
                top = i * self.grid_size + self.border
                right = (j + 1) * self.grid_size + self.border
                bottom = (i + 1) * self.grid_size + self.border
                rectangle = (left, top, right, bottom)
                rectangle_img = img.crop(rectangle)
                rectangle_img = rectangle_img.convert('RGB')
                pixels = list(rectangle_img.getdata())
                color_counter = collections.Counter(pixels)
                most_common = color_counter.most_common(1)[0][0]
                try:
                    if most_common == (255, 0, 0):
                        self.start = (i, j)
                        row.append(False)
                    elif most_common == (0, 171, 28):
                        self.goal = (i, j)
                        row.append(False)
                    elif most_common == (237, 240, 252):
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:
                    row.append(False)
            self.walls.append(row)
        self.solution = None
        return self.solution, self.start, self.goal

    def process_txt(self):
        with open(self.filename) as f:
            contents = f.read()

            if contents.count("A") != 1:
                raise Exception("Only one start requires, check file")
            if contents.count("B") != 1:
                raise Exception("Only one Goal required, check file")

            contents = contents.splitlines()
            self.height = len(contents)
            self.width = max(len(line) for line in contents)

            # Check for walls
            self.walls = []
            for i in range(self.height):
                row = []
                for j in range(self.width):
                    try:
                        if contents[i][j] == "A":
                            self.start = (i, j)
                            row.append(False)
                        elif contents[i][j] == "B":
                            self.goal = (i, j)
                            row.append(False)
                        elif contents[i][j] == " ":
                            row.append(False)
                        else:
                            row.append(True)
                    except IndexError:
                        row.append(False)
                self.walls.append(row)

            self.solution = None
            return self.solution, self.start, self.goal

    def process_file(self):
        if self.mode == "file":
            return self.process_txt()
        elif self.mode == "img":
            return self.process_image()

    def solve(self):
        self.num_explored = 0
        self.solution, self.start, self.goal = self.process_file()
        start = Node(state=self.start, parent=None, action=None)
        frontier = Frontierr(type=self.type)
        frontier.add(start)

        self.explored = set()

        while True:
            if frontier.isEmpty():
                raise Exception("No solution Found")

            node = frontier.remove()
            self.num_explored += 1

            if node.state == self.goal:
                actions = []
                visited = []
                while node.parent is not None:
                    actions.append(node.action)
                    visited.append(node.state)
                    node = node.parent
                actions.reverse()
                visited.reverse()
                self.solution = (actions, visited)
                return
            self.explored.add(node.state)
            for action, state in self.neighbors(node.state):
                if state not in self.explored:
                    child = Node(state=state, parent=node, action=action)
                    frontier.add(child)

    def neighbors(self, state):
        row, col = state

        candidates = [
            ("Up", (row-1, col)),
            ("Down", (row+1, col)),
            ("Left", (row, col-1)),
            ("Right", (row, col+1))
        ]
        result = []
        for action, (r, c) in candidates:
            try:
                if not self.walls[r][c]:
                    result.append((action, (r, c)))
            except IndexError:
                continue
        return result

    def output_image(self, filename, show_solution=True, show_explored=False):
        from PIL import Image, ImageDraw
        cell_size = 50
        cell_border = 2

        # Blank Canvas
        img = Image.new(
            "RGBA", (self.width * self.grid_size,
                     self.height * self.grid_size),
            "black"
        )
        draw = ImageDraw.Draw(img)
        solution = self.solution[1] if self.solution is not None else None
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col:
                    fill = (40, 40, 40)
                elif (i, j) == self.start:
                    fill = (255, 0, 0)
                elif (i, j) == self.goal:
                    fill = (0, 171, 28)
                elif solution is not None and show_solution and (i, j) in solution:
                    fill = (220, 235, 113)
                elif solution is not None and show_explored and (i, j) in self.explored:
                    fill = (212, 97, 85)
                else:
                    fill = (237, 240, 252)

                draw.rectangle(([(j * self.grid_size + self.border, i * self.grid_size + self.border),
                                 ((j + 1) * self.grid_size - self.border, (i + 1) * self.grid_size - self.border)]),
                               fill=fill)

        img.save(filename)


m = Maze(filename="maze.png", type="stack", mode="img")
print("Solving...")
m.solve()
print(
    f"Finsihed\nSolution:{m.solution}\nNumber of explored:{m.num_explored}\nAlgorithm: {m.type}")
m.output_image("maze1Solution.png", show_explored=True)
