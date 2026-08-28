#The Bitcrusher
A Python command-line application that allows the user to record an audio for a custom duration, then apply (if wished) a change of the speed and pitch of the audio and finally to choose how to apply the bitcrush effects on it.

--- 

##How it works?
1 **The user is asked to choose the variables for the process. First the duration and the name of the file.
2 **After the recording, the user is asked whether or not, he/she wants to apply some changes in the pitch and/or the speed on the audio.
3 **Finally, a value for "bit-depth" and the "hold_factor" is asked to aplly the bitrcush effects which consists of two main steps:
  * **Bit-depth: Quantization (Bit depth reduction)
  - **Any audio signal consists of volume levels scaled between -1.0 and 1.0
  - **The original audio is usually in float32 format (providing 2^32 ≈ 4.2 billion possible levels, a very precise audio)
  - **The entered value of "bit depth" redefines the available levels using 2^(bit_depth)
  - **For example, a bit depth of 10 results 2^10 = 1024 possible levels
  - **Each of the 44100 samples per second will get its amplitude is rounded to the nearest allowed level, reducing accuracy and smoothness of the original audio
  - **That's why the lower the value gets, the more saturated the sound gets.
  
  * **Zero-order hold / Sample holding:
  - **We freeze the sound value over multiple samples to create the "choppy" effect
  - **On 5*44100 we take sample #1, copy it {hold_factor-1} times
  - **then, we take the {hold_factor}-th sample, and copy it {hold_factor-1} times etc.
  - **for example, if we got a DF=3 and :
  - ** "abc def ghi jkl mno pqr stu vwx yz" , it would give us:
  - ** "aaa ddd ggg jjj mmm ppp sss vvv yy"
  - ** the rest is discarded
  - ** that's why the higher, the more robot-like it sound

4 **FOR THE FILE SAVING: **WAV Export:** Automatically saves original, pitched/stretched, and bitcrushed WAV files.

---

#REQUIREMENTS FOR CODE MODIFICATION:
**Python 3.10+
**Libraries:
- **sounddevice
- **numpy
- **scipy
- **librosa
- **soundfile
```bash
pip install sounddevice numpy scipy librosa soundfile
```

**To bundle this project into a standalone .exe file for Windows, use PyInstaller.

Because scipy, librosa, and scikit-learn rely on dynamic C-extensions and hidden submodules, run the following command to ensure all dependencies are properly bundled into a single file:
```bash
pyinstaller --onefile --collect-all scipy --collect-all librosa --collect-all sklearn Bitcrushing.py
```bash
pyinstaller --onefile --collect-all scipy --collect-all librosa --collect-all sklearn Bitcrushing.py
