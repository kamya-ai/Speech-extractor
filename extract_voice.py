import argparse
import torch
import os
from glob import glob
from pathlib import Path
torch.set_num_threads(1)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir_path", default='./',
                        help="Path of the audio file of which the voice is to be extracted.", type=str)
    parser.add_argument("--out_path", default = './',
                        help="Path of the output file", type=str)
    parser.add_argument("--save_speech", default=False,
                        help="Flag to save the audio with speech, without other sounds", type=bool)
    parser.add_argument("--save_segments", default=False,
                        help="Save segments", type=bool)
    parser.add_argument("--save_trashhold", default=8,
                        help="Seconds by save_segments", type=int)
    args = parser.parse_args()

    dir_path = args.dir_path
    out_path = args.out_path
    save_speech = args.save_speech
    save_segments = args.save_segments
    save_trashhold = args.save_trashhold

    model, utils = torch.hub.load(repo_or_dir='snakers4/silero-vad',
                              model='silero_vad',
                              force_reload=False)

    (get_speech_timestamps, save_audio, read_audio, VADIterator, collect_chunks) = utils

    sampling_rate = 16000
    for i, path in enumerate(Path(dir_path).glob('*.wav')):
        wav = read_audio(path, sampling_rate=sampling_rate)
        filename = os.path.basename(path)[:-4]

        # get speech timestamps from full audio file
        speech_timestamps = get_speech_timestamps(wav, model, sampling_rate=sampling_rate)
        if not save_speech:
            no_speech_timestamps = []
            start = speech_timestamps[0]['start']
            end = speech_timestamps[0]['end']
            no_speech_timestamps.append({'start': 0, 'end': start})
            for fragment in speech_timestamps[1:(len(speech_timestamps))]:
                start = end
                no_speech_timestamps.append({'start': start, 'end': fragment['start']})
                end = fragment['end']
            start = speech_timestamps[-1]['end']
            end = len(wav)
            no_speech_timestamps.append({'start': start, 'end': end})
            speech_timestamps = no_speech_timestamps

        print(speech_timestamps)
        if(save_segments):
            i = 0
            seconds_prev = 0
            fragments_to_save = []
            for fragment in speech_timestamps:
                fragments_to_save.append(fragment)
                start = fragment["start"]
                end = fragment["end"]
                seconds = ((end - start) / sampling_rate) + seconds_prev
                if seconds > save_trashhold:
                    print(str(filename) + f".{i}_cut.wav", seconds)
                    save_audio(os.path.join(out_path, str(filename) + f".{i}_cut.wav"), collect_chunks(fragments_to_save, wav), sampling_rate=sampling_rate)
                    i += 1
                    seconds_prev = 0
                    fragments_to_save = []
                else:
                    seconds_prev = seconds
            if fragments_to_save != [] and seconds > 3:
                print(str(filename) + f".{i}_cut.wav", seconds)
                save_audio(os.path.join(out_path, str(filename) + f".{i}_cut.wav"), collect_chunks(fragments_to_save, wav), sampling_rate=sampling_rate)
        else:
            save_audio(os.path.join(out_path, str(filename) + "_cut.wav"), collect_chunks(speech_timestamps, wav), sampling_rate=sampling_rate)
        print("Done:", filename)

if __name__ == "__main__":
    main()