import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import glob, os
from itertools import permutations 

class VoxelCube:

    def __init__(self, size):
        self.size = size
        self.data = np.full((size,size,size), True)

    def intersect_x_y_image(self, pixel_square):
        for x in range(self.size):
            for y in range(self.size):
                for z in range(self.size):
                    self.data[x,y,z] = self.data[x,y,z] and pixel_square[x,y]

    def intersect_x_z_image(self, pixel_square):
        for x in range(self.size):
            for y in range(self.size):
                for z in range(self.size):
                    self.data[x,y,z] = self.data[x,y,z] and pixel_square[x,z]

    def intersect_y_z_image(self, pixel_square):
        for x in range(self.size):
            for y in range(self.size):
                for z in range(self.size):
                    self.data[x,y,z] = self.data[x,y,z] and pixel_square[y,z]

    def get_x_y_silhouette(self):
        silhouette = np.full((self.size, self.size), False)
        for x in range(self.size):
            for y in range(self.size):
                for z in range(self.size):
                    silhouette[x,y] = self.data[x,y,z] or silhouette[x,y]
        return silhouette

    def get_x_z_silhouette(self):
        silhouette = np.full((self.size, self.size), False)
        for x in range(self.size):
            for y in range(self.size):
                for z in range(self.size):
                    silhouette[x,z] = self.data[x,y,z] or silhouette[x,z]
        return silhouette

    def get_y_z_silhouette(self):
        silhouette = np.full((self.size, self.size), False)
        for x in range(self.size):
            for y in range(self.size):
                for z in range(self.size):
                    silhouette[y,z] = self.data[x,y,z] or silhouette[y,z]
        return silhouette

    #TODO: Check if it can be fooled by 
    #for example a zigzag snake in all directions and a tower hidng behind it
    def connected(self):
        connected = True
        for x in range(1, self.size - 1):
            layerConnected = False
            empty = True
            for y in range(self.size):
                for z in range(self.size):
                    if self.data[x,y,z]:
                        empty = False
                        layerConnected = layerConnected and self.data[x-1][y][z]
                        layerConnected = layerConnected and self.data[x+1][y][z]
                        if y > 0:
                            layerConnected = layerConnected and self.data[x-1][y-1][z]
                            layerConnected = layerConnected and self.data[x+1][y-1][z]
                        if y < self.size -  1:
                            layerConnected = layerConnected and self.data[x-1][y+1][z]
                            layerConnected = layerConnected and self.data[x+1][y+1][z]
                        if z > 0:
                            layerConnected = layerConnected and self.data[x-1][y][z-1]
                            layerConnected = layerConnected and self.data[x+1][y][z-1]
                        if z < self.size -  1:
                            layerConnected = layerConnected and self.data[x-1][y][z+1]
                            layerConnected = layerConnected and self.data[x+1][y][z+1]
            connected = connected and (layerConnected or empty)
        for y in range(1, self.size - 1):
            layerConnected = False
            empty = True
            for x in range(self.size):
                for z in range(self.size):
                    if self.data[x,y,z]:
                        empty = False
                        layerConnected = layerConnected and self.data[x][y-1][z]
                        layerConnected = layerConnected and self.data[x][y+1][z]
                        if x > 0:
                            layerConnected = layerConnected and self.data[x-1][y-1][z]
                            layerConnected = layerConnected and self.data[x-1][y+1][z]
                        if x < self.size -  1:
                            layerConnected = layerConnected and self.data[x+1][y-1][z]
                            layerConnected = layerConnected and self.data[x+1][y+1][z]
                        if z > 0:
                            layerConnected = layerConnected and self.data[x][y-1][z-1]
                            layerConnected = layerConnected and self.data[x][y+1][z-1]
                        if z < self.size -  1:
                            layerConnected = layerConnected and self.data[x][y-1][z+1]
                            layerConnected = layerConnected and self.data[x][y+1][z+1]
            connected = connected and (layerConnected or empty)
        for z in range(1, self.size - 1):
            layerConnected = False
            empty = True
            for x in range(self.size):
                for y in range(self.size):
                    if self.data[x,y,z]:
                        empty = False
                        layerConnected = layerConnected or self.data[x][y][z-1]
                        layerConnected = layerConnected or self.data[x][y][z+1]
                        if x > 0:
                            layerConnected = layerConnected or self.data[x-1][y][z-1]
                            layerConnected = layerConnected or self.data[x-1][y][z+1]
                        if x < self.size -  1:
                            layerConnected = layerConnected or self.data[x+1][y][z-1]
                            layerConnected = layerConnected or self.data[x+1][y][z+1]
                        if y > 0:
                            layerConnected = layerConnected or self.data[x][y-1][z-1]
                            layerConnected = layerConnected or self.data[x][y-1][z+1]
                        if y < self.size -  1:
                            layerConnected = layerConnected or self.data[x][y+1][z-1]
                            layerConnected = layerConnected or self.data[x][y+1][z+1]
            connected = connected and (layerConnected or empty)
        return True

