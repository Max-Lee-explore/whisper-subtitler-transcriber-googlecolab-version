# Developed by Max Lee to promote the automation of audiovisual translation progress with the power of AI. This tool aims to make content more accessible through accurate transcription and subtitle generation.

#@title Setup and Installation (Click to expand)
!pip install -q openai-whisper pytube yt-dlp tqdm

#@title Import Required Libraries (Click to expand)
import os
import whisper
from pytube import YouTube
import yt_dlp
import tempfile
import torch
from IPython.display import display, HTML, clear_output
import ipywidgets as widgets
from google.colab import files
import shutil
import datetime
from tqdm.notebook import tqdm
import humanize

#@title Step 1: Check GPU (Click to expand)
def check_gpu():
    """Check if T4 GPU is available and selected"""
    if not torch.cuda.is_available():
        print("❌ No GPU detected. Please select T4 GPU in Colab runtime settings.")
        print("Go to Runtime -> Change runtime type -> Hardware accelerator -> GPU -> T4")
        return False
    
    gpu_name = torch.cuda.get_device_name(0)
    if "T4" not in gpu_name:
        print(f"❌ Current GPU: {gpu_name}")
        print("Please select T4 GPU in Colab runtime settings.")
        print("Go to Runtime -> Change runtime type -> Hardware accelerator -> GPU -> T4")
        return False
    
    print(f"✅ GPU detected: {gpu_name}")
    return True

# Run GPU check
check_gpu()

#@title Step 2: Input Video (Click to expand)
def get_file_size(file_path):
    """Get file size in human-readable format"""
    size_bytes = os.path.getsize(file_path)
    return humanize.naturalsize(size_bytes)

def check_file_size(file_path):
    """Check if file size is within limits (2GB)"""
    size_bytes = os.path.getsize(file_path)
    if size_bytes > 2 * 1024 * 1024 * 1024:  # 2GB in bytes
        raise Exception("File size exceeds 2GB limit. Please use a smaller file.")
    return True

def download_video(url):
    """Download video from URL and extract audio"""
    try:
        # Create an audio_source directory in the current folder if it doesn't exist
        if not os.path.exists('audio_source'):
            os.makedirs('audio_source')
        
        # Configure yt-dlp options for audio extraction
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': os.path.join('audio_source', '%(title)s.%(ext)s'),
            'quiet': True,
            'no_warnings': True
        }
        
        # Download and extract audio
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print("⏳ Downloading video...")
            info = ydl.extract_info(url, download=True)
            audio_path = os.path.join('audio_source', f"{info['title']}.mp3")
            
            # Check file size
            check_file_size(audio_path)
            print(f"📁 File size: {get_file_size(audio_path)}")
            
            return audio_path, info['title']
            
    except Exception as e:
        raise Exception(f"Error downloading video: {str(e)}")

