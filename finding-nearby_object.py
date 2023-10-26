Encontrando o objeto mais proximo com coordenadas usando geopy e shapely

import pandas as pd
locations = [
    ('cab_26',43.602508,39.715685, '14:47:44'),
    ('cab_112',43.582243,39.752077, '14:47:55'),
    ('cab_26',43.607480,39.721521, '14:49:11'),
    ('cab_112',43.579258,39.758944, '14:49:51'),
    ('cab_112',43.574906,39.766325, '14:51:53'),
    ('cab_26',43.612203,39.720491, '14:52:48')
]

df = pd.DataFrame(locations, columns =['cab', 'lat', 'long', 'tm'])

#Para localizar o objeto mias proximo, precisamos somente da localização mais recente

latestrows = df.sort_values(['cab', 'tm'], ascending=False).drop_duplicates('cab')

# Convertendo o DataFrame para listas simplas para anexar campos novos usando tolist()

latestrows = latestrows.values.tolist()

#Utilizaremos o geopy  para calcular a distancia entre os objetos

from geopy.distance import distance

#Definimos um local de partida
pick_up = 43.578854, 39.754995


#Usaremos a função distance() para efetuar o calculo
for i,row in enumerate(latestrows):
    dist = distance(pick_up, (row[1],row[2])).m
    print(row[0]+ ':', round(dist))
    latestrows[i].append(round(dist))

#Usaremos a função buiilt-in  min() para deixar evidente qual esta mais perto

closest = min(latestrows, key=lambda x: x[4])
print('The closest cad is: ', closest[0], ' - the distance in meters: ', closest[4])

#Definindo poligonos com Shapely

from shapely.geometry import Point, Polygon

#Vamos simular um rio

coords = [(46.082991, 38.987384),(46.075489, 38.987599),(46.079395, 38.997684),(46.073822, 39.007297),(46.081741, 39.008842)]

poly = Polygon(coords)
cab_26 = Point(46.073852, 38.991890)
cab_112 = Point(46.078228, 39.003949)
pick_up = Point(46.080074, 38.991289)

print('cab_26 within the polygon:', cab_26.within(poly))
print('cab_112 within the polygon:', cab_112.within(poly))
print('pick_upwithin the polygon:', pick_up.within(poly))

#Simulando pontos de entradas com a divisoria do mapa contendo um rio

from shapely.geometry import Point, Polygon
from geopy.distance import distance

#utilizaremos as mesmas coordenadas do exemplo anterior, incluindo o ponto de entrada do rio

coords = [(46.082991, 38.987384),(46.075489, 38.987599),(46.079395, 38.997684),(46.073822, 39.007297),(46.081741, 39.008842)]

poly = Polygon(coords)
cab_26 = Point(46.073852, 38.991890)
cab_112 = Point(46.078228, 39.003949)
pick_up = Point(46.080074, 38.991289)
entry_point = Point(46.075357, 39.000298)

if cab_26.within(poly):
    dist = distance((pick_up.x, pick_up.y),(cab_26.x, cab_26.y)).m
else:
    dist = distance((cab_26.x, cab_26.y), (entry_point.x, entry_point.y)).m + distance((entry_point.x, entry_point.y), (pick_up.x, pick_up.y)).m
    
print(round(dist)) # calculamos o distancia entre o taxi e o ponto de entrada(se estiver fora do limite do poligono rio), depois a entrada do ponto de entrada até o local desejado

