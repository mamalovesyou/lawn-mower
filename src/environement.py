class Environement:
    """
    Origin is BOTTOM-LEFT so to update a cell you alwas need to
    use update_cell() function because it implement the right logic.
    """
    DEFAULT_ORIGIN = (0, 0)

    GRASS = 0
    MOWED_GRASS = 1
    MOWER_N = 'N'
    MOWER_E = 'E'
    MOWER_S = 'S'
    MOWER_W = 'W'

    def __init__(self, width=0, height=0, origin=None):
        self.width = width
        self.height = height
        if origin:
            self.origin_x, self.origin_y = origin
        else:
            self.origin_x, self.origin_y = self.DEFAULT_ORIGIN

        self._cells = [[0]*self.width for i in range(self.height)]

    def __str__(self):
        """
        String representation of an evironement
        """
        result = ""
        for row in self._cells:
            result += " ".join(map(str, row))
            result += "\n"
        return result

    def update_cell(self, x, y, value):
        """
        Update value of a cell in the grid
        @param x: Integer
        @param y: Integer
        @param value: Integer
        @return: True if updated, False either
        """
        x1, y1 = self._transpose_coordinates(x, y)
        if self.is_in_field(x1, y1):
            self._cells[y1][x1] = value
            return True
        return False

    def get_cell(self, x, y):
        """
        Return value of a cell in the grid
        @param x: Integer
        @param y: Integer
        @return: Integer
        """
        x1, y1 = self._transpose_coordinates(x, y)
        if self.is_in_field(x1, y1):
            return self._cells[y1][x1]
        return None

    def is_in_field(self, x, y):
        """
        Return True if those coordinates are in the grid
        Return False either
        @return: True or False
        """
        return (self.origin_x <= x < self.width) and (self.origin_y <= y < self.height)

    def _transpose_coordinates(self, x, y):
        """
        This function trnaspose coordiantes from top left origin
        to a bottom left origin. It will transpose y as gridHeigh - y.
        @param x: Integer
        @param y: Integer
        @return: Tuple of integer
        """
        return (x, self.height - 1 - y)


if __name__ == '__main__':

    field = Environement(6, 6)
    field.update_cell(1, 2, field.MOWER)
    field.update_cell(3, 3, field.MOWER)
    print(field.is_in_field(0, 0))
    field.print()