def create_video_input_interface():
    """Create interactive interface for video input"""
    # Create widgets
    input_type = widgets.RadioButtons(
        options=[
            ('YouTube URL', 'url'),
            ('Upload File', 'file')
        ],
        description='Input Type:',
        disabled=False,
        layout=widgets.Layout(width='50%')
    )
    
    url_input = widgets.Text(
        value='',
        placeholder='Paste your YouTube URL here...',
        description='URL:',
        disabled=False,
        layout=widgets.Layout(width='80%')
    )
    
    status_output = widgets.Output()
    
    def on_url_submit(b):
        with status_output:
            clear_output()
            if not url_input.value:
                print("❌ Please enter a YouTube URL")
                return
            
            try:
                print("⏳ Downloading video...")
                audio_path, title = download_video(url_input.value)
                print(f"✅ Video downloaded: {title}")
                print(f"📁 File saved in: {audio_path}")
                print("\nProceed to Step 3 to configure settings.")
                return audio_path, title
            except Exception as e:
                print(f"❌ Error: {str(e)}")
                return None, None
    
    def on_file_upload(change):
        with status_output:
            clear_output()
            if not change['new']:
                print("❌ No file uploaded")
                return None, None
            
            # Create audio_source directory if it doesn't exist
            if not os.path.exists('audio_source'):
                os.makedirs('audio_source')
            
            # Get the uploaded file
            filename = list(change['new'].keys())[0]
            content = change['new'][filename]['content']
            
            # Check file extension
            allowed_extensions = ('.mp3', '.mp4', '.wav', '.m4a', '.ogg', '.flac', '.aac', '.webm')
            if not filename.lower().endswith(allowed_extensions):
                print(f"❌ Unsupported file format. Please use: {', '.join(allowed_extensions)}")
                return None, None
            
            # Save the file to the audio_source directory
            file_path = os.path.join('audio_source', filename)
            with open(file_path, 'wb') as f:
                f.write(content)
            
            # Check file size
            try:
                check_file_size(file_path)
                print(f"✅ File uploaded: {filename}")
                print(f"📁 File size: {get_file_size(file_path)}")
                print(f"📁 File saved in: {file_path}")
                print("\nProceed to Step 3 to configure settings.")
                return file_path, os.path.splitext(filename)[0]
            except Exception as e:
                print(f"❌ Error: {str(e)}")
                if os.path.exists(file_path):
                    os.remove(file_path)
                return None, None
    
    # Create submit button for URL
    submit_button = widgets.Button(
        description='Download Video',
        disabled=False,
        button_style='primary',
        tooltip='Click to download the video',
        layout=widgets.Layout(width='200px', height='40px')
    )
    submit_button.on_click(on_url_submit)
    
    # Create file upload widget
    file_upload = widgets.FileUpload(
        accept='.mp3,.mp4,.wav,.m4a,.ogg,.flac,.aac,.webm',
        multiple=False,
        description='Upload File:',
        layout=widgets.Layout(width='80%')
    )
    file_upload.observe(on_file_upload, names='value')
    
    # Display the interface
    display(HTML("<h3>Choose how to input your video:</h3>"))
    display(input_type)
    
    # Create container for URL input
    url_container = widgets.VBox([
        widgets.HTML("<h4>Enter YouTube URL:</h4>"),
        url_input,
        submit_button
    ])
    
    # Create container for file upload
    file_container = widgets.VBox([
        widgets.HTML("<h4>Upload Video/Audio File:</h4>"),
        file_upload
    ])
    
    # Show/hide containers based on input type
    def on_input_type_change(change):
        if change['new'] == 'url':
            display(url_container)
            file_container.layout.display = 'none'
        else:
            url_container.layout.display = 'none'
            display(file_container)
    
    input_type.observe(on_input_type_change, names='value')
    
    # Show initial container based on default selection
    if input_type.value == 'url':
        display(url_container)
    else:
        display(file_container)
    
    # Display status output
    display(status_output)

# Create and display the video input interface
create_video_input_interface()

#@title Step 3: Configure Settings (Click to expand)
def create_settings_interface():
    """Create interactive interface for transcription settings"""
    # Create widgets
    format_radio = widgets.RadioButtons(
        options=[
            ('Text Transcription (.txt)', 'txt'),
            ('Subtitles (.srt)', 'srt')
        ],
        description='Output Format:',
        disabled=False,
        layout=widgets.Layout(width='50%')
    )
    
    model_dropdown = widgets.Dropdown(
        options=[
            ('tiny (fastest, least accurate)', 'tiny'),
            ('base (fast, good accuracy)', 'base'),
            ('small (balanced)', 'small'),
            ('medium (accurate)', 'medium'),
            ('large (most accurate, slowest)', 'large')
        ],
        description='Model Size:',
        disabled=False,
        layout=widgets.Layout(width='50%')
    )
    
    language_dropdown = widgets.Dropdown(
        options=[
            ('Auto-detect', None),
            ('English', 'en'),
            ('Spanish', 'es'),
            ('French', 'fr'),
            ('German', 'de'),
            ('Italian', 'it'),
            ('Portuguese', 'pt'),
            ('Dutch', 'nl'),
            ('Japanese', 'ja'),
            ('Korean', 'ko'),
            ('Chinese', 'zh')
        ],
        description='Language:',
        disabled=False,
        layout=widgets.Layout(width='50%')
    )
    
    prompt_input = widgets.Text(
        value='',
        placeholder='Enter initial prompt (optional)...',
        description='Initial Prompt:',
        disabled=False,
        layout=widgets.Layout(width='80%')
    )
    
    status_output = widgets.Output()
    
    def on_submit(b):
        with status_output:
            clear_output()
            settings = {
                "output_format": format_radio.value,
                "model_size": model_dropdown.value,
                "language": language_dropdown.value,
                "initial_prompt": prompt_input.value.strip() or None
            }
            print("✅ Settings configured:")
            print(f"• Output Format: {format_radio.value}")
            print(f"• Model Size: {model_dropdown.value}")
            print(f"• Language: {language_dropdown.value or 'Auto-detect'}")
            if settings['initial_prompt']:
                print(f"• Initial Prompt: {settings['initial_prompt']}")
            print("\nProceed to Step 4 to generate transcription.")
            return settings
    
    # Create submit button
    submit_button = widgets.Button(
        description='Confirm Settings',
        disabled=False,
        button_style='primary',
        tooltip='Click to confirm settings',
        layout=widgets.Layout(width='200px', height='40px')
    )
    submit_button.on_click(on_submit)
    
    # Display the interface
    display(HTML("<h3>Configure Transcription Settings:</h3>"))
    
    # Create settings form
    settings_form = widgets.VBox([
        format_radio,
        model_dropdown,
        language_dropdown,
        prompt_input,
        submit_button
    ])
    
    display(settings_form)
    display(status_output)

