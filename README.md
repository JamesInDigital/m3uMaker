Shield: [![CC BY 4.0][cc-by-shield]][cc-by]

This work is licensed under a
[Creative Commons Attribution 4.0 International License][cc-by].

[![CC BY 4.0][cc-by-image]][cc-by]

[cc-by]: http://creativecommons.org/licenses/by/4.0/
[cc-by-image]: https://i.creativecommons.org/l/by/4.0/88x31.png
[cc-by-shield]: https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg

# m3uMaker
M3U creation script originally designed to help organize roms for retro handhelds. Handles multi-disc games and subfolders.

Update to v2d: Fixed second run. Will ignore games already processed in .hidden folder.

Update to v2c: Fixed disc order in m3u and working with subdirectories.

Update 7-18-24 to v2: Currently setting up a friend RG35XX+ under muOS and have modified the code to make use of .hidden subfolder for a cleaner interface when it comes to multi-disc games. As always, not a real programmer, use at your own discetion with backs. V2 moves multidisc games to .hidden subfolder and modifies the m3u accordingly. Testing work for PS1 games on RG35XX+

The Short:
Scans folder for rom files, taking note of those with Disc 1/2 etc and creates m3u files pointing to the images. In theory, this will allow devices like the RG35XX to run games from subfolders (haven't currently tested as the RG35XX I set up with a friend currently) but also helps declutter rom folder by not have entries for each disc of multi-disc games. For Miyoo/RG35XX look up how to change what extensions the emulators will run and narrow it to m3u.

Usage:
I setup a Miyoo Mini+ and an original RG35XX at the same time with their respective OSes, Onion and Garlic.
For organization purposes some folders were split into lettered subfolders due to amount of games. 
Garlic is unable to read these subfolders and both systems will have duplicate entries for games and m3us unless configs are edited.
Used rusty, old Python memory and some ChatGPT for base code to write a utility to automate M3U creation to help clean up menus and hopefully keep subdirs in tact for cloning SD cards between the two systems.

Notes:
See issues for possible special cases not working.
Not all EMUs will support M3U, so RG35XX won't be able to make use of subfolders (assuming it works currently as is).
This isn't designed to touch the rom files in any ways (as opposed to the Doom setup script I created for the Miyoo) so there shouldn't be any worries there. But take precautions. As always, not a REAL programmer.
