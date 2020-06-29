import os
import csv
import sys

from PIL import Image

if len(sys.argv) < 10:
    print("usage: a2d_image_processor.exe [root directory] [resolution] [country] [iso_country_code] [dvn] ['PNG', 'JPG'] ['DAY', 'NIGHT'] ['ARROWS', 'MULTI_ARROWS'] ['LINK', 'LANE']")
    print("* [root directory] - root directory as SVG Toolbox used.")
    print("* [resolution] - 1920x1080 or 1080x1440")
    print("* [country] - country name of image folder")
    print("* [iso_country_code] - iso country code of A2DGJ LAT file")
    print("* [dvn] - data version number of A2DGJ LAT file")
    print("* ['PNG', 'JPG'] - output format")
    print("* ['DAY', 'NIGHT'] - mode JV image, day or night")
    print("* ['ARROWS', 'MULTI_ARROWS'] - same as file name of arrow images")
    print("* ['LINK', 'LANE'] - type of JV arrow id")
    print("example:")
    print("* directory of arrow images: E:\\a2d_root\\OUTPUT\\A2DGJ\\1920x1080\\AUSTRALIA\\ARROWS")
    print("* directory of junction images: E:\\a2d_root\\OUTPUT\\A2DGJ\\1920x1080\\AUSTRALIA\\JUNCTIONS")
    print("* directory of background images: E:\\a2d_root\\OUTPUT\\A2DGJ\\1920x1080\\BACKGROUND")
    print("* path of JV LAT: E:\\a2d_root\\A2DGJ\\201E0_AU_A2DGJV_LAT.csv")
    print('command:\n* a2d_image_processor.exe E:\\a2d_root 1920x1080 AUSTRALIA AU 201E0 PNG DAY MULTI_ARROWS LINK')
