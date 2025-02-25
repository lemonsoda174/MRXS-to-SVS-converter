import tkinter as tk
from tkinter.filedialog import askopenfilename, askdirectory
tk.Tk().withdraw() # part of the import if you are not using other tkinter functions

mode = 0
while mode != "S" and mode != "B":
    mode = input("Type S if you want to convert a single file \nType B if you want to batch convert all files within a folder \n[S/B]\n")
    if mode == "S":
        fn = askopenfilename()
        print("The file directory is:", fn)
    elif mode == "B":
        fn = askdirectory()
        print("The folder directory is:", fn)
    else:
        print("\nImproper mode choice. Try again")

#Setup library requirements
import os, sys, pyvips

# Get the absolute path to the folder containing this script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Build the path to the "bin" folder inside "vips-dev-8.16"
vipsbin = os.path.join(script_dir, 'lib', 'vips-dev-8.16', 'bin')

add_dll_dir = getattr(os, 'add_dll_directory', None)
if callable(add_dll_dir):
    add_dll_dir(vipsbin)
else:
    os.environ['PATH'] = os.pathsep.join((vipsbin, os.environ['PATH']))


#Converter
def convert_mrxs_to_svs(input_file, output_file, compression="none", tile_width=256, tile_height=256):
    # Open the MRXS file
    image = pyvips.Image.new_from_file(input_file, access="sequential")
    
    # Prepare compression settings (optional)
    if compression == "none":
        compression_option = "none"
    elif compression == "jpeg":
        compression_option = "jpeg"
    elif compression == "lzw":
        compression_option = "lzw"
    elif compression == "deflate":
        compression_option = "deflate"
    elif compression == "packbits":
        compression_option = "packbits"
    elif compression == "ccittfax4":
        compression_option = "ccittfax4"
    else:
        raise ValueError(f"Unsupported compression type: {compression}")
    
    # Save the image to SVS format with the chosen options
    image.tiffsave(f"Output//{output_file}", tile=True, tile_width=tile_width, tile_height=tile_height,
                   compression=compression_option, pyramid=True)
    print(f"Conversion completed: {output_file}")

def write_file_name(input_file_dir):
    input_file_name = input_file_dir.split("/")[-1]
    output_file_name = input_file_name.replace(".mrxs", ".svs")
    return input_file_name, output_file_name 

if __name__ == "__main__":
    # Get input and output file names
    if mode == "S":
        input_file, output_file = write_file_name(fn)

        # Run the conversion
        confirm = input(f"Convert {input_file} into {output_file} ?\n[Y/N]\n")
        if confirm == "Y":
            # compression mode and tile size can later be modified if needed
            convert_mrxs_to_svs(fn, output_file, tile_width = 256, tile_height = 256, compression="jpeg")
        else:
            sys.exit("No conversion. System exit.")


    elif mode == "B":
        file_list = os.listdir(fn)
        mrxs_files_list = []
        convertible_files = []
        #extract paths for MIRAX files only and ignore other files
        for f in file_list:
            if ".mrxs" in f:
                same_name_folder = f.split(".mrxs")[0]
                if same_name_folder in file_list:
                    file_dir = fn + "/" + f
                    mrxs_files_list.append(file_dir)      
                else:
                    print(f"Exception: MIRAX file {f} does not have accompanied .DAT files. Excluded in conversion")
                    continue

        # Run the conversion
        for path in mrxs_files_list:
            input_file, output_file = write_file_name(path)
            print(f"Convert {input_file} into {output_file} ?")
            convertible_files.append((path, output_file))
        print("[Y/N]")
        confirm = input()

        if confirm != "Y":
            sys.exit("No conversion. System exit.")
            # compression mode and tile size can later be modified if needed
        for (a, b) in convertible_files:
            convert_mrxs_to_svs(a, b, tile_width = 256, tile_height = 256, compression="jpeg")
            

            


