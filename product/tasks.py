from __future__ import absolute_import

import re
import json
import random
import subprocess
from multiprocessing.pool import ThreadPool

from lxml.html import document_fromstring, fromstring
from datetime import datetime, timedelta
from django.utils import timezone

from celery.schedules import crontab
from celery.task import task, periodic_task

import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC

from product.models import *

GLOBAL = {'live_auctions': []}


@periodic_task(
    run_every=(crontab(minute='0', hour='9')),
    name="product.tasks.scrap_copart",
    ignore_result=True,
    queue='high',
    options={'queue': 'high'}
)
def scrap_copart():
    scrap_copart_lots.delay([553])
    scrap_copart_lots.delay([1035])
    scrap_copart_lots.delay([846, 1378])
    scrap_copart_lots.delay([3, 765, 825, 1131, 1261])
    scrap_copart_lots.delay([315, 371])
    scrap_copart_lots.delay([200, 571, 627, 743, 1159])
    scrap_copart_lots.delay([169, 359, 801, 830, 860, 1086])
    scrap_copart_lots.delay([1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 170, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 275, 276, 277, 278, 279, 280, 281, 282, 283, 284, 285, 286, 287, 288, 289, 290, 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 312, 313, 314, 316, 317, 318, 319, 320, 321, 322, 323, 324, 325, 326, 327, 328, 329, 330, 331, 332, 333, 334, 335, 336, 337, 338, 339, 340, 341, 342, 343, 344, 345, 346, 347, 348, 349, 350, 351, 352, 353, 354, 355, 356, 357, 358, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473, 474, 475, 476, 477, 478, 479, 480, 481, 482, 483, 484, 485, 486, 487, 488, 489, 490, 491, 492, 493, 494, 495, 496, 497, 498, 499, 500, 501, 502, 503, 504, 505, 506, 507, 508, 509, 510, 511, 512, 513, 514, 515, 516, 517, 518, 519, 520, 521, 522, 523, 524, 525, 526, 527, 528, 529, 530, 531, 532, 533, 534, 535, 536, 537, 538, 539, 540, 541, 542, 543, 544, 545, 546, 547, 548, 549, 550, 551, 552, 554, 555, 556, 557, 558, 559, 560, 561, 562, 563, 564, 565, 566, 567, 568, 569, 570, 572, 573, 574, 575, 576, 577, 578, 579, 580, 581, 582, 583, 584, 585, 586, 587, 588, 589, 590, 591, 592, 593, 594, 595, 596, 597, 598, 599, 600, 601, 602, 603, 604, 605, 606, 607, 608, 609, 610, 611, 612, 613, 614, 615, 616, 617, 618, 619, 620, 621, 622, 623, 624, 625, 626, 628, 629, 630, 631, 632, 633, 634, 635, 636, 637, 638, 639, 640, 641, 642, 643, 644, 645, 646, 647, 648, 649, 650, 651, 652, 653, 654, 655, 656, 657, 658, 659, 660, 661, 662, 663, 664, 665, 666, 667, 668, 669, 670, 671, 672, 673, 674, 675, 676, 677, 678, 679, 680, 681, 682, 683, 684, 685, 686, 687, 688, 689, 690, 691, 692, 693, 694, 695, 696, 697, 698, 699, 700, 701, 702, 703, 704, 705, 706, 707, 708, 709, 710, 711, 712, 713, 714, 715, 716, 717, 718, 719, 720, 721, 722, 723, 724, 725, 726, 727, 728, 729, 730, 731, 732, 733, 734, 735, 736, 737, 738, 739, 740, 741, 742, 745, 746, 747, 748, 749, 750, 751, 752, 753, 754, 755, 756, 757, 758, 759, 760, 761, 762, 763, 764, 766, 767, 768, 769, 770, 771, 772, 773, 774, 775, 776, 777, 778, 779, 780, 781, 782, 783, 784, 785, 786, 787, 788, 789, 790, 791, 792, 793, 794, 795, 796, 797, 798, 799, 800, 802, 803, 804, 805, 806, 807, 808, 809, 810, 811, 812, 813, 814, 815, 816, 817, 818, 819, 820, 821, 822, 823, 824, 826, 827, 828, 829, 831, 832, 833, 834, 835, 836, 837, 838, 839, 840, 841, 842, 843, 844, 845, 847, 848, 849, 850, 851, 852, 853, 854, 855, 856, 857, 858, 859, 861, 862, 863, 864, 865, 866, 867, 868, 869, 870, 871, 872, 873, 874, 875, 876, 877, 878, 879, 880, 881, 882, 883, 884, 885, 886, 887, 888, 889, 890, 891, 892, 893, 894, 895, 896, 897, 898, 899, 900, 901, 902, 903, 904, 905, 906, 907, 908, 909, 910, 911, 912, 913, 914, 915, 916, 917, 918, 919, 920, 921, 922, 923, 924, 925, 926, 927, 928, 929, 930, 931, 932, 933, 934, 935, 936, 937, 938, 939, 940, 941, 942, 943, 944, 945, 946, 947, 948, 949, 950, 951, 952, 953, 954, 955, 956, 957, 958, 959, 960, 961, 962, 963, 964, 965, 966, 967, 968, 969, 970, 971, 972, 973, 974, 975, 977, 978, 979, 980, 981, 982, 983, 984, 985, 986, 987, 988, 989, 990, 991, 992, 993, 994, 995, 996, 997, 998, 999, 1000, 1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008, 1009, 1010, 1011, 1012, 1013, 1014, 1015, 1016, 1017, 1018, 1019, 1020, 1021, 1022, 1023, 1024, 1025, 1026, 1027, 1028, 1029, 1030, 1031, 1032, 1033, 1034, 1036, 1037, 1038, 1039, 1040, 1041, 1042, 1043, 1044, 1045, 1046, 1047, 1048, 1049, 1050, 1051, 1052, 1053, 1054, 1055, 1056, 1057, 1058, 1059, 1060, 1061, 1062, 1063, 1064, 1065, 1066, 1067, 1068, 1069, 1070, 1071, 1072, 1073, 1074, 1075, 1076, 1077, 1078, 1079, 1080, 1081, 1082, 1083, 1084, 1085, 1087, 1088, 1089, 1090, 1091, 1092, 1093, 1094, 1095, 1096, 1097, 1098, 1099, 1100, 1101, 1102, 1103, 1104, 1105, 1106, 1107, 1108, 1109, 1110, 1111, 1112, 1113, 1114, 1115, 1116, 1117, 1118, 1119, 1120, 1121, 1122, 1123, 1124, 1125, 1126, 1127, 1128, 1129, 1130, 1132, 1133, 1134, 1135, 1136, 1137, 1138, 1139, 1140, 1141, 1142, 1143, 1144, 1145, 1146, 1147, 1148, 1149, 1150, 1151, 1152, 1153, 1154, 1155, 1156, 1157, 1158, 1160, 1161, 1162, 1163, 1164, 1165, 1166, 1167, 1168, 1169, 1170, 1171, 1172, 1173, 1174, 1175, 1176, 1177, 1178, 1179, 1180, 1181, 1182, 1183, 1184, 1185, 1186, 1187, 1188, 1189, 1190, 1191, 1192, 1193, 1194, 1195, 1196, 1197, 1198, 1199, 1200, 1201, 1202, 1203, 1204, 1205, 1206, 1207, 1208, 1209, 1210, 1211, 1212, 1213, 1214, 1215, 1216, 1217, 1218, 1219, 1220, 1221, 1222, 1223, 1224, 1225, 1226, 1227, 1228, 1229, 1230, 1231, 1232, 1233, 1234, 1235, 1236, 1237, 1238, 1239, 1240, 1241, 1242, 1243, 1244, 1245, 1246, 1247, 1248, 1249, 1250, 1251, 1252, 1253, 1254, 1255, 1256, 1257, 1258, 1259, 1260, 1262, 1263, 1264, 1265, 1266, 1267, 1268, 1269, 1270, 1271, 1272, 1273, 1274, 1275, 1276, 1277, 1278, 1279, 1280, 1281, 1282, 1283, 1284, 1285, 1286, 1287, 1288, 1289, 1290, 1291, 1292, 1293, 1294, 1295, 1296, 1297, 1298, 1299, 1300, 1301, 1302, 1303, 1304, 1305, 1306, 1307, 1308, 1309, 1310, 1311, 1312, 1313, 1314, 1315, 1316, 1317, 1318, 1319, 1320, 1321, 1322, 1323, 1324, 1325, 1326, 1327, 1328, 1329, 1330, 1331, 1332, 1333, 1334, 1335, 1336, 1337, 1338, 1339, 1340, 1341, 1342, 1343, 1344, 1345, 1346, 1347, 1348, 1349, 1350, 1351, 1352, 1353, 1354, 1355, 1356, 1357, 1358, 1359, 1360, 1361, 1362, 1363, 1364, 1365, 1366, 1367, 1368, 1369, 1370, 1371, 1372, 1373, 1374, 1375, 1376, 1377, 1379, 1380, 1381, 1382, 1383, 1384, 1385, 1386, 1387, 1388, 1389, 1390, 1391, 1392, 1393, 1394, 1395, 1396, 1397, 1398, 1399, 1400, 1401, 1402, 1403, 1404, 1405, 1406, 1407, 1408, 1409, 1410, 1411, 1412, 1413, 1414, 1415, 1416, 1417, 1418, 1419, 1420, 1421, 1422, 1423, 1424, 1425, 1426, 1427, 1428, 1429, 1430, 1431, 1432, 1433, 1434, 1435, 1436, 1437, 1438, 1439, 1440, 1441, 1442, 1443, 1444])


