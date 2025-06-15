#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: tts_module.py
Author: Joseph Katakam
Date: 2020-05-01
Description: A Python module to convert English text to speech using IBM Watson Text-to-Speech service.
             Optionally, it can translate the text to French using the Watson Language Translator before synthesizing speech.
"""

# importing libraries
from ibm_watson import language_translator_v3, text_to_speech_v1
from ibm_cloud_sdk_core.authenticators import iam_authenticator
from ibm_watson import LanguageTranslatorV3, TextToSpeechV1
from playsound import playsound

class TTS:
    """
    Initializes credentials and default settings.

    Note:
        Entire functionality is wrapped using Threading to not freeze the User Interface
    """
    def __init__(self):
        # TTS credentials
        self.tts_api_key = ''
        self.tts_url_service = 'https://api.us-east.text-to-speech.watson.cloud.ibm.com/instances/9a47d4f8-5d24-4297-b696-457e30474968'
        # Language Translator credentials
        self.lt_api_key = ''
        self.lt_url_service = 'https://api.us-south.language-translator.watson.cloud.ibm.com'
        self.lt_version = '2018-05-01'

        self.translation_status = False

    def text_to_speech(self, prompt, translate=False):
        """
        Converts the given text to speech, optionally translating it to French first.

        Attributes:
            prompt (str): The text to be converted.
            translate (bool): Whether to translate to French before speaking.
        """
        # Setup
        tts_authenticator = iam_authenticator.IAMAuthenticator(self.tts_api_key)
        # Initialize
        self.tts = text_to_speech_v1.TextToSpeechV1(authenticator=tts_authenticator)
        # Setup service
        self.tts.set_service_url(self.tts_url_service)

        if translate:
            self.translate_prompt(prompt)
        else:
            self.generate_mp3(prompt)

    def translate_prompt(self, prompt):
        """
        Translates the given text from English to French.

        Attributes:
            prompt (str): The English sentence.
        """
        # Setup
        lt_authenticator = iam_authenticator.IAMAuthenticator(self.lt_api_key)
        # Initialize
        lt = LanguageTranslatorV3(version=self.lt_version, authenticator=lt_authenticator)
        # Setup service
        lt.set_service_url(self.lt_url_service)

        # Set translation, English -> French
        french_translation = lt.translate(text=prompt, model_id='en-fr').get_result()
        # Extract prompt translation
        translated_prompt = french_translation['translations'][0]['translation']
        # print(translated_prompt)

        self.generate_mp3(translated_prompt, voice='fr-FR_ReneeV3Voice')

    def generate_mp3(self, prompt, voice='en-US_EmmaExpressive'):
        """
        Synthesizes speech and saves it as speech.mp3, then plays it.

        Attributes:
            prompt (str): The text to synthesize.
            voice (str): Voice model. Default is English.
                         Can be changed to French voice like 'fr-FR_ReneeV3Voice'.
        """
        # Generate .mp3 file
        with open('./speech.mp3', 'wb') as audio_file:
            res = self.tts.synthesize(text=prompt, accept='audio/mp3', voice=voice).get_result()
            audio_file.write(res.content)

        # Play translation
        playsound('speech.mp3')

def main():
    prompt = "Thank you for checking out my Portfolio!!"
    french_prompt = "Merci d'avoir consulté mon portfolio !!"

    # initialize class
    tts = TTS()

    # test cases
    tts.text_to_speech(prompt)  # convert english prompt to speech
    # tts.text_to_speech(prompt, translate=True)  # translate english to french prompt and convert to speech

if __name__ == "__main__":
    main()
