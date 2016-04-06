# ImtoSV
A script to create a slideshow video from a bunch of images, using ffmpeg.

The script has command line options:

```
$ python ImtoSV.py -h

usage: ImtoSV.py [-h] [-c CONF] [-f FOLDER] [-rp REPEATED_SLIDE]
                 [-sd SLIDE_DUR] [-fd FADE_DUR] [-fo FILE_NAME] [-e EXTENSION]
                 {create-config,slideshow-from-folder,slideshow-from-config}

A slide show creator, from pictures having uniform size and format. Uses
ffmpeg. There is a default fade in and fade out effect that you will need to
edit code to change.

positional arguments:
  {create-config,slideshow-from-folder,slideshow-from-config}
                        The mode in which you want to the script to operate.
                        create-config, will create a .conf file with the
                        default values for the slideshow. You can then edit
                        that config for custom times. slideshow-from-folder,
                        this is an easy way to just create a default slideshow
                        from a dir of files. slideshow-from-conf, here a
                        config file can be read in

optional arguments:
  -h, --help            show this help message and exit
  -c CONF, --conf CONF  The location of the conf file, Final / expected.
  -f FOLDER, --folder FOLDER
                        The location of the images, Final / expected.
  -rp REPEATED_SLIDE, --repeated_slide REPEATED_SLIDE
                        Optional, name of the image you want repeated between
                        each slide. Does nothing when reading config
  -sd SLIDE_DUR, --slide_dur SLIDE_DUR
                        Duration each slide will display for. Does nothing
                        when reading config
  -fd FADE_DUR, --fade_dur FADE_DUR
                        Duration of the fade-out and fade-in effect. Does
                        nothing when reading config
  -fo FILE_NAME, --file_name FILE_NAME
                        The output filename, with ext
  -e EXTENSION, --extension EXTENSION
                        Extension for input files. Does nothing when reading
                        config

```
