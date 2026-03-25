class SchedulingQueue:
    """Cola de planificacion con una politica especifica (RR, SJF, STCF)."""

    def __init__(self, level, policy, quantum=None):
        self.level = level
        self.policy = policy      # "RR", "SJF", "STCF"
        self.quantum = quantum
        self.ready = []
        # Proceso suspendido por preempcion de cola superior
        self.suspended = None
        self.suspended_quantum = 0

    def add(self, process):
        """Agrega un proceso a la cola de listos."""
        self.ready.append(process)

    def has_work(self):
        """Retorna True si hay procesos pendientes."""
        return bool(self.ready) or self.suspended is not None

    def suspend(self, process, quantum_used):
        """Suspende el proceso actual (preemptado por cola superior)."""
        if self.policy == "STCF":
            # STCF es preemptivo: se re-evalua al reanudar
            self.ready.append(process)
        else:
            # RR y SJF: reanudan el mismo proceso
            self.suspended = process
            self.suspended_quantum = quantum_used

    def get_next(self):
        """Selecciona el siguiente proceso segun la politica.
        Retorna (proceso, quantum_usado)."""
        # Reanudar proceso suspendido (RR, SJF)
        if self.suspended:
            p = self.suspended
            qu = self.suspended_quantum
            self.suspended = None
            return p, qu

        if not self.ready:
            return None, 0

        # Ordenar segun politica
        if self.policy == "SJF":
            self.ready.sort(key=lambda p: (p.remaining_time, -p.priority))
        elif self.policy == "STCF":
            self.ready.sort(key=lambda p: (p.remaining_time, -p.priority))
        # RR: FIFO (sin reordenar)

        return self.ready.pop(0), 0