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
    misc = '#MakeCode:{code} OR #MakeDesc:{description}, #VehicleTypeCode:VEHTYPE_{type},#LotYear:[1920 TO 2019]'.format
    payloads = 'draw={draw}&columns[0][data]=0&columns[0][name]=&columns[0][searchable]=true&columns[0][orderable]=false&columns[0][search][value]=&columns[0][search][regex]=false&columns[1][data]=1&columns[1][name]=&columns[1][searchable]=true&columns[1][orderable]=false&columns[1][search][value]=&columns[1][search][regex]=false&columns[2][data]=2&columns[2][name]=&columns[2][searchable]=true&columns[2][orderable]=true&columns[2][search][value]=&columns[2][search][regex]=false&columns[3][data]=3&columns[3][name]=&columns[3][searchable]=true&columns[3][orderable]=true&columns[3][search][value]=&columns[3][search][regex]=false&columns[4][data]=4&columns[4][name]=&columns[4][searchable]=true&columns[4][orderable]=true&columns[4][search][value]=&columns[4][search][regex]=false&columns[5][data]=5&columns[5][name]=&columns[5][searchable]=true&columns[5][orderable]=true&columns[5][search][value]=&columns[5][search][regex]=false&columns[6][data]=6&columns[6][name]=&columns[6][searchable]=true&columns[6][orderable]=true&columns[6][search][value]=&columns[6][search][regex]=false&columns[7][data]=7&columns[7][name]=&columns[7][searchable]=true&columns[7][orderable]=true&columns[7][search][value]=&columns[7][search][regex]=false&columns[8][data]=8&columns[8][name]=&columns[8][searchable]=true&columns[8][orderable]=true&columns[8][search][value]=&columns[8][search][regex]=false&columns[9][data]=9&columns[9][name]=&columns[9][searchable]=true&columns[9][orderable]=true&columns[9][search][value]=&columns[9][search][regex]=false&columns[10][data]=10&columns[10][name]=&columns[10][searchable]=true&columns[10][orderable]=true&columns[10][search][value]=&columns[10][search][regex]=false&columns[11][data]=11&columns[11][name]=&columns[11][searchable]=true&columns[11][orderable]=true&columns[11][search][value]=&columns[11][search][regex]=false&columns[12][data]=12&columns[12][name]=&columns[12][searchable]=true&columns[12][orderable]=true&columns[12][search][value]=&columns[12][search][regex]=false&columns[13][data]=13&columns[13][name]=&columns[13][searchable]=true&columns[13][orderable]=true&columns[13][search][value]=&columns[13][search][regex]=false&columns[14][data]=14&columns[14][name]=&columns[14][searchable]=true&columns[14][orderable]=false&columns[14][search][value]=&columns[14][search][regex]=false&columns[15][data]=15&columns[15][name]=&columns[15][searchable]=true&columns[15][orderable]=false&columns[15][search][value]=&columns[15][search][regex]=false&order[0][column]=1&order[0][dir]=asc&start={start}&length={length}&search[value]=&search[regex]=false&sort=auction_date_type desc,auction_date_utc asc&defaultSort=true&filter[MISC]={misc}&query=*&watchListOnly=false&freeFormSearch=false&page={page}&size={size}'.format

    url = "https://www.copart.com/public/vehicleFinder/search"
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

    data = []

    for id, makes in enumerate(VehicleMakes.objects.all()):
        vtype = makes.type
        description = makes.description
        code = makes.code

        payload = payloads(draw=1, start=0, length=1, misc=misc(code=code, description=description, type=vtype),
                           page=0, size=1)
        while True:
            try:
                response = requests.request("POST", url, data=payload, headers=headers)
                break
            except:
                print(url)
                time.sleep(1)

        result = json.loads(response.text)['data']['results']
        total = result['totalElements']
        print(','.join([str(id), description, str(total)]))
        data.append([makes.id, total])

    div_count = 5
    total = sum([a[1] for a in data])
    average = ((total + div_count - 1) // div_count)
    print(total)
    print(average)

    data = sorted(data, key=lambda x: x[1], reverse=True)

    result = [[] for _ in range(div_count)]
    amount = [0 for _ in range(div_count)]
    for _, item in enumerate(data):
        for i in range(div_count):
            if amount[i] + item[1] <= average:
                amount[i] += item[1]
                result[i].append(item[0])
                break
        result = result[::-1]

    for i in range(div_count):
        print(amount[i], result[i])
        scrap_copart_lots.delay(amount[i])
        time.sleep(25)

    '''scrap_copart_lots.delay([371, 359, 743, 860, 1131, 195, 904, 506, 693, 776, 1254, 1153, 1426, 1074, 279, 831, 18, 1410, 1146, 1325, 725, 577, 344, 81, 1431, 660, 1175, 615, 13, 1285, 144, 1369, 176, 1180, 517, 1151, 95, 949, 231, 935, 624, 326, 1100, 632, 410, 1172, 771, 1264, 178, 108, 220, 321, 75, 526, 366, 393, 96, 824, 1328, 102, 173, 313, 24, 184, 622, 148, 409, 505, 1099, 862, 10, 1021, 202, 345, 820, 1433, 330, 647, 887, 603, 529, 1195, 969, 680, 395, 774, 616, 1183, 596, 1296, 1194, 1044, 43, 110, 211, 690, 1197, 837, 893, 492, 1278, 851, 1191, 343, 1304, 297, 1232, 1064, 1365, 1240, 737, 292, 620, 631, 1269, 1210, 556, 1122, 164, 136, 266, 394, 842, 730, 299, 858, 929, 1020, 905, 1284, 40, 823, 525, 1320, 269, 1253, 939, 463, 1164, 1271, 1383, 15, 1071, 1216, 361, 806, 524, 802, 1299, 223, 870, 187, 180, 692, 1372, 500, 1239, 1217, 516, 684, 92, 1281, 662, 1326, 89, 1441, 197, 955, 1407, 752, 209, 205, 489, 434, 767, 272, 719, 544, 1205, 30, 763, 645, 708, 818, 1403, 264, 323, 514, 1221, 928, 812, 974, 166, 1360, 923, 1084, 1275, 336, 594, 474, 1061, 50, 811, 113, 1176, 996, 1006, 383, 1219, 807, 28, 873, 889, 1082, 1168, 314, 727, 971, 243, 488, 966, 114, 1093, 1171, 558, 152, 53, 255, 497, 1394, 340, 464, 63, 107, 912, 759, 72, 1276, 701, 944, 816, 149, 436, 702, 1200, 78, 1228, 335, 731, 1130, 1417, 1344, 1140, 876, 240, 1256, 886, 1245, 1425, 1376, 37, 564, 1357, 1189, 699, 161, 1244, 282, 897, 587, 355, 456, 167, 1065, 444, 1208, 1358, 289, 856, 239, 535, 819, 446, 1342, 1212, 1401, 1429, 405, 253, 853, 895, 981, 528, 617, 265, 277, 628, 1363, 163, 241, 337, 42, 1222, 490, 958, 1155, 1055, 560, 1116, 785, 866, 1263, 768, 1030, 922, 1179, 986, 950, 19, 1362, 1063, 609, 551, 844, 401, 324, 960, 607, 888, 1162, 296, 334, 903, 726, 788, 1243, 836, 469, 224, 378, 563, 1279, 227, 52, 268, 614, 65, 134, 1125, 573, 413, 907, 559, 97, 493, 194, 916, 399, 773, 351, 1420, 709, 377, 228, 273, 1323, 782, 682, 135, 319, 984, 1373, 175, 606, 1128, 697, 883, 204, 885, 1028, 931, 1201, 815, 430, 710, 119, 989, 576, 1079, 294, 212, 1138, 26, 634, 466, 419, 94, 604, 165, 1220, 555, 311, 369, 246, 101, 1112, 1111, 122, 358, 236, 1424, 1177, 1083, 1404, 593, 1068, 1390, 857, 933, 1113, 1010, 157, 1188, 770, 642, 29, 1066, 742, 921, 1199, 902, 185, 723, 623, 869, 1398, 639, 1418, 673, 663, 1060, 749, 982, 1288, 972, 484, 426, 1198, 143, 696, 947, 578, 320, 547, 1002, 1062, 568, 732, 892, 93, 1302, 1399, 198, 786, 1115, 11, 1078, 557, 795, 387, 416, 865, 84, 1286, 977, 1249, 999, 1008, 1012, 1330, 17, 329, 961, 1318, 677, 1298, 1023, 780, 957, 1355, 711, 1397, 1422, 397, 891, 283, 1436, 695, 962, 396, 375, 1193, 442, 112, 487, 357, 1121, 845, 1050, 1039, 840, 382, 287, 1026, 630, 86, 327, 1096, 1262, 1192, 242, 799, 1227, 1032, 936, 44, 458, 1391, 817, 98, 1186, 522, 2, 821, 1041, 1058, 518, 258, 249, 1137, 256, 310, 288, 305, 250, 567, 1290, 201, 1169, 841, 133, 1005, 1283, 217, 1174, 127, 1282, 251, 655, 794, 925, 373, 1287, 1073, 569, 414, 118, 591, 1089, 980, 778, 168, 1313, 1280, 849, 1316, 1102, 1133, 100, 956, 137, 908, 307, 739, 1248, 906, 312, 970, 649, 1031, 810, 1109, 1013, 301, 530, 309, 284, 1091, 14, 1312, 915, 651, 193, 1234, 23, 585, 1038, 347, 797, 356, 943, 1381, 274, 499, 420, 191, 1120, 700, 87, 734, 546, 758, 385, 565, 993, 27, 1190, 417, 519, 418, 432, 803, 832, 1345, 1421, 745, 1333, 1087, 552, 1094, 707, 1142, 531, 1315, 1400, 1110, 504, 636, 754, 562, 293, 278, 1156, 510, 917, 232, 162, 600, 1375, 76, 1408, 1, 1124, 968, 380, 1289, 1413, 408, 574, 229, 368, 1350, 1009, 1405, 796, 736, 878, 1184, 1368, 838, 990, 772, 657, 38, 252, 712, 1303, 376, 1343, 787, 937, 714, 822, 1165, 864, 592, 73, 1037, 1117, 791, 1046, 424, 1324, 1001, 1332, 859, 932, 1036])
    time.sleep(25)
    scrap_copart_lots.delay([1035, 825, 200, 830, 169, 801, 1159, 1170, 8, 813])
    time.sleep(25)
    scrap_copart_lots.delay([1378, 315, 765, 203])
    time.sleep(25)
    scrap_copart_lots.delay([627, 1086, 3, 1257, 477])
    time.sleep(25)
    scrap_copart_lots.delay([553, 571, 846, 1261, 511, 1292, 318, 1202, 150, 453, 1135, 407, 716, 877, 281, 486, 1215, 1085, 172, 25, 861, 1104, 131, 1148, 502, 389, 5, 51, 482, 1019, 1149, 141, 121, 1107, 769, 147, 438, 276, 735, 498, 402, 275, 1438, 478, 34, 954, 1052, 68, 1295, 722, 1187, 1185, 1386, 839, 637, 1337, 670, 934, 1334, 879, 997, 452, 480, 874, 365, 398, 126, 1145, 190, 629, 894, 718, 12, 959, 847, 675, 1272, 1134, 1218, 262, 512, 1349, 1029, 1161, 156, 1047, 159, 1003, 1163, 783, 433, 1088, 1209, 583, 267, 1353, 538, 496, 1167, 757, 129, 1157, 1406, 941, 379, 218, 1114, 1011, 979, 332, 1258, 1033, 1081, 1106, 644, 99, 33, 1301, 579, 987, 1374, 1178, 706, 481, 985, 476, 542, 331, 1067, 733, 1327, 1307, 930, 666, 652, 57, 257, 54, 1392, 325, 875, 206, 32, 91, 1319, 1152, 1340, 346, 491, 703, 259, 1440, 1428, 237, 61, 658, 835, 688, 580, 104, 391, 471, 468, 868, 1367, 1024, 1361, 20, 140, 390, 521, 1095, 151, 21, 225, 1414, 1364, 1396, 667, 77, 1118, 1395, 1371, 1160, 244, 1045, 618, 1322, 685, 1380, 595, 948, 39, 450, 439, 681, 951, 109, 798, 192, 814, 1004, 440, 738, 67, 610, 22, 852, 41, 291, 56, 829, 1119, 1273, 183, 445, 49, 747, 138, 431, 1018, 671, 83, 317, 386, 470, 362, 1126, 370, 612, 216, 261, 777, 1203, 779, 1359, 665, 1311, 235, 233, 659, 920, 1213, 400, 1432, 79, 1347, 1139, 755, 1423, 539, 503, 411, 1022, 1043, 467, 1385, 465, 1329, 170, 766, 271, 1101, 540, 532, 656, 683, 1051, 650, 1223, 103, 843, 863, 447, 70, 1103, 425, 1291, 47, 111, 1214, 1277, 867, 1352, 1017, 760, 687, 1267, 753, 154, 454, 668, 1314, 613, 541, 946, 983, 548, 1233, 619, 48, 142, 1206, 724, 71, 664, 590, 1346, 1241, 952, 715, 219, 1237, 1416, 441, 834, 1251, 473, 1166, 74, 485, 938, 601, 125, 179, 1443, 1310, 848, 896, 679, 406, 898, 746, 855, 4, 1331, 994, 388, 729, 536, 189, 115, 1393, 475, 597, 792, 804, 584, 1127, 828, 1442, 508, 449, 158, 561, 691, 1238, 507, 1247, 1297, 182, 1025, 1246, 973, 509, 654, 392, 704, 621, 635, 1309, 995, 992, 437, 890, 899, 415, 1341, 213, 1305, 461, 372, 9, 1224, 1336, 427, 226, 1338, 570, 304, 36, 1274, 472, 924, 674, 374, 913, 686, 910, 222, 328, 646, 384, 602, 117, 1053, 66, 599, 513, 1235, 460, 290, 1437, 1129, 1427, 1075, 64, 549, 534, 1387, 661, 1265, 545, 160, 354, 1356, 248, 689, 975, 1379, 1370, 348, 448, 740, 728, 1090, 705, 181, 1294, 124, 1143, 1351, 349, 186, 139, 177, 572, 247, 451, 775, 1007, 1123, 196, 953, 455, 805, 1411, 1415, 1339, 713, 1229, 927, 367, 850, 764, 964, 633, 800, 1270, 751, 260, 116, 35, 422, 55, 501, 1070, 1306, 1382, 146, 1108, 653, 1027, 1268, 1435, 123, 1354, 884, 882, 360, 640, 263, 784, 978, 1335, 963, 1348, 1136, 789, 270, 1076, 1321, 459, 672, 1158, 638, 1250, 1255, 1434, 60, 404, 1092, 827, 1259, 495, 85, 1069, 285, 215, 62, 120, 717, 483, 945, 1252, 1072, 1317, 153, 174, 998, 1098, 1230, 295, 308, 1211, 145, 1080, 881, 188, 575, 59, 1014, 1231, 581, 1000, 1226, 254, 1225, 1388, 515, 462, 1048, 940, 698, 207, 46, 1059, 214, 1154, 586, 1377, 353, 605, 421, 1034, 1444, 566, 643, 641, 1293, 1308, 1236, 1260, 543, 300, 520, 988, 106, 833, 793, 781, 750, 90, 128, 352, 720, 589, 880, 550, 1105, 919, 105, 429, 1204, 901, 588, 1132, 911, 909, 533, 741, 230, 1057, 826, 298, 1042, 1366, 435, 280, 210, 333, 1409, 494, 808, 221, 479, 648, 608, 457, 1181, 130, 1056, 45, 31, 554, 403, 1300, 238, 1402, 626, 364, 199, 762, 967, 748, 155, 942, 1015, 302, 80, 341, 527, 761, 363, 339, 1196, 926, 1040, 58, 523, 809, 412, 303, 611, 1384, 756, 1439, 350, 69, 1182, 1389, 6, 286, 1016, 306, 625, 854, 676, 1173, 1430, 381, 1150, 900, 872, 669, 423, 342, 598, 338, 88, 132, 871, 234, 1144, 914, 1147, 322, 790, 1242, 721, 537, 694, 1097, 82, 1141, 1266, 1077, 16, 1207, 316, 208, 7, 1419, 991, 678, 965, 1049, 245, 918, 428, 582, 443, 1054, 1412])'''


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
