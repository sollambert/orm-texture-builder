from PIL import Image
import sys
import argparse
import glob

# Initialize arg parser
parser = argparse.ArgumentParser(
    prog="ORM Texture Builder",
    description='''This is a utility for creating an ORM map based on given AmbientOcclusion, Roughness, and Metalness information.
All file names must end with their corresponding name (i.e. *.AmbientOcclusion.jpg) to be detected automatically, otherwise the destination can be specified using the respective flag.

If a file is missing of the three, a resolution must be specified for the program to create a new, empty data image to use as the channel.

If no directory is specified, the script will execute in the current directory.''')

# Build flags for argument parsing
parser.add_argument('-d', '--directory', help="Directory to look for files and deposit the final ORM map")
parser.add_argument('-ao', '--ambient_occlusion', help="Ambient Occlusion image location")
parser.add_argument('-r', '--roughness', help="Roughness image location")
parser.add_argument('-m', '--metalness', help="Metalness image location")
parser.add_argument('-res', '--resolution', help="Resolution specified as {width}x{height}")
args = parser.parse_args()

#Acceptable file types for source images
filetypes = ('.png', '.jpg', '.jpeg')

# Init file locations
ao_location = None
r_location = None
m_location = None

# Find first image within directory that matches wildcard string
def find_image_file(directory, file_param):
    for type in filetypes:
        file = glob.glob(f'{directory}/*{file_param}{type}')
        if file:
            return file[0]
    return None

# Set directory to local current location if not given in args
if not args.directory:
    args.directory = "./"
    
# Determine AO image location based on arg or found file
if args.ambient_occlusion:
    ao_location = args.ambient_occlusion
else:
    ao_location = find_image_file(args.directory, "AmbientOcclusion")

# Determine Roughness image location based on arg or found file
if args.roughness:
    r_location = args.roughness
else:
    r_location = find_image_file(args.directory, "Roughness")

# Determine Metalness image location based on arg or found file
if args.metalness:
    m_location = args.metalness
else:
    m_location = find_image_file(args.directory, "Metalness")
    
# Parse resolution arg
if args.resolution:
    args.resolution = args.resolution.split("x")
    if len(args.resolution) != 2 or not args.resolution[0].isnumeric() or not args.resolution[1].isnumeric():
        print("Please specify resolution as (WIDTH)x(HEIGHT) with a decimal numeric value for width and height!")
        sys.exit()
    
# Determine if any file does not have a location, and if so ensure a resolution is specified to compensate
if not (ao_location
    and r_location
    and m_location) and not args.resolution:
    print("If a file is missing a resolution MUST be specified!")
    sys.exit()

# Print file locations
print("AO file: " + str(ao_location))
print("Roughness file: " + str(r_location))
print("Metalness file: " + str(m_location))

# Build a new image with zeroed data if no file location exists, otherwise load converted grayscale texture image
occlusion_map = Image.new('L', (int(args.resolution[0]), int(args.resolution[1]))) if not ao_location else Image.open(ao_location).convert('L')
roughness_map = Image.new('L', (int(args.resolution[0]), int(args.resolution[1]))) if not r_location else Image.open(r_location).convert('L')
metallic_map = Image.new('L', (int(args.resolution[0]), int(args.resolution[1]))) if not m_location else Image.open(m_location).convert('L')

# Create a new image with RGB mode
packed_texture = Image.new('RGB', occlusion_map.size)

# Combine the grayscale maps into RGB channels
combined_data = [(occlusion, roughness, metallic) for occlusion, roughness, metallic in zip(
    occlusion_map.getdata(), roughness_map.getdata(), metallic_map.getdata()
)]

# Build the new packed texture
packed_texture.putdata(combined_data)

# Save the packed texture
packed_texture.save(f'{args.directory}/{args.directory.split("/")[-1]}_orm_map.png')
