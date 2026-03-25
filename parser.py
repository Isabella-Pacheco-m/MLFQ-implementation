from process import Process


def parse_input(filepath):
    """Lee un archivo de entrada y retorna una lista de procesos."""
    processes = []
    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = [p.strip() for p in line.split(";")]
            processes.append(Process(
                label=parts[0],
                burst_time=int(parts[1]),
                arrival_time=int(parts[2]),
                queue=int(parts[3]),
                priority=int(parts[4]),
            ))
    return processes
