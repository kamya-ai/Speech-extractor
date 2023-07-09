import argparse
import torch
torch.set_num_threads(1)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file_path", default='test.mp3',
                        help="Path of the audio file of which the voice is to be extracted.", type=str)
    args = parser.parse_args()

    file_path = args.file_path

    model, utils = torch.hub.load(repo_or_dir='snakers4/silero-vad',
                              model='silero_vad',
                              force_reload=False)

    (get_speech_timestamps, save_audio, read_audio, VADIterator, collect_chunks) = utils

    sampling_rate = 16000

    wav = read_audio('test.mp3', sampling_rate=sampling_rate)

    # get speech timestamps from full audio file
    speech_timestamps = get_speech_timestamps(wav, model, sampling_rate=sampling_rate)
    print(speech_timestamps)

    # # If timestamps are to be saved in a seperate .txt file
    # with open('timestamps.txt', 'w') as file:
    #     file.write(str(speech_timestamps))

    # Merging all speech chunks into one file
    save_audio('speech.wav', collect_chunks(speech_timestamps, wav), sampling_rate=sampling_rate) 

if __name__ == "__main__":
    main()