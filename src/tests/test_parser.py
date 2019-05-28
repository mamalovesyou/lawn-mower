from src.parser import Parser


class TestParser(object):

    GRID_SIZES = {
        "4 4\n": (5, 5),
        "5 5\n": (6, 6),
        "0 0\n": (1, 1),
        "1 1 1\n": (None, None)
    }

    POSITIONS = {
        "1 2 N\n": ((1, 2), "N"),
        "0 0 N\n": ((0, 0), "N"),
        "-1 -2 A\n": ((-1, -2), "A"),
        "1 2 N E Z\n": ((None, None), None)
    }

    def test_extract_grid_size(self):
        """
        Test extract grid size method
        """
        parser = Parser()
        for k, v in self.GRID_SIZES.items():
            assert parser._extract_grid_size(k) == v

    def test_extract_position(self):
        """
        Test extract grid size method
        """
        parser = Parser()
        for k, v in self.POSITIONS.items():
            assert parser._extract_mower_position(k) == v
