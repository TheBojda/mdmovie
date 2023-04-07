import html.parser
import os.path
from moviepy.editor import ImageClip, CompositeVideoClip, AudioFileClip


def find_key(key, lst):
    return next((tup[1] for tup in lst if key in tup), None)


class VideoGenerator(html.parser.HTMLParser):

    def __init__(self, base_path):
        super().__init__()
        self.base_path = base_path
        self.clips = []
        self.audio = None
        self.width = None
        self.height = None

    def handle_starttag(self, tag, attrs):
        # print("Encountered a start tag:", tag, attrs)
        if tag == 'video:settings':
            self.width = find_key('width', attrs)
            self.height = find_key('height', attrs)
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
            zoomout = find_key('zoomout', attrs)

            print('image', attrs)
            image_clip = ImageClip(path)
            if self.width and self.height:
                image_clip = image_clip.resize(width=int(self.width), height=int(self.height))
            if start:
                image_clip = image_clip.set_start(int(start))
            if end:
                image_clip = image_clip.set_end(int(end))
            if zoomout:
                scale = float(zoomout)
                step = (scale - 1) / image_clip.duration
                w = image_clip.w
                h = image_clip.h

                def crop_center(get_frame, t):
                    frame = get_frame(t)
                    y1 = int((frame.shape[0] - h) / 2)
                    x1 = int((frame.shape[1] - w) / 2)
                    return frame[y1: y1 + h, x1: x1 + w]

                image_clip = image_clip.resize(lambda t: scale - step * t).fl(crop_center)
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
