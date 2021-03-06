import os
import csv
import sys
import requests
import json

from PIL import Image

if len(sys.argv) < 10:
    print("usage: a2d_image_processor.exe [root directory] [resolution] [country] [iso_country_code] [lat_file_name] ['PNG', 'JPG'] ['DAY', 'NIGHT'] ['ARROWS', 'MULTI_ARROWS'] ['LINK', 'LANE', 'LANE_GROUP'] ['APIKEY' (optional)]")
    print("* [root directory] - root directory as SVG Toolbox used.")
    print("* [resolution] - 1920x1080 or 1080x1440")
    print("* [country] - country name of image folder")
    print("* [iso_country_code] - iso country code of A2DGJ LAT file")
    print("* [lat_file_name] - full name of A2DGJ LAT file")
    print("* ['PNG', 'JPG'] - output format")
    print("* ['DAY', 'NIGHT'] - mode JV image, day or night")
    print("* ['ARROWS', 'MULTI_ARROWS'] - same as file name of arrow images")
    print("* ['LINK', 'LANE', 'LANE_GROUP'] - type of JV arrow id")
    print("* ['APIKEY' (optional)] - API KEY of HERE Location Services")
    print("example:")
    print("* directory of arrow images: E:\\a2d_root\\OUTPUT\\A2DGJ\\1920x1080\\AUSTRALIA\\ARROWS")
    print("* directory of junction images: E:\\a2d_root\\OUTPUT\\A2DGJ\\1920x1080\\AUSTRALIA\\JUNCTIONS")
    print("* directory of background images: E:\\a2d_root\\OUTPUT\\A2DGJ\\1920x1080\\BACKGROUND")
    print("* path of JV LAT: E:\\a2d_root\\A2DGJ\\201E0_AU_A2DGJV_LAT.csv")
    print("* your HERE apikey: abc123")
    print('command:')
    print('* a2d_image_processor.exe E:\\a2d_root 1920x1080 AUSTRALIA AU 201E0_AU_A2DGJV_LAT.csv PNG DAY MULTI_ARROWS LINK')
    print('command with MDPS link listing from HERE Routing API:')
    print('* a2d_image_processor.exe E:\\a2d_root 1920x1080 AUSTRALIA AU 201E0_AU_A2DGJV_LAT.csv PNG DAY MULTI_ARROWS LINK abc123')
