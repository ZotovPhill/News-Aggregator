import sys

sys.path.append("..")

import run
import unittest


class FlaskTest(unittest.TestCase):
    def setUp(self):
        run.app.testing = True
        self.app = run.app.test_client()

    def test_home(self):
        result = self.app.get("/")
        assert b"Hello Friend" in result.data


if __name__ == "__main__":
    unittest.main()
