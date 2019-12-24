class Grid3:
    def __init__(self, default=" "):
        self.default = default
        self.places = {(0, 0, 0): self.default}

    def put(self, x, y, z, tile):
        self.places[(x, y, z)] = tile

    def get(self, x, y, z):
        return self.places[(x, y, z)]

    def clear(self, x, y, z):
        del self.places[(x, y, z)]

    def validate_pos(self, pos):
        if len(pos) != 3:
            raise TypeError("Bad position")

    def __setitem__(self, pos, tile):
        # so ``grid[(x, y, z)] = '*'`` works
        self.validate_pos(pos)
        self.places[pos] = tile

    def __getitem__(self, pos):
        # so ``tile = grid[(x, y, z)]`` works
        self.validate_pos(pos)
        try:
            return self.places[pos]
        except KeyError:
            return self.default

    def __delitem__(self, pos):
        self.validate_pos(pos)
        del self.places[pos]

    def __len__(self):
        return len(self.places)

    def __contains__(self, pos):
        self.validate_pos(pos)
        return pos in self.places

    def min_x(self):
        return min([pos[0] for pos in self.places])

    def max_x(self):
        return max([pos[0] for pos in self.places])

    def min_y(self):
        return min([pos[1] for pos in self.places])

    def max_y(self):
        return max([pos[1] for pos in self.places])

    def min_z(self):
        return min([pos[2] for pos in self.places])

    def max_z(self):
        return max([pos[2] for pos in self.places])

    def add_z_layer(self, z, grid2):
        for pos2 in grid2.places:
            self.places[pos2[0], pos2[1], z] = grid2[pos2]

    def has_z_layer(self, z):
        return any([pos[2] == z for pos in self.places])
    
    def string_level(self, z):
        origin_x = -self.min_x()
        origin_y = -self.min_y()

        width = self.max_x() - self.min_x() + 1
        height = self.max_y() - self.min_y() + 1

        canvas = []
        for _y in range(height):
            canvas.append([self.default] * width)

        for place in self.places:
            if place[2] == z:
                canvas[origin_y + place[1]][origin_x + place[0]] = self.places[place]

        return "\n".join(["".join(line) for line in canvas])

    def __str__(self):
        all_levels = []
        for z in range(self.min_z(), self.max_z()+1):
            all_levels.append(f"Level {z}\n{self.string_level(z)}")
        return "\n".join(all_levels)
        
    def print(self):
        print(str(self))
