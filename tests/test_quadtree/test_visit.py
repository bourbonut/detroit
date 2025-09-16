import detroit as d3


def test_visit_1():
    results = []
    q = d3.quadtree().add_all([[0, 0], [1, 0], [0, 1], [1, 1]])

    def visit(node, x0, y0, x1, y1):
        results.append([x0, y0, x1, y1])
        return

    assert q.visit(visit) == q
    assert results == [
        [0, 0, 2, 2],
        [0, 0, 1, 1],
        [1, 0, 2, 1],
        [0, 1, 1, 2],
        [1, 1, 2, 2],
    ]


def test_visit_2():
    results = []
    q = (
        d3.quadtree()
        .set_extent([[0, 0], [960, 960]])
        .add_all([[100, 100], [200, 200], [300, 300]])
    )

    def visit(node, x0, y0, x1, y1):
        results.append([x0, y0, x1, y1])
        return

    assert q.visit(visit) == q
    assert results == [
        [0, 0, 1024, 1024],
        [0, 0, 512, 512],
        [0, 0, 256, 256],
        [0, 0, 128, 128],
        [128, 128, 256, 256],
        [256, 256, 512, 512],
    ]


def test_visit_3():
    results = []
    q = (
        d3.quadtree()
        .set_extent([[0, 0], [960, 960]])
        .add_all([[100, 100], [700, 700], [800, 800]])
    )

    def visit(node, x0, y0, x1, y1):
        results.append([x0, y0, x1, y1])
        return x0 > 0

    assert q.visit(visit) == q
    assert results == [[0, 0, 1024, 1024], [0, 0, 512, 512], [512, 512, 1024, 1024]]


def test_visit_4():
    results = []
    q = d3.quadtree()

    def visit(node, x0, y0, x1, y1):
        results.append([x0, y0, x1, y1])
        return

    assert q.visit(visit) == q
    assert len(results) == 0


def test_visit_5():
    results = []
    q = d3.quadtree().set_extent([[0, 0], [960, 960]])

    def visit(node, x0, y0, x1, y1):
        results.append([x0, y0, x1, y1])
        return

    assert q.visit(visit) == q
    assert len(results) == 0
