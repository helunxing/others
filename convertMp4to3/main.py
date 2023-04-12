import moviepy.editor as mp
import os

folder_addr = ""

dist_folder = os.path.join(folder_addr, 'dist')

os.mkdir(dist_folder)

for file_name in os.listdir(folder_addr):
    if file_name.startswith('.'):
        continue
    if not file_name.endswith('.mp4'):
        continue

    full_addr = os.path.join(folder_addr, file_name)
    clip = mp.VideoFileClip(full_addr)

    dst_addr = os.path.join(dist_folder, file_name[:-4] + '.mp3')
    clip.audio.write_audiofile(dst_addr)
