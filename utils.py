import dicts as dct
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import plotly.io as pio
from IPython.display import clear_output
from matplotlib.animation import FuncAnimation
import numpy as np


def codigo_especializacion(df_filtrado, caso):
    # Obtener las columnas que terminan con 'E'
    columnas_con_E = [col for col in df_filtrado.columns if col.endswith('E')]

    fig, ax = plt.subplots(figsize=(4, 4))
    def update(frame, col_name):
        ax.clear()

        if frame < len(df_filtrado):  # Verificar si estamos dentro de los límites del DataFrame
            codsw = df_filtrado[col_name].iloc[frame]

            ax.axhline(0, color='black', linewidth=1)
            ax.axvline(0, color='black', linewidth=1)
            ax.set_xlim(-1, 1)
            ax.set_ylim(-1, 1)

            ax.annotate('', xy=(1, 0), xytext=(0.95, 0), arrowprops=dict(arrowstyle='-|>', color='black'))
            ax.annotate('', xy=(0, 1), xytext=(0, 0.95), arrowprops=dict(arrowstyle='-|>', color='black'))
            ax.annotate('', xy=(-1, 0), xytext=(-0.95, 0), arrowprops=dict(arrowstyle='-|>', color='black'))
            ax.annotate('', xy=(0, -1), xytext=(0, -0.95), arrowprops=dict(arrowstyle='-|>', color='black'))

            ax.text(0.05, 0.9, 'RE+', fontsize=9.5, color='blue')
            ax.text(0.05, -0.9, 'RE-', fontsize=9.5, color='red')
            ax.text(0.8, 0.05, 'RS+', fontsize=9.5, color='blue')
            ax.text(-0.9, 0.05, 'RS-', fontsize=9.5, color='red')

            if codsw in dct.cuadrantes:
                x, y, text_x, text_y = dct.cuadrantes[codsw]
                ax.fill(x, y, color='GRAY', alpha=0.5)
                ax.text(text_x, text_y, dct.nivel_esp[codsw], fontsize=13, color='black', ha='center', va='center')

            ax.set_title(f'{col_name} - {caso} \n Código de especialización - Minuto: {df_filtrado["TIEMPO"].iloc[frame]}', fontsize=11)
            ax.set_xticks([])
            ax.set_yticks([])
            ax.grid(True)

        if frame == len(df_filtrado) - 1:
            clear_output(wait=True)  # Borrar la última imagen cuando termine la animación

    animaciones = []

    # Iterar a través de las columnas y crear un archivo de video único para cada columna
    for col_name in columnas_con_E:
        if not (df_filtrado[col_name] == 0).all():  # Verificar si la columna contiene solo ceros
            ani = FuncAnimation(fig, update, frames=len(df_filtrado), repeat=False, interval=2000, fargs=(col_name,))
            animaciones.append(ani)  
        else:
            print(f"La columna '{col_name}' contiene solo ceros y no se creará un video para ella.")

    return animaciones


def graf_2d(df_filtrado_C, caso):
    # Cambiar paleta de colores actores
    x = df_filtrado_C.iloc[:, 1]  # Tiempo
    x1 = df_filtrado_C.iloc[:, 2]  # Docente
    x2 = df_filtrado_C.iloc[:, 5]  # Est 1
    x3 = df_filtrado_C.iloc[:, 8]  # Est 2
    x4 = df_filtrado_C.iloc[:, 11]  # Est 3

    # Definir el tamaño de la figura
    fig, ax = plt.subplots(figsize=(10,5))

    # Graficar los datos
    ax.plot(x, x1, marker='o', label='Docente', color='red')
    ax.plot(x, x2, marker='o', label='Estudiante 1', color='green')
    ax.plot(x, x4, marker='o', label='Estudiante 2', color='blue')
    ax.plot(x, x3, marker='o', label='Estudiante 3', color='purple')

    ax.set_xlabel('TIEMPO')
    ax.set_ylabel('NIVEL')
    ax.set_title(f'Onda Semántica - {caso}', fontsize=13)
    ax.legend()
    ax.grid(visible=True, color='silver', linestyle='-', linewidth=0.1)
    
    return fig


# Función para agregar un rastro 3D al gráfico
def add_trace_3d(x, y, z, color, opacity, name, df_filtrado):
    # Filtrar las coordenadas en cero
    x_filtered = [xi for xi, yi, zi in zip(x, y, z) if yi != 0 or zi != 0]
    y_filtered = [yi for yi, zi in zip(y, z) if yi != 0 or zi != 0]
    z_filtered = [zi for zi in z if zi != 0]

    return go.Scatter3d(
        x=x_filtered,
        y=y_filtered,
        z=z_filtered,
        mode='markers',
        marker=dict(
            size=10,
            symbol='circle',  # Utilizar el símbolo 'circle' para esferas
            color=color,
            opacity=opacity,
            line=dict(color='black', width=1)
        ),
        text=df_filtrado.index,
        name=name
    )


