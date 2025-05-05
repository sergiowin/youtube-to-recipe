import openai
import traceback
from typing import Dict, Optional
import os
import json

class RecipeExtractor:
    def __init__(self):
        openai.api_key = os.getenv('OPENAI_API_KEY')

    def transcribe_audio(self, audio_path: str) -> str:
        """Transcribes audio file to text using OpenAI's Audio API"""
        try:
            with open(audio_path, "rb") as audio_file:
                transcript = openai.Audio.transcribe(
                    model="whisper-1",
                    file=audio_file,
                    response_format="text"
                )
            return transcript
        except Exception as e:
            print(f"Error transcribing audio: {str(e)}")
            return ""

    def extract_recipe(self, transcription: str) -> Optional[Dict]:
        """Extracts recipe information from transcribed text using OpenAI"""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that extracts recipe information from text. Extract the title(based upon the transcript), ingredients (as a list), instructions (as steps), cooking time, and servings if available. Respond ONLY with a valid JSON object. If content is unrelated to food, respond with a message stating that content is unrelated to food."},
                    {"role": "user", "content": transcription}
                ]
            )
            
            # Parse the response
            recipe_data = response.choices[0].message.content
            recipe_dict = json.loads(recipe_data)
            return recipe_dict

        except Exception as e:
            print("Error extracting recipe:", e)
            traceback.print_exc()
            return None

    def process_video(self, audio_path: str) -> Optional[Dict]:
        """Process video audio to extract recipe information"""
        # First transcribe the audio
        transcription = self.transcribe_audio(audio_path)
        if not transcription:
            return None

        # Then extract recipe information
        recipe_info = self.extract_recipe(transcription)
        return recipe_info 