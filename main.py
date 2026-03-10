import os
import json
import wave
import threading
import urllib.request

import customtkinter as ctk
import sounddevice as sd

from vosk import Model, KaldiRecognizer
from gtts import gTTS
import pyttsx3
from playsound import playsound
import argostranslate.translate as argos

from tkinter import messagebox


# ================= SETTINGS =================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

SAMPLE_RATE = 16000
RECORD_TIME = 5


COLORS = {
"bg": "#FFFBDE",
"panel": "#90D1CA",
"accent": "#129990",
"success": "#096B68",
"error": "#EF4444",
"text": "#000000",
"online": "#10B981",
"offline": "#6B7280"
}


# ================= LANGUAGE MAPS =================

speech_langs = {
"en": "English",
"hi": "Hindi",
"fr": "French",
"de": "German",
"ru": "Russian"
}

tts_langs = {
"en": "English",
"hi": "Hindi",
"mr": "Marathi",
"ta": "Tamil",
"te": "Telugu",
"es": "Spanish",
"fr": "French",
"de": "German",
"ru": "Russian"
}


# Load Argos languages
argos.load_installed_languages()
installed_languages = argos.get_installed_languages()
argos_map = {l.code: l.name for l in installed_languages}


# ================= MAIN APPLICATION =================

class SpeechTranslatorApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.geometry("480x320")
        self.resizable(False, False)
        self.title("Hybrid Speech Translator")

        self.configure(fg_color=COLORS["bg"])

        self.source_lang = ctk.StringVar(value="English")
        self.target_lang = ctk.StringVar(value="Hindi")
        self.status_text = ctk.StringVar(value="Idle")
        self.use_online_tts = ctk.BooleanVar(value=True)

        self.speech_options = list(speech_langs.values())
        self.tts_options = list(tts_langs.values())

        self.build_interface()


# ================= USER INTERFACE =================

    def build_interface(self):

        toggle_frame = ctk.CTkFrame(self, fg_color="transparent")
        toggle_frame.pack(pady=4)

        ctk.CTkLabel(toggle_frame, text="Mode:",
                     text_color=COLORS["text"]).pack(side="left")

        self.mode_toggle = ctk.CTkSwitch(
            toggle_frame,
            text="Online TTS",
            variable=self.use_online_tts,
            progress_color=COLORS["online"],
            button_color=COLORS["offline"]
        )
        self.mode_toggle.pack(side="left", padx=5)


        lang_frame = ctk.CTkFrame(self, fg_color="transparent")
        lang_frame.pack(pady=5)

        ctk.CTkLabel(lang_frame, text="From:",
                     text_color=COLORS["text"]).grid(row=0, column=0)

        self.from_menu = ctk.CTkOptionMenu(
            lang_frame,
            variable=self.source_lang,
            values=self.speech_options,
            width=100
        )
        self.from_menu.grid(row=0, column=1, padx=4)


        swap_btn = ctk.CTkButton(
            lang_frame,
            text="⇄",
            width=30,
            fg_color=COLORS["panel"],
            command=self.swap_languages
        )
        swap_btn.grid(row=0, column=2, padx=5)


        ctk.CTkLabel(lang_frame, text="To:",
                     text_color=COLORS["text"]).grid(row=0, column=3)

        self.to_menu = ctk.CTkOptionMenu(
            lang_frame,
            variable=self.target_lang,
            values=self.tts_options,
            width=100
        )
        self.to_menu.grid(row=0, column=4, padx=4)


        # Input box
        self.input_box = ctk.CTkTextbox(self, height=45)
        self.input_box.insert("1.0", "🎤 Press Translate to start recording")
        self.input_box.pack(padx=10, pady=3, fill="x")


        # Output box
        self.output_box = ctk.CTkTextbox(self, height=45)
        self.output_box.insert("1.0", "🌐 Translation will appear here")
        self.output_box.pack(padx=10, pady=3, fill="x")


        # Buttons
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(pady=5)

        self.translate_btn = ctk.CTkButton(
            button_frame,
            text="🎤 Translate",
            width=140,
            fg_color=COLORS["success"],
            command=self.process_audio
        )
        self.translate_btn.pack(side="left", padx=6)


        reset_btn = ctk.CTkButton(
            button_frame,
            text="Reset",
            fg_color=COLORS["error"],
            command=self.reset_interface
        )
        reset_btn.pack(side="left", padx=6)


        status_frame = ctk.CTkFrame(self, fg_color=COLORS["panel"])
        status_frame.pack(fill="x", padx=10)

        ctk.CTkLabel(status_frame,
                     textvariable=self.status_text).pack()