@task(
    name="product.tasks.scrap_copart_lots",
    ignore_result=True,
    time_limit=36000,
    queue='high',
    options={'queue': 'high'}
)
def scrap_copart_lots(make_ids):
    options = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)
    options.add_argument('--disable-extensions')
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    while True:
        try:
            driver = webdriver.Chrome(chrome_options=options)
            break
        except:
            time.sleep(1)

    driver.get('https://www.copart.com/')
    wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//a[@data-uname="homePageSignIn"]'))).click()
    wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//a[@data-uname="homePageMemberSignIn"]'))).click()
    wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//input[@data-uname="loginUsernametextbox"]'))).send_keys('vdm.cojocaru@gmail.com')
    wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//input[@data-uname="loginPasswordtextbox"]'))).send_keys('c0p2rt')
    wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//button[@data-uname="loginSigninmemberbutton"]'))).click()

    page_count = 1000
    misc = '#MakeCode:{code} OR #MakeDesc:{description}, #VehicleTypeCode:VEHTYPE_{type},#LotYear:[1920 TO 2019]'.format
    payloads = 'draw={draw}&columns[0][data]=0&columns[0][name]=&columns[0][searchable]=true&columns[0][orderable]=false&columns[0][search][value]=&columns[0][search][regex]=false&columns[1][data]=1&columns[1][name]=&columns[1][searchable]=true&columns[1][orderable]=false&columns[1][search][value]=&columns[1][search][regex]=false&columns[2][data]=2&columns[2][name]=&columns[2][searchable]=true&columns[2][orderable]=true&columns[2][search][value]=&columns[2][search][regex]=false&columns[3][data]=3&columns[3][name]=&columns[3][searchable]=true&columns[3][orderable]=true&columns[3][search][value]=&columns[3][search][regex]=false&columns[4][data]=4&columns[4][name]=&columns[4][searchable]=true&columns[4][orderable]=true&columns[4][search][value]=&columns[4][search][regex]=false&columns[5][data]=5&columns[5][name]=&columns[5][searchable]=true&columns[5][orderable]=true&columns[5][search][value]=&columns[5][search][regex]=false&columns[6][data]=6&columns[6][name]=&columns[6][searchable]=true&columns[6][orderable]=true&columns[6][search][value]=&columns[6][search][regex]=false&columns[7][data]=7&columns[7][name]=&columns[7][searchable]=true&columns[7][orderable]=true&columns[7][search][value]=&columns[7][search][regex]=false&columns[8][data]=8&columns[8][name]=&columns[8][searchable]=true&columns[8][orderable]=true&columns[8][search][value]=&columns[8][search][regex]=false&columns[9][data]=9&columns[9][name]=&columns[9][searchable]=true&columns[9][orderable]=true&columns[9][search][value]=&columns[9][search][regex]=false&columns[10][data]=10&columns[10][name]=&columns[10][searchable]=true&columns[10][orderable]=true&columns[10][search][value]=&columns[10][search][regex]=false&columns[11][data]=11&columns[11][name]=&columns[11][searchable]=true&columns[11][orderable]=true&columns[11][search][value]=&columns[11][search][regex]=false&columns[12][data]=12&columns[12][name]=&columns[12][searchable]=true&columns[12][orderable]=true&columns[12][search][value]=&columns[12][search][regex]=false&columns[13][data]=13&columns[13][name]=&columns[13][searchable]=true&columns[13][orderable]=true&columns[13][search][value]=&columns[13][search][regex]=false&columns[14][data]=14&columns[14][name]=&columns[14][searchable]=true&columns[14][orderable]=false&columns[14][search][value]=&columns[14][search][regex]=false&columns[15][data]=15&columns[15][name]=&columns[15][searchable]=true&columns[15][orderable]=false&columns[15][search][value]=&columns[15][search][regex]=false&order[0][column]=1&order[0][dir]=asc&start={start}&length={length}&search[value]=&search[regex]=false&sort=auction_date_type desc,auction_date_utc asc&defaultSort=true&filter[MISC]={misc}&query=*&watchListOnly=false&freeFormSearch=false&page={page}&size={size}'.format

    url = "https://www.copart.com/public/vehicleFinder/search"
    detail_url = 'https://www.copart.com/public/data/lotdetails/solr/lotImages/{}'.format
    headers = {
        "Host": "www.copart.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "Connection": "keep-alive",
        "Cache-Control": "max-age=0",
    }

    for make_id in make_ids:
        make = VehicleMakes.objects.get(id=make_id)
        vtype = make.type
        description = make.description
        code = make.code

        payload = payloads(draw=1, start=0, length=page_count, misc=misc(code=code, description=description, type=vtype),
                           page=0, size=page_count)
        while True:
            try:
                response = requests.request("POST", url, data=payload, headers=headers)
                break
            except:
                print(url)
                time.sleep(1)

        result = json.loads(response.text)['data']['results']
        total = result['totalElements']

        # finder_item = VehicleMakes.objects.get(type=vtype, description=description, code=code)
        # finder_item.count = total
        # finder_item.save()

        pages_num = (total + 999) // 1000
        print(description, 'total - ' + str(total))
        print(description, 'total pages - ' + str(pages_num))

        if total == 0:
            continue

        page = 1

        driver.get(detail_url(result['content'][0]['ln']))

        while page <= pages_num:
            for _lot in result['content']:
                driver.get(detail_url(_lot['ln']))
                lot = json.loads(document_fromstring(driver.page_source).text_content())['data']
                images = lot.get('imagesList', {'FULL_IMAGE': [], 'THUMBNAIL_IMAGE': [], 'HIGH_RESOLUTION_IMAGE': []})
                try:
                    lot = lot['lotDetails']
                except:
                    print(_lot['ln'], lot, detail_url(_lot['ln']))
                    continue
                print(description + ' - ' + str(lot['ln']))

                vin = lot.get('fv', '')
                if not vin or len(vin) > 17:
                    continue

                # if Vehicle.objects.filter(lot=_lot['ln']).filter(vin=vin).exists():
                #     print('exists - ' + str(_lot['ln']))
                #     continue

                db_item, created = Vehicle.objects.get_or_create(lot=lot['ln'])

                db_item.make = lot['mkn']
                db_item.model = lot['lm']
                db_item.year = lot['lcy']
                db_item.vin = vin
                db_item.retail_value = lot['la']
                # rc
                # obc
                db_item.odometer_orr = lot['orr']   # 0 mi (NOT ACTUAL), 0 km (EXEMPT), 76,848 mi (ACTUAL)
                db_item.odometer_ord = lot['ord']   # NOT ACTUAL
                db_item.engine_type = lot.get('egn', '')
                db_item.cylinders = lot.get('cy', '')
                db_item.name = lot['ld']
                db_item.location = lot['yn']
                db_item.currency = lot['cuc']
                # tz
                if 'ad' in lot:
                    db_item.sale_date = timezone.make_aware(datetime.fromtimestamp(lot['ad'] / 1000), timezone.get_current_timezone()) + timedelta(hours=14)
                # at
                db_item.item = str(lot['aan'])
                # ahb
                # ss
                # bndc  BUY IT NOW
                # bnp   buyTodayBid 3000
                # sbf
                db_item.doc_type_ts = lot.get('ts', '')
                db_item.doc_type_stt = lot.get('stt', '')
                db_item.doc_type_td = lot.get('td', '')    # TN - SALVAGE CERTIFICATE, QC - GRAVEMENT ACCIDENTE
                # tgc
                db_item.lot_1st_damage = lot['dd']
                db_item.avatar = lot.get('tims', None)
                # lic[2]
                db_item.grid = lot['gr']
                # dtc
                db_item.lane = lot.get('al', '')
                # adt
                # ynumb
                # phynumb
                # bf
                # ymin
                # offFlg    condition
                # htsmn
                db_item.transmission = lot.get('tmtp', '')
                # myb
                # lmc - same with makecode
                # lcc
                db_item.lot_2nd_damage = lot.get('sdd', '')
                db_item.body_style = lot.get('bstl', '')
                db_item.lot_highlights = lot.get('lcd', '')
                db_item.fuel = lot.get('ft', '')
                db_item.keys = lot.get('hk', '')
                db_item.drive = lot.get('drv', '')
                # showSeller
                # sstpflg
                # syn same with yn
                # ifs
                # pbf
                # crg
                # brand
                db_item.notes = lot.get('ltnte', '').strip()
                db_item.color = lot.get('clr')
                db_item.lot_seller = lot.get('scn', '')

                db_item.current_bid = lot['dynamicLotDetails']['currentBid']
                db_item.bid_status = lot['dynamicLotDetails']['bidStatus']
                db_item.sale_status = lot['dynamicLotDetails']['saleStatus']

                db_item.images = '|'.join([a['url'][44:] for a in images.get('FULL_IMAGE', [])])
                db_item.thumb_images = '|'.join([a['url'][44:] for a in images.get('THUMBNAIL_IMAGE', [])])
                # db_item.high_images = '|'.join([a['url'][44:] for a in images.get('HIGH_RESOLUTION_IMAGE', [])])

                db_item.save()

            if page == pages_num:
                break

            page += 1
            payload = payloads(draw=page, start=page_count * (page - 1), length=page_count,
                               misc=misc(code=code, description=description, type=vtype), page=page - 1, size=page_count)
            while True:
                try:
                    response = requests.request("POST", url, data=payload, headers=headers)
                    break
                except:
                    print(url)
                    time.sleep(1)
            print('page - ' + str(page))

            result = json.loads(response.text)['data']['results']
            total = result['totalElements']
            pages_num = (total + 999) // 1000

        # finder_item = VehicleMakes.objects.get(type=vtype, description=description, code=code)
        # finder_item.count = total
        # finder_item.save()

        print('total - ' + str(total))
        print('total pages - ' + str(pages_num))

    # Checking Foregoing Lots
    # created_at    lot     vin     foregoing   show
    # 2018-07-08    111     aaa     empty       false
    # 2018-07-09    222     bbb     empty       false
    # 2018-07-10    333     aaa     111         false
    # 2018-07-11    444     bbb     222         true
    # 2018-08-09    555     aaa     333         true
    current_vin = ''
    lots = Vehicle.objects.filter(source=True).order_by('vin', 'lot')
    for lot_id, lot in enumerate(lots):
        if lot.vin == current_vin:
            lots[lot_id - 1].show = False
            lots[lot_id - 1].save()
            lot.foregoing = lots[lot_id - 1]
            lot.save()
            print(', '.join([current_vin, str(lots[lot_id - 1].lot), str(lot.lot)]))
        current_vin = lot.vin

    driver.close()
    driver.quit()


