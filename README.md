# AS32JS
Automatic conversion of Action Script 3 classes to Javascript

The tool is developed to automatically convert Action Script 3 sources into JavaScript

The tool is designed to convert Starling AIR game into Phaser HTML5 gamce, but it can be used for various cases

1. Place your AS3 source files into source_as3 folder
2. Run class_processor.py. If you have several orders of ancestry in your project, you might need to run it several times (it's quick). The folder temp/jsons will be filled with json files which resemble the structure of your classes
3. Run better_converter.py. Your as3 files will be converted into js files and placed in the folder results_js 

After this you'll be able to include the converted js files into your project and run it as a web game/app after occasional minor fixes.

I used it to provide the HTML5 version of my AIR game Farm and Mine
AIR/Starling game for Android, iOS, Windows, Linux: https://airapport.itch.io/farm-and-mine
Converted HTML5/Phaser game: https://poki.com/en/g/farm-and-mine

If you find the tool useful for your project, please support Ukraine, as our country is surviving agains devastating terrorussian strikes for over 2 years now.

Here are some of the initiatives which support Ukraine directly:
Gamedev under Bombs: https://www.ggconference.com/en/gamedev-under-bombs/
O-Pocket: https://o-pocket.org/
UNITED24: https://u24.gov.ua/
Come Back Alive: https://savelife.in.ua/en/
You help is appreciated and it can really save lives.