import ffmpeg

def convert_480p(source):    
    new_file_name = source + '_480p.mp4'
    ffmpeg.input(source).output(new_file_name, s='hd480', vcodec='libx264', crf=23, acodec='aac', strict='experimental').run()


def convert_720p(source):    
    new_file_name = source + '_720p.mp4'
    ffmpeg.input(source).output(new_file_name, s='hd720', vcodec='libx264', crf=23, acodec='aac', strict='experimental').run()




# import subprocess

# def convert_480p(source):    
#     new_file_name = source  + '_480p.mp4'    
#     cmd = '/opt/homebrew/bin/ffmpeg -i "{}" -s hd480 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, new_file_name)    
#     run = subprocess.run(cmd, capture_output=True)

