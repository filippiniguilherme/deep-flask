# Overview

A friend has a YouTube channel, and wants to understand which themes get more attention, so he can make more videos on them.

# Task

* Create a simple [Flask](https://flask.palletsprojects.com/en/1.1.x/) app using Mongo as the back-end and Jinja to render the front-end.
* On the home page I can list and create videos. Each video has a name and a theme (like "Music").
* On each video I can click buttons to add thumbs up or thumbs down. I can thumbs up and thumbs down each video multiple times. It should show total thumbs up 
& thumbs down next to each video.
* On another page, it lists themes, sorted by highest score. The score for a theme is the sum of `thumbs_up - (thumbs_down/2)` for 
each video in the theme. The scores for each theme should be visible.

# Deliverable

A working Flask project that uses Mongo for the database. I should be able to visit a URL that demonstrates the fully functioning site, and get access to all the code that lets me deploy the site.