"""
Script para generar e insertar distractores para preguntas de opcion multiple.
Los distractores son opciones incorrectas pero plausibles.
"""

from database import get_connection, init_db
from text_normalizer import normalize_spanish_text

# Diccionario con distractores por ID de tarjeta
# Cada tarjeta tiene 3 distractores plausibles pero incorrectos
DISTRACTORES = {
    # ===== FUNCIONES MENTALES =====
    1: [
        "La actividad del sistema nervioso periferico.",
        "Los procesos metabolicos del organismo.",
        "La respuesta inmunologica ante estimulos externos."
    ],
    2: [
        "Sensoriales, motoras, vegetativas, reflejas y automaticas.",
        "Superiores, inferiores, basales, corticales y subcorticales.",
        "Primarias, secundarias, terciarias, cuaternarias y ejecutivas."
    ],
    3: [
        "Memoria, lenguaje, pensamiento, inteligencia y calculo.",
        "Sensopercepcion, afectividad, juicio, raciocinio y voluntad.",
        "Emocion, motivacion, aprendizaje, personalidad y conducta."
    ],
    4: [
        "Porte y actitud, conciencia, orientacion, atencion y sueno.",
        "Inteligencia, juicio, raciocinio, calculo y voluntad.",
        "Afectividad, psicomotricidad, conducta, impulsos y volicion."
    ],
    5: [
        "Sensopercepcion, lenguaje, memoria y pensamiento.",
        "Porte y actitud, conciencia, orientacion, atencion y sueno.",
        "Afectividad, psicomotricidad, impulsos y volicion."
    ],

    # ===== PORTE Y ACTITUD =====
    6: [
        "Es el estado de conciencia y orientacion del paciente.",
        "Es la capacidad de memoria y atencion durante la evaluacion.",
        "Es el nivel de inteligencia y juicio que demuestra el sujeto."
    ],
    7: [
        "El nivel educativo y la ocupacion laboral.",
        "El estado nutricional y el indice de masa corporal.",
        "Los antecedentes familiares y personales."
    ],
    8: [
        "Nivel de conciencia, orientacion y memoria.",
        "Frecuencia cardiaca, presion arterial y temperatura.",
        "Estado emocional, nivel de ansiedad y humor."
    ],
    9: [
        "Coordinada, ataxica, espastica o paralitica.",
        "Normal, alterada, abolida o ausente.",
        "Voluntaria, involuntaria, refleja o automatica."
    ],
    11: [
        "Rigida, flacida o espastica.",
        "Normal, alterada o ausente.",
        "Voluntaria, involuntaria o automatica."
    ],
    12: [
        "Normales, alterados o ausentes.",
        "Voluntarios, involuntarios o reflejos.",
        "Coordinados, incoordinados o espasticos."
    ],
    13: [
        "Nivel de conciencia y grado de orientacion.",
        "Memoria reciente y capacidad de atencion.",
        "Contenido del pensamiento y juicio critico."
    ],
    14: [
        "Movimientos bruscos, agitacion y agresividad hacia el entorno.",
        "Exceso de energia, locuacidad y euforia marcada.",
        "Tristeza profunda, llanto facil y desesperanza."
    ],
    15: [
        "Agitacion e hiperactividad motora.",
        "Hostilidad y agresividad verbal.",
        "Euforia y grandiosidad."
    ],
    16: [
        "Persona euforica y de voz elevada.",
        "Persona hostil y de actitud desafiante.",
        "Persona indiferente y de expresion plana."
    ],
    17: [
        "Movimientos lentos, expresion triste y voz apagada.",
        "Actitud colaboradora, amabilidad y disposicion.",
        "Temeroso, retraido y de bajo volumen de voz."
    ],
    18: [
        "Mantiene una distancia excesiva con el entrevistador.",
        "Muestra indiferencia total hacia la entrevista.",
        "Presenta mutismo y negacion a colaborar."
    ],
    19: [
        "Expresion de alegria, bienestar y satisfaccion.",
        "Expresion de indiferencia y desapego emocional.",
        "Expresion de hostilidad y rechazo hacia otros."
    ],
    20: [
        "El porte y la actitud son propios de un anciano.",
        "El porte y la actitud son propios de un adolescente rebelde.",
        "El porte y la actitud son formales y distantes."
    ],
    21: [
        "Calma, voz suave, paciencia y pasividad.",
        "Indiferencia, apatia y desinteres por el entorno.",
        "Temeroso, retraido y evitativo."
    ],
    22: [
        "Rostro y mirada de tristeza, movimientos lentos y pausados.",
        "Rostro y mirada de miedo, movimientos de huida.",
        "Rostro y mirada de indiferencia, movimientos escasos."
    ],
    23: [
        "Hostilidad abierta en el comportamiento.",
        "Colaboracion activa en el comportamiento.",
        "Indiferencia total en el comportamiento."
    ],
    24: [
        "Componente agresivo, hostil o amenazante.",
        "Componente infantil, inmaduro o dependiente.",
        "Componente distante, frio o indiferente."
    ],
    25: [
        "Inhibicion en las expresiones.",
        "Monotonia en las expresiones.",
        "Agresividad en las expresiones."
    ],
    26: [
        "Mirada fija al entrevistador; el paciente busca aprobacion constante.",
        "Mirada evitativa; el paciente rechaza el contacto visual.",
        "Mirada perdida; el paciente muestra desinteres total."
    ],
    27: [
        "Mejoria general con expresion facial animada y verbal fluida.",
        "Estado de hiperactividad con expresion exagerada y verborrea.",
        "Estado ansioso con expresion de preocupacion y nerviosismo."
    ],
    28: [
        "Movimientos bruscos y rapidos que reflejan ansiedad del paciente.",
        "Movimientos lentos y escasos que reflejan apatia del paciente.",
        "Movimientos repetitivos y estereotipados que reflejan compulsion."
    ],
    29: [
        "Aumento de la expresion facial y mirada inquieta.",
        "Expresion facial exagerada y mirada seductora.",
        "Expresion facial hostil y mirada desafiante."
    ],
    30: [
        "Malestar, inseguridad y desconfianza.",
        "Indiferencia, apatia y desinteres.",
        "Ansiedad, preocupacion y tension."
    ],

    # ===== CONCIENCIA =====
    31: [
        "La capacidad de recordar eventos pasados y recientes.",
        "El conocimiento que tiene la persona de si misma y del entorno.",
        "La habilidad para realizar operaciones mentales complejas."
    ],
    32: [
        "Disminucion del nivel de conciencia.",
        "Estado normal de vigilia y alerta.",
        "Ausencia total de respuesta a estimulos."
    ],
    33: [
        "Tendencia a estar agitado, con respuesta exagerada a estimulos.",
        "Estado de vigilia normal, con respuesta adecuada a estimulos.",
        "Ausencia de respuesta verbal o motora ante cualquier estimulo."
    ],
    34: [
        "Estado de agitacion y respuesta exagerada a estimulos.",
        "Tendencia a estar dormido, pero logra despertar ante estimulos.",
        "Estado de vigilia aumentada con hiperreactividad."
    ],
    35: [
        "Estado en el que hay respuesta verbal pero no motora. Solo es superficial.",
        "Estado de somnolencia con despertar ante estimulos fuertes.",
        "Estado de confusion con desorientacion fluctuante."
    ],
    36: [
        "Estado de alerta aumentada e hipervigilancia.",
        "Estado de agitacion psicomotora intensa.",
        "Estado de lucidez completa sin alteraciones."
    ],
    37: [
        "Estado de hipervigilancia, respuesta exagerada a estimulos, reconocimientos precisos; el paciente responde correctamente.",
        "Estado de somnolencia, tendencia al sueno, respuesta lenta; el paciente apenas responde.",
        "Estado de lucidez, atencion normal, orientacion completa; el paciente colabora adecuadamente."
    ],
    38: [
        "Sindrome caracterizado por lucidez, calma, orientacion, coherencia y ausencia de alucinaciones.",
        "Sindrome caracterizado por somnolencia, bradipsiquia, orientacion parcial y bradilalia.",
        "Sindrome caracterizado por estupor, mutismo, rigidez y negativismo."
    ],
    39: [
        "Sensacion de familiaridad, de ser completamente uno mismo. Hay claridad.",
        "Sensacion de irrealidad respecto del entorno externo.",
        "Sensacion de bienestar y euforia sin causa aparente."
    ],
    40: [
        "Sensacion de familiaridad o realidad aumentada respecto del entorno.",
        "Sensacion de extraneza, de no ser uno mismo.",
        "Sensacion de bienestar y conexion profunda con el entorno."
    ],
    41: [
        "Percepcion normal de la imagen corporal que mejora con procedimientos esteticos.",
        "Ausencia de conciencia corporal sin preocupacion por la apariencia.",
        "Aumento de la conciencia corporal con satisfaccion por la imagen."
    ],
    42: [
        "Hipervigilia o estado de alerta aumentado.",
        "Estupor o ausencia de respuesta.",
        "Delirium o estado confusional agudo."
    ],
    43: [
        "Letargia o somnolencia.",
        "Obnubilacion o confusion.",
        "Coma superficial o profundo."
    ],

    # ===== ORIENTACION =====
    44: [
        "La capacidad de mantener la atencion sobre un estimulo especifico.",
        "La respuesta a estimulos reales o provocados del ambiente.",
        "La habilidad de recordar eventos pasados y almacenar nueva informacion."
    ],
    45: [
        "Atencion, memoria y lenguaje.",
        "Conciencia, afectividad y pensamiento.",
        "Sensopercepcion, juicio y calculo."
    ],
    46: [
        "El paciente no sabe donde se encuentra ni la fecha actual.",
        "El paciente no reconoce a familiares cercanos pero sabe quien es.",
        "El paciente confunde lugares pero mantiene su identidad intacta."
    ],
    47: [
        "Incapacidad de saber quien es; perdida de la identidad personal.",
        "Incapacidad de mantener la atencion; perdida de la concentracion.",
        "Incapacidad de recordar eventos; perdida de la memoria reciente."
    ],
    48: [
        "Desorientacion solo en tiempo, con conservacion de lugar y persona.",
        "Desorientacion solo en lugar, con conservacion de tiempo y persona.",
        "Desorientacion solo en persona, con conservacion de tiempo y lugar."
    ],

    # ===== ATENCION =====
    52: [
        "Almacenar informacion para uso posterior (memoria). Es de manera involuntaria.",
        "Responder a estimulos del entorno (conciencia). Es de manera refleja.",
        "Interpretar los datos sensoriales (percepcion). Es de manera automatica."
    ],
    53: [
        "Almacenamiento, consolidacion y recuperacion.",
        "Codificacion, retencion y evocacion.",
        "Vigilia, lucidez y alerta."
    ],
    54: [
        "Pidiendo al sujeto que repita numeros hacia atras (atencion voluntaria).",
        "Evaluando la respuesta a estimulos dolorosos (atencion refleja).",
        "Solicitando que resuelva problemas matematicos (atencion sostenida)."
    ],
    55: [
        "Observando si el sujeto responde a estimulos inesperados: sonidos fuertes, luces brillantes.",
        "Evaluando si el sujeto recuerda informacion presentada previamente: palabras, imagenes.",
        "Verificando si el sujeto reconoce objetos y personas: caras familiares, lugares conocidos."
    ],
    56: [
        "Disminucion de la atencion que permite responder a multiples estimulos.",
        "Ausencia total de capacidad para fijar la atencion.",
        "Capacidad atencional normal sin alteraciones."
    ],
    57: [
        "Aumento de la capacidad de atencion.",
        "Incapacidad total para fijar la atencion.",
        "Cambio frecuente del foco atencional."
    ],
    58: [
        "Aumento de la atencion sobre un estimulo especifico.",
        "Disminucion leve de la capacidad atencional.",
        "Cambio frecuente del foco de atencion."
    ],
    59: [
        "El foco de la atencion permanece fijo en un solo estimulo.",
        "La capacidad de atencion esta completamente ausente.",
        "La atencion esta aumentada sobre estimulos especificos."
    ],
    60: [
        "Incapacidad para fijar la atencion.",
        "Aumento excesivo de la atencion.",
        "Disminucion de la capacidad atencional."
    ],
    61: [
        "Hipoprosexia.",
        "Hiperprosexia.",
        "Distractibilidad."
    ],

    # ===== SUENO =====
    62: [
        "12 horas.",
        "48 horas.",
        "8 horas."
    ],
    64: [
        "Sueno profundo; no hay tono muscular y hay movimientos oculares rapidos.",
        "Sueno REM; hay atonia muscular completa y suenos vividos.",
        "Sueno consolidado; aparecen los husos de sueno y complejos K."
    ],
    65: [
        "Somnolencia o adormecimiento; hay tono muscular y movimientos oculares lentos.",
        "Sueno profundo de ondas lentas; el tono muscular esta muy disminuido.",
        "Sueno REM; hay atonia muscular y movimientos oculares rapidos."
    ],
    66: [
        "Somnolencia o adormecimiento; hay tono muscular y movimientos oculares lentos.",
        "Sueno ligero consolidado; aparecen los husos de sueno.",
        "Sueno REM; hay movimientos oculares rapidos y atonia muscular."
    ],
    67: [
        "Sueno profundo de ondas lentas; no hay movimientos oculares y hay tono muscular.",
        "Sueno ligero; persiste el tono muscular y aparecen husos de sueno.",
        "Somnolencia; hay tono muscular y movimientos oculares muy lentos."
    ],
    68: [
        "En hipersomnia (exceso de sueno) e insomnio (falta de sueno).",
        "En primarias (sin causa conocida) y secundarias (por otra enfermedad).",
        "En agudas (corta duracion) y cronicas (larga duracion)."
    ],
    69: [
        "Dificultad para iniciar o mantener el sueno nocturno.",
        "Actividad motora anormal durante el sueno.",
        "Episodios de detencion respiratoria durante el sueno."
    ],
    70: [
        "Estado de hipervigilancia con aumento del estado de alerta.",
        "Estado de confusion con desorientacion temporal.",
        "Estado de agitacion con movimientos excesivos."
    ],
    71: [
        "Exceso de sueno durante el dia. Se subdivide en: leve, moderado y severo.",
        "Movimientos anormales durante el sueno. Se subdivide en: ritmicos, no ritmicos y mixtos.",
        "Episodios respiratorios durante el sueno. Se subdivide en: obstructiva, central y mixta."
    ],
    73: [
        "Episodios de movimientos involuntarios durante el sueno.",
        "Episodios de sueno excesivo durante el dia.",
        "Episodios de vocalizacion durante el sueno."
    ],
    74: [
        "Suenos que no se recuerdan y no generan malestar emocional.",
        "Episodios de actividad motora inconsciente durante el sueno.",
        "Suenos placenteros que generan bienestar al despertar."
    ],
    75: [
        "Suenos que se recuerdan muy bien y generan miedo o angustia.",
        "Episodios de habla durante el sueno sin activacion motora.",
        "Movimientos ritmicos de extremidades sin despertar completo."
    ],
    76: [
        "Dificultad para iniciar el sueno por pensamientos intrusivos.",
        "Interrupcion repetida del sueno por estimulos externos.",
        "Despertar temprano con incapacidad de volver a dormir."
    ],
    77: [
        "Movimientos ritmicos de las piernas durante el sueno.",
        "Vocalizacion involuntaria de palabras durante el sueno.",
        "Episodios de apnea obstructiva durante el sueno."
    ],
    78: [
        "Durante el sueno, la persona realiza actividad motora como caminar o sentarse.",
        "Durante el sueno, la persona presenta episodios de apnea.",
        "Durante el sueno, la persona rechina los dientes de forma involuntaria."
    ],

    # ===== SENSOPERCEPCION =====
    79: [
        "El proceso mediante el cual se almacenan los datos en la memoria.",
        "El proceso mediante el cual se reciben los estimulos sensoriales.",
        "El proceso mediante el cual se emite una respuesta conductual."
    ],
    80: [
        "Las que provienen de musculos, articulaciones y tendones.",
        "Las que informan estimulos viscerales internos.",
        "Las que permiten conocer la posicion del cuerpo en el espacio."
    ],
    81: [
        "Las que provienen de los organos de los sentidos externos.",
        "Las que informan estimulos viscerales como sed y hambre.",
        "Las que permiten interpretar los datos de las sensaciones."
    ],
    82: [
        "Las que provienen de los organos de los sentidos.",
        "Las que permiten conocer la situacion del cuerpo en el espacio.",
        "Las que provienen de musculos, articulaciones y tendones."
    ],
    83: [
        "Disminucion de la percepcion de los estimulos.",
        "Percepcion irreal sin estimulo externo.",
        "Percepcion distorsionada de un estimulo real."
    ],
    84: [
        "Aumento de la percepcion de los estimulos.",
        "Percepcion irreal de estimulos inexistentes.",
        "Percepcion normal sin alteraciones."
    ],
    86: [
        "Cambios perceptivos en el tamano de los objetos.",
        "Percepcion de estimulos inexistentes.",
        "Aumento de la intensidad de los estimulos visuales."
    ],
    87: [
        "Percepcion irreal sin ningun estimulo externo.",
        "Percepcion normal y adecuada de un estimulo real.",
        "Ausencia de percepcion ante un estimulo presente."
    ],
    88: [
        "La ilusion es una percepcion irreal sin estimulo; la alucinacion es a partir de un objeto concreto.",
        "La ilusion y la alucinacion son sinonimos que describen percepciones irreales.",
        "La ilusion es voluntaria y controlable; la alucinacion es involuntaria."
    ],
    89: [
        "El individuo no es consciente de su caracter irreal, por lo que la acepta completamente.",
        "El individuo experimenta la percepcion con mayor intensidad que en la alucinacion clasica.",
        "El individuo presenta la percepcion solo en estados de sueno o somnolencia."
    ],

    # ===== ALUCINACIONES =====
    90: [
        "Las elementales son voces claras con mensaje; las complejas son ruidos confusos sin significado.",
        "Las elementales ocurren en vigilia; las complejas solo durante el sueno.",
        "Las elementales son voluntarias; las complejas son involuntarias."
    ],
    91: [
        "Las elementales son personas u objetos definidos; las complejas son luces difusas.",
        "Las elementales ocurren con ojos cerrados; las complejas con ojos abiertos.",
        "Las elementales son en blanco y negro; las complejas son en color."
    ],
    92: [
        "Percepcion aumentada de olores y sabores reales que existen.",
        "Percepcion disminuida de olores y sabores presentes.",
        "Incapacidad total para percibir olores y sabores."
    ],
    93: [
        "Activa: cree que la ha tocado una persona. Pasiva: cree haber tocado algo inexistente.",
        "Activa: ocurre durante la vigilia. Pasiva: ocurre durante el sueno.",
        "Activa: es consciente de su irrealidad. Pasiva: la acepta como real."
    ],
    94: [
        "Alucinaciones que se manifiestan a nivel auditivo; por ejemplo, escuchar voces.",
        "Alucinaciones que se manifiestan a nivel visual; por ejemplo, ver personas.",
        "Alucinaciones que se manifiestan a nivel tactil; por ejemplo, sentir que lo tocan."
    ],
    95: [
        "Experimentar un olor o sabor irreal de algo inexistente.",
        "Experimentar una sensacion tactil irreal en la piel.",
        "Experimentar una sensacion visceral irreal en organos internos."
    ],

    # ===== PENSAMIENTO =====
    96: [
        "La velocidad del pensamiento y la continuidad de las asociaciones.",
        "Las ideas especificas que expresa el paciente.",
        "La capacidad de memoria y atencion durante el discurso."
    ],
    97: [
        "La logica del pensamiento, teniendo en cuenta coherencia y racionalidad.",
        "Las ideas especificas como delirios, obsesiones o fobias.",
        "La capacidad de expresar el pensamiento mediante el lenguaje."
    ],
    98: [
        "La logica y coherencia del pensamiento.",
        "La velocidad y continuidad del pensamiento.",
        "La capacidad de expresion verbal del pensamiento."
    ],
    99: [
        "Es la capacidad de almacenar y evocar informacion. Se expresa a traves de la conducta.",
        "Es la respuesta emocional ante estimulos. Se expresa a traves de la afectividad.",
        "Es la capacidad de percibir estimulos. Se expresa a traves de los sentidos."
    ],
    100: [
        "Pensamiento que sigue las reglas de la logica formal.",
        "Pensamiento que se basa en evidencia empirica.",
        "Pensamiento que es coherente y organizado."
    ],
    101: [
        "Enlentecimiento del flujo con asociaciones lentas y pausadas.",
        "Suspension subita del flujo con bloqueo del pensamiento.",
        "Perdida de la logica con frases incoherentes."
    ],
    102: [
        "Disminucion del flujo y lentitud de asociacion, con coherencia.",
        "Suspension subita de la idea, seguida de una pausa.",
        "Perdida del ordenamiento logico entre las ideas."
    ],
    103: [
        "Aumento del flujo y rapidez de asociacion.",
        "Suspension subita de la idea con bloqueo.",
        "Perdida de la coherencia entre las ideas."
    ],
    104: [
        "Frases ordenadas con una hilacion logica clara.",
        "Exceso de detalles para llegar a la idea central.",
        "Enlentecimiento del flujo del pensamiento."
    ],
    105: [
        "Aceleracion del flujo con asociaciones rapidas y sucesivas.",
        "Frases desordenadas sin estructura gramatical correcta.",
        "Suspension subita de la idea seguida de una pausa."
    ],
    106: [
        "Aceleracion continua de la idea sin pausas.",
        "Exceso de rodeos para llegar a la idea central.",
        "Perdida del ordenamiento logico entre las ideas."
    ],
    107: [
        "Las respuestas no llegan a la idea, aunque estan cerca.",
        "Suspension subita de la idea, seguida de una pausa.",
        "Aceleracion del flujo con asociaciones rapidas."
    ],
    108: [
        "Exceso de rodeos para llegar a la idea central.",
        "Suspension subita de la idea con bloqueo.",
        "Perdida completa de la coherencia gramatical."
    ],
    109: [
        "Ideas que el paciente reconoce como racionales y apropiadas.",
        "Ideas que el paciente puede controlar facilmente.",
        "Ideas que son congruentes con la realidad externa."
    ],
    110: [
        "Idea que aparece ocasionalmente, racional, que el paciente no reconoce como propia.",
        "Idea fija que no es repetitiva ni persistente.",
        "Idea delirante que el paciente acepta como verdadera."
    ],
    111: [
        "Es una creencia verdadera. Tipos: realista, adaptativa, funcional, racional.",
        "Es un pensamiento obsesivo. Tipos: contaminacion, duda, simetria, agresion.",
        "Es una idea fija. Tipos: recurrente, intrusiva, persistente, egodistonica."
    ],
    112: [
        "Idea verdadera de padecer una enfermedad confirmada.",
        "Idea obsesiva de contaminacion sin relacion con enfermedad.",
        "Idea delirante de persecucion por entidades medicas."
    ],
    113: [
        "Idea de que lo interno genera un significado para el paciente.",
        "Idea de que el paciente puede controlar lo externo.",
        "Idea de que lo externo no tiene ningun significado especial."
    ],
    114: [
        "Bradipsiquia.",
        "Bloqueo del pensamiento.",
        "Disgregacion."
    ],
    115: [
        "Fuga de ideas.",
        "Bradipsiquia.",
        "Tangencialidad."
    ],

    # ===== LENGUAJE =====
    116: [
        "Tono, volumen, ritmo y articulacion.",
        "Memoria, atencion, orientacion y conciencia.",
        "Pensamiento, afectividad, conducta y percepcion."
    ],
    117: [
        "La capacidad de entender ordenes verbales.",
        "La capacidad de nombrar objetos correctamente.",
        "La capacidad de repetir frases escuchadas."
    ],
    118: [
        "Evaluando la cantidad de palabras que articula por minuto.",
        "Pidiendo al paciente que repita frases complejas.",
        "Solicitando que nombre objetos y sus partes."
    ],
    119: [
        "Pidiendo al paciente senalar objetos mencionados.",
        "Evaluando la cantidad de palabras por minuto.",
        "Verificando la capacidad de nombrar objetos."
    ],
    120: [
        "Evaluando la capacidad de repetir frases en orden.",
        "Pidiendo al paciente senalar objetos mencionados.",
        "Evaluando la cantidad de palabras por minuto."
    ],
    121: [
        "Disminucion excesiva del flujo de palabras.",
        "Repeticion involuntaria de palabras o frases.",
        "Dificultad para articular silabas correctamente."
    ],
    122: [
        "Aumento excesivo del flujo de palabras.",
        "Repeticion de la ultima silaba pronunciada.",
        "Dificultad para pronunciar palabras completas."
    ],
    123: [
        "Repeticion involuntaria de palabras completas.",
        "Aumento excesivo del flujo de palabras.",
        "Dificultad en la articulacion de silabas."
    ],
    124: [
        "Repeticion de la ultima silaba pronunciada.",
        "Uso incontrolable de palabras obscenas.",
        "Invension de palabras nuevas sin significado."
    ],
    125: [
        "Repeticion involuntaria de palabras o frases.",
        "Dificultad para pronunciar palabras correctamente.",
        "Aumento excesivo del flujo de palabras."
    ],
    126: [
        "Dificultad en la articulacion de silabas.",
        "Repeticion involuntaria de palabras.",
        "Alteracion del tono de la voz."
    ],
    127: [
        "Dificultad para pronunciar palabras completas.",
        "Alteracion del tono y calidad de la voz.",
        "Repeticion involuntaria de frases escuchadas."
    ],
    128: [
        "Alteracion del tono de la voz por lesion laringea.",
        "Dificultad en la articulacion de silabas por lesion neurologica.",
        "Aumento excesivo del flujo de palabras por estado maniaco."
    ],
    129: [
        "Alteracion del habla por repeticion de silabas.",
        "Dificultad en la articulacion por lesion neurologica.",
        "Repeticion involuntaria de palabras escuchadas."
    ],
    131: [
        "Repetir palabras existentes de forma involuntaria.",
        "Usar palabras obscenas de forma incontrolable.",
        "Articular silabas de forma incorrecta."
    ],
    132: [
        "Inhibicion completa del lenguaje verbal.",
        "Dificultad para pronunciar palabras correctamente.",
        "Inventar palabras nuevas con significado personal."
    ],
    133: [
        "Aumento excesivo del flujo de palabras.",
        "Repeticion involuntaria de frases escuchadas.",
        "Dificultad para articular silabas."
    ],
    134: [
        "Discurso en voz alta dirigido a otros presentes.",
        "Inhibicion total del lenguaje verbal.",
        "Repeticion involuntaria de palabras o frases."
    ],
    135: [
        "Discurso dirigido a otras personas presentes.",
        "Movimiento de labios sin emision de sonido.",
        "Inhibicion completa del lenguaje."
    ],
    136: [
        "Ecolalia, coprolalia, logorrea y mutismo.",
        "Taquilalia, bradilalia, disartria y disfonia.",
        "Neologismo, verborrea, soliloquio y muscitacion."
    ],
    137: [
        "Coprolalia.",
        "Logorrea.",
        "Logoclonia."
    ],
    138: [
        "Dislalia.",
        "Disfemia.",
        "Disfonia."
    ],

    # ===== MEMORIA =====
    139: [
        "Funcion que permite percibir estimulos del presente. Implica sensacion y percepcion.",
        "Funcion que permite anticipar eventos futuros. Implica planificacion y prospeccion.",
        "Funcion que permite atender a estimulos especificos. Implica focalizacion y concentracion."
    ],
    140: [
        "Inmediata y diferida.",
        "Explicita e implicita.",
        "Declarativa y procedimental."
    ],
    141: [
        "Retrograda y anterograda.",
        "Explicita e implicita.",
        "Episodica y semantica."
    ],
    142: [
        "Capacidad de formar nuevos recuerdos despues de un punto de referencia.",
        "Capacidad de retener informacion durante segundos a un minuto.",
        "Capacidad de retener informacion de meses a anos."
    ],
    143: [
        "Capacidad de recordar eventos ocurridos antes de un punto de referencia.",
        "Capacidad de retener informacion durante segundos (memoria de trabajo).",
        "Capacidad de retener informacion de meses a anos (memoria remota)."
    ],
    144: [
        "Retencion de informacion de minutos a dias.",
        "Retencion de informacion de meses a anos.",
        "Capacidad de recordar eventos previos a un trauma."
    ],
    145: [
        "Retencion de informacion durante segundos a un minuto.",
        "Retencion de informacion de meses a anos.",
        "Capacidad de formar nuevos recuerdos despues de un evento."
    ],
    146: [
        "Retencion de informacion durante segundos a un minuto.",
        "Retencion de informacion de minutos a dias.",
        "Capacidad de recordar eventos previos a un trauma."
    ],
    147: [
        "Disminucion de la capacidad para almacenar detalles.",
        "Incapacidad total para formar nuevos recuerdos.",
        "Dificultad para evocar recuerdos almacenados."
    ],
    149: [
        "Facilidad para recordar eventos con precision y detalle.",
        "Incapacidad total para almacenar nueva informacion.",
        "Reconocimiento correcto de eventos previamente experimentados."
    ],
    150: [
        "Considerar como desconocidos hechos que si son conocidos.",
        "Dificultad para almacenar nuevos recuerdos.",
        "Llenar espacios de memoria con versiones falsas."
    ],
    151: [
        "La persona cree no haber experimentado nunca la situacion.",
        "La persona no puede recordar eventos recientes.",
        "La persona confunde recuerdos reales con imaginarios."
    ],

    # ===== AFECTIVIDAD =====
    152: [
        "El conjunto de los pensamientos, las ideas y el juicio critico.",
        "El conjunto de las percepciones, las sensaciones y la memoria.",
        "El conjunto de las conductas, los impulsos y la voluntad."
    ],
    153: [
        "Reaccion afectiva subita ante un estimulo, de corta duracion. Es mas intenso.",
        "Estado emocional que predomina en un momento dado.",
        "Respuesta conductual ante un estimulo amenazante."
    ],
    154: [
        "Estado afectivo estable influenciado por la personalidad. Es de larga duracion.",
        "Estado emocional que predomina y persiste durante un tiempo.",
        "Respuesta cognitiva ante estimulos ambiguos."
    ],
    155: [
        "Reaccion emocional breve ante un estimulo especifico.",
        "Estado afectivo estable influenciado por experiencias previas.",
        "Respuesta conductual automatica ante amenazas."
    ],
    156: [
        "Estado afectivo caracterizado por malestar, tristeza y desesperanza.",
        "Estado afectivo caracterizado por miedo, ansiedad y preocupacion.",
        "Estado afectivo caracterizado por indiferencia, apatia y desinteres."
    ],
    157: [
        "Sensacion de malestar intenso.",
        "Sensacion de indiferencia total.",
        "Sensacion de ansiedad extrema."
    ],
    158: [
        "Sensacion de malestar extremo.",
        "Sensacion de bienestar moderado.",
        "Sensacion de indiferencia total."
    ],
    159: [
        "Sindrome conformado por tristeza, bradipsiquia y actividad disminuida, improductiva.",
        "Sindrome conformado por ansiedad, preocupacion y actividad aumentada, desorganizada.",
        "Sindrome conformado por indiferencia, apatia y ausencia de actividad."
    ],
    160: [
        "Sindrome conformado por tristeza afectiva, bradipsiquia, disminucion de la actividad y aumento del sueno.",
        "Sindrome conformado por ansiedad, preocupacion excesiva, inquietud y dificultad para dormir.",
        "Sindrome conformado por indiferencia, apatia, ausencia de motivacion y sueno normal."
    ],
    161: [
        "La mania incluye tristeza mas intensa y disminucion de la actividad; la hipomania mantiene funcionalidad.",
        "La mania y la hipomania son sinonimos sin diferencias clinicas significativas.",
        "La mania es menos severa que la hipomania y no requiere tratamiento."
    ],
    162: [
        "Sensacion de temor ante un peligro imaginario.",
        "Sensacion de incertidumbre sin objeto especifico.",
        "Sensacion de tristeza ante una perdida."
    ],
    163: [
        "Estado emocional placentero, de certidumbre y calma.",
        "Sensacion de temor ante un peligro real identificable.",
        "Reaccion de miedo extremo ante una amenaza inminente."
    ],
    164: [
        "Miedo leve o preocupacion como respuesta a incertidumbre.",
        "Tristeza profunda o desesperanza ante una perdida.",
        "Ansiedad moderada o inquietud sin causa especifica."
    ],
    165: [
        "Tendencia a la calma e hiposensibilidad a los estimulos externos.",
        "Tendencia a la tristeza e indiferencia ante el entorno.",
        "Tendencia al miedo y evitacion de estimulos amenazantes."
    ],
    166: [
        "Presencia de euforia como emocion principal durante un tiempo, que mejora la cotidianidad.",
        "Presencia de ansiedad como emocion principal durante un tiempo, que altera el sueno.",
        "Presencia de irritabilidad como emocion principal durante un tiempo, que afecta relaciones."
    ],
    167: [
        "Hipersensibilidad y exceso de afecto.",
        "Labilidad y cambios bruscos de afecto.",
        "Euforia y bienestar exagerado."
    ],
    168: [
        "Estabilidad constante en el estado de animo.",
        "Ausencia total de expresion emocional.",
        "Incapacidad de experimentar placer."
    ],
    169: [
        "Aumento o exceso de expresion emocional.",
        "Cambios bruscos en el estado de animo.",
        "Incapacidad de experimentar placer."
    ],
    170: [
        "Capacidad aumentada de experimentar placer.",
        "Cambios bruscos en el estado de animo.",
        "Ausencia de expresion emocional externa."
    ],

    # ===== PSICOMOTOR =====
    171: [
        "Movimientos subitos y aislados en alguna parte del cuerpo.",
        "Movimientos lentos y sostenidos de contraccion muscular.",
        "Movimientos repetitivos sin proposito aparente."
    ],
    172: [
        "Movimientos ritmicos y oscilatorios continuos.",
        "Movimientos lentos de contraccion muscular sostenida.",
        "Movimientos repetitivos sin proposito en extremidades."
    ],
    173: [
        "Movimientos ritmicos y oscilatorios continuos.",
        "Movimientos breves y espasmódicos en cara y cuello.",
        "Movimientos lentos de contraccion sostenida."
    ],
    174: [
        "Capacidad aumentada para permanecer sentado o de pie.",
        "Incapacidad para iniciar el movimiento voluntario.",
        "Movimientos involuntarios ritmicos en reposo."
    ],
    175: [
        "Movimientos ritmicos y oscilatorios sin dolor.",
        "Movimientos breves y espasmódicos sin contraccion.",
        "Movimientos subitos y breves en extremidades."
    ],
    176: [
        "Exceso de voluntad para ejecutar actos.",
        "Ejecucion infrenable de actos sin control.",
        "Deseo irresistible de repetir rituales."
    ],
    177: [
        "Presencia o ausencia, respectivamente, de movimientos involuntarios.",
        "Velocidad o lentitud, respectivamente, del pensamiento.",
        "Exceso o ausencia, respectivamente, de expresion emocional."
    ],
    178: [
        "Ausencia completa de movimiento voluntario.",
        "Deseo irresistible que lleva a repetir rituales.",
        "Resistencia a toda sugerencia externa."
    ],
    179: [
        "Ejecucion infrenable de actos unicos sin control.",
        "Falta total de voluntad para ejecutar actos.",
        "Movimientos repetidos sin proposito aparente."
    ],
    180: [
        "Movimientos unicos y variados.",
        "Resistencia a toda sugerencia.",
        "Ejecucion infrenable de actos."
    ],
    181: [
        "Aceptacion de toda sugerencia.",
        "Movimientos repetidos sin proposito.",
        "Ejecucion infrenable de actos."
    ],
    183: [
        "Aumento o disminucion, respectivamente, de la voluntad.",
        "Presencia o ausencia, respectivamente, de temblor.",
        "Exceso o falta, respectivamente, de atencion."
    ],
    184: [
        "Movimiento con control voluntario adecuado.",
        "Ausencia total de movimiento voluntario.",
        "Movimientos lentos y disminuidos."
    ],
    185: [
        "Temblor.",
        "Distonia.",
        "Abulia."
    ],
    186: [
        "Agitacion psicomotora.",
        "Hiperquinesia aislada.",
        "Sindrome maniaco."
    ],

    # ===== INTELIGENCIA =====
    187: [
        "Capacidad de recordar informacion almacenada previamente.",
        "Capacidad de mantener la atencion sobre un estimulo.",
        "Capacidad de percibir y procesar estimulos sensoriales."
    ],
    189: [
        "Mejoria progresiva de las funciones cognoscitivas.",
        "Estabilidad de las funciones cognoscitivas.",
        "Deficit congenito de las funciones cognoscitivas."
    ],
    190: [
        "Mayor a 120.",
        "Mayor a 100.",
        "Mayor a 160."
    ],
    191: [
        "140 - 160.",
        "90 - 110.",
        "80 - 100."
    ],
    192: [
        "70 - 90.",
        "110 - 130.",
        "80 - 100."
    ],
    193: [
        "Menor a 70.",
        "Menor a 110.",
        "Menor a 80."
    ],
    195: [
        "140 o mas.",
        "120 o mas.",
        "110 o mas."
    ],
    196: [
        "80-89.",
        "60-69.",
        "90-99."
    ],
    197: [
        "120-129.",
        "100-109.",
        "90-99."
    ],

    # ===== JUICIO =====
    198: [
        "Capacidad de almacenar y evocar informacion del pasado.",
        "Capacidad de mantener la atencion sobre un estimulo.",
        "Capacidad de percibir e interpretar estimulos sensoriales."
    ],
    199: [
        "Comparacion simple de dos ideas sin obtener conocimiento nuevo.",
        "Capacidad de mantener la atencion durante un tiempo prolongado.",
        "Habilidad de percibir estimulos del ambiente externo."
    ],
    200: [
        "Capacidad de proyectarse mentalmente hacia el futuro.",
        "Capacidad de observar y evaluar conductas externas.",
        "Capacidad de reconocer la propia enfermedad."
    ],
    201: [
        "Capacidad de examinar y reflexionar sobre pensamientos propios.",
        "Capacidad de recordar eventos pasados con precision.",
        "Capacidad de mantener la atencion sobre estimulos actuales."
    ],
    202: [
        "Desconocimiento por parte del paciente de que padece un trastorno. Su presencia es tipica en trastornos de ansiedad.",
        "Reconocimiento excesivo de sintomas que no existen. Su presencia es tipica en hipocondria.",
        "Capacidad de proyectarse hacia el futuro. Su ausencia afecta la planificacion."
    ],
    203: [
        "Exceso del conocimiento de la realidad interna o externa.",
        "Capacidad normal de evaluar la realidad.",
        "Distorsion severa de la evaluacion de la realidad."
    ],
    204: [
        "Mejoria de la capacidad critica de la realidad.",
        "Capacidad normal de evaluar la realidad.",
        "Deficit leve del conocimiento de la realidad."
    ],
    205: [
        "Perdida total de la capacidad critica de la realidad.",
        "Distorsion severa de la evaluacion critica.",
        "Capacidad normal de evaluar la realidad."
    ],
    206: [
        "Evaluacion normal y adecuada de la realidad.",
        "Deficit leve del conocimiento de la realidad.",
        "Perdida de la capacidad critica sin distorsion."
    ],

    # ===== CALCULO =====
    207: [
        "La capacidad de recordar numeros y cantidades.",
        "La capacidad de leer y escribir numeros.",
        "La capacidad de orientarse en tiempo y espacio."
    ],
    208: [
        "Incapacidad total para realizar operaciones matematicas.",
        "Capacidad normal para resolver operaciones matematicas.",
        "Habilidad aumentada para el calculo mental."
    ],
    209: [
        "Dificultad leve para resolver operaciones matematicas.",
        "Capacidad normal para realizar calculos.",
        "Habilidad superior para las matematicas."
    ],
}


def main():
    init_db()
    conn = get_connection()
    cursor = conn.cursor()

    # Limpiar distractores existentes
    cursor.execute("DELETE FROM distractors")

    inserted = 0
    for card_id, distractors in DISTRACTORES.items():
        for i, distractor in enumerate(distractors):
            normalized = normalize_spanish_text(distractor)
            cursor.execute("""
                INSERT INTO distractors (card_id, distractor_text, posicion)
                VALUES (?, ?, ?)
            """, (card_id, normalized, i + 1))
            inserted += 1

    conn.commit()
    conn.close()

    print(f"Distractores insertados: {inserted}")
    print(f"Tarjetas con distractores: {len(DISTRACTORES)}")


if __name__ == "__main__":
    main()