def scatter_2d(df_filtrado, df, caso):
    # Escalar el eje 'x' para que el espacio se vea como un cubo
    x_max = df_filtrado['TIEMPO'].max()
    df_filtrado['TIEMPO'] = df['TIEMPO'] / x_max

    # Configurar diseño del gráfico
    layout = go.Layout(
        title= f'Scatter semántica frente a especialización - {caso} ',  # Título del gráfico
        scene=dict(
            xaxis=dict(title='Tiempo'),
            yaxis=dict(title='Especialización'),
            zaxis=dict(title='Semántica'),
            bgcolor='rgb(250, 250, 250)',
            aspectmode="cube"  # Para que el espacio se vea como un cubo
        ),
        legend=dict(orientation="h", xanchor="right", x=0.6, y=-0.02),
        margin=dict(l=0, r=0),
        height=800,
        width=800,
        scene_camera=dict(center=dict(x=0, y=0, z=0))
    )

    # Crear trazos 3D iniciales
    traces = [
        add_trace_3d(df_filtrado['TIEMPO'], df_filtrado['DOCENTE E'], df_filtrado['DOCENTE S'], 'red', 0.8, 'DOCENTE', df_filtrado),
        add_trace_3d(df_filtrado['TIEMPO'], df_filtrado['Est 1 E'], df_filtrado['Est 1 S'], 'green', 0.8, 'Est 1', df_filtrado),
        add_trace_3d(df_filtrado['TIEMPO'], df_filtrado['Est 2 E'], df_filtrado['Est 2 S'], 'purple', 0.8, 'Est 2', df_filtrado),
        add_trace_3d(df_filtrado['TIEMPO'], df_filtrado['Est 3 E'], df_filtrado['Est 3 S'], 'blue', 0.8, 'Est 3', df_filtrado)
    ]

    # Crear una figura 3D
    fig = go.Figure(layout=layout, data=traces)

    # Crear una animación
    frames = []
    for i in range(1, len(df)):
        frame = go.Frame(
            data=[
                add_trace_3d(df_filtrado['TIEMPO'][:i], df_filtrado['DOCENTE E'][:i], df_filtrado['DOCENTE S'][:i], 'red', 0.8, 'DOCENTE', df_filtrado),
                add_trace_3d(df_filtrado['TIEMPO'][:i], df_filtrado['Est 1 E'][:i], df_filtrado['Est 1 S'][:i], 'green', 0.8, 'Est 1', df_filtrado),
                add_trace_3d(df_filtrado['TIEMPO'][:i], df_filtrado['Est 2 E'][:i], df_filtrado['Est 2 S'][:i], 'purple', 0.8, 'Est 2', df_filtrado),
                add_trace_3d(df_filtrado['TIEMPO'][:i], df_filtrado['Est 3 E'][:i], df_filtrado['Est 3 S'][:i], 'blue', 0.8, 'Est 3', df_filtrado)
            ],
            name=f'Frame {i}'
        )
        frames.append(frame)

    # Agregar los frames de animación
    fig.update(frames=frames)
    # Mostrar la leyenda
    fig.update_layout(showlegend=True)

    return fig


def scatter_3d(df_filtrado, df, caso):
    # Escalar el eje 'x' para que el espacio se vea como un cubo
    x_max = df_filtrado['TIEMPO'].max()
    df_filtrado['TIEMPO'] = df['TIEMPO'] / x_max

    # Crear una figura 3D
    fig = go.Figure()

    # Configurar diseño del gráfico
    fig.update_layout(scene=dict(
            xaxis_title='TIEMPO',
            yaxis_title='ESPECIALIZACIÓN',
            zaxis_title='SEMÁNTICA',
            bgcolor='rgb(250, 250, 250)',
            yaxis=dict(range=[0, 5]),  # Establecer el rango fijo para 'ESPECIALIZACIÓN'
            zaxis=dict(range=[0, 5]),  # Establecer el rango fijo para 'SEMÁNTICA'
        ),
        title=f'Ondas de códigos de semántica y especialización en el tiempo - {caso}',
        scene_aspectmode='cube',  # Para que el espacio se vea como un cubo
        width=800,
        height=800,
        margin=dict(l=0, r=0),
        scene_camera=dict(up=dict(x=0, y=0, z=1), center=dict(x=0, y=0, z=0), eye=dict(x=0.5, y=1, z=2))
    )

    # Mostrar la leyenda
    fig.update_layout(showlegend=True)

    # Función para agregar un rastro 3D al gráfico con etiquetas
    def add_trace_3d_with_labels(x, y, z, color, opacity, name, labels):
        return go.Mesh3d(
            x=x,
            y=y,
            z=z,
            opacity=opacity,
            color=color,
            name=name,
            text=labels,  # Agregar etiquetas a los puntos
            hoverinfo='text'  # Mostrar etiquetas al pasar el cursor sobre los puntos
        )

    # Crear trazos 3D iniciales con etiquetas

