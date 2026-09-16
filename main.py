import sounddevice as sd
import scipy.io.wavfile as wav
import speech_recognition as sr
from googletrans import Translator
import random
import asyncio

duration = 5
sample_rate = 44100

words_by_level = {
    "fácil": ["gato", "cachorro", "maçã", "leite", "sol"],
    "médio": ["casa", "escola", "amigo", "janela", "amarelo"],
    "difícil": ["tecnologia", "universidade", "informação", "pronúncia", "imaginação"]
}

lang = input("Para qual idioma devo traduzir? (ex: en, es): ")
dif = input("Escolha uma dificuldade (fácil, médio ou difícil): ").lower()

translator = Translator()


def choiced():
    return random.choice(words_by_level[dif]).lower()


while True:

    word = choiced()
    print(f"\nA palavra sorteada foi: {word}")  # retire esta linha se não quiser mostrar

    print("Fale a palavra sorteada agora...")

    recording = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,
        channels=1,
        dtype="int16"
    )
    sd.wait()

    wav.write("output.wav", sample_rate, recording)
    print("Gravação concluída, reconhecendo...")

    recognizer = sr.Recognizer()

    with sr.AudioFile("output.wav") as source:
        audio = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio, language=lang).lower()
        print("Você disse:", text)

        translated = asyncio.run(translator.translate(text, dest="pt"))
        print("Tradução:", translated.text)

        if translated.text.lower() == word:

            print("Você acertou! 😁")

            if dif == "fácil":
                continuar = input("Deseja ir para o nível médio? ").lower()
                if continuar == "sim":
                    dif = "médio"
                    continue
                else:
                    print("Finalizando jogo...")
                    break

            elif dif == "médio":
                continuar = input("Deseja ir para o nível difícil? ").lower()
                if continuar == "sim":
                    dif = "difícil"
                    continue
                else:
                    print("Finalizando jogo...")
                    break

            elif dif == "difícil":
                print(r"""
██╗   ██╗ ██████╗  ██████╗███████╗     ██████╗  █████╗ ███╗   ██╗██╗  ██╗ ██████╗ ██╗   ██╗
██║   ██║██╔═══██╗██╔════╝██╔════╝    ██╔════╝ ██╔══██╗████╗  ██║██║  ██║██╔═══██╗██║   ██║
██║   ██║██║   ██║██║     █████╗      ██║  ███╗███████║██╔██╗ ██║███████║██║   ██║██║   ██║
╚██╗ ██╔╝██║   ██║██║     ██╔══╝      ██║   ██║██╔══██║██║╚██╗██║██╔══██║██║   ██║██║   ██║
 ╚████╔╝ ╚██████╔╝╚██████╗███████╗    ╚██████╔╝██║  ██║██║ ╚████║██║  ██║╚██████╔╝╚██████╔╝
  ╚═══╝   ╚═════╝  ╚═════╝╚══════╝     ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝ ╚═════╝  ╚═════╝
""")
                break

        else:
            print("Você errou.")

            print(r"""
 ██████╗  █████╗ ███╗   ███╗███████╗     ██████╗ ██╗   ██╗███████╗██████╗
██╔════╝ ██╔══██╗████╗ ████║██╔════╝    ██╔═══██╗██║   ██║██╔════╝██╔══██╗
██║  ███╗███████║██╔████╔██║█████╗      ██║   ██║██║   ██║█████╗  ██████╔╝
██║   ██║██╔══██║██║╚██╔╝██║██╔══╝      ██║   ██║╚██╗ ██╔╝██╔══╝  ██╔══██╗
╚██████╔╝██║  ██║██║ ╚═╝ ██║███████╗    ╚██████╔╝ ╚████╔╝ ███████╗██║  ██║
 ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝     ╚═════╝   ╚═══╝  ╚══════╝╚═╝  ╚═╝
""")
            break

    except sr.UnknownValueError:
        print("A fala não pôde ser reconhecida.")

    except sr.RequestError as e:
        print(f"Erro do serviço: {e}")
        break
