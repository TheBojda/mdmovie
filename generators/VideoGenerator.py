import os.path
from moviepy.editor import ImageClip, CompositeVideoClip, AudioFileClip

from generators.GeneratorBase import GeneratorBase


def find_key(key, lst):
    return next((tup[1] for tup in lst if key in tup), None)


class VideoGenerator(GeneratorBase):

    def __init__(self, base_path):
        super().__init__()
        self.base_path = base_path
        self.clips = []
        self.audio = None

    def handle_starttag(self, tag, attrs):
        # print("Encountered a start tag:", tag, attrs)
        if tag == 'audio:clip':
            path = os.path.join(self.base_path, find_key('src', attrs))
            self.audio = AudioFileClip(path)
        if tag == 'img':
            path = os.path.join(self.base_path, find_key('src', attrs))
            start = find_key('start', attrs)
            end = find_key('end', attrs)
            crossfadein = find_key('crossfadein', attrs)
            fadein = find_key('fadein', attrs)
            fadeout = find_key('fadeout', attrs)

            print('image', attrs)
            image_clip = ImageClip(path)
            if start:
                image_clip = image_clip.set_start(int(start))
            if end:
                image_clip = image_clip.set_end(int(end))
            if crossfadein:
                image_clip = image_clip.crossfadein(int(crossfadein))
            if fadein:
                image_clip = image_clip.fadein(int(fadein))
            if fadeout:
                image_clip = image_clip.fadeout(int(fadeout))

            self.clips.append(image_clip)

    def generate(self, movie_file):
        video = CompositeVideoClip(self.clips).set_duration(self.audio.duration)
        video = video.set_audio(self.audio)
        video.write_videofile(movie_file, fps=30)