# Crear trazos 3D iniciales con etiquetas


    traces = [
        add_trace_3d_with_labels(
            df_filtrado['TIEMPO'],
            df_filtrado['DOCENTE E'],
            df_filtrado['DOCENTE S'],
            'red',
            0.7,
            'DOCENTE',
            np.where(df_filtrado['DOCENTE CODIGO M'] != 0,
                    df_filtrado['DOCENTE CODIGO M'].astype(str) + '<br>' + df_filtrado['UNIDAD LÉXICA DOCENTE'].astype(str),
                    df_filtrado['UNIDAD LÉXICA DOCENTE'].astype(str))
        ),
        add_trace_3d_with_labels(
            df_filtrado['TIEMPO'],
            df_filtrado['Est 1 E'],
            df_filtrado['Est 1 S'],
            'green',
            0.7,
            'ESTUDIANTE 1',
            np.where(df_filtrado['Est 1 CODIGO M'] != 0,
                    df_filtrado['Est 1 CODIGO M'].astype(str) + '<br>' + df_filtrado['UNIDAD LÉXICA EST 1'].astype(str),
                    df_filtrado['UNIDAD LÉXICA EST 1'].astype(str))
        ),

        add_trace_3d_with_labels(
            df_filtrado['TIEMPO'],
            df_filtrado['Est 2 E'],
            df_filtrado['Est 2 S'],
            'purple',
            0.7,
            'ESTUDIANTE 1',
            np.where(df_filtrado['Est 2 CODIGO M'] != 0,
                    df_filtrado['Est 2 CODIGO M'].astype(str) + '<br>' + df_filtrado['UNIDAD LÉXICA EST 2'].astype(str),
                    df_filtrado['UNIDAD LÉXICA EST 2'].astype(str))
        ),

        add_trace_3d_with_labels(
            df_filtrado['TIEMPO'],
            df_filtrado['Est 3 E'],
            df_filtrado['Est 3 S'],
            'blue',
            0.7,
            'ESTUDIANTE 1',
            np.where(df_filtrado['Est 3 CODIGO M'] != 0,
                    df_filtrado['Est 3 CODIGO M'].astype(str) + '<br>' + df_filtrado['UNIDAD LÉXICA EST 3'].astype(str),
                    df_filtrado['UNIDAD LÉXICA EST 3'].astype(str))
        )

    ]
    # Agregar los trazos 3D al gráfico
    for trace in traces:
        fig.add_trace(trace)

    # Crear una animación
    frames = []
    for i in range(1, len(df_filtrado)):
        frame = go.Frame(
            data=[
                add_trace_3d(df_filtrado['TIEMPO'][:i], df_filtrado['DOCENTE E'][:i], df_filtrado['DOCENTE S'][:i], 'red', 0.8, 'DOCENTE', df_filtrado),
                add_trace_3d(df_filtrado['TIEMPO'][:i], df_filtrado['Est 1 E'][:i], df_filtrado['Est 1 S'][:i], 'green', 0.5, 'ESTUDIANTE 1', df_filtrado),
                add_trace_3d(df_filtrado['TIEMPO'][:i], df_filtrado['Est 2 E'][:i], df_filtrado['Est 2 S'][:i], 'purple', 0.8, 'ESTUDIANTE 2', df_filtrado),
                add_trace_3d(df_filtrado['TIEMPO'][:i], df_filtrado['Est 3 E'][:i], df_filtrado['Est 3 S'][:i], 'blue', 0.5, 'ESTUDIANTE 3', df_filtrado)
            ],
            name=f'Frame {i}'
        )
        frames.append(frame)

    # Agregar los frames de animación
    fig.update(frames=frames)
    fig.update(frames=frames)
    
    return fig


def obtener_casos(df):
    # Mostrar las etiquetas únicas en la columna "CASO"
    etiquetas_disponibles = df['CASO'].unique()
    return tuple(etiquetas_disponibles)


def procesar_caso(df, caso):
    df_filtrado = df[df['CASO'] == caso]
    df_filtrado_C = df_filtrado.copy(deep=True)

    # Invertir el diccionario para mapear números a cadenas
    mapeo_numeros_a_cadenas = {v: k for k, v in dct.mapeo_valores.items()}

    # Reemplazar los valores en las columnas relevantes del DataFrame
    columnas_relevantes = ['DOCENTE CODIGO M', 'Est 1 CODIGO M', 'Est 2 CODIGO M', 'Est 3 CODIGO M']

    for columna in columnas_relevantes:
        df_filtrado[columna] = df_filtrado[columna].replace(mapeo_numeros_a_cadenas)

    archivos_anims = codigo_especializacion(df_filtrado, caso)

    return archivos_anims, df_filtrado_C, df_filtrado