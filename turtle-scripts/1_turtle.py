import turtle

# Configuración inicial
turtle.speed(2)  # Velocidad del dibujo
turtle.bgcolor("white")  # Color de fondo

# Función para dibujar un círculo
def dibujar_circulo(radio):
    turtle.circle(radio)

# Dibujar la espiral
radio_inicial = 100
for i in range(50):
    dibujar_circulo(radio_inicial)
    radio_inicial -= 2  # Disminuir el radio para cada círculo siguiente
    turtle.right(15)  # Girar ligeramente a la derecha

turtle.done()
