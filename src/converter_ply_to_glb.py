import trimesh

# Загружаем PLY
mesh = trimesh.load("E:/program/3Dbuilding/data/dense/meshed-poisson.ply")

# Экспортируем в glb для веба
mesh.export("E:/program/3Dbuilding/data/dense/meshed-poisson.glb")