# Create and display the settings interface
create_settings_interface()

#@title Step 4: Generate Transcription (Click to expand)
def format_timestamp(seconds):
    """Convert seconds to SRT timestamp format"""
    td = datetime.timedelta(seconds=seconds)
    hours = td.seconds // 3600
    minutes = (td.seconds % 3600) // 60
    seconds = td.seconds % 60
    milliseconds = int(td.microseconds / 1000)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

def create_srt(segments, output_file):
    """Create SRT subtitle file from segments"""
    with open(output_file, 'w', encoding='utf-8') as f:
        for i, segment in enumerate(segments, 1):
            start = format_timestamp(segment['start'])
            end = format_timestamp(segment['end'])
            text = segment['text'].strip()
            f.write(f"{i}\n{start} --> {end}\n{text}\n\n")

def create_transcription_interface():
    """Create interactive interface for transcription generation"""
    # Create widgets
    status_output = widgets.Output()
    
    def on_generate(b):
        with status_output:
            clear_output()
            try:
                # Get the latest audio file from audio_source directory
                allowed_extensions = ('.mp3', '.mp4', '.wav', '.m4a', '.ogg', '.flac', '.aac', '.webm')
                audio_files = [f for f in os.listdir('audio_source') if f.lower().endswith(allowed_extensions)]
                if not audio_files:
                    print("❌ No audio files found in audio_source directory.")
                    print("Please run Step 2 to download or upload an audio file.")
                    return
                
                # Use the most recent file
                audio_path = os.path.join('audio_source', audio_files[-1])
                title = os.path.splitext(audio_files[-1])[0]
                
                # Check file size
                check_file_size(audio_path)
                print(f"📁 Processing file: {audio_files[-1]}")
                print(f"📁 File size: {get_file_size(audio_path)}")
                
                # Get settings from Step 3
                settings = {
                    "output_format": "srt",  # Default to SRT
                    "model_size": "base",    # Default to base model
                    "language": None,        # Default to auto-detect
                    "initial_prompt": None   # Default to no prompt
                }
                
                print(f"⏳ Loading {settings['model_size']} model...")
                with tqdm(total=100, desc="Loading Model") as pbar:
                    model = whisper.load_model(settings['model_size'])
                    pbar.update(100)
                
                print("⏳ Generating transcription...")
                with tqdm(total=100, desc="Transcription Progress") as pbar:
                    result = model.transcribe(
                        audio_path,
                        language=settings['language'],
                        initial_prompt=settings['initial_prompt'],
                        fp16=torch.cuda.is_available()
                    )
                    pbar.update(100)
                
                # Save output
                if settings['output_format'] == "srt":
                    output_file = f"{title}_subtitles.srt"
                    create_srt(result["segments"], output_file)
                else:
                    output_file = f"{title}_transcription.txt"
                    with open(output_file, "w", encoding="utf-8") as f:
                        f.write(result["text"])
                
                print(f"✅ Transcription saved as: {output_file}")
                print(f"📁 File size: {get_file_size(output_file)}")
                
                # Add download button
                download_button = widgets.Button(
                    description='Download File',
                    disabled=False,
                    button_style='success',
                    tooltip='Click to download the transcription',
                    layout=widgets.Layout(width='200px', height='40px')
                )
                
                def on_download(b):
                    files.download(output_file)
                    print("✅ File downloaded successfully!")
                
                download_button.on_click(on_download)
                display(download_button)
                
            except Exception as e:
                print(f"❌ Error during transcription: {str(e)}")
    
    # Create generate button
    generate_button = widgets.Button(
        description='Generate Transcription',
        disabled=False,
        button_style='primary',
        tooltip='Click to start transcription',
        layout=widgets.Layout(width='200px', height='40px')
    )
    generate_button.on_click(on_generate)
    
    # Display the interface
    display(HTML("<h3>Generate Transcription:</h3>"))
    display(HTML("<p>Click the button below to start transcription of your audio file.</p>"))
    display(generate_button)
    display(status_output)

# Create and display the transcription interface
create_transcription_interface() 