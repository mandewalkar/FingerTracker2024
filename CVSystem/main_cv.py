import sys
import time
import os
import shutil
from code import Video_PreProcessing
from code import Braille_Finger_tracker
from code import Convert_txt_2_csv
from code import predict
#from code import Map_Braille_character
#from code import Braille_2_coord
from code import Display


if __name__ == '__main__':
    command_line_arguments = sys.argv[1:] #argument 0 is  file name and argument 1 is fps and arg 2 is touchscreen file name
    Video_PreProcessing.main(command_line_arguments[0], int(command_line_arguments[1]))
    Convert_txt_2_csv.main(command_line_arguments[2])
    predict.main(Braille_Finger_tracker.main(int(command_line_arguments[1])))
    Display.main()
    #Map_Braille_character.main()

    #post processing
    new_dir = "output_" + time.strftime('%Y-%m-%d_%H.%M.%S', time.localtime(time.time()))
    folder_path = os.path.join(os.getcwd(), 'output_logs')
    files_in_directory = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    os.makedirs(os.path.join(folder_path,new_dir), exist_ok=True)
    # move each file in the list
    for file_path in files_in_directory:
        shutil.move(os.path.join(folder_path,file_path), os.path.join(folder_path, new_dir, file_path))
    


