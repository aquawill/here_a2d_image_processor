# HERE A2D Junction Images Processor
Combines components/layers of HERE A2D Junction/Sign raster images produced by HERE SVG Toolbox.

usage: a2d_image_processor.exe [root directory] [resolution] [country] [iso_country_code] [dvn] ['PNG', 'JPG'] ['DAY', 'NIGHT'] ['ARROWS', 'MULTI_ARROWS'] ['LINK', 'LANE']
* [root directory] - root directory as SVG Toolbox used.
* [resolution] - 1920x1080 or 1080x1440
* [country] - country name of image folder
* [iso_country_code] - iso country code of A2DGJ LAT file
* [dvn] - data version number of A2DGJ LAT file
* ['PNG', 'JPG'] - output format
* ['DAY', 'NIGHT'] - mode JV image, day or night
* ['ARROWS', 'MULTI_ARROWS'] - same as file name of arrow images
* ['LINK', 'LANE'] - type of JV arrow id

example:
* directory of arrow images: E:\a2d_root\OUTPUT\A2DGJ\1920x1080\AUSTRALIA\ARROWS
* directory of junction images: E:\a2d_root\OUTPUT\A2DGJ\1920x1080\AUSTRALIA\JUNCTIONS
* directory of background images: E:\a2d_root\OUTPUT\A2DGJ\1920x1080\BACKGROUND
* path of JV LAT: E:\a2d_root\A2DGJ\201E0_AU_A2DGJV_LAT.csv

command:
* a2d_image_processor.exe E:\a2d_root 1920x1080 AUSTRALIA AU 201E0 PNG DAY MULTI_ARROWS LINK

----------------------------------

![](https://i.imgur.com/MJZnfHn.jpg)

![](https://i.imgur.com/Z3kfjCH.jpg)