else:
    root = sys.argv[1]
    a2dgj_root = os.path.join(root, 'A2DGJ')
    a2dgs_root = os.path.join(root, 'SIGN_PROFILE_1')
    output_root = os.path.join(root, 'OUTPUT')
    products = ['A2DGJ', 'A2DGS']
    resolution = sys.argv[2]
    country = sys.argv[3]
    iso_country_code_filter = sys.argv[4]
    lat_file_name = sys.argv[5]
    output_format = sys.argv[6]
    day_night = sys.argv[7]  # ['DAY', 'NIGHT']
    arrow_type = sys.argv[8]  # ['ARROWS', 'MULTI_ARROWS'].
    arrow_id_type = sys.argv[9]  # ['LINK', 'LANE', 'LANE_GROUP']
    if len(sys.argv) == 11:
        apikey = sys.argv[10]
    a2dgj_lat_file = os.path.join(a2dgj_root, lat_file_name)
    output_merged_path = os.path.join(output_root, 'MERGED')
    backgrounds = None
    realistic_background_path = os.path.join(output_root, products[0], resolution, 'BACKGROUND', 'COMBINED_REALISTIC')
    futuristic_background_path = os.path.join(output_root, products[0], resolution, 'BACKGROUND', 'COMBINED_FUTURISTIC')
    if os.path.exists(realistic_background_path):
        backgrounds = realistic_background_path
    elif os.path.exists(futuristic_background_path):
        backgrounds = futuristic_background_path
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
    report = open('{}_report.txt'.format(lat_file_name), mode='w', encoding='utf-8')
    with open(a2dgj_lat_file) as a2dgj_lat_csv:
        reader = csv.DictReader(a2dgj_lat_csv)
        for row in reader:
            j_path = None
            b_path = None
            f_path = None
            a_path = None
            t_path = None
            s_path = None
            j = None
            b = None
            f = None
            a = None
            t = None
            s = None
            if row['A2DGJ_FILENAME'] != '' or row['A2DGJ_FILENAME_2'] != '' or row['A2DGJ_FILENAME_3'] != '':
                iso_country_code = row['ISO_COUNTRY_CODE']
                if iso_country_code == iso_country_code_filter:
                    background_image_file_name = os.path.join(backgrounds, 'JV_BACKGROUND_{}_{}.png'.format(day_night, row['TERRAIN']))
                    background_with_horizon_image_file_name = os.path.join(backgrounds, 'JV_BACKGROUND_{}_{}_{}.png'.format(day_night, row['TERRAIN'], row['HORIZON']))
                    junction_image_file_name_level_1 = os.path.join(junctions, '{}_{}.png'.format(row['A2DGJ_FILENAME'].split('.')[0], day_night))
                    junction_image_file_name_level_2 = os.path.join(junctions, '{}_{}.png'.format(row['A2DGJ_FILENAME_2'].split('.')[0], day_night))
                    junction_image_file_name_level_3 = os.path.join(junctions, '{}_{}.png'.format(row['A2DGJ_FILENAME_3'].split('.')[0], day_night))
                    fog_image_file_name = os.path.join(fogs, 'FOG_{}.png'.format(day_night))
                    trees_image_file_name = os.path.join(junctions, '{}_{}_TREES.png'.format(row['A2DGJ_FILENAME'].split('.')[0], day_night))
                    arrow_name = ''
                    if arrow_id_type == 'LANE_GROUP':
                        arrow_name = row['LANE_ARROW_ID'].split('.')[0]
                    elif arrow_id_type == 'LANE':
                        arrow_name = row['LANE_ARROW_ID']
                    elif arrow_id_type == 'LINK':
                        arrow_name = row['LINK_ARROW_ID']
                    arrow_image_file_name_level_1 = os.path.join(arrows, '{}_{}_{}.{}.png'.format(row['A2DGJ_FILENAME'].split('.')[0], day_night, arrow_type, arrow_name))
                    arrow_image_file_name_level_2 = os.path.join(arrows, '{}_{}_{}.{}.png'.format(row['A2DGJ_FILENAME_2'].split('.')[0], day_night, arrow_type, arrow_name))
                    arrow_image_file_name_level_3 = os.path.join(arrows, '{}_{}_{}.{}.png'.format(row['A2DGJ_FILENAME_2'].split('.')[0], day_night, arrow_type, arrow_name))
                    sign_image_file_name = os.path.join(signs, '{}_{}.png'.format(row['A2DGS_FILENAME'].split('.')[0], day_night))
                    sign_image_separated_file_name = os.path.join(signs, '{}_{}_{}.png'.format(row['A2DGS_FILENAME'].split('.')[0], day_night, row['SIDE']))
                    o_link_id = row['ORIGINATING_LINK_ID']
                    d_link_id = row['DEST_LINK_ID']
                    link_list = []
                    tunnel = row['TUNNEL']
                    dps = ''
                    if row['MDPS'] == 'Y':
                        dps = 'MDPS'
                        if len(sys.argv) == 11:
                            apikey = sys.argv[10]
                            here_calculate_route_url = 'https://route.ls.hereapi.com/routing/7.2/calculateroute.json?mode=fastest;car&legAttributes=links&waypoint0=link!*{},0.5&waypoint1=link!*{},0.5&apiKey={}'.format(o_link_id, d_link_id, apikey)
                            # print('GET: ' + here_calculate_route_url)
                            r = requests.get(here_calculate_route_url)
                            if r.status_code == 200:
                                t = r.text
                                j = json.loads(t)
                                legs = j['response']['route'][0]['leg']
                                i = 0
                                for leg in legs:
                                    links = leg['link']
                                    for link in links:
                                        link_list.append(link['linkId'].replace('-', '').replace('+', ''))
                                if d_link_id not in link_list or o_link_id not in link_list:
                                    report.write('Failed: no valid route from ORIGINATING_LINK_ID = {} to DEST_LINK_ID = {}'.format(o_link_id, d_link_id))
                                    print('Failed: no valid route from ORIGINATING_LINK_ID = {} to DEST_LINK_ID = {}'.format(o_link_id, d_link_id))
                                    continue
                            else:
                                link_list = [row['ORIGINATING_LINK_ID'], row['DEST_LINK_ID']]
                        else:
                            link_list = [row['ORIGINATING_LINK_ID'], row['DEST_LINK_ID']]
                    else:
                        dps = 'SDPS'
                        link_list = [row['ORIGINATING_LINK_ID'], row['DEST_LINK_ID']]
                    output_image_file = os.path.join(output_merged_path, country, day_night, 'JV_{}_{}_{}_{}_{}_{}_{}.{}'.format(iso_country_code, dps, '_'.join(link_list), row['SIDE'], day_night, arrow_type, arrow_name, output_format))
                    if not os.path.exists(output_image_file):
                        try:
                            if os.path.exists(junction_image_file_name_level_1):
                                j_path = junction_image_file_name_level_1
                            elif os.path.exists(junction_image_file_name_level_2):
                                j_path = junction_image_file_name_level_2
                            elif os.path.exists(junction_image_file_name_level_3):
                                j_path = junction_image_file_name_level_3
                            j = Image.open(j_path).convert('RGBA')
                            if os.path.exists(arrow_image_file_name_level_1):
                                a_path = arrow_image_file_name_level_1
                            elif os.path.exists(arrow_image_file_name_level_2):
                                a_path = arrow_image_file_name_level_2
                            elif os.path.exists(arrow_image_file_name_level_3):
                                a_path = arrow_image_file_name_level_3
                            a = Image.open(a_path).convert('RGBA')
                            if tunnel == 'N':
                                if os.path.exists(background_image_file_name):
                                    b_path = background_image_file_name
                                elif os.path.exists(background_with_horizon_image_file_name):
                                    b_path = background_with_horizon_image_file_name
                                b = Image.open(b_path).convert('RGBA')
                                if os.path.exists(fog_image_file_name):
                                    f_path = fog_image_file_name
                                    f = Image.open(f_path).convert('RGBA')
                                if os.path.exists(trees_image_file_name):
                                    t_path = trees_image_file_name
                                    t = Image.open(t_path).convert('RGBA')
                                bj = Image.alpha_composite(b, j)
                                bjf = Image.alpha_composite(bj, f)
                                junction_base = Image.alpha_composite(bjf, t)
                                result = Image.alpha_composite(junction_base, a)
                            else:
                                result = Image.alpha_composite(j, a)
                            if os.path.exists(sign_image_file_name):
                                s_path = sign_image_file_name
                                s = Image.open(s_path).convert('RGBA')
                                result = Image.alpha_composite(result, s)
                                # print(o_link_id, d_link_id, dps, background_image_file_name, junction_image_file_name, arrow_image_file_name, sign_image_file_name)
                            elif os.path.exists(sign_image_separated_file_name):
                                s = Image.open(sign_image_separated_file_name).convert('RGBA')
                                result = Image.alpha_composite(result, s)
                            if output_format == 'JPEG':
                                jpeg_result = Image.new('RGB', (result.width, result.height), color=(255, 255, 255))
                                jpeg_result.paste(result)
                                jpeg_result.save(output_image_file, output_format, quality=95)
                            elif output_format == 'PNG':
                                result.save(output_image_file, output_format)
                            print('merged: ' + output_image_file)
                            report.write('merged: {}\n'.format(output_image_file))
                        except Exception as e:
                            report.write('Failed: {}, Junction = {}, Arrow = {}, Background = {}, Fog = {}, Tree = {}, Sign = {}\n'.format(row, j_path, a_path, b_path, f_path, t_path, s_path))
                            print('Failed: {}, Junction = {}, Arrow = {}, Background = {}, Fog = {}, Tree = {}, Sign = {}\n'.format(row, j_path, a_path, b_path, f_path, t_path, s_path))
                            pass
