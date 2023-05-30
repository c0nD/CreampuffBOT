## This is for **WINDOWS USERS ONLY**:

- Included are both the 64 bit and 32 bit installer executables
If you wish to download them yourself, the version being used is:
> Tesseract v5.0.0 2021-12-01 14:53

32-bit MD5: 49a55104b9556709dcfb2db1870053b6
64-bit MD5: 4282f5e90cd5e498684a397bccd5bcac

You can find them here https://digi.bib.uni-mannheim.de/tesseract/


## Adding Tesseract to PATH

1. Windows Key
2. Search "Edit the system environment variables"
3. Under the "Advanced" tab, click "Environment Variables" at the bottom 
(alternatively press Alt + N)
4. In the top box, click on the line that says "Path" and press "Edit"
5. On the right-hand side: press "New"
6. On the new line, include the directory to Tesseract (typically 'C:\Program Files\Tesseract-OCR')
7. Press enter on your keyboard, and click Ok.

(Testing)
Open up a command prompt (Win + R -> "cmd"    | Or |     Windows Key -> Search "Command Prompt")
Enter: `tesseract --version`

So long as you do not get an error, everything should have been properly installed.
If you do get an error, check to make sure it is properly installed, but more importantly: added to your Path.

## Setting up trained data language

The `mikado.traineddata` file is a file that has specifically trained on the Cookie Run: Kingdom font. (located in `./fonts`)

> To make it work, place this file in your Tesseract-OCR location (usually): `C:/Program Files/Tesseract-OCR/tessdata`

- Note: if you would like to forgo this process, change `mikado` to `eng` for the `lang` parameter in `image_processing.py`

## Build Information

To build this yourself, you will need the `pyinstaller` library (found in requirements.txt)

From the directory `ToppingOCR/gui_src`, you will input this command

> `pyinstaller --onefile --windowed --paths="<yourdir>\ToppingOCR\src" main.py`
