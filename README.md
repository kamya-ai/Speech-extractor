# Voice Activity Detection with Silero VAD Model 🔊🎙️

## Description 📝

This Python-based program utilizes the Silero VAD (Voice Activity Detection) model to extract voice segments from an audio file and save them in a new .wav file. 🎤📦

The Silero VAD model is a state-of-the-art model that can accurately detect speech activity in an audio signal. It is trained on a large dataset and can effectively distinguish between speech and non-speech segments. 🌟💡

## Features ✨

- Detects voice segments in an audio file. 🗣️
- Filters out non-speech segments. 🙉
- Gives the timestamps of the speech segments. ⏰
- Saves the extracted voice segments in a new .wav' file. 💾🎵

## Installation 🚀

1. Clone the repository:

   ```
   git clone https://github.com/kamya-ai/Speech-extractor.git
   ```

2. Install the required dependencies:

   ```
   pip install -r requirements.txt
   ```

## Usage 🎯

1. Run the script:

   ```
   python extract_voice.py --file_path test.mp3
   ```
   where, 'test.mp3' is the target file path.

3. The program will process the audio file using the Silero VAD model and save the extracted voice segments as `speech.wav` directory as a new .wav file.

## Configuration ⚙️

You can modify the following parameters in the `extract_voice.py` script:

- `file_path`: The name of the input audio file.

## Example 🌈

For example, let's say you have an audio file named `test.mp3` that contains both speech and background noise. Running the program using this file will generate a new .wav file named `speech.wav` that contains only the speech segments from the original file.

## Credits 💡

This program utilizes the Silero VAD model, developed by the Silero team. You can find more information about the model and the team on their [GitHub repository](https://github.com/snakers4/silero-vad).

Feel free to contribute and provide feedback to make this program even better! 🙌🚀
