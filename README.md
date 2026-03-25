# MLFQ - Simulador de Planificacion Multi-Level Feedback Queue

## Que es MLFQ

MLFQ (Multi-Level Feedback Queue) es un algoritmo de planificacion de procesos que organiza los procesos en multiples colas con diferentes niveles de prioridad. Cada cola puede usar una politica distinta (Round Robin, SJF, STCF). Las colas de mayor prioridad se ejecutan primero.

El componente de **feedback** es la clave: cuando un proceso agota su quantum en una cola RR, desciende automaticamente a la siguiente cola de menor prioridad. Esto penaliza los procesos CPU-intensivos y favorece los de rafagas cortas, sin necesidad de conocer su comportamiento de antemano.

## Como ejecutar

```bash
python3 main.py <archivo_entrada> <esquema>
```

**Ejemplos:**
```bash
python3 main.py tests/test1.txt 1
python3 main.py tests/test2.txt 2
python3 main.py tests/test3.txt 3
```

El resultado se guarda en `outputs/output_<nombre_archivo>.txt`.

### Esquemas disponibles

| Esquema | Cola 1 | Cola 2 | Cola 3 | Cola 4 |
|---------|--------|--------|--------|--------|
| 1       | RR(1)  | RR(3)  | RR(4)  | SJF    |
| 2       | RR(2)  | RR(3)  | RR(4)  | STCF   |
| 3       | RR(3)  | RR(5)  | RR(6)  | RR(20) |

## Estructura del proyecto

```
MLFQ/
├── main.py          # Punto de entrada
├── process.py       # Clase Process
├── queue.py         # Clase SchedulingQueue
├── mlfq.py          # Clase MLFQ (planificador)
├── parser.py        # Lectura de archivos de entrada
├── metrics.py       # Calculo y escritura de metricas
├── inputs/          # Archivos de entrada
├── outputs/         # Archivos de salida generados
├── tests/           # Casos de prueba
├── README.md
└── guion.md
```

## Explicacion del algoritmo

1. **Llegada**: en cada tick, los procesos que cumplen su `arrival_time` se agregan a su cola inicial asignada, ordenados por prioridad.
2. **Seleccion de cola**: se busca la cola de mayor prioridad (numero menor) que tenga procesos listos.
3. **Preempcion entre colas**: si una cola de mayor prioridad recibe un proceso mientras una inferior esta ejecutando, el proceso inferior se suspende inmediatamente.
4. **Politica interna**: cada cola ejecuta segun su politica:
   - **RR(q)**: Round Robin con quantum `q`. Al expirar el quantum, el proceso **desciende a la siguiente cola** (feedback).
   - **SJF**: Shortest Job First no preemptivo. Ejecuta el proceso con menor `remaining_time`.
   - **STCF**: Shortest Time to Completion First preemptivo. Interrumpe al proceso actual si llega uno con menor tiempo restante.
5. **Degradacion (feedback)**: al agotar el quantum RR, el proceso pasa a `queues[nivel + 1]`. Si ya esta en la ultima cola, se reencola en la misma.
6. **Metricas**: al completarse cada proceso se calculan WT, CT, RT y TAT.

### Metricas

| Metrica | Significado              | Formula                  |
|---------|--------------------------|--------------------------|
| WT      | Waiting Time             | TAT - BT                 |
| CT      | Completion Time          | tick en que termina      |
| RT      | Response Time            | primer tick de CPU - AT  |
| TAT     | Turnaround Time          | CT - AT                  |

Los promedios al final del archivo de salida corresponden a la media aritmetica de cada metrica sobre todos los procesos.

## Formato de entrada

```
# etiqueta; BT; AT; Q; Prioridad
A;6;0;1;5
B;9;0;1;4
C;10;0;2;3
```

- **Etiqueta**: identificador del proceso.
- **BT** (Burst Time): tiempo total de CPU que necesita.
- **AT** (Arrival Time): tick en que llega al sistema.
- **Q** (Queue): cola inicial asignada (1 = mayor prioridad). El proceso puede degradarse a colas inferiores durante la ejecucion.
- **Prioridad**: desempate dentro de la misma cola (5 = mas alta, 1 = mas baja).

## Formato de salida

```
# etiqueta; BT; AT; Q; Pr; WT; CT; RT; TAT
A;6; 0; 1; 5; 24; 30; 0; 30
B;9; 0; 1; 4; 27; 36; 1; 36
...
WT=30.2; CT=39.8; RT=5.2; TAT=39.8;
```

Link video explicativo: https://drive.google.com/drive/folders/1lZwp2gacBkzieAGSW7Uaa0Tiz5scUu0L?usp=sharing
