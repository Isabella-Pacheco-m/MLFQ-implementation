import os

NUM_QUEUES = 4

def _fmt(value):
    """Formatea un numero eliminando decimales innecesarios."""
    return f"{value:g}"


def write_output(filepath, processes, scheme_num):
    """Genera el archivo de salida con metricas por proceso y promedios."""
    basename = os.path.basename(filepath)
    output_path = os.path.join("outputs", f"output_{basename}")

    n = len(processes)
    avg_wt  = sum(p.waiting_time     for p in processes) / n
    avg_ct  = sum(p.completion_time  for p in processes) / n
    avg_rt  = sum(p.response_time    for p in processes) / n
    avg_tat = sum(p.turnaround_time  for p in processes) / n

    with open(output_path, "w") as f:
        f.write("# etiqueta; BT; AT; Q; Pr; WT; CT; RT; TAT\n")

        for p in processes:
            f.write(
                f"{p.label};{p.burst_time}; {p.arrival_time}; {p.queue}; "
                f"{p.priority}; {p.waiting_time}; {p.completion_time}; "
                f"{p.response_time}; {p.turnaround_time}\n"
            )

        f.write(f"\nWT={_fmt(avg_wt)}; CT={_fmt(avg_ct)}; "
                f"RT={_fmt(avg_rt)}; TAT={_fmt(avg_tat)};\n")

    return output_path