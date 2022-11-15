from os import walk
import pygame as pg


#walk will return tuple with 3 members (folder_path), (that file's subfolder), (filename in that folder)

def import_folder(path):
    surface_list = []
    for _,__,img_files in walk(path): #its will return list of img_file
        #imgfile is file name.
        for i in img_files:
            surface_list.append(pg.image.load(path + i).convert_alpha())
    return surface_list

#warning!! Each folder should have only img file only.

path = "Infographics/character/run/"
