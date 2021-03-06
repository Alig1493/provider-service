from django.contrib.gis.geos import Polygon


class Utils:
    polygon_data = {
        "type": "Polygon",
        "coordinates": [
            [
                [-84.3228, 34.9895],
                [-82.6062, 36.0335],
                [-82.6062, 35.9913],
                [-82.6062, 35.9791],
                [-82.5787, 35.9613],
                [-82.5677, 35.9513],
                [-84.2211, 34.9850],
                [-84.3228, 34.9895]
            ],
            [
                [-75.6903, 35.7420],
                [-75.5914, 35.7420],
                [-75.7067, 35.7420],
                [-75.6903, 35.7420]
            ],
        ]
    }

    first_polygon = Polygon(((90.37851332360677, 23.7614982192334),
                             (90.42898176842237, 23.76244087432721),
                             (90.42263029747184, 23.72331495223073),
                             (90.38091658288414, 23.72032895762397),
                             (90.38091658288414, 23.7204861169399),
                             (90.37851332360677, 23.7614982192334)
                             ))
    second_polygon = Polygon(((-79.5214462169377, 43.87007960512792),
                              (-79.2948531993911, 43.87700936674391),
                              (-79.46788786733593, 43.73230748137799),
                              (-79.5214462169377, 43.87007960512792)))