else:
    # root = 'E:\\a2d_root'
    # a2dgj_root = os.path.join(root, 'A2DGJ\\')
    # a2dgs_root = os.path.join(root, 'SIGN_PROFILE_1\\')
    # resolution = '1920x1080'
    # country = 'AUSTRALIA'
    # iso_code = 'AU'
    # dvn = '201E0'
    # output_format = 'PNG'
    # day_night = 'DAY'  # ['DAY', 'NIGHT']
    # arrow_type = 'MULTI_ARROWS'  # ['ARROWS', 'MULTI_ARROWS'].
    # arrow_id_type = 'LINK'  # ['LINK', 'LANE']
    root = sys.argv[1]
    a2dgj_root = os.path.join(root, 'A2DGJ')
    a2dgs_root = os.path.join(root, 'SIGN_PROFILE_1')
    output_root = os.path.join(root, 'OUTPUT')
    products = ['A2DGJ', 'A2DGS']
    resolution = sys.argv[2]
    country = sys.argv[3]
    iso_code = sys.argv[4]
    dvn = sys.argv[5]
    output_format = sys.argv[6]
    day_night = sys.argv[7]  # ['DAY', 'NIGHT']
    arrow_type = sys.argv[8]  # ['ARROWS', 'MULTI_ARROWS'].
    arrow_id_type = sys.argv[9]  # ['LINK', 'LANE']
    a2dgj_lat_file = os.path.join(a2dgj_root, '{}_{}_A2DGJV_LAT.csv'.format(dvn, iso_code))
    output_merged_path = os.path.join(output_root, 'MERGED')
    backgrounds = os.path.join(output_root, products[0], resolution, 'BACKGROUND', 'COMBINED_REALISTIC')
    fogs = os.path.join(output_root, products[0], resolution, 'BACKGROUND', 'FOG')
    junctions = os.path.join(output_root, products[0], resolution, country, 'JUNCTIONS')
    arrows = os.path.join(output_root, products[0], resolution, country, 'ARROWS')
    signs = os.path.join(output_root, products[1], resolution, country)
    if not os.path.exists(output_root):
        os.mkdir(output_root)
    if not os.path.exists(output_merged_path):
        os.mkdir(output_merged_path)
    if not os.path.exists(os.path.join(output_merged_path, country)):
        os.mkdir(os.path.join(output_merged_path, country))
    if not os.path.exists(os.path.join(output_merged_path, country, day_night)):
        os.mkdir(os.path.join(output_merged_path, country, day_night))
    print('open: ' + a2dgj_lat_file)
    with open(a2dgj_lat_file) as a2dgj_lat_csv:
        reader = csv.DictReader(a2dgj_lat_csv)
        for row in reader:
            if row['A2DGJ_FILENAME'] != '':
                background_image_file_name = os.path.join(backgrounds, 'JV_BACKGROUND_{}_{}_{}.png'.format(day_night, row['TERRAIN'], row['HORIZON']))
                junction_image_file_name = os.path.join(junctions, '{}_{}.png'.format(row['A2DGJ_FILENAME'].split('.')[0], day_night))
                fog_image_file_name = os.path.join(fogs, 'FOG_{}.png'.format(day_night))
                trees_image_file_name = os.path.join(junctions, '{}_{}_TREES.png'.format(row['A2DGJ_FILENAME'].split('.')[0], day_night))
                arrow_name = ''
                if arrow_id_type == 'LINK':
                    arrow_name = row['LANE_ARROW_ID'].split('.')[0]
                else:
                    arrow_name = row['LANE_ARROW_ID']
                arrow_image_file_name = os.path.join(arrows, '{}_{}_{}.{}.png'.format(row['A2DGJ_FILENAME'].split('.')[0], day_night, arrow_type, arrow_name))
                sign_image_file_name = os.path.join(signs, '{}_{}.png'.format(row['A2DGS_FILENAME'].split('.')[0], day_night))
                sign_image_separated_file_name = os.path.join(signs, '{}_{}_{}.png'.format(row['A2DGS_FILENAME'].split('.')[0], day_night, row['SIDE']))
                o_link_id = row['ORIGINATING_LINK_ID']
                d_link_id = row['DEST_LINK_ID']
                tunnel = row['TUNNEL']
                iso_country_code = row['ISO_COUNTRY_CODE']
                dps = ''
                if row['MDPS'] == 'Y':
                    dps = 'MDPS'
                else:
                    dps = 'SDPS'
                output_image_file = os.path.join(output_merged_path, country, day_night, 'JV_{}_{}_{}_{}_{}_{}_{}_{}.png'.format(iso_country_code, dps, o_link_id, d_link_id, row['SIDE'], day_night, arrow_type, arrow_name))
                if not os.path.exists(output_image_file):
                    try:
                        j = Image.open(junction_image_file_name).convert("RGBA")
                        a = Image.open(arrow_image_file_name).convert("RGBA")
                        if tunnel == 'N':
                            b = Image.open(background_image_file_name).convert("RGBA")
                            f = Image.open(fog_image_file_name).convert("RGBA")
                            t = Image.open(trees_image_file_name).convert("RGBA")
                            bj = Image.alpha_composite(b, j)
                            bjf = Image.alpha_composite(bj, f)
                            junction_base = Image.alpha_composite(bjf, t)
                            result = Image.alpha_composite(junction_base, a)
                        else:
                            result = Image.alpha_composite(j, a)
                        if os.path.exists(sign_image_file_name):
                            s = Image.open(sign_image_file_name).convert("RGBA")
                            result = Image.alpha_composite(result, s)
                            # print(o_link_id, d_link_id, dps, background_image_file_name, junction_image_file_name, arrow_image_file_name, sign_image_file_name)
                        elif os.path.exists(sign_image_separated_file_name):
                            s = Image.open(sign_image_separated_file_name).convert("RGBA")
                            result = Image.alpha_composite(result, s)
                        print('merged: ' + output_image_file)
                        result.save(output_image_file, output_format)
                    except:
                        print('failed: ' + output_image_file)
                        pass