# ================= UTILITIES =================

    def get_key(self, dictionary, value):
        for k, v in dictionary.items():
            if v == value:
                return k
        return None


    def internet_available(self):
        try:
            urllib.request.urlopen("https://google.com", timeout=2)
            return True
        except:
            return False


# ================= AUDIO RECORDING =================

    def record_audio(self):

        recording = sd.rec(
            int(RECORD_TIME * SAMPLE_RATE),
            samplerate=SAMPLE_RATE,
            channels=1,
            dtype="int16"
        )

        sd.wait()

        with wave.open("input.wav", "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(SAMPLE_RATE)
            wf.writeframes(recording.tobytes())


# ================= SPEECH RECOGNITION =================

    def speech_to_text(self):

        lang_code = self.get_key(speech_langs, self.source_lang.get())
        model_path = os.path.join("vosk", lang_code)

        model = Model(model_path)
        recognizer = KaldiRecognizer(model, SAMPLE_RATE)

        with wave.open("input.wav", "rb") as wf:
            audio_data = wf.readframes(wf.getnframes())

        if recognizer.AcceptWaveform(audio_data):
            result = json.loads(recognizer.Result())
            return result.get("text", "")

        return ""


# ================= TRANSLATION =================

    def translate_text(self, text):

        source_code = self.get_key(argos_map, self.source_lang.get())
        target_code = self.get_key(tts_langs, self.target_lang.get())

        src = next((l for l in installed_languages if l.code == source_code), None)
        tgt = next((l for l in installed_languages if l.code == target_code), None)

        return src.get_translation(tgt).translate(text)


# ================= TEXT TO SPEECH =================

    def speak_output(self, text):

        lang_code = self.get_key(tts_langs, self.target_lang.get())

        if self.use_online_tts.get() and self.internet_available():

            tts = gTTS(text=text, lang=lang_code)
            tts.save("output.mp3")
            playsound("output.mp3")

        else:

            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()


# ================= MAIN WORKFLOW =================

    def process_audio(self):

        def task():

            try:

                self.status_text.set("Recording...")
                self.record_audio()

                self.status_text.set("Recognizing speech...")
                spoken_text = self.speech_to_text()

                self.input_box.delete("1.0", "end")
                self.input_box.insert("1.0", spoken_text)

                if not spoken_text:
                    self.status_text.set("No speech detected")
                    return

                self.status_text.set("Translating...")
                translated = self.translate_text(spoken_text)

                self.output_box.delete("1.0", "end")
                self.output_box.insert("1.0", translated)

                self.status_text.set("Speaking output...")
                self.speak_output(translated)

                self.status_text.set("Done")

            except Exception as e:
                messagebox.showerror("Error", str(e))
                self.status_text.set("Error occurred")

        threading.Thread(target=task, daemon=True).start()


# ================= BUTTON FUNCTIONS =================

    def swap_languages(self):

        src = self.source_lang.get()
        tgt = self.target_lang.get()

        if src in self.tts_options and tgt in self.speech_options:
            self.source_lang.set(tgt)
            self.target_lang.set(src)
            self.status_text.set("Languages swapped")


    def reset_interface(self):

        self.input_box.delete("1.0", "end")
        self.output_box.delete("1.0", "end")

        self.input_box.insert("1.0", "🎤 Press Translate to start recording")
        self.output_box.insert("1.0", "🌐 Translation will appear here")

        self.status_text.set("Reset complete")


# ================= RUN APPLICATION =================

if __name__ == "__main__":
    app = SpeechTranslatorApp()
    app.mainloop()