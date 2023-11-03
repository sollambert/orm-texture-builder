This is a utility for creating an ORM map based on given AmbientOcclusion,
Roughness, and Metalness information. All file names must end with their
corresponding name (i.e. *.AmbientOcclusion.jpg) to be detected automatically,
otherwise the destination can be specified using the respective flag. If a
file is missing of the three, a resolution must be specified for the program
to create a new, empty data image to use as the channel. If no directory is
specified, the script will execute in the current directory.

<pre>
options:
  -h, --help            show this help message and exit
  -d DIRECTORY, --directory DIRECTORY
                        Directory to look for files and deposit the final ORM
                        map
  -ao AMBIENT_OCCLUSION, --ambient_occlusion AMBIENT_OCCLUSION
                        Ambient Occlusion image location
  -r ROUGHNESS, --roughness ROUGHNESS
                        Roughness image location
  -m METALNESS, --metalness METALNESS
                        Metalness image location
  -res RESOLUTION, --resolution RESOLUTION
                        Resolution specified as {width}x{height}
</pre>
```
python3 orm_texture_builder.py
```
