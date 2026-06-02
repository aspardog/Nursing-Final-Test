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

    # ===== URGENCIAS: ARRITMIAS DX (IDs 210-222) =====
    210: [
        "Fibrilacion auricular.",
        "Taquicardia supraventricular paroxistica.",
        "Bloqueo AV de segundo grado."
    ],
    211: [
        "Ritmo irregular, onda P visible (normal) y QRS ancho.",
        "Ritmo irregular, onda P no visible (sustituida por ondas f) y QRS angosto.",
        "Ritmo regular, onda P picuda y QRS angosto con intervalo PR corto."
    ],
    212: [
        "Flutter auricular.",
        "Taquicardia sinusal.",
        "Bloqueo AV de primer grado."
    ],
    213: [
        "El flutter tiene ondas f (fibrilatorias); la fibrilacion auricular tiene ondas F en serrucho.",
        "Ambas tienen ritmo regular; se diferencian por la frecuencia auricular.",
        "El flutter tiene QRS ancho; la fibrilacion auricular tiene QRS angosto."
    ],
    214: [
        "Bloqueo AV de segundo grado Mobitz I.",
        "Bloqueo AV de tercer grado.",
        "Bradicardia sinusal."
    ],
    215: [
        "P-R <0,12 s (acortado y variable); algunas P no conducen a QRS.",
        "P-R normal (0,12-0,20 s); todas las P conducen a QRS.",
        "P-R variable; el intervalo se alarga progresivamente antes de una P bloqueada."
    ],
    216: [
        "Bloqueo AV de primer grado.",
        "Bloqueo AV de tercer grado.",
        "Bloqueo AV de segundo grado Mobitz II."
    ],
    217: [
        "Bloqueo AV de primer grado.",
        "Bloqueo AV de segundo grado Mobitz I (Wenckebach).",
        "Bloqueo AV de tercer grado."
    ],
    218: [
        "Mobitz I: el P-R permanece constante y la P se bloquea de forma subita. Mobitz II: el P-R se alarga progresivamente antes de la P bloqueada.",
        "Mobitz I: tiene disociacion AV completa. Mobitz II: tiene P-R prolongado y constante.",
        "Mobitz I y Mobitz II son sinonimos para el mismo tipo de bloqueo."
    ],
    219: [
        "Taquicardia ventricular monomorfica.",
        "Flutter ventricular.",
        "Taquicardia supraventricular con aberrancia."
    ],
    220: [
        "Generalmente con pulso; manejo: cardioversion.",
        "Generalmente sin pulso; manejo: atropina.",
        "Siempre con pulso; manejo: adenosina."
    ],
    221: [
        "Fibrilacion ventricular.",
        "Taquicardia ventricular polimorfica.",
        "Flutter auricular con conduccion aberrante."
    ],
    222: [
        "Con pulso: desfibrilar. Sin pulso: cardioversion.",
        "Con pulso: adenosina. Sin pulso: amiodarona.",
        "Con pulso: atropina. Sin pulso: adrenalina."
    ],

    # ===== URGENCIAS: ARRITMIAS MANEJO (IDs 223-231) =====
    223: [
        "Amiodarona, bolo de 150 mg en 100 cc de DAD.",
        "Atropina, bolo de 1 mg en 10 cc de SSN.",
        "Metoprolol, bolo de 5 mg en 20 cc de SSN."
    ],
    224: [
        "6 mg, seguida de 10 cc de SSN.",
        "18 mg, seguida de 20 cc de SSN.",
        "24 mg, seguida de 30 cc de SSN."
    ],
    225: [
        "Amiodarona en bolo de 150 mg, maximo 450 mg.",
        "Adenosina en bolos de 12 mg, maximo 36 mg.",
        "Atropina en bolos de 0,5 mg, maximo 3 mg."
    ],
    226: [
        "Carga de 300-600 mg, diluir y pasar en 10 min; infusion de 0,5 mg/min.",
        "Carga de 50-100 mg, diluir y pasar en 5 min; infusion de 2 mg/min.",
        "Carga de 75-150 mg, diluir y pasar en 30 min; infusion de 0,25 mg/min."
    ],
    227: [
        "Adenosina.",
        "Desfibrilacion.",
        "Amiodarona."
    ],
    228: [
        "Adenosina, bolo de 6 mg cada 1-2 min, maximo 18 mg.",
        "Adrenalina, bolo de 0,5 mg cada 3-5 min, maximo 2 mg.",
        "Amiodarona, bolo de 150 mg cada 10 min, maximo 450 mg."
    ],
    229: [
        "2-5 mcg/kg/min, ajustar segun el estado del paciente.",
        "5-10 mcg/kg/min, dosis fija sin ajuste.",
        "0,5-1 mcg/kg/min, ajustar segun la frecuencia cardiaca."
    ],
    230: [
        "1 mcg/min, ajustar segun el estado del paciente.",
        "5 mcg/min, dosis fija sin ajuste.",
        "0,1 mcg/min, ajustar segun la presion arterial."
    ],
    231: [
        "Bloqueo AV de primer grado, bradicardia sinusal y ritmo de escape auricular.",
        "Bloqueo AV de segundo grado Mobitz I, taquicardia sinusal y ritmo auricular ectopico.",
        "Fibrilacion auricular lenta, flutter auricular y taquicardia auricular multifocal."
    ],

    # ===== URGENCIAS: IAM (IDs 232-240) =====
    232: [
        "Onda Q patologica.",
        "Descenso del segmento ST.",
        "Onda P picuda."
    ],
    233: [
        "Onda T simetrica (invertida y simetrica).",
        "Descenso del segmento ST.",
        "Onda Q patologica."
    ],
    234: [
        "Ascenso (elevacion) del segmento ST.",
        "Onda T simetrica invertida.",
        "Ensanchamiento del QRS."
    ],
    235: [
        "Derivaciones V1-V4; arteria circunfleja izquierda.",
        "Derivaciones DI, aVL; arteria coronaria derecha.",
        "Derivaciones V5-V6; arteria descendente posterior."
    ],
    236: [
        "DII, DIII y aVF; arteria circunfleja izquierda.",
        "V1-V4; arteria coronaria derecha.",
        "DI, aVL; arteria descendente anterior izquierda."
    ],
    237: [
        "V1-V2; arteria coronaria derecha.",
        "DII, DIII, aVF; arteria circunfleja izquierda.",
        "V5-V6; arteria marginal obtusa."
    ],
    238: [
        "V1-V3; arteria circunfleja izquierda y rama marginal.",
        "DII, DIII, aVF; arteria descendente anterior izquierda.",
        "aVL-DI; arteria coronaria derecha."
    ],
    239: [
        "V3-V4; arteria descendente posterior y rama septal.",
        "DII, DIII, aVF; arteria descendente anterior izquierda.",
        "V1-V2; arteria coronaria derecha."
    ],
    240: [
        "Trombolizar dentro de la ventana (12-24 h), siempre que la TA sea <200/120.",
        "Angioplastia primaria sin importar la TA ni el tiempo de evolucion.",
        "Anticoagulacion con heparina, sin limite de TA ni de tiempo."
    ],

    # ===== URGENCIAS: ACV (IDs 241-247) =====
    241: [
        "6 horas.",
        "12 horas.",
        "1 hora."
    ],
    242: [
        "Activar el codigo ACV, glucometria, oxigenoterapia, resonancia magnetica y valoracion cardiologica.",
        "Trombolizar inmediatamente, glucometria, acceso IV y observacion.",
        "TAC de craneo, puncion lumbar, oxigenoterapia y valoracion neurologica."
    ],
    243: [
        "Anticoagular (dentro de la ventana de tiempo).",
        "Observacion y manejo conservador.",
        "Cirugia de emergencia."
    ],
    244: [
        "Trombolizar con rtPA y luego observacion.",
        "Anticoagulacion sistemica y rehabilitacion temprana.",
        "Craniectomia descompresiva de urgencia."
    ],
    245: [
        "TA <200/120 para trombolizar; si se superan esas cifras, administrar metoprolol.",
        "TA <160/100 para trombolizar; si se superan esas cifras, administrar enalapril.",
        "TA <140/90 para trombolizar; si se superan esas cifras, administrar amlodipino."
    ],
    246: [
        "1,5 mg/kg.",
        "0,6 mg/kg.",
        "0,3 mg/kg."
    ],
    247: [
        "20% de la dosis total en bolo y el 80% restante en infusion durante 30 minutos.",
        "5% de la dosis total en bolo y el 95% restante en infusion durante 2 horas.",
        "50% de la dosis total en bolo y el 50% restante en infusion durante 30 minutos."
    ],

    # ===== URGENCIAS: METABOLICAS (IDs 248-261) =====
    248: [
        "Diabetes tipo 2.",
        "Diabetes gestacional.",
        "Prediabetes."
    ],
    249: [
        "Diabetes tipo 1.",
        "Diabetes gestacional.",
        "Diabetes tipo MODY."
    ],
    250: [
        "100-200 mg/dl.",
        "600-800 mg/dl.",
        "<100 mg/dl."
    ],
    251: [
        "250-600 mg/dl.",
        "<200 mg/dl.",
        "100-250 mg/dl."
    ],
    252: [
        "Cuerpos cetonicos ausentes o leves.",
        "Cuerpos cetonicos + (ligeramente elevados).",
        "Cuerpos cetonicos negativos."
    ],
    253: [
        "Cuerpos cetonicos +++ (marcadamente elevados).",
        "Cuerpos cetonicos moderados (++).",
        "Cuerpos cetonicos ausentes."
    ],
    254: [
        "pH >7,35 y HCO3 >22 mEq/l (alcalosis metabolica).",
        "pH normal (7,35-7,45) y HCO3 normal (22-26 mEq/l).",
        "pH <7,25 y HCO3 <10 mEq/l (acidosis metabolica severa)."
    ],
    255: [
        "Anion GAP <8.",
        "Anion GAP normal (8-12).",
        "Anion GAP negativo."
    ],
    256: [
        "Hiperosmolaridad <280 mOsm/kg.",
        "Osmolaridad normal (280-295 mOsm/kg).",
        "Hipoosmolaridad <260 mOsm/kg."
    ],
    257: [
        "Hipoventilacion con retencion de CO2 (respiracion de Cheyne-Stokes).",
        "Respiracion normal sin alteraciones del patron.",
        "Bradipnea con periodos de apnea (respiracion de Biot)."
    ],
    258: [
        "Hiperactividad motora y agitacion psicomotriz.",
        "Respiracion de Kussmaul con acidosis.",
        "Deshidratacion leve sin compromiso neurologico."
    ],
    259: [
        "Exceso de insulina → hipoglicemia → aumento de la glucogenolisis → hiperglicemia de rebote → diuresis osmotica.",
        "Resistencia a la insulina → hiperglicemia leve → glucosuria → deshidratacion moderada → cetogenesis minima.",
        "Deficit de glucagon → disminucion de la gluconeogenesis → hipoglicemia → liberacion de cortisol → hiperglicemia."
    ],
    260: [
        "Hipoglicemia severa → disminucion de la osmolaridad → edema cerebral → convulsiones.",
        "Cetoacidosis → acumulacion de cetonas → acidosis metabolica → coma diabetico.",
        "Deficit de insulina → lipogenesis aumentada → acumulacion de trigliceridos → esteatosis hepatica."
    ],
    261: [
        "CAD: cetonas ausentes sin acidosis. EH: cuerpos cetonicos +++ con acidosis severa (pH <7,1).",
        "CAD y EH son sinonimos; ambos tienen cetonas elevadas y acidosis similar.",
        "CAD: hiperosmolaridad >350 mOsm/kg. EH: osmolaridad normal con cetonas elevadas."
    ],

    # ===== SALAS DE CIRUGIA: CALCULOS (IDs 262-275) =====
    262: [
        "Se multiplica la cantidad total por el volumen: 500 mcg x 10 ml = 5000 mcg/ml.",
        "Se resta la cantidad total del volumen: 500 mcg - 10 ml = 490 mcg/ml.",
        "Se suma la cantidad total al volumen: 500 mcg + 10 ml = 510 mcg/ml."
    ],
    263: [
        "200 mcg x 50 mcg/cc = 10000 cc.",
        "200 mcg + 50 mcg/cc = 250 cc.",
        "50 mcg/cc / 200 mcg = 0,25 cc."
    ],
    264: [
        "X% = X miligramos por cada 100 ml. Ej.: 100% = 100 mg/100 ml.",
        "X% = X microgramos por cada 1000 ml. Ej.: 100% = 100 mcg/1000 ml.",
        "X% = X gramos por cada 10 ml. Ej.: 100% = 100 g/10 ml."
    ],
    265: [
        "Induccion 0,2 mcg/kg/min; mantenimiento 0,4 mcg/kg/min.",
        "Induccion 1,0 mcg/kg/min; mantenimiento 0,5 mcg/kg/min.",
        "Induccion 0,1 mcg/kg/min; mantenimiento 0,1 mcg/kg/min."
    ],
    266: [
        "cc/h = (dosis x peso x cc totales) / mcg totales = (0,4 x 66 x 100) / 2000 = 1,32 cc/h.",
        "cc/h = (dosis + 60 + peso) x cc totales / mcg totales = (0,4 + 60 + 66) x 100 / 2000 = 6,32 cc/h.",
        "cc/h = dosis x peso / (60 x mcg totales) = 0,4 x 66 / (60 x 2000) = 0,00022 cc/h."
    ],
    267: [
        "cc/h = (0,4 x 90 x 100) / 2000 = 1,8 cc/h.",
        "cc/h = (0,4 + 60 + 90) x 100 / 2000 = 7,52 cc/h.",
        "cc/h = (0,4 x 60 x 90) / (100 x 2000) = 0,0108 cc/h."
    ],
    268: [
        "50 mg x 10 mg/cc = 500 cc.",
        "50 mg + 10 mg/cc = 60 cc.",
        "10 mg/cc / 50 mg = 0,2 cc."
    ],
    269: [
        "40 mg x 10 mg/cc = 400 cc.",
        "40 mg + 10 mg/cc = 50 cc.",
        "10 mg/cc / 40 mg = 0,25 cc."
    ],
    270: [
        "3 ampollas de neostigmina + 2 ampollas de atropina.",
        "10 ampollas de neostigmina + 1 ampolla de glicopirrolato.",
        "2 ampollas de sugammadex + 1 ampolla de atropina."
    ],
    271: [
        "Ondansetron 8 mg, neostigmina 5 mg, etomidato 20 mg, propofol 200 mg y rocuronio 40 mg.",
        "Ondansetron 2 mg, neostigmina 1,25 mg, etomidato 5 mg, propofol 50 mg y rocuronio 10 mg.",
        "Ondansetron 16 mg, neostigmina 10 mg, etomidato 40 mg, propofol 400 mg y rocuronio 80 mg."
    ],
    272: [
        "General, regional, local y sedacion consciente.",
        "Topica, infiltrativa, troncular y raquidea.",
        "Inhalatoria, intravenosa, intramuscular y subcutanea."
    ],

    # ===== SALAS DE CIRUGIA: HERIDAS (IDs 273-279) =====
    273: [
        "Apertura de viscera hueca controlada, sin proceso inflamatorio, tecnica aseptica perfecta. ISO 3-11%.",
        "Apertura no controlada de viscera con derrame, proceso inflamatorio, mala tecnica. ISO 10-17%.",
        "Contaminacion fecal, proceso inflamatorio severo, perdida de vitalidad tisular. ISO >27%."
    ],
    274: [
        "No hay apertura de viscera hueca, sin proceso inflamatorio, tecnica aseptica perfecta. ISO 1-5%.",
        "Apertura controlada de viscera hueca con minimo derrame. ISO 5-10%.",
        "Transgresion mayor de la tecnica con contaminacion. ISO 15-20%."
    ],
    275: [
        "Apertura controlada de viscera hueca, sin proceso inflamatorio, tecnica perfecta. ISO 1-5%.",
        "No hay apertura de viscera hueca, proceso inflamatorio leve. ISO 5-8%.",
        "Contaminacion fecal minima, proceso inflamatorio moderado. ISO 15-20%."
    ],
    276: [
        "Apertura controlada de viscera hueca sin derrame de contenido y sin proceso inflamatorio. ISO 1-5%.",
        "No hay apertura de viscera, proceso inflamatorio presente, tecnica aseptica imperfecta. ISO 5-10%.",
        "Contaminacion fecal, proceso inflamatorio severo, perdida de vitalidad tisular. ISO >27%."
    ],
    277: [
        "La tipo I abre viscera hueca de forma controlada; la tipo II NO abre viscera hueca.",
        "La tipo I y la tipo II son sinonimos que describen heridas sin apertura de viscera.",
        "La tipo I tiene contaminacion fecal; la tipo II tiene apertura controlada de viscera."
    ],
    278: [
        "Contaminada (10-17%) < Limpia contaminada (3-11%) < Limpia (1-5%) < Sucia (>27%).",
        "Sucia (>27%) < Contaminada (10-17%) < Limpia (1-5%) < Limpia contaminada (3-11%).",
        "Limpia contaminada (3-11%) < Limpia (1-5%) < Sucia (>27%) < Contaminada (10-17%)."
    ],

    # ===== SALAS DE CIRUGIA: ASA (IDs 279-284) =====
    279: [
        "Paciente con enfermedad sistemica leve sin limitacion funcional: hipertension controlada.",
        "Paciente con enfermedad cronica compensada: diabetes sin complicaciones.",
        "Paciente moribundo que no se espera sobreviva a la cirugia."
    ],
    280: [
        "Paciente normal sano: no fumador, sin consumo de alcohol.",
        "Enfermedad sistemica severa con limitacion funcional sustancial.",
        "Paciente moribundo con ruptura de aneurisma."
    ],
    281: [
        "Enfermedad sistemica moderada con limitacion funcional moderada.",
        "Paciente normal sano sin limitacion funcional.",
        "Enfermedad sistemica severa que amenaza la vida."
    ],
    282: [
        "Enfermedad sistemica severa con limitacion funcional sustancial.",
        "Enfermedad sistemica moderada con limitacion funcional moderada.",
        "Paciente moribundo que no se espera sobreviva a la cirugia."
    ],
    283: [
        "Enfermedad sistemica severa que amenaza la vida: IAM reciente, sepsis.",
        "Paciente moribundo con ruptura de aneurisma y sangrado masivo.",
        "Paciente con muerte cerebral cuyos organos seran removidos para donacion."
    ],
    284: [
        "Paciente moribundo en quien no se espera que sobreviva a la cirugia.",
        "Paciente con enfermedad sistemica severa que amenaza la vida.",
        "Paciente con enfermedad sistemica severa con limitacion funcional sustancial."
    ],

    # ===== SALAS DE CIRUGIA: VALORACION (IDs 285-290) =====
    285: [
        "Paciente solo, sin tomar signos vitales, con accesorios y esmalte, sin consentimientos.",
        "Paciente con acompanante, sin signos vitales, con protesis, sin ayuno ni lavado.",
        "Solo valoracion por anestesiologia, sin verificar ayuno ni consentimientos."
    ],
    286: [
        "30 minutos antes de la cirugia: ampicilina/sulbactam 3 g o vancomicina 1 g.",
        "2 horas antes de la cirugia: metronidazol 500 mg o ciprofloxacino 400 mg.",
        "Inmediatamente antes de la incision: penicilina G 4 millones UI."
    ],
    287: [
        "Parada de seguridad en silencio, no llenar el tablero, profilaxis antibiotica durante cirugia.",
        "Solo anotar los insumos, sin parada de seguridad ni profilaxis.",
        "Profilaxis antibiotica 2 h despues de la cirugia, sin parada de seguridad."
    ],
    288: [
        "Escala de Glasgow, tolerancia al ejercicio, patron urinario y monitorizacion de glucosa.",
        "Escala de Ramsay, tolerancia a liquidos, patron intestinal y monitorizacion de temperatura.",
        "Escala de Norton, tolerancia al decubito, patron respiratorio y monitorizacion de presion."
    ],
    289: [
        "Temperatura, frecuencia respiratoria, dolor, nauseas y estado de la piel.",
        "Presion arterial, frecuencia cardiaca, nivel de glucosa, diuresis y estado mental.",
        "Motilidad intestinal, tolerancia oral, dolor abdominal, fiebre y herida quirurgica."
    ],
    290: [
        "Vision, audicion, olfato, gusto y sensibilidad tactil.",
        "Temperatura, dolor, presion, equilibrio y coordinacion.",
        "Memoria, orientacion, lenguaje, calculo y juicio."
    ],

    # ===== SALAS DE CIRUGIA: VIA AEREA Y AREAS (IDs 291-295) =====
    291: [
        "Para valorar el nivel de sedacion del paciente en recuperacion postanestesica.",
        "Para evaluar el riesgo de broncoaspiracion durante la induccion.",
        "Para determinar la dosis de relajante muscular necesaria."
    ],
    292: [
        "Segunda zona de restriccion; incluye la sala de operaciones. Se accede con uniforme esteril.",
        "Zona sin restriccion; incluye cafeteria y salas de espera. Se accede con ropa de calle.",
        "Tercera zona de restriccion; incluye la central de esterilizacion. Solo personal autorizado."
    ],
    293: [
        "Requiere portar bata clinica. Incluye la sala de operaciones, central de esterilizacion y oficinas.",
        "No requiere uniforme especial. Incluye vestidores, banos y area de admision quirurgica.",
        "Requiere portar gorro y tapabocas. Incluye sala de recuperacion y cuarto de anestesia."
    ],
    294: [
        "Area de restriccion intermedia donde se encuentran los vestidores y admision quirurgica.",
        "Area de menor restriccion que funciona como zona de transito para visitantes.",
        "Area de alta restriccion donde se realiza la esterilizacion de instrumentos."
    ],
    295: [
        "Blanca (menor restriccion, zona de transito) → Gris (restriccion media) → Negra (mayor restriccion, sala de operaciones).",
        "Gris (menor restriccion, admision) → Negra (restriccion media) → Blanca (mayor restriccion, sala de operaciones).",
        "Negra (menor restriccion, vestidores) → Blanca (restriccion media) → Gris (mayor restriccion, sala de operaciones)."
    ],

    # ===== ARRITMIAS: TAQUICARDIAS SUPRAVENTRICULARES (IDs 296-309) =====
    296: [
        "Patologica; FC 60-100 lpm; QRS ancho; ausencia de onda P; conducta: cardioversion.",
        "Anormal; FC 150-200 lpm; QRS angosto; onda P invertida; conducta: adenosina.",
        "Compensatoria; FC 40-60 lpm; QRS normal; onda P ausente; conducta: marcapasos."
    ],
    297: [
        "La taquicardia sinusal muestra solo 1 montana entre R-R. La supraventricular muestra 2 montanas.",
        "La taquicardia sinusal tiene QRS ancho. La supraventricular tiene QRS angosto.",
        "La taquicardia sinusal no tiene onda P. La supraventricular si tiene onda P."
    ],
    298: [
        "Ritmo irregular; presenta onda P invertida; muestra 2 montanas entre R-R.",
        "Ritmo regular; presenta onda P normal; muestra ondas f entre R-R.",
        "Ritmo irregular; ausencia de onda P; muestra ondas F en serrucho."
    ],
    299: [
        "Ritmo regular; QRS ancho; FC 60-100 lpm; se evidencia onda P; presenta ondas F.",
        "Ritmo irregular; QRS estrecho; FC 100-150 lpm; no se evidencia onda P; presenta ondas delta.",
        "Ritmo regular; QRS angosto; FC 300-400 lpm; se evidencia onda P invertida; sin ondas f."
    ],
    300: [
        "Siempre es regular; presenta onda P normal.",
        "Siempre es irregular; presenta ondas f (fibrilatorias).",
        "Siempre es regular; presenta onda T invertida."
    ],
    301: [
        "Se origina en el nodo sinusal; la onda P es positiva y aparece antes del QRS.",
        "Se origina en el haz de His; no hay onda P visible en el trazado.",
        "Se origina en las fibras de Purkinje; la onda P es bifasica."
    ],
    302: [
        "Taquicardia sinusal (sin P, con ondas f), bradicardia sinusal (ondas F en serrucho) y ritmo nodal (P normal).",
        "TSV (P normal), fibrilacion auricular (P invertida), flutter (sin ondas F) y taquicardia nodal (P visible).",
        "Solo la fibrilacion auricular no muestra onda P normal; las demas si la tienen."
    ],
    303: [
        "La taquicardia sinusal. La TSV, la fibrilacion auricular y el flutter son regulares.",
        "El flutter auricular. La taquicardia sinusal, la TSV y la nodal son irregulares.",
        "La taquicardia nodal. Las demas taquicardias supraventriculares son regulares."
    ],

    # ===== ARRITMIAS: TAQUICARDIAS VENTRICULARES (IDs 304-308) =====
    304: [
        "Se presenta onda P; FC 60-100 lpm; QRS angosto (<0,12 s).",
        "Se presenta onda P invertida; FC 100-150 lpm; QRS normal.",
        "No hay onda P ni QRS identificables; el ritmo es caotico."
    ],
    305: [
        "Monomorfica: la forma de los complejos varia. Polimorfica: todos los complejos tienen la misma forma.",
        "Monomorfica: ocurre con pulso. Polimorfica: siempre es sin pulso.",
        "No hay diferencia visual; se diferencian solo por la frecuencia cardiaca."
    ],
    306: [
        "Es un ritmo regular; se evidencia claramente el complejo QRS ancho.",
        "Es un ritmo irregular pero organizado; el QRS es angosto.",
        "Es un ritmo lento; el QRS es normal con ondas P visibles."
    ],
    307: [
        "Onda ancha/gruesa = fibrilacion ventricular de mayor tiempo. Onda delgada/fina = fibrilacion reciente.",
        "No hay diferencia; ambas representan el mismo estado de la fibrilacion.",
        "Onda ancha = paciente con buen pronostico. Onda fina = paciente con mal pronostico."
    ],

    # ===== ARRITMIAS: BRADIARRITMIAS Y BLOQUEOS (IDs 308-312) =====
    308: [
        "Patologica; FC 30-40 lpm; QRS ancho; ausencia de onda P.",
        "Respuesta a taquiarritmia; FC 100-120 lpm; QRS angosto; onda P presente.",
        "Respuesta a hipoxia; FC 70-80 lpm; QRS normal; onda P bifasica."
    ],
    309: [
        "Segmento PR acortado: mide menos de 3 mm o <0,12 s; ritmo irregular.",
        "Segmento PR normal: mide entre 3-5 mm o 0,12-0,20 s; ritmo regular.",
        "Segmento PR ausente: no se identifica la onda P; ritmo regular."
    ],
    310: [
        "El PR se mantiene constante y una onda P no conduce de forma subita.",
        "El PR se acorta progresivamente hasta que todas las P conducen.",
        "El PR es normal y todas las ondas P conducen sin interrupcion."
    ],
    311: [
        "El PR mide mas de 0,20 s (prolongado y constante); todas las ondas P conducen.",
        "El PR se alarga progresivamente antes de una P bloqueada.",
        "El PR es variable y las ondas P tienen diferentes morfologias."
    ],
    312: [
        "Auriculas y ventriculos estan sincronizados; su conduccion electrica es coherente (asociacion AV).",
        "Las auriculas laten mas rapido que los ventriculos pero estan coordinados.",
        "Solo los ventriculos laten; las auriculas estan en asistolia completa."
    ],

    # ===== MEZCLAS Y DILUCIONES (IDs 313-326) =====
    313: [
        "La dosis mas alta del rango.",
        "El promedio del rango.",
        "La dosis intermedia del rango."
    ],
    314: [
        "1,5 g = 1500 mg x 4 ml = 6000 mg/ml.",
        "1,5 g = 1500 mg + 4 ml = 1504 mg/ml.",
        "1,5 g = 150 mg / 4 ml = 37,5 mg/ml."
    ],
    315: [
        "750 mg x 375 mg/ml = 281250 ml.",
        "750 mg + 375 mg/ml = 1125 ml.",
        "375 mg/ml / 750 mg = 0,5 ml."
    ],
    316: [
        "Solo alteplasa/rtPA (la PA de 165/120 no supera el limite de 180/110).",
        "Solo labetalol (la trombolisis esta contraindicada en ACV isquemico).",
        "Nitroglicerina y aspirina (el ACV isquemico se maneja como un IAM)."
    ],
    317: [
        "Triage I (resucitacion): requiere atencion inmediata por riesgo vital inminente.",
        "Triage III (urgente): requiere atencion en los proximos 30-60 minutos.",
        "Triage IV (menos urgente): puede esperar hasta 2 horas para ser atendido."
    ],
    318: [
        "Total = 0,9 x 95 = 85,5 mg. Bolo (20%) = 17,1 mg en 2 min. Infusion (80%) = 68,4 mg en 2 h.",
        "Total = 1,5 x 95 = 142,5 mg. Bolo (5%) = 7,1 mg en 30 s. Infusion (95%) = 135,4 mg en 30 min.",
        "Total = 0,6 x 95 = 57 mg. Bolo (50%) = 28,5 mg en 5 min. Infusion (50%) = 28,5 mg en 3 h."
    ],
    319: [
        "85,5 mg x 1 mg/ml = 85,5 ml en 30 min ≈ 171 ml/h.",
        "76,95 mg + 1 mg/ml = 77,95 ml en 2 h ≈ 39 ml/h.",
        "76,95 mg / 2 mg/ml = 38,5 ml en 1 h ≈ 38,5 ml/h."
    ],
    320: [
        "Diluir 250 mg de labetalol en SSN hasta completar 250 ml → concentracion 1 mg/ml.",
        "Diluir 1000 mg de labetalol en SSN hasta completar 100 ml → concentracion 10 mg/ml.",
        "Diluir 100 mg de labetalol en SSN hasta completar 500 ml → concentracion 0,2 mg/ml."
    ],
    321: [
        "Concentracion = 3 mg/100 ml = 3 mcg/ml. Dosis = 5 x 68 = 340 mcg/h. ml/h = 340 / 3 = 113,3 ml/h.",
        "Concentracion = 3 mg/100 ml = 300 mcg/ml. Dosis = 5 x 68 = 340 mcg/h. ml/h = 340 / 300 = 1,13 ml/h.",
        "Concentracion = 3 mg/100 ml = 0,3 mcg/ml. Dosis = 5 x 68 = 340 mcg/h. ml/h = 340 / 0,3 = 1133 ml/h."
    ],
    322: [
        "3 mg / 0,5 mg = 6 ampollas (6 x 10 ml = 60 ml) + 100 ml de SSN para completar 160 ml.",
        "3 mg x 0,5 mg = 1,5 ampollas (15 ml) + 85 ml de SSN para completar 100 ml.",
        "3 mg + 0,5 mg = 3,5 ampollas (35 ml) + 65 ml de SSN para completar 100 ml."
    ],
    323: [
        "Concentracion = 2 g/100 ml = 200 mg/ml. Dosis = 0,4 x 76 = 30,4 mg/h. ml/h = 30,4 / 200 = 0,152 ml/h.",
        "Concentracion = 2 g/100 ml = 2 mg/ml. Dosis = 0,4 x 76 = 30,4 mg/h. ml/h = 30,4 / 2 = 15,2 ml/h.",
        "Concentracion = 2 g/100 ml = 0,2 mg/ml. Dosis = 0,4 x 76 = 30,4 mg/h. ml/h = 30,4 / 0,2 = 152 ml/h."
    ],
    324: [
        "2000 mg / 500 mg = 4 ampollas (4 x 10 ml = 40 ml) + 100 ml de SSN para completar 140 ml.",
        "2000 mg x 500 mg = 1000000, usar 2 ampollas + 80 ml de SSN.",
        "2000 mg + 500 mg = 2500 mg, usar 5 ampollas + 50 ml de SSN."
    ],
    325: [
        "Concentracion = 50 mg/500 ml = 1 mg/ml = 1000 mcg/ml. Dosis = 0,5 x 83 = 41,5 mcg/min. ml/h = 41,5 x 60 / 1000 = 2,49 ml/h.",
        "Concentracion = 50 mg/500 ml = 0,01 mg/ml = 10 mcg/ml. Dosis = 0,5 x 83 = 41,5 mcg/min. ml/h = 41,5 x 60 / 10 = 249 ml/h.",
        "Concentracion = 50 mg/500 ml = 10 mg/ml = 10000 mcg/ml. Dosis = 0,5 x 83 = 41,5 mcg/min. ml/h = 41,5 x 60 / 10000 = 0,249 ml/h."
    ],
    326: [
        "50 mg / 50 mg = 1 ampolla (10 ml) + SSN hasta completar 100 ml.",
        "50 mg x 50 mg = 2500, usar 50 ampollas + DAD 5%.",
        "50 mg + 50 mg = 100 mg, usar 2 ampollas + DAD 5% hasta completar 1000 ml."
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
