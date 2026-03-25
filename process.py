class Process:
    """Representa un proceso del sistema."""

    def __init__(self, label, burst_time, arrival_time, queue, priority):
        self.label = label
        self.burst_time = burst_time
        self.arrival_time = arrival_time
        self.queue = queue
        self.priority = priority

        # Estado de ejecucion
        self.remaining_time = burst_time
        self.started = False

        # Metricas (se calculan al finalizar)
        self.completion_time = 0
        self.response_time = 0
        self.waiting_time = 0
        self.turnaround_time = 0

    def finish(self, time):
        """Marca el proceso como completado y calcula metricas."""
        self.completion_time = time
        self.turnaround_time = time - self.arrival_time
        self.waiting_time = self.turnaround_time - self.burst_time

    def __repr__(self):
        return f"Process({self.label}, BT={self.burst_time}, AT={self.arrival_time})"
