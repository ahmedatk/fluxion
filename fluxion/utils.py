import numpy as np

def read_fbo_to_ndarray(fbo, width, height):
    data = fbo.read(components=3, alignment=1)
    arr = np.frombuffer(data, dtype=np.uint8)
    arr = arr.reshape((height, width, 3))
    arr = np.flipud(arr)
    return arr
