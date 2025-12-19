from celery import shared_task
import speech_recognition as sr
from googletrans import Translator
from pydub import AudioSegment
import os

@shared_task
def translate_video_audio(video_id, target_languages):
    """
    Extract audio from video, transcribe, and translate to multiple languages
    This is a background task that will run asynchronously
    """
    from videos.models import Video, VideoSubtitle
    
    video = Video.objects.get(id=video_id)
    video_path = video.video_file.path
    
    # Extract audio from video
    audio = AudioSegment.from_file(video_path)
    audio_path = video_path.replace('.mp4', '.wav')
    audio.export(audio_path, format='wav')
    
    # Transcribe audio to text (English first)
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio_data = recognizer.record(source)
        try:
            english_text = recognizer.recognize_google(audio_data, language='en-US')
            
            # Create English subtitle
            create_srt_file(video, 'en', 'English', english_text)
            
            # Translate to other languages
            translator = Translator()
            language_map = {
                'sw': 'Swahili',
                'fr': 'French',
                'ar': 'Arabic',
                'pt': 'Portuguese',
                'es': 'Spanish'
            }
            
            for lang_code in target_languages:
                if lang_code in language_map:
                    translated = translator.translate(english_text, dest=lang_code)
                    create_srt_file(video, lang_code, language_map[lang_code], translated.text)
        
        except Exception as e:
            print(f"Translation error: {str(e)}")
    
    # Clean up audio file
    os.remove(audio_path)
    
    return True

def create_srt_file(video, lang_code, lang_name, text):
    """Create SRT subtitle file from text"""
    from videos.models import VideoSubtitle
    from django.core.files.base import ContentFile
    
    # Simple SRT format (this can be improved with proper timing)
    srt_content = f"""1
00:00:00,000 --> 00:00:{video.duration},000
{text}
"""
    
    subtitle = VideoSubtitle.objects.create(
        video=video,
        language_code=lang_code,
        language_name=lang_name
    )
    
    subtitle.subtitle_file.save(
        f'{video.title}_{lang_code}.srt',
        ContentFile(srt_content.encode('utf-8'))
    )
    
    return subtitle
