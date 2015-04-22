#!/usr/bin/python
# fbpic2id.py
# Author: stderr (www.chokepoint.net)
# Given a direct link to a Facebook image, return the owner's name & URL (if available)
# 	Also return anyone tagged in the photo along with their profile (if available)
#	If the owner returns as Facebook, privacy settings don't allow a non logged in user to view the content
#	For better results implement logging in to a FB profile

import sys
from ContentParser import ContentParser


def main(argv):
    if len(argv) != 1:
        print "Usage: ./fbpic2id.py <Facebook Image URL>"
        exit(1)

    pic_url = argv[0]
    img_id = pic_url.split('_')[1]
    ContentParser.parse(img_id)

if __name__ == "__main__":
    main(sys.argv[1:])
