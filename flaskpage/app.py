from flask import Flask, render_template


app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hola, estas en la materia de Patrones de Comportamiento!</p>"

@app.route("/saludo")
def saludoatodos():
    return "<center>Bienvenido al analisis de NASCAR</center>"

@app.route("/about")
def sobremi():
    return "<marquee><h1> Johana Galvan Contreras, Matricula: 368703  Correo: Johana.galvan@gmail.com</h1></marquee>"

@app.route("/grafica")
def grafica():
    import pandas as pd
    import matplotlib.pyplot as plt
    # Cargar el archivo Excel
    archivo_excel = 'C:/Users/galva/datospy/flaskpage/NASCAR.xlsx'  # Cambia esto si el archivo está en otra ubicación
    df = pd.read_excel(archivo_excel)

    # 1. Cantidad total de puntos por cada fabricante
    points_by_manufacturer = df.groupby('MFR')['Points'].sum()

    # 2. Piloto con el mayor puntaje acumulado en la temporada
    top_driver = df.loc[df['Acumulado'].idxmax()]

    # 3. Promedio de puntos obtenidos por los pilotos
    average_points = df['Points'].mean()

    # 4. Cantidad total de puntos por piloto
    points_by_driver = df.groupby('Driver')['Points'].sum()

    # 5. Número de pilotos diferentes que han ganado al menos una carrera
    drivers_with_wins = df[df['Wins'] > 0]['Driver'].nunique()

    # Mostrar resultados calculados
    print("Cantidad total de puntos por fabricante:\n", points_by_manufacturer)
    print("\nPiloto con el mayor puntaje acumulado en la temporada:\n", top_driver)
    print("\nPromedio de puntos obtenidos por los pilotos:\n", average_points)
    print("\nCantidad total de puntos por piloto:\n", points_by_driver)
    print("\nNúmero de pilotos diferentes que han ganado al menos una carrera:\n", drivers_with_wins)

    # Graficar resultados

    # Configuración de subgráficas
    fig, axs = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('Análisis de Puntos de Pilotos NASCAR', fontsize=18)

    # Gráfica de puntos por fabricante
    axs[0, 0].bar(points_by_manufacturer.index, points_by_manufacturer.values, color='skyblue')
    axs[0, 0].set_title('Cantidad Total de Puntos por Fabricante')
    axs[0, 0].set_xlabel('Fabricante')
    axs[0, 0].set_ylabel('Total de Puntos')

    # Gráfica de puntos por piloto
    axs[0, 1].bar(points_by_driver.index, points_by_driver.values, color='salmon')
    axs[0, 1].set_title('Cantidad Total de Puntos por Piloto')
    axs[0, 1].set_xlabel('Piloto')
    axs[0, 1].set_ylabel('Total de Puntos')
    axs[0, 1].tick_params(axis='x', rotation=45)

    # Gráfica de promedio de puntos por piloto (texto)
    axs[1, 0].text(0.5, 0.5, f'Promedio de Puntos por Piloto: {average_points:.2f}',
                   ha='center', va='center', fontsize=14)
    axs[1, 0].set_axis_off()  # Ocultar ejes

    # Gráfica de número de pilotos con al menos una victoria (texto)
    axs[1, 1].text(0.5, 0.5, f'Número de Pilotos con al Menos una Victoria: {drivers_with_wins}',
                   ha='center', va='center', fontsize=14)
    axs[1, 1].set_axis_off()  # Ocultar ejes

    # Ajuste de diseño
    plt.tight_layout(rect=[0, 0, 1, 0.95])

    # Guardar la grafica en un archivo (En este caso, PNG)
    plt.savefig('C:/Users/galva/datospy/flaskpage/static/images/grafica.png')

    # Mostrar la gráfica
    plt.show()
    return render_template("grafica.html")


@app.route("/matrix")
def matrix():
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt

    # Ruta al archivo NASCAR.xlsx
    archivo_excel = 'C:/Users/galva/datospy/flaskpage/NASCAR.xlsx'

    # Cargar el archivo Excel
    df = pd.read_excel(archivo_excel)

    # Verificar que las columnas necesarias existen
    if 'Driver' not in df.columns or 'Wins' not in df.columns:
     return "El archivo debe contener las columnas 'Driver' y 'Wins'."

    # Obtener pilotos y sus victorias
    nodos = df['Driver'].tolist()
    victorias = dict(zip(df['Driver'], df['Wins']))

    # Crear matriz de adyacencia
    matriz_adyacencia = np.array([[0] * len(nodos) for _ in range(len(nodos))])

    # Rellenar la matriz: dos pilotos están conectados si tienen el mismo número de victorias
    for i, piloto1 in enumerate(nodos):
        for j, piloto2 in enumerate(nodos):
            if i != j and victorias.get(piloto1) == victorias.get(piloto2):
                matriz_adyacencia[i, j] = 1

    # Mostrar la matriz en la consola
    print("Matriz de Adyacencia:")
    print(matriz_adyacencia)

    # Ejemplo de conexiones desde el primer nodo
    nodo_inicio = nodos[0]
    indice_inicio = nodos.index(nodo_inicio)
    conexiones = [nodos[i] for i, conectado in enumerate(matriz_adyacencia[indice_inicio]) if conectado == 1]
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig('C:/Users/galva/datospy/flaskpage/static/images/grafica.png')

    #print(f"El nodo {nodo_inicio} está conectado con: {', '.join(conexiones)}")
    return render_template("grafica.html")