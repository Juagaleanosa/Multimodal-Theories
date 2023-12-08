# Definir el diccionario de mapeo
mapeo_valores = {
    'Oral': 1,
    'Escrito': 2,
    'Deíctico Escrito Oral': 3,
    'Escrito Oral': 4,
    'Escrito Visual': 5,
    'Metafórico Oral': 6,
    'Metafórico Visual': 7,
    'Deíctico Escrito Metafórico': 8,
    'Deíctico Escrito Oral Visual': 9,
    'Deíctico Escrito Visual': 10,
    'Deíctico Metafórico Oral': 11,
    'Deíctico Oral Visual': 12,
    'Escrito Metafórico Oral': 13,
    'Escrito Metafórico Visual': 14,
    'Escrito Oral Visual': 15,
    'Metafórico Oral Visual': 16,
    'Deíctico Escrito Metafórico Oral': 17,
    'Deíctico Escrito Metafórico Visual': 18,
    'Deíctico Metafórico Oral Visual': 19,
    'Escrito Metafórico Oral Visual': 20,
    'Deíctico Escrito Metafórico Oral Visual': 21,
    'Icónico Oral':	22,
    'Deíctico Icónico Oral Escrito': 23,
    'Icónico Oral Visual': 24,
    'Visual Oral': 25,
    'Deíctico Icónico Oral Visual': 26,
    'Icónico Oral Deíctico': 27,
    'Oral Deíctico': 28
}

nivel_esp = {
    4: "Élite",
    3: "Conocimiento",
    2: "Conocedor",
    1: "Relativista"
}

cuadrantes = {
    4: ([0, 1, 1, 0], [0, 0, 1, 1], 0.5, 0.5),
    3: ([0, -1, -1, 0], [0, 0, 1, 1], -0.5, 0.5),
    2: ([0, 1, 1, 0], [0, 0, -1, -1], 0.5, -0.5),
    1: ([0, -1, -1, 0], [0, 0, -1, -1], -0.5, -0.5)
}