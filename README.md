# Whisper Subtitler/Transcriber for Google Colab

A Google Colab notebook that uses OpenAI's Whisper model to generate transcriptions and subtitles from audio/video files or online platforms.

> Developed by Max Lee to promote the automation of audiovisual translation progress with the power of AI. This tool aims to make content more accessible through accurate transcription and subtitle generation.

## 🚀 Try it now on Google Colab!

<div align="center">
<a href="https://colab.research.google.com/drive/14osxUm5FeE9GjyGuRPLCiTuPpRyZs06R?usp=sharing">
<img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab" width="200"/>
</a>
</div>

> 💡 **Note**: This repository contains the Google Colab version. For a local version with a web interface, please visit [whisper-subtitler-transcriber](https://github.com/Max-Lee-explore/whisper-subtitler-transcriber).

> 💡 **Getting Started**:
> 1. Click the "Open in Colab" button above to open the notebook
> 2. To save a copy to your Google Drive:
>    - Go to File -> Save a copy in Drive
>    - This will create your own editable version
>    - You can then run and modify the code as needed

## Features

- 🎥 **Multiple Input Sources**
  - YouTube URL support
  - Local file upload support
  - Supported formats: `.mp3`, `.mp4`, `.wav`, `.m4a`, `.ogg`, `.flac`, `.aac`, `.webm`

- 🎯 **Transcription Options**
  - Text transcription (.txt)
  - Subtitle file (.srt)
  - Multiple language support
  - Optional initial prompt for better accuracy

- 🚀 **Model Selection**
  - tiny (fastest, least accurate)
  - base (fast, good accuracy)
  - small (balanced)
  - medium (accurate)
  - large (most accurate, slowest)

- 📊 **Progress Tracking**
  - Progress bars for model loading
  - Progress bars for transcription
  - File size information
  - Clear status messages

## Usage

1. **Setup**
   - Open the notebook in Google Colab
   - Make sure to select T4 GPU in Runtime settings
   - Run the setup cell to install dependencies

   > 💡 **Tip**: The setup cell will install all required packages. This may take a few minutes.

2. **Input Video/Audio**
   - Choose between YouTube URL or file upload
   - For YouTube: Paste URL and click "Download Video"
   - For local files: Click "Choose Files" to upload
   - Files are saved in the `audio_source` folder

   > 💡 **Tip**: For YouTube videos, make sure the URL is publicly accessible. For local files, ensure they're in a supported format.

3. **Configure Settings**
   - Select output format (txt or srt)
   - Choose model size
   - Select language (or auto-detect)
   - Add optional initial prompt

   > 💡 **Tip**: 
   > - For general use, start with the "base" model
   > - If you know the language, select it for better accuracy
   > - Initial prompts help with technical terms or specific contexts

4. **Generate Transcription**
   - Click "Generate Transcription"
   - Wait for the process to complete
   - Download the generated file

   > 💡 **Tip**: The process time depends on the file length and model size. Progress bars will show the current status.

## Requirements

- Google Colab account
- T4 GPU runtime
- Internet connection for YouTube downloads

> 💡 **Note**: The free Colab tier has limitations on GPU usage time. Consider upgrading for longer processing times if you have large batch transcription tasks.

## File Size Limits

- Maximum file size: 2GB
- Files exceeding this limit will be rejected
- File sizes are displayed in human-readable format

> 💡 **Tip**: For longer videos, consider splitting them into smaller segments.

## Output Files

- Text transcription: `[filename]_transcription.txt`
- Subtitles: `[filename]_subtitles.srt`
- Files are saved in the current Colab session
- Download button appears after generation

> 💡 **Tip**: Always download your files before closing the Colab session, as files are temporarily stored.

## Notes

- The process requires a GPU for optimal performance
- Larger models provide better accuracy but take longer to process
- Initial prompts can help improve accuracy for specific content
- All files are temporarily stored in the Colab session

> 💡 **Tip**: For best results with technical content, provide an initial prompt with relevant terminology.

## Troubleshooting

1. **GPU Not Found**
   - Go to Runtime -> Change runtime type
   - Select GPU as Hardware accelerator
   - Choose T4 GPU

   > 💡 **Tip**: If GPU is not available, try refreshing the page or waiting a few minutes.

2. **File Upload Issues**
   - Check file format is supported
   - Ensure file size is under 2GB
   - Try refreshing the page if upload fails

   > 💡 **Tip**: If upload fails, try clearing your browser cache or using a different browser.

3. **Download Issues**
   - Check internet connection
   - Try using a different YouTube URL
   - Ensure the video is publicly accessible

   > 💡 **Tip**: For YouTube videos, try using the video ID format if the full URL doesn't work.

## License

This project is open source and available under the MIT License.

---

> Developed by Max Lee to make audiovisual content more accessible through AI-powered transcription and translation. 