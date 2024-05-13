import json
import torch
from openai import OpenAI
from typing import Optional


class ICT4DTTS:
    def __init__(self, openai_api: str) -> None:
        self.base_voice_path = "voices/fr_voice.wav"
        self.openai_client = OpenAI(api_key=openai_api)

    def _translate_en_to_fr(self, text: str) -> str:
        response = self.openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {'role': "system", "content": "you are a translator, translating English to French in JSON format:"
                                              " {'french': 'bonjour'}"},
                {'role': "user", "content": text},
            ],
            response_format={"type": "json_object"}
        )
        try:
            french_text = json.loads(
                response.choices[0].message.content)["french"]
        except json.JSONDecodeError as e:
            raise ValueError(f"JSON decoding error: {e}")
        except KeyError as e:
            raise KeyError(f"Key error in parsing response: {e}")
        except Exception as e:
            raise Exception(f"Unexpected error: {e}")

        return french_text

    def _translate_en_to_bo(self, text: str) -> str:
        response = self.openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {'role': "system", "content": "you are a translator, translating English to Bobo (Spoken language in Mali) in JSON format:"
                                              " {'bobo': 'hi'}"},
                {'role': "user", "content": text},
            ],
            response_format={"type": "json_object"}
        )
        try:
            spanish_text = json.loads(
                response.choices[0].message.content)["bobo"]
        except json.JSONDecodeError as e:
            raise ValueError(f"JSON decoding error: {e}")
        except KeyError as e:
            raise KeyError(f"Key error in parsing response: {e}")
        except Exception as e:
            raise Exception(f"Unexpected error: {e}")

        return spanish_text

    def _translate_en_to_fl(self, text: str) -> str:
        response = self.openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {'role': "system", "content": "you are a translator, translating English to Fula (Spoken language in Mali) in JSON format:"
                                              " {'fula': 'hi'}"},
                {'role': "user", "content": text},
            ],
            response_format={"type": "json_object"}
        )
        try:
            spanish_text = json.loads(
                response.choices[0].message.content)["fula"]
        except json.JSONDecodeError as e:
            raise ValueError(f"JSON decoding error: {e}")
        except KeyError as e:
            raise KeyError(f"Key error in parsing response: {e}")
        except Exception as e:
            raise Exception(f"Unexpected error: {e}")

        return spanish_text

    def _translate_en_to_ba(self, text: str) -> str:
        response = self.openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {'role': "system", "content": "you are a translator, translating English to Bambara (Mali language) in JSON format:"
                                              " {'bambara': 'hi'}"},
                {'role': "user", "content": text},
            ],
            response_format={"type": "json_object"}
        )
        try:
            italian_text = json.loads(
                response.choices[0].message.content)["bambara"]
        except json.JSONDecodeError as e:
            raise ValueError(f"JSON decoding error: {e}")
        except KeyError as e:
            raise KeyError(f"Key error in parsing response: {e}")
        except Exception as e:
            raise Exception(f"Unexpected error: {e}")

        return italian_text

    def _generate_voice(self,
                        text: str,
                        is_generate_wav_file: bool = False,
                        file_path: Optional[str] = None,
                        ) -> Optional[list[float]]:

        if is_generate_wav_file:
            if file_path is None:
                raise ValueError("file_path cannot be None")
            else:
                response = self.openai_client.audio.speech.create(
                    model="tts-1",
                    voice="alloy",
                    input=text
                )

                response.stream_to_file(file_path)
                return

    def english_text_to_speech(self,
                               text: str,
                               language: str,
                               is_generate_wav_file: bool = False,
                               file_path: Optional[str] = None,
                               ) -> Optional[list[float]]:

        if (language == "french"):
            text = self._translate_en_to_fr(text)

        if (language == "bambara"):
            text = self._translate_en_to_ba(text)

        if (language == "bobo"):
            text = self._translate_en_to_bo(text)

        if (language == "fula"):
            text = self._translate_en_to_bo(text)

        return self._generate_voice(text, is_generate_wav_file, file_path)
