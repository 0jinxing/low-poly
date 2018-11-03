import numpy as np


def get_poisson(width, height):
    r = int(max(min(width, height) / 40, 4))
    k = r
    a = r / np.sqrt(2)
    nx, ny = int(width / a) + 1, int(height / a) + 1

    coords_list = [(ix, iy) for ix in range(nx) for iy in range(ny)]
    cells = {coords: None for coords in coords_list}

    def get_cell_coords(pt):
        return int(pt[0] / a), int(pt[1] / a)

    def get_neighbours(coords):
        dxdy = [(-1, -2), (0, -2), (1, -2), (-2, -1), (-1, -1), (0, -1), (1, -1), (2, -1),
                (-2, 0), (-1, 0), (1, 0), (2, 0), (-2, 1), (-1, 1), (0, 1), (1, 1), (2, 1),
                (-1, 2), (0, 2), (1, 2), (0, 0)]
        neighbours = []
        for dx, dy in dxdy:
            neighbour_coords = coords[0] + dx, coords[1] + dy
            if not (0 <= neighbour_coords[0] < nx and 0 <= neighbour_coords[1] < ny): continue
            neighbour_cell = cells[neighbour_coords]
            if neighbour_cell:
                neighbours.append(neighbour_cell)
        return neighbours

    def point_valid(pt):
        cell_coords = get_cell_coords(pt)
        for idx in get_neighbours(cell_coords):
            nearby_pt = samples[idx]
            distance2 = (nearby_pt[0] - pt[0]) ** 2 + (nearby_pt[1] - pt[1]) ** 2
            if distance2 < r ** 2: return False
        return True

    def get_point(refpt):
        for _ in range(k):
            rho, theta = np.random.uniform(r, 2 * r), np.random.uniform(0, 2 * np.pi)
            pt = refpt[0] + rho * np.cos(theta), refpt[1] + rho * np.sin(theta)
            if not (0 < pt[0] < width and 0 < pt[1] < height): continue
            if point_valid(pt): return pt
        return False

    pt = (np.random.uniform(0, width), np.random.uniform(0, height))
    samples = [pt]
    cells[get_cell_coords(pt)] = 0
    active = [0]
    nsamples = 1

    while active:
        idx = np.random.choice(active)
        refpt = samples[idx]
        pt = get_point(refpt)
        if pt:
            samples.append(pt)
            nsamples += 1
            active.append(len(samples) - 1)
            cells[get_cell_coords(pt)] = len(samples) - 1
        else:
            active.remove(idx)
    poisson = np.zeros((width, height), dtype=np.uint8)
    for row, col in samples:
        poisson[int(row), int(col)] = 255
    return poisson
