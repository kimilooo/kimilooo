# Kimiloo's Sakura Cinema

An English GitHub profile with midnight-plum backgrounds, pearl serif lettering,
cherry-pink film details and original editorial artwork. The look is romantic,
playful, feminine and cinematic.

## Assets

- `assets/sakura-poster.jpg`: original artwork from the built-in image-generation tool, encoded as JPEG for the profile. The illustrated adult character is fictional, not a photograph of Kimiloo.
- `assets/cinema-intro.gif`: six-second film countdown, drifting petals and welcome title.
- `assets/casting.gif`: twelve-second typewriter sequence for three creative roles.
- `assets/end-credits.gif`: six-second petal and sparkle loop with closing credits.
- `assets/*-still.png`: readable static alternatives selected for reduced-motion preferences.
- `assets/*.svg`: original project cards and navigation graphics with no scripts, external fonts or remote resources.

Motion graphics were drawn from shapes and type; they do not alter the generated
poster. No rapid flashes, visitor trackers or externally hosted stats/typing-image
dependencies are included in this profile design.

## Regenerate the motion graphics

Use Python with Pillow and NumPy and the DejaVu font family:

```sh
python -m pip install pillow numpy
python tools/generate-effects.py
```

If fonts are installed elsewhere, set `PROFILE_FONT_DIR` to a directory containing
`DejaVuSerif.ttf`, `DejaVuSans.ttf` and `DejaVuSansMono.ttf`. All generated files
remain under `assets/`. Changing README text does not require running the generator.

## Original artwork prompt

[tools/artwork-prompt.txt](tools/artwork-prompt.txt) contains the complete prompt.
The image was made with the built-in image-generation tool, not the fallback CLI.

## Public identity

This profile uses the public brand Kimiloo, linked GitHub repositories and the X
handle @Kimilooweb3. It includes no legal name, personal financial records, access
tokens or private contact details.
