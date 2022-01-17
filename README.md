# PDF to JPEG Discord Bot

This bot will send pictures into your current discord channel based on a pdf link.

# How to use
First download this repo. This script uses the various packages. You can install them with
```
pip install discord
pip install python-dotenv
pip istall PyMUPDF
```
Then, add in your discord token at the bottom of the file.

## Commands
Some valid commands include:
```
!pdf website.com/file.pdf" (sends all pages)
"!pdf website.com/file.pdf 1 3" (sends pages 1 to 3)
"!pdf website.com/file.pdf 5" (sends pages 5 to the end)
```
