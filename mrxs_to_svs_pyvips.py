#Setup library requirements

import os

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
import pyvips
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

  
if __name__ == "__main__":
    # Get input and output file names from command line
    input_file = input("Type input file name (abc.mrxs): ")
    output_file = input("Type output file name (xyz.svs): ")

    # Run the conversion
    convert_mrxs_to_svs(input_file, output_file, tile_width = 256, tile_height = 256, compression="jpeg")


