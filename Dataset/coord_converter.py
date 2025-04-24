import math

#lat : 위도 , lon : 경도
def convert_to_grid(lat, lon):
    # 기상청 제공 공식 (초단기예보용 격자 변환)
    RE = 6371.00877  # Earth radius (km)
    GRID = 5.0       # Grid spacing (km)
    SLAT1 = 30.0     # Projection latitude 1 (degree)
    SLAT2 = 60.0     # Projection latitude 2 (degree)
    OLON = 126.0     # Reference longitude (degree)
    OLAT = 38.0      # Reference latitude (degree)
    XO = 43          # Origin X (GRID)
    YO = 136         # Origin Y (GRID)

    DEGRAD = math.pi / 180.0
    re = RE / GRID
    slat1 = SLAT1 * DEGRAD
    slat2 = SLAT2 * DEGRAD
    olon = OLON * DEGRAD
    olat = OLAT * DEGRAD

    sn = math.tan(math.pi * 0.25 + slat2 * 0.5) / math.tan(math.pi * 0.25 + slat1 * 0.5)
    sn = math.log(math.cos(slat1) / math.cos(slat2)) / math.log(sn)
    sf = math.tan(math.pi * 0.25 + slat1 * 0.5)
    sf = math.pow(sf, sn) * math.cos(slat1) / sn
    ro = math.tan(math.pi * 0.25 + olat * 0.5)
    ro = re * sf / math.pow(ro, sn)

    ra = math.tan(math.pi * 0.25 + lat * DEGRAD * 0.5)
    ra = re * sf / math.pow(ra, sn)
    theta = lon * DEGRAD - olon
    if theta > math.pi:
        theta -= 2.0 * math.pi
    if theta < -math.pi:
        theta += 2.0 * math.pi
    theta *= sn

    x = int(ra * math.sin(theta) + XO + 0.5)
    y = int(ro - ra * math.cos(theta) + YO + 0.5)
    return x, y