@periodic_task(
    run_every=(crontab(minute='0', hour='8')),
    name="product.tasks.scrap_iaai_lots",
    ignore_result=True,
    time_limit=36000,
    queue='normal',
    options={'queue': 'normal'}
)
def scrap_iaai_lots():
    first_url = 'Search?url=pd6JWbJ9kRzcBdFK3vKeyjpx+85A4wDWncLLWXG+ICNJ+99sqMaoisYKWs6Cr9ehv9+/+aONWE6H6WT3ZwrT5WJbMzhonrNwbBqJ1gz8MLhEGYLSkxHCvDCjFfWbo0PvmwHJtE0eSnJvuIuIOW9/5g==&crefiners=&keyword='
    item_url = 'https://www.iaai.com/Vehicle?itemID={item_id}'.format

    def get_detail(item_and_stock_number):
        item_id = item_and_stock_number[0]
        stock_id = item_and_stock_number[1]
        try:
            if Vehicle.objects.filter(lot=int(stock_id)).exists():
                print('exists - ' + item_id + ', ' + stock_id)
                return

            while True:
                try:
                    response = requests.get(item_url(item_id=item_id))
                    break
                except:
                    print('reconnect to ' + item_url(item_id=item_id))
                    time.sleep(1)
            if response.text.__contains__('<h1>Vehicle details are not found for this stock.</h1>'):
                print(item_url(item_id=item_id) + ' - Vehicle details are not found for this stock.')
                return
            t = fromstring(response.text)
            data = t.xpath('//script[@id="layoutVM"]/text()')[0].strip()
            lot = json.loads(data)['VehicleDetailsViewModel']

            print(', '.join(['ItemID: ' + lot['ItemID'], 'StockNo: ' + lot['StockNo']]))

            try:
                vin = bytearray.fromhex(lot['VIN']).decode()
                if not vin or len(vin) != 17:
                    raise Exception
            except:     # Unknown, BILL OF SALE, N/A, NONE
                print(item_url(item_id=item_id) + ' - vin not correct ' + lot['VIN'])
                return

            # db_item, created = Vehicle.objects.get_or_create(lot=item_id)
            db_item = Vehicle(lot=int(stock_id))
            db_item.vin = vin

            # General Information
            db_item.name = t.xpath('//h1[@class="pd-title-ymm"]/text()')[0]
            db_item.make = lot['Make']
            db_item.model = lot['Model']
            db_item.year = int(lot['Year'])
            db_item.currency = 'USD'

            def get_item(items, key, index=0):
                value = [a for a in items if a['Name'].strip() == key]
                if value and len(value[0]['DisplayValues']) > index:
                    return value[0]['DisplayValues'][index]['Text']
                return ''

            # Lot Information
            db_item.doc_type_td = lot['SaleDoc']
            odometer_orr = get_item(lot['ConditionInfo'], 'Odometer')
            odometer_orr = re.sub('[^0-9]', '', odometer_orr)
            db_item.odometer_orr = int(odometer_orr) if odometer_orr else 0
            db_item.odometer_ord = get_item(lot['ConditionInfo'], 'Odometer', 1)
            db_item.lot_highlights = get_item(lot['ConditionInfo'], 'runAndDrive')
            db_item.lot_seller = lot['SaleInfo']['Seller']
            db_item.lot_1st_damage = get_item(lot['ConditionInfo'], 'PrimaryDamage')
            db_item.lot_2nd_damage = get_item(lot['ConditionInfo'], 'SecondaryDamage')
            db_item.retail_value = int(re.sub('[^0-9]', '', lot['SaleInfo']['ACV'])) if lot['SaleInfo']['ACV'] else 0

            # Features
            db_item.body_style = get_item(lot['VINInfo'], 'BodyStyle')
            db_item.color = get_item(lot['VINInfo'], 'Color')
            db_item.engine_type = get_item(lot['VINInfo'], 'Engine')
            db_item.cylinders = get_item(lot['VINInfo'], 'Cylinders')
            db_item.transmission = get_item(lot['VINInfo'], 'Transmission')
            db_item.drive = get_item(lot['VINInfo'], 'DriveLineType')
            db_item.fuel = get_item(lot['VINInfo'], 'FuelType')
            db_item.keys = get_item(lot['ConditionInfo'], 'Keys')
            db_item.notes = get_item(lot['ConditionInfo'], 'MissingComponents')

            # Bid Information
            # db_item.bid_status = models.CharField(_('Bid Status'), max_length=30, default='')
            # db_item.sale_status = lot['AuctionStatusDescription']
            db_item.current_bid = int(re.sub('[^0-9]', '', lot['HighBidAmount'])) if lot['HighBidAmount'] else 0
            # db_item.buy_today_bid = models.IntegerField(_('Buy Today Bid'), default=0)
            # db_item.sold_price = models.IntegerField(_('Sold Price'), default=0)

            # Sale Information
            db_item.location = lot['SaleInfo']['TitleState'] if lot['SaleInfo']['TitleState'] else ''
            db_item.lane = lot['AuctionLane'] if lot['AuctionLane'] else '-'
            db_item.item = lot['Slot']
            # db_item.grid = models.CharField(_('Grid/Row'), max_length=5, default='')
            db_item.sale_date = timezone.make_aware(datetime.strptime(lot['LiveDate'], '%m/%d/%Y %I:%M:%S %p'), timezone.get_current_timezone())
            db_item.last_updated = timezone.make_aware(datetime.strptime(str(datetime.now().year) + '-' + lot['SaleInfo']['ModifiedDate'], '%Y-%b-%d %I:%M%p (CDT)'), timezone.get_current_timezone())

            db_item.source = False

            image_url = 'https://www.iaai.com/Images/GetJsonImageDimensions?json={"stockNumber":"%s","branchCode":"%s","salvageId":"%s"}' % (
                lot['SaleInfo']['StockNumber'], lot['BranchCode'], lot['SalvageID']
            )
            while True:
                try:
                    response = requests.get(image_url)
                    break
                except:
                    print('reconnect to ' + image_url)
                    time.sleep(1)
            if response.text != '':
                images = json.loads(response.text)
                db_item.images = '|'.join([a['K'] for a in images['keys']])
                db_item.avatar = 'https://vis.iaai.com:443/resizer?imageKeys=%s&width=128&height=96' % images['keys'][0]['K']

            db_item.save()
        except Exception as e:
            error_file = open('error.txt', 'a')
            error_file.write(item_url(item_id=item_id) + ' ' + str(e))
            error_file.close()
            print(item_url(item_id=item_id), e)

    def get_lot_urls(pg):
        payload = {
            'URL': first_url,
            'Key': 'pg',
            'Value': pg
        }
        while True:
            try:
                response = requests.post('https://www.iaai.com/Search/ChangeKey', data=payload)
                print('search key - ' + str(pg))
                break
            except:
                print('search key again - ' + str(pg))
                time.sleep(1)

        while True:
            try:
                response = requests.get('https://www.iaai.com/' + response.text)
                t = fromstring(response.text)
                print('page - ' + str(pg))
                break
            except:
                print('page again - ' + str(pg))
                time.sleep(1)

        urls = t.xpath('//div[@id="dvSearchList"]/div/div/table/tbody/tr/td[3]/a/@href')
        stock_nums = t.xpath('//div[@id="dvSearchList"]/div/div/table/tbody/tr/td[3]/p/text/text()')
        return [url.split('?')[1].split('&')[0].split('=')[1] for url in urls], stock_nums

    start = datetime.now()

    print('page - 1')
    response = requests.get('https://www.iaai.com/' + first_url)
    t = fromstring(response.text)
    results = t.xpath('//div[@id="dvSearchList"]/div/div/table/tbody/tr/td[3]/a/@href')
    stock_numbers = t.xpath('//div[@id="dvSearchList"]/div/div/table/tbody/tr/td[3]/p/text/text()')
    lots = [url.split('?')[1].split('&')[0].split('=')[1] for url in results]

    total = int(t.xpath('//span[@id="dvTotalText"]/text()')[0].strip().replace(',', ''))
    pages = (total + 99) // 100

    pool = ThreadPool(32)
    for chunk in pool.imap_unordered(get_lot_urls, range(2, pages + 1)):
        a, b = chunk
        lots += a
        stock_numbers += b

    end = datetime.now()
    print(len(lots), len(stock_numbers), (end - start).total_seconds())

    lots = [[item, stock_numbers[item_id]] for item_id, item in enumerate(lots)]

    pool = ThreadPool(32)
    for _ in pool.imap_unordered(get_detail, lots):
        pass

    current_vin = ''
    lots = Vehicle.objects.filter(source=False).order_by('vin', 'lot')
    for lot_id, lot in enumerate(lots):
        if lot.vin == current_vin:
            lots[lot_id - 1].show = False
            lots[lot_id - 1].save()
            lot.foregoing = lots[lot_id - 1]
            lot.save()
            print(', '.join([current_vin, str(lots[lot_id - 1].lot), str(lot.lot)]))
        current_vin = lot.vin


