import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import librosa
import soundfile as sf
import time


print("""
WELCOME USER OF "BITCRUSHER"

Where here only sound is bit crushed at YOUR desire!""")


def apply_bitcrush(audio, bit_depth, hold_factor):

    steps = 2**bit_depth

    # 1. Quantization (Bit depth reduction)
    # Any audio signal consists of volume levels scaled between -1.0 and 1.0
    # The original audio is in float32 format (providing 2^32 ≈ 4.2 billion possible levels, a very precise audio)
    # The entered value of "bit depth" redefines the available levels using 2^(bit_depth)
    # For example, a bit depth of 10 results 2^10 = 1024 possible levels
    # Each of the 44100 samples per second will get its amplitude is rounded to the nearest allowed level, reducing accuracy and smoothness of the original audio
    # that's why the lower the value gets, the more saturated the sound gets.

    quantified_audio = np.round(audio * (steps / 2)) / (steps / 2)

    # 2. Zero-order hold / Sample holding
    # We freeze the sound value over multiple samples to create the "choppy" effect
    # on 5*44100 we take sample #1, copy it {hold_factor-1} times
    # then, we take the {hold_factor}-th sample, and copy it {hold_factor-1} times etc.
    # for example, if we got a DF=3 and :
    # abc def ghi jkl mno pqr stu vwx yz , it would give us:
    # aaa ddd ggg jjj mmm ppp sss vvv yy
    # the rest is discarded
    # that's why the higher, the more robot-like it sound

    audio_crush = np.zeros_like(quantified_audio)

    for i in range(0, len(quantified_audio), hold_factor):
        audio_crush[i : i + hold_factor] = quantified_audio[i]

    return audio_crush


def main():

    # A BUNCH OF CONTINUE VARIABLES BECAUSE I DON'T LIKE USING "break" THAT MUCH
    continue0=1
    continue1=1
    continue2=1
    continue3=1         #4 because we got 4 loops

    while continue0==1:
        
        continue0=1
        continue1=1
        continue2=1
        continue3=1 
        
        while continue1==1:
            print("\nIn this case, choose your variables:\n")

            # --- Recording parameters ---
            duree = float(input("How long should the recording last? (in seconds): "))          # Duration in seconds
            name=input("How your file will be named : ")
            # SAMPLING FREQUENCY: to reproduce 99% of the sound; historically, audio CDs adopted 44.1 kHz.
            FS = 44100
            sample_rate=FS
            Channels = 1
            print(f"\nGood\n\nLet's start your {duree} seconds recording in ", end="")

            for i in range(3, 0, -1):
                print(f"{i}... ", end="", flush=True)
                time.sleep(1)
            print("\nNOW!\n..........\n")

            # 1. RECORDING
            recording = sd.rec(int(duree * FS), samplerate=FS, channels=Channels, dtype="float32")
            sd.wait()

            # 2. Saving the original file
            original_file = name+".wav"
            write(original_file, FS, recording)

            print(f"Original file saved! : {original_file}")
        
            print("Before applying the changes, are you satisfied with your audio? : y/n    ", end="")
            res=input().lower()
                
            while res not in ("y", "n"):
                print("NOT A VALID ANSWER...\nTry again : ", end="")
                res=input().lower()

            if res=='y':
                continue1=0
        
        print("\nGood!\nBut before the showdown, would you like to change the pitch and the speed of your recording? : y/n    ", end="")
        res = input().lower()

        while res not in ("y", "n"):
            print("NOT A VALID ANSWER...\nTry again : ", end="")
            res=input().lower()
        
        # 3. Voice synthesis
        if res == "y":
            while continue2==1:
                print("\nThen, shall we proceed.\n")

                pitch = float(
                    input(
                        "Write down the value of your pitch (minus before the value means lower pitch!): "
                        )
                )
                speed = float(
                    input("Good, now how about the speed? (example: 1.2 means 20% faster): ")
                )

                # 3.1. Load the existing audio file
                recording, sample_rate = librosa.load(original_file, sr=None, mono=True)

                # 3.2. Pitch Shift
                # n_steps = number of semitones (+4 = higher pitch/robot voice, -4 = lower pitch)
                recording = librosa.effects.pitch_shift(
                    recording, sr=sample_rate, n_steps=pitch
                    )

                # 3.3. Change speed (Time Stretch)
                # rate = 1.2 (20% faster), rate = 0.8 (20% slower)
                recording = librosa.effects.time_stretch(recording, rate=speed)

                # 3.4. Save the new file
                sf.write("new_"+name+".wav", recording, sample_rate)

                print("\nNEW AUDIO FILE SAVED WITH SUCCESS!\n")

                print("Are you satisfied with your modified audio? : y/n    ", end="")
                res=input().lower()
                
                while res not in ("y", "n"):
                    print("NOT A VALID ANSWER...\nTry again : ", end="")
                    res=input().lower()

                if res=='y':
                    continue2=0

        if res=='n':
            print("\nAs you wish.\n")

        print("A \"BIT\" More before the outcome!\n")

        while continue3==1:
            bit_depth = int(
                input("Bit-depth: the lower the value is, the more saturated the sound gets: ")
            )

            hold_factor = int(
                input(
                    "The hold factor: the higher it is, the more robot-like the record gets: "
                )
            )

            # 4. Applying the Bit-Crush effect
            bit_audio = apply_bitcrush(
                recording, bit_depth=bit_depth, hold_factor=hold_factor
            )

            # 4. Saving the modified file
            new_file = "bitcrushed.wav"
            sf.write(new_file, bit_audio, sample_rate)

            print(f"\nHave fun listening to your new voice: {new_file}\nAre you satified by it?: y/n    ", end="")
            res=input().lower()
                
            while res not in ("y", "n"):
                print("NOT A VALID ANSWER...\nTry again : ", end="")
                res=input().lower()

            if res=='y':
                continue3=0

        print("\n\nWould you like to bitcrush another audio? : y/n   ", end="")
        replay = input().lower()

        while res not in ("y", "n"):
                print("NOT A VALID ANSWER...\nTry again : ", end="")
                res=input().lower()
        
        if replay == 'y':
            print("\nThen shall we continue!\n")
            print("=" * 40)
        else:
            print("See you next time")
            continue0=0


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error has occured : {e}")
        input("press any key to close app.")
    
