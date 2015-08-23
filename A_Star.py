import pygame
from object_classes import *
from tileC import Tile

def A_Star(screen, survivor, total_frames, FPS):
    
    half = Tile.width / 2
    N = -40
    S = 40
    E = 1
    W = -1

    for tile in Tile.List:
        tile.parent = None
        tile.heuristic, tile.G_cost, tile.F_cost = 0,0,0

    def get_surrounding_tiles(base_node):
        
        array =(
            (base_node.number + N),
            (base_node.number + E),
            (base_node.number + S),
            (base_node.number + W),
            )

        tiles = []

        for tile_number in array:
            surrounding_tile = tile.get_tile(tile_number)            
            if tile_number not in range(1, Tile.total_tiles + 1):
                continue
            if surrounding_tile.walkable and surrounding_tile not in closed_list:
                tiles.append(surrounding_tile)
        return tiles

    def G(tile):
        tile.G_cost = tile.parent.G + 10

    def H(): # heuristic estimate the distance vaue from the player and hunter
        for tile in Tile.List:
            tile.heuristic = 10 * (abs(tile.x - survivor.x) + abs(tile.y - survivor.y)) / Tile.width

    def F(tile): # movement cost + heuristic
        # F = G + H
        tile.F_cost = tile.G_cost + tile.heuristic

    def swap(tile):
        open_list.remove(tile)
        closed_list.append(tile)

    def get_LFT(): # get Lowest F Value
        F_Values = []
        for tile in open_list:
            F_Values.append(tile.F_cost)

        o = open_list[::-1]

        for tile in o:
            if tile.F_cost == min(F_Values):
                return tile


    def loop():

        LFT = get_LFT() 
        swap(LFT)
        surrounding_nodes = get_surrounding_tiles(LFT)

        for node in surrounding_nodes:
            if node not in open_list:
                open_list.append(node)
                node.parent = LFT
            elif node in open_list:                
                calculated_G = LFT.G + 10
                if calculated_G < node.G:
                    node.parent = LFT
                    G(node)
                    F(node)

        if open_list == [] or survivor.get_tile() in closed_list:
            return
        for node in open_list:
            G(node)
            F(node)

        loop()        

    for zombie in Zombie.List:
        if zombie.tx != None or zombie.ty != None:
            continue

        open_list = []
        closed_list = []
        zombie_tile = zombie.get_tile()
        open_list.append(zombie_tile)
        surrounding_nodes = get_surrounding_tiles(zombie_tile)
        
        for node in surrounding_nodes:
            node.parent = zombie_tile
            open_list.append(node)
        swap(zombie_tile)
        H()

        for node in surrounding_nodes:
            G(node)
            F(node) 

        loop()
        return_tiles = []
        parent = survivor.get_tile()

        while True:
            return_tiles.append(parent)
            parent = parent.parent
            if parent == None:
                break
            if parent.number == zombie.get_number():
                break
            
        if len(return_tiles) > 1:
            next_tile = return_tiles[-1]
            zombie.set_target(next_tile)
