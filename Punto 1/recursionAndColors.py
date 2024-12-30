def recursion(n, discos, origen="A", destino="C", auxiliar="B"):
    movimientos = []

    # Validar colores repetidos
    for i in range(n - 1):
        if discos[i][1] == discos[i + 1][1]:
            return -1 

    def mover_discos(num_discos, origen, destino, auxiliar):
        if num_discos == 0:
            return
        mover_discos(num_discos - 1, origen, auxiliar, destino)
        movimientos.append((discos[num_discos - 1], origen, destino))
        mover_discos(num_discos - 1, auxiliar, destino, origen)
    mover_discos(n, origen, destino, auxiliar)
    return movimientos

n = int(input("Ingresa el número de discos (1 a 8): "))
if n < 1 or n > 8:
    print("El número de discos debe estar entre 1 y 8.")
else:
    discos = []
    print(f"Ingresa los discos en orden descendente de tamaño:")
    for i in range(n):
        tamaño = int(input(f"Tamaño del disco {i + 1}: "))
        color = input(f"Color del disco {i + 1}: ")
        discos.append((tamaño, color))

    resultado = recursion(n, discos)

    if resultado == -1:
        print("Imposible completar la transferencia")
    else:
        print("Movimientos necesarios:")
        for movimiento in resultado:
            print(movimiento)
            