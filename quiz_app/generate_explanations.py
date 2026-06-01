"""
Script para agregar explicaciones educativas a todas las tarjetas.
Generado por Claude para complementar el aprendizaje.
"""

import sqlite3

# Diccionario con explicaciones por ID de tarjeta
EXPLICACIONES = {
    # ===== FUNCIONES MENTALES =====
    1: "Las funciones mentales son la base de la evaluacion psiquiatrica. Entender que representan la actividad del SNC ayuda a conceptualizar que cualquier alteracion mental tiene un correlato neurologico, aunque no siempre identificable con estudios actuales.",

    2: "Esta clasificacion permite organizar sistematicamente el examen mental. Las funciones de relacion nos conectan con el entorno, las cognoscitivas procesan informacion, las afectivas manejan emociones, las de sintesis integran todo, y las ejecutivas permiten actuar.",

    3: "Las funciones de relacion son las primeras que se evaluan en el examen mental porque establecen si el paciente puede participar de la entrevista. Un paciente con alteracion de conciencia severa no podra evaluarse en otras areas.",

    4: "Las funciones cognoscitivas son esenciales para el procesamiento de informacion. Su alteracion puede indicar desde trastornos psicoticos (pensamiento) hasta demencias (memoria) o lesiones cerebrales focales (lenguaje, sensopercepcion).",

    5: "Las funciones de sintesis son las mas 'superiores' porque requieren integrar multiples procesos. El juicio y la inteligencia se afectan en demencias, mientras que el calculo puede alterarse en lesiones parietales especificas.",

    # ===== PORTE Y ACTITUD =====
    6: "El porte y actitud es lo primero que observamos, incluso antes de que el paciente hable. Un paciente descuidado puede sugerir depresion, psicosis o demencia. La actitud hacia el entrevistador orienta sobre la alianza terapeutica posible.",

    7: "La discrepancia entre edad cronologica y aparente es clinicamente significativa. Un paciente que aparenta mas edad puede tener desgaste por consumo de sustancias, enfermedad cronica o estres severo. Aparentar menos puede verse en retraso mental.",

    8: "El autocuidado refleja funciones ejecutivas y motivacion. Su deterioro progresivo es frecuente en esquizofrenia y demencias. Un cambio agudo sugiere episodio depresivo mayor o inicio de psicosis.",

    9: "La marcha puede revelar efectos de medicamentos (rigidez por antipsicoticos), intoxicacion (inestable), o estados emocionales (lenta en depresion, acelerada en mania). Es parte del examen neurologico basico.",

    10: "Las facies son una ventana al estado emocional. La 'mascara' inexpresiva puede indicar parkinsonismo o aplanamiento afectivo. Las facies de dolor sin causa aparente pueden sugerir somatizacion.",

    11: "La postura comunica sin palabras. Encorvada sugiere depresion o baja autoestima. Rigida puede indicar ansiedad o catatonia. Recostada puede ser apatia o simulation.",

    12: "Los gestos estereotipados son repetitivos y sin proposito, tipicos de esquizofrenia o autismo. Los exagerados sugieren histrionismo o mania. Los disminuidos aparecen en depresion y parkinsonismo.",

    13: "El tono de voz bajo y monotono sugiere depresion. La voz fuerte y acelerada aparece en mania. La disartria puede indicar intoxicacion, lesion neurologica o efectos de medicamentos.",

    14: "La perplejidad indica que el paciente no comprende lo que le sucede. Es frecuente en estados confusionales agudos, primeros episodios psicoticos y despersonalizacion. El paciente puede preguntar repetidamente donde esta.",

    15: "La actitud distante dificulta la entrevista. En esquizofrenia refleja sintomas negativos. En depresion, anhedonia y aislamiento. En autismo, dificultad innata para la conexion social.",

    16: "La inhibicion sugiere ansiedad social, depresion o trauma reciente. El bajo volumen de voz puede ser un intento de no llamar la atencion, frecuente en pacientes que han sufrido abuso.",

    17: "La actitud altiva puede ser defensa narcisista o grandiosidad maniaca. Algunos pacientes la usan para ocultar inseguridad. Es importante no reaccionar defensivamente como entrevistador.",

    18: "La intrusividad rompe limites fisicos y personales. Aparece en mania, trastornos de personalidad y a veces en demencia frontal donde se pierde el juicio social.",

    19: "La queja constante puede ser depresion ansiosa, somatizacion o busqueda de atencion. Es importante validar el malestar mientras se evalua si hay causa organica.",

    20: "La actitud pueril (infantil) puede verse en retraso mental, regresion por estres severo, o como mecanismo de defensa. En demencias puede indicar deterioro frontal.",

    21: "El paciente demandante genera contratransferencia negativa. Puede tener trastorno de personalidad, dolor no tratado, o ansiedad severa. Establecer limites claros es terapeutico.",

    22: "La hostilidad requiere evaluacion de riesgo inmediato. Puede preceder agresion fisica. Causas incluyen intoxicacion, psicosis paranoide, personalidad antisocial o frustracion extrema.",

    23: "Lo pasivo-agresivo es indirecto: el paciente dice que si pero no colabora. Frustra al equipo de salud. Suele reflejar conflicto con la autoridad o dificultad para expresar enojo.",

    24: "La seduccion puede ser manipulativa o parte de un trastorno de personalidad histrionico. Es importante mantener limites profesionales claros y no responder al contenido seductor.",

    25: "El histrionismo implica dramatizacion excesiva de las emociones. Las expresiones parecen exageradas y poco genuinas. Es caracteristico del trastorno de personalidad histrionico.",

    26: "La actitud alucinatoria se detecta cuando el paciente mira, escucha o responde a estimulos que no existen. Puede reir solo, murmurar o hacer gestos hacia el vacio.",

    27: "La actitud psicotica refleja desconexion con la realidad. El deterioro general sugiere cronicidad. La poca expresion puede ser aplanamiento afectivo o efectos de antipsicoticos.",

    28: "El interes genuino facilita la alianza terapeutica. Los movimientos fluidos y la mirada atenta indican que el paciente esta presente y dispuesto a colaborar.",

    29: "La extraneza sugiere despersonalizacion o desrealizacion. El paciente puede sentirse 'raro' o que el mundo no es real. Es frecuente en ansiedad severa y trauma.",

    30: "La confianza en si mismo puede ser saludable o patologica (grandiosidad). En contexto adecuado refleja buena autoestima. En mania o narcisismo puede ser irrealista.",

    # ===== CONCIENCIA =====
    31: "La conciencia es el 'interruptor maestro' del funcionamiento mental. Sin conciencia adecuada, no pueden evaluarse otras funciones. Es lo primero a determinar en urgencias.",

    32: "La hipervigilia no es simplemente estar despierto, sino hiperreactivo. El paciente salta ante cualquier estimulo. Causas: estimulantes, mania, ansiedad extrema, TEPT con hiperactivacion.",

    33: "La somnolencia se distingue del coma porque el paciente responde a estimulos. Es importante determinar la causa: metabolica, toxica, infecciosa o estructural. Es una urgencia medica.",

    34: "El estupor es mas profundo que la somnolencia. El paciente no responde verbalmente pero puede tener reflejos. Causas organicas y psiquiatricas (estupor catatonico) deben diferenciarse.",

    35: "El coma requiere manejo en UCI. El coma superficial tiene algunos reflejos; el profundo no tiene ninguno. La escala de Glasgow ayuda a cuantificar la profundidad.",

    36: "La obnubilacion combina confusion y somnolencia. El paciente puede parecer borracho. Es frecuente en delirium, intoxicaciones y alteraciones metabolicas.",

    37: "La confusion implica que el paciente no procesa bien la informacion. Hace preguntas repetidas, no retiene respuestas, puede tener falsos reconocimientos. Requiere evaluacion medica.",

    38: "El delirium es una urgencia medica. La causa suele ser organica: infecciones, alteraciones metabolicas, medicamentos, abstinencia. Es fluctuante y empeora de noche (sundowning).",

    39: "La despersonalizacion es aterradora para quien la experimenta. 'Soy yo pero no me siento yo'. Aparece en ansiedad, panico, trauma, y uso de cannabis. Suele ser transitoria.",

    40: "La desrealizacion hace que el mundo parezca irreal, como una pelicula o un sueno. Frecuentemente acompana a la despersonalizacion. Es un mecanismo disociativo ante estres extremo.",

    41: "La dismorfofobia (trastorno dismorfico corporal) causa sufrimiento intenso por defectos imaginarios o minimos. Los pacientes buscan cirugia repetidamente sin satisfaccion. Es un trastorno del espectro obsesivo.",

    42: "La letargia es una alerta de que algo no esta bien. En ancianos puede ser el unico signo de infeccion urinaria o neumonia. Siempre descartar causas organicas primero.",

    43: "El estupor tiene causas organicas (metabolicas, toxicas, estructurales) y psiquiatricas (catatonico, disociativo, depresivo). El estupor catatonico puede responder a benzodiacepinas IV.",

    # ===== ORIENTACION =====
    44: "La orientacion evalua si el paciente sabe quien es, donde esta y cuando es. Es basica para determinar si puede dar consentimiento informado y participar en su tratamiento.",

    45: "Las tres esferas se afectan en orden tipico en demencias: primero tiempo, luego lugar, finalmente persona. La desorientacion en persona es signo de deterioro severo.",

    46: "La desorientacion autopsiquica (no saber quien soy) es rara y grave. Puede verse en demencia avanzada, estados disociativos severos (fuga disociativa) o psicosis profunda.",

    47: "La desorientacion alopsiquica es mas comun. No saber la fecha exacta puede ser normal, pero no saber el mes o el ano sugiere patologia. No saber donde esta indica confusion significativa.",

    48: "La desorientacion global indica compromiso severo. En delirium es fluctuante. En demencia es progresiva. En psicosis puede mejorar con tratamiento antipsicotico.",

    49: "Las preguntas sobre persona evaluan memoria autobiografica e identidad. Un paciente puede saber su nombre pero no su edad o profesion en demencias moderadas.",

    50: "Las preguntas de lugar van de lo especifico (este hospital) a lo general (esta ciudad, este pais). La incapacidad de orientarse en lugares conocidos sugiere deterioro significativo.",

    51: "Las preguntas de tiempo son las mas sensibles. No saber el ano actual es muy significativo. No saber la fecha exacta puede ser normal si el paciente no tiene razon para saberla.",

    # ===== ATENCION =====
    52: "La atencion es prerequisito para la memoria: no podemos recordar lo que no atendimos. Su evaluacion es fundamental antes de atribuir quejas de memoria a otras causas.",

    53: "La orientacion dirige el foco, la focalizacion lo mantiene en un estimulo, y la concentracion permite sostenerlo en el tiempo. Las tres pueden afectarse independientemente.",

    54: "La atencion pasiva evalua que tan distraible es el paciente. Si no noto elementos obvios del consultorio, su atencion espontanea esta comprometida.",

    55: "La atencion activa requiere esfuerzo. Los dias de la semana al reves o restas seriadas de 7 son pruebas clasicas. La incapacidad sugiere delirium, demencia o ansiedad severa.",

    56: "La hiperprosexia parece paradojica: atencion excesiva en algo impide atender a otras cosas. Se ve en obsesiones, ansiedad y a veces en autismo con intereses restringidos.",

    57: "La hipoprosexia es la queja de 'no puedo concentrarme'. Causas comunes: depresion, ansiedad, TDAH, fatiga, efectos de medicamentos. Requiere determinar la etiologia.",

    58: "La aprosexia es la ausencia total de capacidad atencional. Es rara y sugiere compromiso organico severo como delirium grave o demencia avanzada.",

    59: "La distractibilidad es caracteristica del TDAH y la mania. El paciente cambia de tema, no termina tareas, responde a cualquier estimulo del ambiente.",

    60: "Euprosexia significa atencion normal. Es el estado esperado. Su documentacion indica que se evaluo la atencion y estaba intacta.",

    61: "Esta pregunta refuerza el concepto de aprosexia: ausencia total de capacidad para fijar la atencion, lo cual es clinicamente muy significativo.",

    # ===== SUENO =====
    62: "El sueno es vital para la salud mental. Su alteracion puede ser sintoma (depresion, mania) o causa (privacion de sueno precipita mania) de trastornos psiquiatricos.",

    63: "Disomnias son alteraciones en cantidad, calidad o horario del sueno. Incluyen insomnio, hipersomnia, narcolepsia y trastornos del ritmo circadiano.",

    64: "Las parasomnias son conductas anormales durante el sueno. No afectan tanto la cantidad pero si la calidad y pueden ser peligrosas (sonambulismo con lesiones).",

    65: "El insomnio de conciliacion (no poder dormirse) es tipico de ansiedad. El de mantenimiento (despertares) se ve en depresion. El despertar temprano es clasico de depresion mayor.",

    66: "La hipersomnia puede ser sintoma de depresion atipica, apnea del sueno, narcolepsia o efecto de medicamentos. Dormir mucho no siempre es descansar bien.",

    67: "El sonambulismo ocurre en sueno profundo (fases 3-4). El paciente puede realizar actos complejos sin recordarlos. Puede ser peligroso y requiere medidas de seguridad.",

    68: "Los terrores nocturnos son diferentes de las pesadillas: ocurren en sueno profundo, el paciente grita y no recuerda. Las pesadillas son en REM y se recuerdan vividamente.",

    69: "El bruxismo (rechinar dientes) puede causar dano dental y dolor mandibular. Se asocia a estres. El tratamiento incluye ferulas nocturnas y manejo del estres.",

    70: "La jactatio capitis (golpear la cabeza) y la somnilalia (hablar dormido) son parasomnias generalmente benignas, mas comunes en ninos. En adultos pueden indicar estres.",

    71: "La narcolepsia causa ataques de sueno irresistibles, cataplejia (perdida subita del tono muscular con emociones), paralisis del sueno y alucinaciones hipnagogicas. Es un trastorno neurologico tratable.",

    72: "La apnea del sueno causa pausas respiratorias, ronquido, sueno no reparador y somnolencia diurna. Es factor de riesgo cardiovascular. El CPAP es el tratamiento estandar.",

    73: "Las alteraciones del ritmo circadiano incluyen jet lag, trabajo por turnos, y sindrome de fase retrasada (noctambulos extremos). La luz y la melatonina ayudan a reajustar el reloj biologico.",

    74: "Los hipnoticos deben usarse con precaucion por riesgo de dependencia y tolerancia. Las benzodiacepinas de vida corta y los Z-drugs (zolpidem) son opciones, pero la higiene del sueno es fundamental.",

    75: "El insomnio inicial es no poder quedarse dormido dentro de 20-30 minutos. Es muy frustrante y genera ansiedad anticipatoria que empeora el problema ('no voy a poder dormir').",

    76: "El despertar muy temprano (4-5 am) sin poder volver a dormir es clasico de depresion mayor. El paciente rumia pensamientos negativos en esas horas.",

    77: "La hipersomnia diurna requiere descartar apnea del sueno, narcolepsia, depresion y efectos de medicamentos antes de asumir que es solo 'flojera'.",

    78: "La inversion del ritmo (dormir de dia, despierto de noche) puede ser voluntaria (trabajadores nocturnos) o patologica (demencia, psicosis). Afecta el funcionamiento social.",

    # ===== SENSOPERCEPCION =====
    79: "La sensopercepcion es como el cerebro interpreta los estimulos sensoriales. Sus alteraciones van desde distorsiones menores hasta alucinaciones complejas.",

    80: "Las sensaciones exteroceptivas (tacto, temperatura, dolor) nos protegen del ambiente. Las propioceptivas nos ubican en el espacio. Las interoceptivas nos informan del estado interno.",

    81: "La propiocepcion permite cerrar los ojos y tocarse la nariz. Su alteracion causa ataxia. En psiquiatria, los trastornos de la imagen corporal pueden relacionarse con alteraciones propioceptivas.",

    82: "Las sensaciones interoceptivas incluyen hambre, sed, nausea, urgencia urinaria. En trastornos somatoformes, estas sensaciones se interpretan catastroficamente.",

    83: "Las ilusiones son interpretaciones erroneas de estimulos reales. Ver una sombra y pensar que es una persona es una ilusion, no alucinacion. Son comunes en estados de miedo o baja luz.",

    84: "Las alucinaciones auditivas son las mas comunes en esquizofrenia. Las visuales sugieren causa organica (delirium, intoxicacion, demencia con cuerpos de Lewy). Esta distincion es clinicamente importante.",

    85: "Las alucinaciones pueden evaluarse preguntando directamente: 'Algunas personas escuchan voces que otros no oyen, le ha pasado?' La actitud no juiciosa facilita la revelacion.",

    86: "Las distorsiones visuales incluyen cambios en color (cromatopsias), tamano (macro/micropsia) y forma. El LSD causa distorsiones caracteristicas. Las migranas con aura tambien.",

    87: "La agnosia visual es no reconocer objetos vistos (diferentes de no verlos). Indica lesion de corteza de asociacion visual. El paciente puede describir el objeto pero no nombrarlo.",

    88: "Las hiperestesias (aumento de sensibilidad) y las hipoestesias (disminucion) pueden ser organicas o funcionales. En conversion, no siguen patrones anatomicos.",

    89: "La sinestesia es percibir un estimulo en una modalidad como otra (oir colores, ver sonidos). Puede ser congenita o inducida por drogas. No es patologica per se.",

    # ===== ALUCINACIONES =====
    90: "Las alucinaciones auditivas elementales (ruidos) son menos especificas que las complejas (voces). Las voces que comentan o dan ordenes son muy sugestivas de esquizofrenia.",

    91: "Las alucinaciones visuales complejas (personas, animales) sugieren fuertemente causa organica. Las 'zoopsias' (ver insectos, animales pequenos) son clasicas del delirium tremens por abstinencia alcoholica.",

    92: "Las alucinaciones olfativas y gustativas pueden indicar crisis epilepticas del lobulo temporal (auras con olores desagradables) o tumores cerebrales. Requieren evaluacion neurologica.",

    93: "La distincion activa/pasiva en alucinaciones tactiles es importante. Las pasivas ('me tocan') son mas comunes. Las formicaciones (sentir insectos) son clasicas de intoxicacion por cocaina.",

    94: "Las alucinaciones cenestesicas (viscerales) son bizarras: 'tengo un animal en el estomago', 'me queman los organos'. Son muy sugestivas de esquizofrenia.",

    95: "Las alucinaciones cinestesicas afectan la percepcion del movimiento corporal. El paciente puede sentir que se mueve, gira o cae cuando esta quieto. Tambien ocurren en vertigo.",

    # ===== PENSAMIENTO =====
    96: "La forma del pensamiento evalua si sigue reglas logicas. El pensamiento normal tiene identidad (A=A), no contradiccion (A no puede ser no-A) y tercero excluido. El pensamiento psicotico viola estas reglas.",

    97: "El curso incluye velocidad (taquipsiquia/bradipsiquia) y continuidad (bloqueos, tangencialidad). Permite distinguir mania (rapido pero comprensible) de esquizofrenia (disgregado).",

    98: "El contenido son las ideas especificas: obsesiones, delirios, fobias, ideas de muerte. Es lo que el paciente piensa, mientras forma y curso son como lo piensa.",

    99: "El pensamiento se infiere del lenguaje y conducta. No podemos leer la mente, pero si observar sus manifestaciones. Un paciente mutista puede tener pensamiento normal o severamente alterado.",

    100: "El pensamiento magico es normal en ninos pero patologico en adultos cuando interfiere con la realidad. Ejemplos: 'si piso las lineas, algo malo pasara' llevado al extremo.",

    101: "La fuga de ideas es tan rapida que el paciente salta de tema en tema por asociaciones superficiales (rimas, sonidos). Se ve en mania. El discurso es dificil de seguir pero tiene cierta logica.",

    102: "La taquipsiquia es pensamiento acelerado pero coherente. El paciente habla rapido pero se le entiende. Es menos severa que la fuga de ideas.",

    103: "La bradipsiquia (pensamiento lento) es tipica de depresion. El paciente tarda en responder, habla despacio, parece que le cuesta pensar. Tambien aparece en hipotiroidismo.",

    104: "La incoherencia es mas severa que la disgregacion: las frases mismas no tienen sentido gramatical. Se ve en psicosis severas y estados confusionales. Es la 'ensalada de palabras'.",

    105: "La disgregacion mantiene frases correctas pero sin conexion logica entre ellas. El paciente salta de un tema a otro sin relacion aparente. Es caracteristica de esquizofrenia.",

    106: "El bloqueo es una interrupcion subita del pensamiento. El paciente se detiene a mitad de frase y puede decir que 'le robaron la idea'. Muy sugestivo de esquizofrenia.",

    107: "La circunstancialidad eventualmente llega al punto, pero con muchos rodeos innecesarios. Se ve en personalidades obsesivas, epilepsia y algunos cuadros organicos.",

    108: "La tangencialidad nunca llega al punto. Las respuestas estan relacionadas pero no responden la pregunta. El paciente se va por las ramas indefinidamente.",

    109: "Las ideas fijas son intrusivas y molestas. A diferencia de las obsesiones, el paciente puede no reconocerlas como irracionales. Son menos elaboradas que los delirios.",

    110: "Las obsesiones son egodistonicas: el paciente sabe que son irracionales y absurdas pero no puede evitarlas. Causan ansiedad. Son el nucleo del TOC.",

    111: "El delirio es una creencia falsa, fija, que no cambia con evidencia contraria. Tipos comunes: persecutorio (me persiguen), referencial (hablan de mi), grandioso (soy especial), celotipico (me enganan).",

    112: "La hipocondria implica conviccion de enfermedad pese a evaluaciones normales. Genera consultas medicas multiples y ansiedad de salud. Hoy se clasifica como trastorno de ansiedad por enfermedad.",

    113: "Las ideas referenciales hacen que el paciente sienta que todo tiene significado especial dirigido a el: la TV le habla, los desconocidos lo miran, las canciones tienen mensajes para el.",

    114: "La fuga de ideas se distingue de la disgregacion porque tiene asociaciones identificables (aunque superficiales), mientras la disgregacion no tiene conexion logica aparente.",

    115: "El bloqueo del pensamiento a veces se interpreta como 'robo del pensamiento' por el paciente psicotico, quien cree que alguien externo le quita las ideas de la mente.",

    # ===== LENGUAJE =====
    116: "Estas cuatro dimensiones permiten clasificar las afasias. Broca: no fluida, comprension ok, repeticion alterada. Wernicke: fluida, sin comprension, repeticion alterada. Conduccion: todo ok excepto repeticion.",

    117: "La fluidez normal es 100-150 palabras por minuto. Menos de 50 sugiere afasia no fluida. Mas de 150 puede indicar mania o ansiedad. Se evalua con habla espontanea.",

    118: "La comprension se evalua con ordenes de complejidad creciente: 'cierre los ojos', 'senale la ventana', 'con la mano izquierda toque su oreja derecha'. Fallas indican afasia receptiva.",

    119: "La repeticion evalua el fasciculo arcuato. Frases como 'ni si, ni no, ni pero' o 'el flan tiene frutillas y frambuesas' son dificiles de repetir en afasia de conduccion.",

    120: "La denominacion se afecta en casi todas las afasias. Se evalua pidiendo nombrar objetos (reloj, lapiz) y partes (correa, manecillas). La anomia es la dificultad para encontrar palabras.",

    121: "La logorrea es hablar excesivamente, tipica de mania. El paciente no puede parar de hablar, interrumpe, y habla sobre muchos temas. Diferente de la afasia de Wernicke donde hay fluidez pero sin sentido.",

    122: "La bradilalia (habla lenta) puede ser por depresion, parkinsonismo, hipotiroidismo o efectos de medicamentos. Evaluar si el pensamiento tambien es lento (bradipsiquia).",

    123: "La logoclonia (repetir la ultima silaba: 'voy a casa-sa-sa') se ve en demencias, especialmente en etapas avanzadas. Es diferente de la tartamudez.",

    124: "La ecolalia (repetir lo que se le dice) aparece en autismo, catatonia, demencia frontal y afasia transcortical. El paciente repite como eco sin procesar el significado.",

    125: "La coprolalia (decir obscenidades) es clasica del sindrome de Tourette, pero solo aparece en una minoria de casos. Tambien puede verse en demencia frontal por desinhibicion.",

    126: "La dislalia es dificultad articulatoria por causas perifericas (labio leporino, frenillo corto) o del desarrollo. Es diferente de la disartria que tiene causa neurologica central.",

    127: "La disartria indica problema neurologico: lesion de cerebelo, tronco cerebral, nervios craneales o musculos. El habla es arrastrada, como de borracho. Importante en ACV.",

    128: "La tartamudez puede ser del desarrollo (inicia en infancia) o adquirida (por lesion cerebral o trauma emocional). El estres la empeora. Tiene tratamiento fonoaudiologico.",

    129: "La disfonia afecta el tono o calidad de la voz. Puede ser por lesion de cuerdas vocales, paralisis del nervio laringeo o causas funcionales (disfonia psicogena por estres).",

    130: "Las afasias indican lesion cerebral focal. Broca: frontal posterior izquierdo. Wernicke: temporal posterior izquierdo. Su aparicion aguda sugiere ACV y es una urgencia.",

    131: "Los neologismos son palabras inventadas con significado solo para el paciente. En esquizofrenia pueden formar un lenguaje privado incomprensible para otros.",

    132: "La verborrea en este contexto se refiere a palabras sin contenido significativo, diferente de la logorrea que es simplemente hablar mucho. Es mas desorganizada.",

    133: "El mutismo puede ser voluntario (mutismo selectivo por ansiedad), involuntario (catatonia, afasia global) o simulado. La causa determina el tratamiento.",

    134: "La muscitacion es habla muy baja, casi inaudible, como murmurando. Puede indicar que el paciente responde a alucinaciones o esta muy inhibido.",

    135: "El soliloquio (hablar solo) puede ser normal en pequenas cantidades pero si es frecuente y dirigido a algo inexistente, sugiere alucinaciones auditivas.",

    136: "Disgrafia: dificultad para escribir. Agrafia: incapacidad total. Dislexia: dificultad para leer. Alexia: incapacidad para leer. Pueden coexistir o presentarse aisladas.",

    137: "La ecolalia es un signo importante que debe documentarse. Su presencia en un adulto sin historia de autismo sugiere patologia aguda (catatonia, delirium, demencia).",

    138: "La disartria requiere examen neurologico completo. Evaluar nervios craneales, cerebelo y fuerza de musculos orofaringeos. Puede ser el primer signo de ELA o miastenia.",

    # ===== MEMORIA =====
    139: "La memoria tiene fases: codificacion (registrar), almacenamiento (guardar) y recuperacion (recordar). Fallas en cualquier fase causan 'olvido' pero por mecanismos diferentes.",

    140: "Retrograda: no recuerda antes del evento (accidente, enfermedad). Anterograda: no puede formar nuevos recuerdos despues. La anterograda es mas discapacitante funcionalmente.",

    141: "Esta clasificacion temporal es clinicamente util. En Alzheimer se afecta primero la reciente (olvida eventos de hoy) mientras preserva la remota (recuerda su infancia).",

    142: "La amnesia retrograda puede ser por trauma craneal, demencias o causas psicogenas (amnesia disociativa). En TCE suele recuperarse gradualmente de lo lejano a lo cercano al trauma.",

    143: "La amnesia anterograda impide aprender cosas nuevas. El paciente pregunta lo mismo repetidamente. Es clasica del sindrome de Korsakoff (deficiencia de tiamina por alcoholismo).",

    144: "La memoria inmediata o de trabajo se evalua pidiendo repetir una serie de numeros. Lo normal es 7 mas/menos 2 digitos. Es como la RAM del computador.",

    145: "La memoria reciente se evalua preguntando que desayuno, que hizo ayer, noticias recientes. Su alteracion aislada sugiere inicio de demencia o trastorno amnesico.",

    146: "La memoria remota se evalua con eventos historicos (fechas importantes), autobiograficos antiguos (donde nacio, escuelas). Su alteracion indica demencia avanzada.",

    147: "La hipermnesia puede ser una habilidad excepcional (memoria fotografica) o un sintoma (recuerdos intrusivos en TEPT donde el trauma se recuerda con detalle excesivo).",

    148: "La amnesia tiene multiples causas. Descartar causas tratables: deficiencia de tiamina (B1), hipotiroidismo, infecciones del SNC, hidrocefalia normotensiva.",

    149: "La confabulacion es inventar recuerdos para llenar vacios, sin intencion de mentir. El paciente cree lo que dice. Clasica del sindrome de Korsakoff.",

    150: "Los falsos reconocimientos hacen que el paciente crea conocer a desconocidos o lugares nuevos. Pueden causar comportamiento inapropiado con extranos. Aparecen en demencias.",

    151: "El deja vu ocasional es normal. Si es frecuente o prolongado, puede indicar epilepsia del lobulo temporal. Se siente intensamente que esto ya se vivio antes.",

    # ===== AFECTIVIDAD =====
    152: "La afectividad abarca todo el mundo emocional. Su evaluacion incluye observar expresiones, preguntar como se siente, y notar la congruencia entre contenido y expresion emocional.",

    153: "Los sentimientos son mas estables y menos intensos que las emociones. El amor es un sentimiento; el enamoramiento intenso es mas cercano a emocion. Influyen en la personalidad.",

    154: "Las emociones son respuestas rapidas a estimulos. Miedo ante peligro, ira ante frustracion. Son breves pero intensas. Su desregulacion es nucleo de muchos trastornos.",

    155: "El tono afectivo es el humor predominante. Un tono depresivo tine negativamente todas las experiencias. Un tono euforico las tine positivamente. Es el 'fondo' emocional.",

    156: "La euforia patologica en mania es diferente de la alegria normal: es excesiva, no proporcional a la situacion, y se acompana de otros sintomas maniacos.",

    157: "La exaltacion es bienestar aun mas intenso que la euforia. El paciente puede sentirse invencible o con poderes especiales. Sugiere mania severa.",

    158: "El extasis es el extremo: bienestar intensisimo, casi mistico. Se ve en intoxicaciones (MDMA se llama 'extasis'), mania y algunos estados disociativos o religiosos patologicos.",

    159: "La hipomania es 'mania lite': euforia, menos sueno, mas productividad, pero el paciente funciona bien. De hecho, puede ser muy productivo. El problema es que puede escalar a mania.",

    160: "La mania es un sindrome completo: exaltacion, fuga de ideas, aumento psicomotor, poco sueno. Interfiere severamente con el funcionamiento. Puede incluir psicosis.",

    161: "La distincion es crucial: en hipomania el paciente funciona (incluso mejor de lo usual); en mania el paciente esta desorganizado, puede ser psicotico, requiere hospitalizacion.",

    162: "El miedo es adaptativo ante peligro real. Se convierte en patologico (fobia) cuando es excesivo, ante estimulos no peligrosos, y causa evitacion disfuncional.",

    163: "La ansiedad es miedo sin objeto claro, una sensacion difusa de que algo malo pasara. Es el nucleo de los trastornos de ansiedad. Tiene componentes cognitivos, fisicos y conductuales.",

    164: "El panico es terror extremo con sensacion de muerte inminente. Los ataques de panico tienen pico en 10 minutos y sintomas fisicos intensos (taquicardia, disnea, sudoracion).",

    165: "La irritabilidad puede ser sintoma de depresion (especialmente en hombres y adolescentes), mania, abstinencia, o rasgos de personalidad. Es un estado de umbral bajo para el enojo.",

    166: "La depresion como sindrome requiere tristeza persistente mas otros sintomas (sueno, apetito, energia, concentracion, ideacion suicida). Diferente de tristeza normal.",

    167: "La apatia/atimia es ausencia de afecto, indiferencia total. El paciente no esta triste ni feliz, simplemente no siente. Se ve en demencia frontal, esquizofrenia y depresion severa.",

    168: "La labilidad afectiva son cambios rapidos e inesperados de humor. Pasar de risa a llanto en segundos. Se ve en demencia, esclerosis multiple, lesiones frontales.",

    169: "El afecto plano es ausencia de expresion emocional aunque pueda haber sentimientos internos. Cara inexpresiva, voz monotona. Tipico de esquizofrenia (sintoma negativo).",

    170: "La anhedonia es incapacidad de sentir placer. Actividades antes disfrutadas ya no generan nada. Es sintoma cardinal de depresion mayor y predictor de severidad.",

    # ===== PSICOMOTOR =====
    171: "El temblor puede ser de reposo (Parkinson), de accion (esencial, fisiologico) o intencional (cerebeloso). En psiquiatria, es efecto comun de litio y antipsicoticos.",

    172: "Los tics son mas comunes en ninos y suelen mejorar en adultos. El sindrome de Tourette combina tics motores y vocales. El estres los exacerba.",

    173: "Las mioclonias son sacudidas subitas, como el sobresalto al quedarse dormido (mioclonia hipnica, normal). Tambien aparecen en epilepsia, encefalopatias y algunos medicamentos.",

    174: "La acatisia es muy molesta: el paciente no puede quedarse quieto, camina, mueve las piernas. Es efecto de antipsicoticos. Puede confundirse con ansiedad o empeoramiento psicotico.",

    175: "Las distonias son contracciones musculares sostenidas que causan posturas anormales y dolor. La distonia aguda por antipsicoticos (torticolis, crisis oculogiras) es una urgencia tratable con anticolinergicos.",

    176: "La abulia es falta de voluntad para actuar. El paciente puede saber que debe hacer algo pero no logra iniciarlo. Se ve en depresion severa, demencia frontal y lesiones de ganglios basales.",

    177: "La hiperbulia es exceso de voluntad/motivacion, tipica de mania. El paciente inicia multiples proyectos (que no termina). La hipobulia es motivacion disminuida, comun en depresion.",

    178: "Los impulsos son actos sin reflexion previa. Pueden ser autolesivos (cortarse), agresivos (golpear) o de otro tipo (robar, apostar). Son el nucleo de los trastornos del control de impulsos.",

    179: "Las compulsiones son rituales repetitivos para reducir ansiedad de obsesiones. Lavarse las manos (contaminacion), verificar (duda), ordenar (simetria). Son egodistonicas en TOC.",

    180: "Las estereotipias son movimientos repetitivos sin proposito: balanceo, aleteo de manos, golpear. Se ven en autismo, retraso mental, esquizofrenia y demencia.",

    181: "El negativismo es oposicion automatica a toda indicacion. Puede ser pasivo (no hace nada) o activo (hace lo opuesto). Es caracteristico de catatonia.",

    182: "La catatonia es un sindrome, no solo inmovilidad. Incluye estupor, mutismo, posturas, negativismo, ecolalia, ecopraxia, flexibilidad cerea. Puede ser mortal y responde a benzodiacepinas.",

    183: "Hiperquinesia es aumento del movimiento, hipoquinesia es disminucion. En depresion hay hipoquinesia; en mania, hiperquinesia. El parkinsonismo causa hipoquinesia mas rigidez.",

    184: "La agitacion psicomotora es movimiento excesivo, desorganizado, con imposibilidad de control. Es una urgencia psiquiatrica. Causas: mania, psicosis, intoxicacion, delirium.",

    185: "La acatisia por antipsicoticos se trata reduciendo dosis, cambiando de medicamento, o agregando propranolol o benzodiacepinas. No debe confundirse con ansiedad.",

    186: "El sindrome catatonico requiere reconocimiento rapido. La catatonia maligna puede ser fatal. El tratamiento de primera linea son benzodiacepinas IV (lorazepam). La TEC es muy efectiva.",

    # ===== INTELIGENCIA =====
    187: "La inteligencia es adaptacion a situaciones nuevas. Alguien puede tener mucho conocimiento academico pero poca inteligencia practica, y viceversa. Es multidimensional.",

    188: "El deficit cognitivo (antes retraso mental) se clasifica por CI y nivel de funcionamiento. Leve: CI 50-69, pueden ser independientes con apoyo. Profundo: CI <20, requieren cuidado total.",

    189: "El deterioro mental es perdida progresiva de funciones previamente adquiridas. Es el sello de las demencias. Diferente del deficit cognitivo donde nunca se adquirieron.",

    190: "CI >140 es genialidad, aproximadamente 0.1% de la poblacion. Estas personas pueden tener dificultades de adaptacion social por pensar muy diferente a sus pares.",

    191: "CI 120-140 es superior, aproximadamente 5-10% de la poblacion. Suficiente para exito academico alto y profesiones demandantes.",

    192: "CI 90-110 es el promedio, donde cae el 50% de la poblacion. Es lo esperado. Permite funcionamiento normal en la sociedad.",

    193: "CI <90 indica algún grado de dificultad. Es importante determinar si es estable (deficit cognitivo) o si ha disminuido (demencia). La historia es clave.",

    194: "Los rangos de retardo mental ayudan a planificar educacion y servicios. Leve: educable, puede trabajar. Moderado: entrenable, supervision. Severo/profundo: cuidado dependiente.",

    195: "La escala WISC es para ninos. Sus rangos difieren ligeramente de las escalas para adultos (WAIS). Muy superior (130+) sugiere altas capacidades que requieren estimulacion especial.",

    196: "Inteligencia limitrofe (70-79) es zona gris: no califica como deficit cognitivo pero tiene dificultades. Estas personas son vulnerables a explotacion y pueden tener problemas legales.",

    197: "Media alta (110-119) representa personas que rinden bien academicamente pero no son excepcionales. Aproximadamente 15% de la poblacion.",

    # ===== JUICIO =====
    198: "El juicio evalua la capacidad de tomar decisiones apropiadas. Se pregunta: 'Que haria si encuentra una carta sellada en el piso?' o 'Si hay fuego en un cine?'",

    199: "El raciocinio es encadenar juicios para llegar a conclusiones. 'Todos los hombres son mortales, Socrates es hombre, por lo tanto...' Es pensamiento logico formal.",

    200: "La introspeccion es mirarse hacia adentro, examinar propios pensamientos y motivaciones. Es fundamental para la psicoterapia. Su ausencia dificulta el tratamiento.",

    201: "La prospeccion es proyectarse al futuro, planificar, anticipar consecuencias. Esta alterada en mania (no prevé consecuencias de actos) y en lesiones frontales.",

    202: "El insight (conciencia de enfermedad) es crucial. Un psicotico sin insight no tomara medicamentos porque no cree estar enfermo. Mejora con tratamiento.",

    203: "El juicio deficiente implica que las decisiones no son las mejores pero el paciente intenta razonar. Puede verse en intoxicacion leve, demencia incipiente, retraso leve.",

    204: "El juicio suspendido es mas severo: no hay capacidad critica. El paciente no puede evaluar si algo es bueno o malo, real o irreal. Se ve en psicosis activa.",

    205: "El juicio debilitado es alteracion leve y a menudo transitoria, relacionada con estados emocionales intensos (depresion, ansiedad) o condiciones fisicas (fatiga, enfermedad).",

    206: "El juicio desviado es distorsion severa de como se evalua la realidad. Las conclusiones del paciente estan consistentemente erradas. Se ve en paranoia, demencias.",

    # ===== CALCULO =====
    207: "El calculo se evalua con operaciones simples (sumas, restas) y complejas (problemas). La resta seriada de 7 desde 100 (100, 93, 86...) evalua calculo y atencion.",

    208: "La discalculia es dificultad para el calculo, puede ser del desarrollo (como dislexia para numeros) o adquirida por lesion cerebral, tipicamente parietal.",

    209: "La acalculia es incapacidad total para calcular. Indica lesion de corteza parietal izquierda. Puede asociarse a otros signos del sindrome de Gerstmann.",
}

def main():
    conn = sqlite3.connect('data/quiz.db')
    cursor = conn.cursor()

    cursor.execute("PRAGMA table_info(cards)")
    card_columns = {row[1] for row in cursor.fetchall()}
    if "explicacion" not in card_columns:
        cursor.execute("ALTER TABLE cards ADD COLUMN explicacion TEXT")

    updated = 0
    for card_id, explicacion in EXPLICACIONES.items():
        cursor.execute(
            'UPDATE cards SET explicacion = ? WHERE id = ?',
            (explicacion, card_id)
        )
        if cursor.rowcount > 0:
            updated += 1

    conn.commit()
    conn.close()

    print(f'Explicaciones actualizadas: {updated} de {len(EXPLICACIONES)}')

    # Verificar cuantas tarjetas quedan sin explicacion
    conn = sqlite3.connect('data/quiz.db')
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM cards WHERE explicacion IS NULL')
    sin_explicacion = cursor.fetchone()[0]
    print(f'Tarjetas sin explicacion: {sin_explicacion}')
    conn.close()

if __name__ == '__main__':
    main()
