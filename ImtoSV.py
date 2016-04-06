#!/usr/bin/env python
from subprocess import call
import os
import argparse

# (Im)age (to) (S)lideshow (V)ideo
# Created by Andrew James Collett, for the creation of slide shows from
# images, for use at Stellenbosch University.
'''
This script is intended to help one create a video from a set
of images, using ffmpeg. It is a Work In Progress
'''


def create_video(args, fname):
    args.append(fname)
    call(args)


# Adapted from http://stackoverflow.com/a/5921708
def intersperse(lst, item):

    # Remove the slide, so we don't have 3 in a row
    if item in lst:
        lst.remove(item)

    result = [item] * (len(lst) * 2 - 1)
    result[0::2] = lst
    return result


def slides(timings,    f_names):
    loop_arg = []
    final_args = ['ffmpeg']
    filter_str = ''
    end_string = ''
    i = 0

    for name in f_names:
        loop_arg.extend(['-loop', '1', '-t',
                        timings[name]['slide_dur'], '-i', name])
        filter_str = filter_str + '[' + str(i) + \
            ':v]setsar=sar=300/300,fade=t=in:st=0:d=' + \
            timings[name]['fade_dur'] + ',fade=t=out:st=' + \
            timings[name]['fade_start'] + ':d=' + \
            timings[name]['fade_dur'] + '[v' + str(i) + '];'

        end_string = end_string + '[v' + str(i) + ']'

        i = i + 1

    final_args.extend(loop_arg)
    end_string = end_string + 'concat=n=' + str(len(f_names)) + ':v=1:a=0[v]'
    final_args.extend(['-filter_complex', filter_str + end_string])
    final_args.extend(['-map', '[v]'])

    return final_args


# find all the files in the folder that match the extension
def process_folder(folder_name, ext):
    f_names = list([[dirpath + filename for filename in filenames] for dirpath,
                    dirnames, filenames in os.walk(folder_name)])[0]

    f_names.sort()

    for name in f_names:
        if not name.endswith(ext):
            f_names.remove(name)

    return f_names


# Create the arguments parser
def define_args():

    parser = argparse.ArgumentParser(
                        description='A slide show creator, from pictures having \
                        uniform size and format. Uses ffmpeg. \
                        There is a default fade in and fade out effect \
                        that you will need to edit code to change.')
    parser.add_argument('mode', help='The mode in which you want to the script \
                        to operate. create-config, will create a .conf file \
                        with the default values for the slideshow. You can \
                        then edit that config for custom times. \
                        slideshow-from-folder, this is an easy way to just \
                        create a default slideshow from a dir of files.\
                        slideshow-from-conf, here a config file can be read in\
                        ', choices=['create-config',
                        'slideshow-from-folder', 'slideshow-from-config'])
    parser.add_argument('-c', '--conf', help='The location of the conf file, \
                         Final / expected.', default='./tmp/gen.conf')
    parser.add_argument('-f', '--folder', help='The location of the images, \
                        Final / expected.', default='./tmp/')
    parser.add_argument('-rp', '--repeated_slide', help='Optional, \
                        name of the image you want repeated between each \
                        slide. Does nothing when reading config', default=None)
    parser.add_argument('-sd', '--slide_dur', help='Duration each slide will \
                        display for. Does nothing when reading config',
                        default='10')
    parser.add_argument('-fd', '--fade_dur', help='Duration of the fade-out and \
                        fade-in effect. Does nothing when reading config',
                        default='2')
    parser.add_argument('-fo', '--file_name', help='The output filename, \
                        with ext', default='out.mp4')
    parser.add_argument('-e', '--extension', help='Extension for input files. \
                        Does nothing when reading config', default='.jpg')
    return parser


def main():
    parser = define_args()
    args = parser.parse_args()

    mode = args.mode
    folder = args.folder
    timings = {}
    f_names = []

    if mode == 'slideshow-from-folder' or mode == 'create-config':
        ext = args.extension
        slide_dur = args.slide_dur
        fade_dur = args.fade_dur
        fade_start = str(int(slide_dur) - int(fade_dur))
        f_names = process_folder(folder, ext)
        rp_slide = args.repeated_slide
        timings = dict([(name, dict([('slide_dur', slide_dur),
                        ('fade_dur', fade_dur),
                        ('fade_start', fade_start)])) for name in f_names])

        if rp_slide is not None:
            f_names = intersperse(f_names, rp_slide)

        if mode == 'slideshow-from-folder':
            args_out = slides(timings, f_names)
            fname = args.file_name
            create_video(args_out, fname)
        else:
            conf_name = args.conf
            f = open(conf_name, 'w+')
            f.write('# Slide name, slide duration, fade duration. \
            All in seconds\n')
            for name in f_names:
                f.write(name + ', ' + timings[name]['slide_dur'] + ', ' +
                        timings[name]['fade_dur'] + '\n')

    elif mode == 'slideshow-from-config':
        conf_name = args.conf

        f = open(conf_name, 'r+')
        for line in f:
            if not line.startswith('#'):

                bits = line.strip().split(', ')
                timings[bits[0]] = dict([('slide_dur', bits[1]),
                                        ('fade_dur', bits[2]),
                                        ('fade_start', str(float(bits[1]) -
                                                           float(bits[2])))])
                f_names.append(bits[0])

        args_out = slides(timings, f_names)
        fname = args.file_name
        create_video(args_out, fname)

if __name__ == "__main__":
    main()
