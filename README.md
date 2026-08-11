## about

This is a program that I made to help memorize passwords. I used to use my notes app and found it quite annoying when passwords exceeded 10 digits, so I made this. The idea is to take as much burden away from you and allow you to focus of memorization. I would spend more time making sure there were no typos or errors while practicing, and I hope to never deal with that again.

## feature list

- presets:

You can make and delete presets, so you don't have to remember the password you are trying to memorize

- memorizing function:

When you enter the correct password (skipped if you use a preset), that will be the password you are trying to memorize. Then you just type it out, and the program will tell you if you get it right or wrong. If you get it wrong 5 times in a row, it will temporarily pause input and display the correct password so you can see where you got it wrong.

- password storage:

The obvious security concern is giving a random program all of your passwords. The way I tried to address this was with storing your passowrds in your computers keychain, keeping it encrypted and only ever in plain text when the program is running.

## to do

- [ ] animations on fail/success

- [ ] password lock program

- [ ] settings:
  - [ ] gui
  - [ ] wrong counter
  - [ ] animations




## compatability

This program is compatible with Linux, Windows(11), and MacOS
The MacOS version was tested on a MacBook Neo (ARM CPU)
The Linux version was tested on a Fedora and Arch machine

## program files

Currently, all I have are executables. EXE for Windows, and generic exacutable files for mac and linux. I do plan on making a .deb and maybe a macOS dmg.

## install
windows: double click on the exe
MacOS: double-click on the executable
Linux: make sure it has executable permissions, and double-click on the executable

## arch / no executable
if you do not use the exacutable, you will need a few depedencies:
pip - to install packages
DearPyGui
cryptography
fernet
keyring
(maybe more, I dont have a complete list)

## donations
i worked really hard on this

please?  🥺👉👈
        
[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/H0L824UPYI)
