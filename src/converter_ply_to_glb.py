import trimesh

# Загружаем PLY
mesh = trimesh.load("C:/Users/Mr_Herceg/Desktop/3Dbuilding/data/dense/mesh.ply")

# Экспортируем в glb для веба
mesh.export("C:/Users/Mr_Herceg/Desktop/3Dbuilding/data/dense/mesh.glb")