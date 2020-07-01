# HERE A2D Junction Images Processor

**It's not a replacement of HERE SVG Toolbox.**

This tool combines components/layers of HERE A2DGJ/A2DGS raster images produced by HERE SVG Toolbox to complete Junction image files.

Note: A2DGJ images are mandatory and A2DGS images are optional, so if A2DGS image is not present in the output folder, only A2DGJ images will be processed.

Usage: a2d_image_processor.exe [root_directory] [resolution] [country] [iso_country_code] [lat_file_name] ['PNG', 'JPG'] ['DAY', 'NIGHT'] ['ARROWS', 'MULTI_ARROWS'] ['LINK', 'LANE']
* [root_directory] - root directory as SVG Toolbox used.
* [resolution] - 1920x1080 or 1080x1440
* [country] - country name of image folder
* [iso_country_code] - 3-digit iso country code to be processed in A2DGJ LAT
* [lat_file_name] - full name of A2DGJ LAT file
* ['PNG', 'JPG'] - output format
* ['DAY', 'NIGHT'] - mode JV image, day or night
* ['ARROWS', 'MULTI_ARROWS'] - same as file name of arrow images
* ['LINK', 'LANE'] - type of JV arrow id (same as output setting of SVG Toolbox)
* ['APIKEY' (optional)] - API KEY of HERE Location Services

Example, A2DGJ of 201E0 Australia:
* directory of arrow images: *E:\a2d_root\OUTPUT\A2DGJ\1920x1080\AUSTRALIA\ARROWS*
* directory of junction images: *E:\a2d_root\OUTPUT\A2DGJ\1920x1080\AUSTRALIA\JUNCTIONS*
* directory of sign images (optional): *E:\a2d_root\OUTPUT\A2DGS\1920x1080\AUSTRALIA*
* directory of background images: *E:\a2d_root\OUTPUT\A2DGJ\1920x1080\BACKGROUND*
* path of A2DGJ LAT: *E:\a2d_root\A2DGJ\201E0_AU_A2DGJV_LAT.csv*
* country name of Australia that to be processed: *AUSTRALIA*
* iso country code of Australia that to be processed: *AUS*
* format of output image: *PNG*
* color scheme of A2DGJ: *DAY*
* file name of arrow images: *MULTI_ARROWS*
* arrow type: *LINK* 
* your HERE apikey: *abc123*

Command:
* *a2d_image_processor.exe E:\a2d_root 1920x1080 AUSTRALIA AUS 201E0_AU_A2DGJV_LAT.csv PNG DAY MULTI_ARROWS LINK*

Command with MDPS link listing from HERE Routing API:
* *a2d_image_processor.exe E:\a2d_root 1920x1080 AUSTRALIA AUS 201E0_AU_A2DGJV_LAT.csv PNG DAY MULTI_ARROWS LINK abc123*

![](https://i.imgur.com/MsnXiwM.jpg)



---

Processed Image: 

SDPS A2DGJ + A2DGS:
**JV_AUS_SDPS_1233710436_1235484381_R_DAY_MULTI_ARROWS_LINK2.png**

![](https://i.imgur.com/hhXh0Yg.jpg)


SDPS A2DGJ + A2DGS:
**JV_AUS_MDPS_1226444315_130686948_L_DAY_MULTI_ARROWS_LINK1.png**

![](https://i.imgur.com/pDXJ4EP.jpg)

MDPS A2DGJ with link listing:
**JV_AUS_MDPS_782330849_1464939107_1464939106_133438667_R_DAY_MULTI_ARROWS_LINK3.png**

![](https://i.imgur.com/FRfTZnq.jpg)

MDPS A2DGJ + A2DGS with link listing:
**JV_AUS_MDPS_1209318725_802509065_802509064_782967165_M_DAY_MULTI_ARROWS_LINK2.png**

![](https://i.imgur.com/ZcQrYor.jpg)
