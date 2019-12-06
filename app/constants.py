SEX = (
    ('femenino', 'Femenino'),
    ('masculino', 'Masculino'),
    ('otro', 'Otro'),
)


# Taken from the OECD's Frascati Manual
# https://read.oecd-ilibrary.org/science-and-technology/frascati-manual-2015_9789264239012-en#.XeKZE-dKjRY
MAIN_SCIENTIFIC_AREA = {
    'ciencias_naturales' : [
        'matematica', 'ciencias_informacion',
        'fisica', 'quimica',
        'ciencias_ambiente', 'biologia',
        'otras_naturales'
    ],
    'ingenieria': [
        'ing_civil', 'ing_electronica',
        'informatica', 'ing_mecanica',
        'ing_quimica', 'ing_materiales',
        'ing_medica', 'ing_ambiente',
        'biotecnologia_ambiente',
        'biotecnologia_industrial',
        'nano_tecnologia',
        'otras_ingenierias'
    ],
    'ciencias_medicas': [
        'medicina_basica', 'medicina_clinica',
        'ciencias_salud', 'biotecnologia_medica',
        'otras_medica'
    ],
    'ciencias_agricolas': [
        'agricultura', 'ciencias_animal',
        'veterinaria', 'biotecnologia_agricola',
        'otras_agricola'
    ],
    'ciencias_sociales': [
        'psicologia', 'economia',
        'educacion', 'sociologia',
        'leyes', 'ciencias_politicas',
        'geografia', 'comunicaciones',
        'otras_sociales'
    ],
    'humanidades_artes': [
        'historia', 'lengua_literatura',
        'filosofia', 'arte',
        'otras_humanas'
    ]
}


FIRST_CAT_SCIENTIFIC_AREA = (
    ('ciencias_naturales', 'Ciencias Naturales'),
    ('ingenieria', 'Ingeniería y Tecnología'),
    ('ciencias_medicas', 'Ciencias Médicas y de la Salud'),
    ('ciencias_agricolas', 'Ciencias Agrícolas y Veterinarias'),
    ('ciencias_sociales', 'Ciencias Sociales'),
    ('humanidades_artes', 'Humanidades y Artes'),
    ('', ''),
)


SCIENTIFIC_AREA = (
    ('agricultura', 'Agricultura, Silvicultura y Pesca'),
    ('arte', 'Artes'),
    ('biologia', 'Biología'),
    ('biotecnologia_agricola', 'Biotecnología Agrícola'),
    ('biotecnologia_ambiente', 'Biotecnología Ambiental'),
    ('biotecnologia_industrial', 'Biotecnología Industrial'),
    ('biotecnologia_medica', 'Biotecnología Médica'),
    ('ciencias_animal', 'Ciencia Animal y de los Lácteos'),
    ('ciencias_informacion', 'Ciencias de la Información y Comunicación'),
    ('ciencias_politicas', 'Ciencias Políticas'),
    ('ciencias_salud', 'Ciencias de la Salud'),
    ('ciencias_ambiente', 'Ciencias de la Tierra y relacionadas al Medio Ambiente'),
    ('comunicaciones', 'Medios de Comunicación'),
    ('leyes', 'Derecho'),
    ('economia', 'Economía y Comercio'),
    ('educacion', 'Educación'),
    ('filosofia', 'Filosofía, Ética y Religión'),
    ('fisica', 'Fisica'),
    ('geografia', 'Geografía Social y Económica'),
    ('historia', 'Historia y Arqueología'),
    ('informatica', 'Informática'),
    ('ing_ambiente', 'Ingenieria Ambiental'),
    ('ing_civil', 'Ingenieria Civil'),
    ('ing_electronica', 'Ingenieria Eléctrica y Electrónica'),
    ('ing_materiales', 'Ingenieria de Materiales'),
    ('ing_mecanica', 'Ingenieria Mecánica'),
    ('ing_medica', 'Ingenieria Médica'),
    ('ing_quimica', 'Ingenieria Química'),
    ('lengua_literatura', 'Lengua y Literatura'),
    ('matematica', 'Matemática'),
    ('medicina_basica', 'Medicina Básica'),
    ('medicina_clinica', 'Medicina Clínica'),
    ('nano_tecnologia', 'Nanotecnología'),
    ('psicologia', 'Psicología y ciencias cognitivas'),
    ('quimica', 'Quimica'),
    ('sociologia', 'Sociología'),
    ('veterinaria', 'Veterinaria'),
    ('otras_agricola', 'Otras ciencias agricolas'),
    ('otras_humanas', 'Otras ciencias humanas'),
    ('otras_naturales', 'Otras ciencias naturales'),
    ('otras_medica', 'Otras ciencias médicas'),
    ('otras_ingenierias', 'Otras ingenierías y tecnologías'),
    ('otras_sociales', 'Otras ciencias sociales'),
)

POSITION = (
    ('master_academico', 'Estudiante de Máster Académico'),
    ('doctorando', 'Estudiante de Doctorado'),
    ('postdoc', 'Post-doc'),
    ('profesor', 'Profesor'),
    ('otro', 'Otro'),
)

COMMUNICATION_CHANNELS = (
    ('whatsapp', 'Grupo de Whatsapp'),
    ('slack', 'Espacio de Trabajo en Slack'),
    ('telegram', 'Grupo de Telegram'),
    ('lista_correo', 'Lista de Correo'),
    ('facebook', 'Grupo de Facebook'),
    ('otro', '')
)