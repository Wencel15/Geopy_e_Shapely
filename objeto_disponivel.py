#Derivando atributos não espaciais
#Vamos simular situações onde temos solicitações abertas e encerradas

import pandas as pd
orders = [
    ('order_039', 'open', 'cab_14'),
    ('order_034', 'open', 'cab_79'),
    ('order_032', 'open', 'cab_104'),
    ('order_026', 'closed', 'cab_79'),
    ('order_021', 'open', 'cab_45'),
    ('order_018', 'closed', 'cab_26'),
    ('order_008', 'closed', 'cab_112')
    ]

df_orders = pd.DataFrame(orders, columns =['order', 'status', 'cab'])
df_orders_open = df_orders[df_orders['status']=='open']
unavailable_list = df_orders_open['cab'].values.tolist()
print(unavailable_list)

# Vamos incluir as coordenadas dos objetos e o ponto de partida

from geopy.distance import distance
pick_up = 46.083822, 38.967845
cab_26 = 46.073852, 38.991890
cab_112 = 46.078228, 39.003949
cab_104 = 46.071226, 39.004947
cab_14 = 46.004859, 38.095825
cab_79 = 46.088621, 39.033929
cab_45 = 46.141225, 39.124934
cabs = {'cab_26': cab_26, 'cab_112': cab_112, 'cab_104': cab_104, 'cab_14': cab_14, 'cab_79': cab_79, 'cab_45': cab_45}

dist_list = []

for cab_name, cab_loc in cabs.items():
    if cab_name not in unavailable_list:
        dist = distance(pick_up, cab_loc).m
        dist_list.append((cab_name, round(dist)))

# Lista dos disponiveis
print(dist_list)

# Lista o mais proximo
print(min(dist_list, key=lambda x: x[1]))

#Join de conjuntos de dados espaciais e não espaciais
#Digamos que o cap tenha acento preferencial "1"

cabs_list = [
    ('cab_14',1),
    ('cab_79',0),
    ('cab_104',0),
    ('cab_45',1),
    ('cab_26',0),
    ('cab_112',1)
]

df_cabs = pd.DataFrame(cabs_list, columns=['cab', 'seat'])
df_dist = pd.DataFrame(dist_list, columns=['cab', 'dist'])

#Merge com base na coluna cab:

df = pd.merge(df_cabs, df_dist, on='cab', how='inner')
 
print(df)

#Filtramos deixando apenas as linhas que seat = 1

result_list = list(df.itertuples(index=False,name=None))
result_list = [x for x in result_list if x[1] ==1]

print(min(result_list, key=lambda x: x[2]))






