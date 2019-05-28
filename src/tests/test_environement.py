from src.environement import Environement


class TestEnviroment(object):

    GRIDS = {
        (3, 3): [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
        (6, 3): [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]
    }

    # Enviroment size (10, 10)
    TRANSPOSED_COORDS = {
        (1, 2): (1, 7),
        (-1, -2): (-1, 11),
        (1, 5): (1, 4),
    }

    # Enviroment size (10, 10)
    IN_FIELD = {
        (1, 2): True,
        (-1, -2): False,
        (1, 5): True,
        (20, 1): False,
        (5, 5): True
    }

    # Enviroment size (10, 10)
    UPDATE_CELLS = {
        (1, 2): [0, True],
        (0, 0): [None, True],
        (-1, 5): ["A", False],
        (20, 1): [1, False],
        (5, 5): ["B", True]
    }

    # Enviroment size (4, 4)
    STRING_REP = "0 0 0 0\n0 0 0 0\n0 0 0 0\n0 0 0 0\n"

    def createEnv(self, size):
        width, height = size
        return Environement(width, height)

    def test_initialization(self):
        """
        Test initialization. This test verify that after initialization
        the enviroement is composed of a grid of 0 with the right size
        """
        for k, v in self.GRIDS.items():
            env = self.createEnv(k)
            assert env._cells == v

    def test_transpose_coordinates(self):
        """
        Test transpose coordinates from a top left origin to
        a bottom left origin
        """
        environement_size = (10, 10)
        env = self.createEnv(environement_size)
        for k, v in self.TRANSPOSED_COORDS.items():
            x, y = k
            assert env._transpose_coordinates(x, y) == v

    def test_is_in_field(self):
        """
        Test is in field
        """
        environement_size = (10, 10)
        env = self.createEnv(environement_size)
        for k, v in self.IN_FIELD.items():
            x, y = k
            assert env.is_in_field(x, y) == v

    def test_update_cell(self):
        """
        Test update cell
        """
        environement_size = (10, 10)
        env = self.createEnv(environement_size)
        for k, v in self.UPDATE_CELLS.items():
            x, y = k
            print(x, y)
            # Verify if upated performed
            assert env.update_cell(x, y, v[0]) == v[1]
            if v[1]:  # Verify value
                assert env.get_cell(x, y) == v[0]
            else:
                # Verify got None value
                assert env.get_cell(x, y) == None

    def test_get_cell(self):
        """
        Test get cell
        """
        environement_size = (10, 10)
        env = self.createEnv(environement_size)
        for row in range(environement_size[1]):
            for column in range(environement_size[0]):
                assert env.get_cell(column, row) == env.GRASS

    def test_str(self):
        """
        Test string representation of an environement
        """
        environement_size = (4, 4)
        env = self.createEnv(environement_size)
        assert str(env) == self.STRING_REP