def all_symbol_variants_from_file(path):
    symbols = []
    name = path.split("\\")[-1].split("/")[-1].split(".")[0]    #should split off file path and name
    symbol = load_symbol_from_file(file_name)
    symbols.append((symbol, name))
    mirrors = create_symbolmirs(symbol)
    symbols.append((mirrors[0], name+"_xmir"))
    symbols.append((mirrors[1], name+"_ymir"))
    rotations = create_symbol_rotations(symbol)
    symbols.append((rotations[0], name+"_r90"))
    symbols.append((rotations[1], name+"_r180"))
    symbols.append((rotations[2], name+"_r270"))
    mirrors = create_symbolmirs(rotations[0])
    symbols.append((mirrors[0], name+"_r90_xmir"))
    symbols.append((mirrors[1], name+"_r90_ymir"))
    mirrors = create_symbolmirs(rotations[1])
    symbols.append((mirrors[0], name+"_r180_xmir"))
    symbols.append((mirrors[1], name+"_r180_ymir"))
    mirrors = create_symbolmirs(rotations[2])
    symbols.append((mirrors[0], name+"_r270_xmir"))
    symbols.append((mirrors[1], name+"_r270_ymir"))
    return symbols

def load_symbol_from_file(path):
    with Image.open(path) as im:
        symbol = np.full((5,5), True)
        (xmax, ymax) = im.size
        for x in range(xmax):
            for y in range(ymax):
                symbol[x,y] = im.getpixel((x, y)) == 0
        return symbol

def create_symbol_rotations(symbol):
    rotated_90 = np.rot90(symbol,1,(1,0))
    rotated_180 = np.rot90(rotated_90,1,(1,0))
    rotated_270 = np.rot90(rotated_180,1,(1,0))
    return [rotated_90, rotated_180, rotated_270]

def create_symbolmirs(symbol):
    mirror_x = np.flipud(symbol)
    mirror_y = np.fliplr(symbol)
    return [mirror_x, mirror_y]

def test_symbol_set(symbol1tuple,symbol2tuple,symbol3tuple):
    (symbol1, symbol1_name) = symbol1tuple
    (symbol2, symbol2_name) = symbol2tuple
    (symbol3, symbol3_name) = symbol3tuple
    voxels = VoxelCube(5)
    voxels.intersect_x_y_image(symbol1)
    voxels.intersect_x_z_image(symbol2)
    voxels.intersect_y_z_image(symbol3)
    silhouettes_intact = np.array_equal(symbol1, voxels.get_x_y_silhouette())
    silhouettes_intact = silhouettes_intact and np.array_equal(symbol2, voxels.get_x_z_silhouette())
    silhouettes_intact = silhouettes_intact and np.array_equal(symbol3, voxels.get_y_z_silhouette())
    if silhouettes_intact:
        print(symbol1_name + symbol2_name + symbol3_name + " silhouette intact")
    if voxels.connected():
        print(symbol1_name + symbol2_name + symbol3_name + " connected voxels")
    if silhouettes_intact and voxels.connected():
        voxelarray = np.asarray(voxels.data)
        colors = np.empty(voxelarray.shape, dtype=object)
        colors[voxelarray] = 'red'
        ax = plt.figure().add_subplot(projection='3d')
        ax.voxels(voxelarray, facecolors=colors, edgecolor='k')
        plt.show()

if __name__ == "__main__":
    useInput = input("Do you want to input 3 letters y/n(default): ")
    if not useInput == "y":
        symbols = []
        fileNames = glob.glob("symbols/*.png")
        for file_name in fileNames:
            symbols.extend(all_symbol_variants_from_file(file_name))

        # symbols = [([
        #             [True, True, True, True, True],
        #             [True, False, False, False, False],
        #             [True, True, True, True, True],
        #             [False, False, False, False, True],
        #             [True, True, True, True, True]],"Test")]

        for symbol1tuple in symbols:
            for symbol2tuple in symbols:
                for symbol3tuple in symbols:
                    test_symbol_set(symbol1tuple,symbol2tuple,symbol3tuple)
    else:
        chars = ""
        while len(chars) != 3:
            chars = input("Input 3 letter characters without spaces in between: ")
        chars = chars.capitalize()
        chars = list(chars)
        charsymbols = []
        fileNames = glob.glob(f"symbols/{chars[0]}.png")
        for file_name in fileNames:
            charsymbols.append(all_symbol_variants_from_file(file_name))
        fileNames = glob.glob(f"symbols/{chars[1]}.png")
        for file_name in fileNames:
            charsymbols.append(all_symbol_variants_from_file(file_name))
        fileNames = glob.glob(f"symbols/{chars[2]}.png")
        for file_name in fileNames:
            charsymbols.append(all_symbol_variants_from_file(file_name))
        perms = permutations([0, 1, 2]) 
        for perm in perms:
            for symbol1tuple in charsymbols[perm[0]]:
                for symbol2tuple in charsymbols[perm[1]]:
                    for symbol3tuple in charsymbols[perm[2]]:
                        test_symbol_set(symbol1tuple,symbol2tuple,symbol3tuple)