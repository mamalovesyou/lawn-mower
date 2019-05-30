import pytest

from src.mower import Mower
from src.environment import Environment


class TestMower(object):

    ENVIRONMENT_SIZE = (6, 6)

    # Mower initital position at origin oriented to North
    INSTRUCTIONS_LIST = {
        "FFFFFRFR": {'results': [((0, 1), 'N'), ((0, 2), 'N'), ((0, 3), 'N'), ((0, 4), 'N'), ((0, 5), 'N'), ((0, 5), 'E'), ((1, 5), 'E'), ((1, 5), 'S')],
                     'environment': "1 S 0 0 0 0\n1 0 0 0 0 0\n1 0 0 0 0 0\n1 0 0 0 0 0\n1 0 0 0 0 0\n1 0 0 0 0 0\n"},
    }

    @pytest.fixture()
    def setup_environement(self):
        self.environment = Environment(*self.ENVIRONMENT_SIZE)

    def test_mower_iterator(self, setup_environement):
        """
        Test that ensure we can use a mower as an iterator
        Ensure that it return right position after each iteration
        """
        index = 0
        for instructions, metadata in self.INSTRUCTIONS_LIST.items():
            mower = Mower(index, (0, 0), "N", instructions, self.environment)
            for k, pos in enumerate(mower):
                assert pos == metadata['results'][k]
            index += 1

    def test_mower_environment(self):
        """
        This test ensure the mower will alter the environement field
        """
        index = 0
        for instructions, metadata in self.INSTRUCTIONS_LIST.items():
            environment = Environment(*self.ENVIRONMENT_SIZE)
            mower = Mower(index, (0, 0), "N", instructions, environment)
            for pos in mower:
                pass
            assert metadata['environment'] == str(environment)
            index += 1
