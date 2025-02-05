class TestClassExample:
    def test_example(self):
        assert 1 == 1

    def test_math_op(self):
        r = 10 * 5
        assert r == 50

# pytest . -v