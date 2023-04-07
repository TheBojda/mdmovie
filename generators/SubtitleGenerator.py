import re


class SubtitleGenerator:

    def generate(self, input_marks_file, output_sub_file):
        with open(input_marks_file, 'r') as f:
            data = f.read()

        pattern = r'"time":(\d+),"type":"sentence","start":(\d+),"end":(\d+),"value":"(.*?)"'
        matches = re.findall(pattern, data)

        # Create a list to hold the SRT subtitle data
        srt_data = []

        # Loop through each match and convert the timestamp to SRT format
        for i, match in enumerate(matches):
            start_time = int(match[0])
            end_time = int(matches[i + 1][0]) if i < len(matches) - 1 else None
            text = match[3]
            srt_timecode = '{:02d}:{:02d}:{:02d},{:03d} --> {:02d}:{:02d}:{:02d},{:03d}'.format(
                start_time // 3600000,
                start_time // 60000 % 60,
                start_time // 1000 % 60,
                start_time % 1000,
                end_time // 3600000 if end_time else 0,
                end_time // 60000 % 60 if end_time else 0,
                end_time // 1000 % 60 if end_time else 0,
                end_time % 1000 if end_time else 0
            )
            srt_data.append('{}\n{}\n{}\n\n'.format(i + 1, srt_timecode, text))

        # Write the SRT subtitle data to a new file
        with open(output_sub_file, 'w') as f:
            f.writelines(srt_data)
