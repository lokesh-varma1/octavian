from flask import Flask, request, jsonify
import os
import assemblyai as aai
from moviepy.editor import VideoFileClip
import logging

app = Flask(__name__)

# Replace 'your_api_key' with your AssemblyAI API key
ASSEMBLYAI_API_KEY = '63523cf4483f46e880edaac2465f4811'
aai.settings.api_key = ASSEMBLYAI_API_KEY

# Set up logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/transcribe', methods=['POST'])
def transcribe():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    file_path = os.path.join('uploads', file.filename)
    file.save(file_path)

    try:
        # Extract audio from video
        logging.debug(f"Processing file: {file_path}")
        video = VideoFileClip(file_path)
        audio_path = file_path.replace('.mp4', '.wav')
        video.audio.write_audiofile(audio_path)

        # Upload audio file to AssemblyAI
        logging.debug(f"Uploading audio file: {audio_path}")
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(audio_path)

        # Get the transcription text
        transcription = transcript.text
        logging.debug(f"Transcription: {transcription}")

        # Save the transcription to a text file
        transcript_file_path = file_path.replace('.mp4', '.txt')
        with open(transcript_file_path, 'w') as transcript_file:
            transcript_file.write(transcription)
        
        logging.debug(f"Transcription saved to: {transcript_file_path}")

        # Clean up
        os.remove(file_path)
        os.remove(audio_path)

        return jsonify({'transcription': transcription, 'transcript_file': transcript_file_path})
    except Exception as e:
        logging.error(f"Error during transcription: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    app.run(debug=True, host='0.0.0.0')
