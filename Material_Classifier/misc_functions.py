import os
import json


def write_json(data, filename):
    '''
    FUNCTION TO WRITE A JSON FILE 
    '''
    with open(filename, "w") as outfile:
        json.dump(data, outfile, indent=4, sort_keys=True)


def open_json(filename):
    '''
    FUNCTION TO OPEN A JSON FILE
    Parameters
    ----------
    filename : TYPE STRING
        DESCRIPTION: NAME OF THE FILE TO BE OPENED.
    Returns
    -------
    data : TYPE DICT
        DESCRIPTION RETURN THE DATA FILE IN A DICT TYPE .
    '''
    with open(filename) as json_file:
        data = json.load(json_file)
        return data

def move_images(current_path, history_path):
    '''
    Function to move images into history folder
    '''
    # get the number of images in history folder
    if os.listdir(history_path) == 0:
        nb_images = 1
    else:
        nb_images = len(os.listdir(history_path))
    os.rename(current_path, history_path+"/image_"+str(nb_images)+".jpg")
    return history_path+"/image_"+str(nb_images)+".jpg", "image_"+str(nb_images)




def DisposalBin(ItemIdentifiedClass, region):

    if region == "The Hague":
        if ItemIdentifiedClass == "Cardboard" or ItemIdentifiedClass == "Paper":
            return "Papers Container"
        elif ItemIdentifiedClass =="Plastic Bag" or ItemIdentifiedClass == "Plastic Box" or ItemIdentifiedClass == "Plastic Round Container" or ItemIdentifiedClass == "Plastic Bottle":
            return "PMD"
        elif ItemIdentifiedClass == "Metal Can":
            return "PMD"
        elif ItemIdentifiedClass == "Glass Cup" or ItemIdentifiedClass == "Glass Bottle":
            return "Glass"
        elif ItemIdentifiedClass == "Drinking Carton":
            return "PMD" # this was done intentionally in different block for later testing purposes
        elif ItemIdentifiedClass == "Organic" or ItemIdentifiedClass == "Chips Bag":
            return "Rest"
        else:
            return "Rest (Unrecognized Item)"
    
    elif region == "Rotterdam":
        if ItemIdentifiedClass == "Cardboard" or ItemIdentifiedClass == "Paper":
            return "Papers Containers"
        elif ItemIdentifiedClass == "Chips Bag" or ItemIdentifiedClass == "Drinking Carton" or ItemIdentifiedClass == "Metal Can" or ItemIdentifiedClass =="Plastic Bag" or ItemIdentifiedClass == "Plastic Box" or ItemIdentifiedClass == "Plastic Round Container" or ItemIdentifiedClass == "Plastic Bottle":
            return "Rest"
        elif ItemIdentifiedClass == "Organic":
            return "Organics Container"
        elif ItemIdentifiedClass == "Glass Cup" or ItemIdentifiedClass == "Glass Bottle":
            return "Glass Container"
        else:
            return "Rest (Unrecognized Item)"
   
    elif region == "Amsterdam":
        if ItemIdentifiedClass == "Cardboard" or ItemIdentifiedClass == "Paper":
            return "Papers Container"
        elif ItemIdentifiedClass == "Glass Cup" or ItemIdentifiedClass == "Glass Bottle":
            return "Glass Container"
        elif ItemIdentifiedClass == "Drinking Carton" or ItemIdentifiedClass =="Plastic Bag" or ItemIdentifiedClass == "Plastic Box" or ItemIdentifiedClass == "Plastic Round Container" or ItemIdentifiedClass == "Plastic Bottle":
            return "Plastic Container"
        elif ItemIdentifiedClass == "Organic" or ItemIdentifiedClass == "Chips Bag" or ItemIdentifiedClass == "Metal Can":
            return "Rest"
        else:
            return "Rest (Unrecognized Item)"


