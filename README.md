#It ain't perfect nor pretty, but it runs...

This little bot, written in Python, runs on a Raspberry Pi 4. It communicates using the Telegram app to multiple users using another library called telepot. You'll need to install telepot to make it work. One note- I haven't figure out how to get telepot and Thonny to work together, so be aware. (I've just used vi and no debugger.)

Currently, it provides the following functions:

1- Maintains a grocery list
2- Maintains a todo list
3- Maintains locations of grocery items in a store. (Such as cinnamon is on the baking aisle.)
4- Miscellaneous commands:
a- Displays command help
b- RPi CPU temperature
c- current users

Future releases will upgrade the todo list and grocery list functionality. I have a basic way to push notices to users via Telegram, so I'm sure I'll be doing something fun with that.
