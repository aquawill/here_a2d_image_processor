# HERE A2D Junction Images Processor

**It's not a replacement of HERE SVG Toolbox.**

This tool combines components/layers of HERE A2D Junction/Sign raster images produced by HERE SVG Toolbox to complete Junction image files.

Usage: a2d_image_processor.exe [root directory] [resolution] [country] [iso_country_code] [lat_file_name] ['PNG', 'JPG'] ['DAY', 'NIGHT'] ['ARROWS', 'MULTI_ARROWS'] ['LINK', 'LANE']
* [root directory] - root directory as SVG Toolbox used.
* [resolution] - 1920x1080 or 1080x1440
* [country] - country name of image folder
* [iso_country_code] - 3-digit iso country code to be processed in A2DGJ LAT
* [lat_file_name] - full name of A2DGJ LAT file
* ['PNG', 'JPG'] - output format
* ['DAY', 'NIGHT'] - mode JV image, day or night
* ['ARROWS', 'MULTI_ARROWS'] - same as file name of arrow images
* ['LINK', 'LANE'] - type of JV arrow id
* ['APIKEY' (optional)] - API KEY of HERE Location Services

Example:
* directory of arrow images: E:\a2d_root\OUTPUT\A2DGJ\1920x1080\AUSTRALIA\ARROWS
* directory of junction images: E:\a2d_root\OUTPUT\A2DGJ\1920x1080\AUSTRALIA\JUNCTIONS
* directory of background images: E:\a2d_root\OUTPUT\A2DGJ\1920x1080\BACKGROUND
* path of A2DGJ LAT: E:\a2d_root\A2DGJ\201E0_AU_A2DGJV_LAT.csv
* iso country code of Australia that to be processed: AUS
* your HERE apikey: abc123

Command:
* a2d_image_processor.exe E:\a2d_root 1920x1080 AUSTRALIA AUS 201E0 PNG DAY MULTI_ARROWS LINK

Command with MDPS link listing from HERE Routing API:
* a2d_image_processor.exe E:\a2d_root 1920x1080 AUSTRALIA AUS 201E0 PNG DAY MULTI_ARROWS LINK abc123

![](https://i.imgur.com/MsnXiwM.jpg)



---

Processed Image: 

SDPS: **JV_TWN_SDPS_1110093768_1084548699_R_DAY_MULTI_ARROWS_LINK2.png**

![](https://i.imgur.com/s1IykI1.jpg)

MDPS: **JV_TWN_MDPS_791548740_873367940_R_NIGHT_MULTI_ARROWS_LINK3.png**

![](https://i.imgur.com/TQuPm1C.jpg)

MDPS link listing: **JV_TWN_MDPS_1105405421_901972028_901972029_834184831_834184832_867764838_867764839_914323840_913910857_L_DAY_MULTI_ARROWS_LINK1.png**

![](https://i.imgur.com/3mt5qib.jpg)