@periodic_task(
    run_every=crontab(minute='0', hour='*', day_of_week='mon,tue,wed,thu,fri'),
    name="product.tasks.scrap_live_auctions",
    ignore_result=True,
    time_limit=3600,
    queue='low',
    options={'queue': 'low'}
)
def scrap_live_auctions():
    try:
        options = webdriver.ChromeOptions()
        prefs = {"profile.managed_default_content_settings.images": 2}
        options.add_experimental_option("prefs", prefs)
        options.add_argument('--disable-extensions')
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')

        while True:
            try:
                driver = webdriver.Chrome(chrome_options=options)
                break
            except:
                time.sleep(1)
        driver.implicitly_wait(300)
        driver.set_page_load_timeout(300)

        driver.get('https://www.copart.com/todaysAuction/')

        auction_live_now = driver.find_element_by_xpath('//table[@id="auctionLiveNow-datatable"]')
        no_auction = 'There are no auctions available at this time.'
        if auction_live_now.text.__contains__(no_auction):
            print(no_auction)
            return

        auction_urls = auction_live_now.find_elements_by_xpath('./tbody/tr/td/ul/li[1]/a')
        auction_urls = [a.get_attribute('href') for a in auction_urls]

        driver.close()
        driver.quit()

        params = []
        for url in auction_urls:
            param = url.split('=')[-1]
            num = '%03d' % int(param.split('-')[0])
            params.append(num + param.split('-')[1])

        for param in params:
            if param in GLOBAL['live_auctions']:
                continue
            command = "python auction.py " + param + '-' + str(random.randint(204, 206)) + " &"
            subprocess.call(command, shell=True)
            print('new auction - https://www.copart.com/auctionDashboard?auctionDetails=' + param[:-1].lstrip('0') + '-' + param[-1])
        GLOBAL['live_auctions'] = params
        print(len(params))
    except Exception as e:
        print(e)
