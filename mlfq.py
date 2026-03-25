from queue import SchedulingQueue

class MLFQ:
    """Planificador Multi-Level Feedback Queue."""

    # Tres esquemas de configuracion
    SCHEMES = {
        1: [("RR", 1), ("RR", 3), ("RR", 4), ("SJF", None)],
        2: [("RR", 2), ("RR", 3), ("RR", 4), ("STCF", None)],
        3: [("RR", 3), ("RR", 5), ("RR", 6), ("RR", 20)],
    }

    def __init__(self, scheme_num):
        scheme = self.SCHEMES[scheme_num]
        self.queues = {}
        for i, (policy, quantum) in enumerate(scheme, 1):
            self.queues[i] = SchedulingQueue(i, policy, quantum)

    def run(self, processes):
        """Ejecuta la simulacion tick a tick."""
        time = 0
        pending = sorted(list(processes), key=lambda p: p.arrival_time)
        total = len(processes)
        completed = 0

        current = None       # proceso en ejecucion
        current_level = None  # cola del proceso actual
        quantum_used = 0

        while completed < total:
            # 1. Agregar procesos que llegan en este tick
            arrived = [p for p in pending if p.arrival_time <= time]
            pending = [p for p in pending if p.arrival_time > time]

            # Ordenar por prioridad (mayor primero) para orden consistente
            arrived.sort(key=lambda p: -p.priority)
            for p in arrived:
                if p.queue in self.queues:
                    self.queues[p.queue].add(p)

            # 2. Preempcion STCF dentro de la misma cola
            if current and arrived and current_level in self.queues:
                q = self.queues[current_level]
                if q.policy == "STCF":
                    current, quantum_used = self._check_stcf_preemption(
                        q, current, quantum_used, time
                    )

            # 3. Buscar cola activa de mayor prioridad
            best_level = self._find_active_level(current, current_level)

            if best_level is None:
                time += 1
                continue

            # 4. Preempcion por cola de mayor prioridad
            if current and current_level != best_level:
                self.queues[current_level].suspend(current, quantum_used)
                current = None
                quantum_used = 0

            q = self.queues[best_level]

            # 5. Verificar si expiro el quantum (RR) → degradar a cola inferior
            if current and q.policy == "RR" and quantum_used >= q.quantum:
                next_level = current_level + 1
                if next_level in self.queues:
                    self.queues[next_level].add(current)
                else:
                    # Ya está en la última cola, se reencola en la misma
                    q.add(current)
                current = None
                quantum_used = 0

            # 6. Seleccionar proceso si no hay uno ejecutando
            if current is None:
                current, quantum_used = q.get_next()
                current_level = best_level
                if current is None:
                    time += 1
                    continue

            # 7. Registrar tiempo de respuesta
            if not current.started:
                current.response_time = time - current.arrival_time
                current.started = True

            # 8. Ejecutar un tick
            current.remaining_time -= 1
            quantum_used += 1
            time += 1

            # 9. Verificar si el proceso termino
            if current.remaining_time == 0:
                current.finish(time)
                completed += 1
                current = None
                quantum_used = 0

    def _find_active_level(self, current, current_level):
        """Encuentra la cola de mayor prioridad con trabajo.
        Si hay un proceso ejecutándose, su cola también cuenta como activa."""
        for level in sorted(self.queues.keys()):
            if self.queues[level].has_work():
                return level
            if current is not None and current_level == level:
                return level
        return None

    def _check_stcf_preemption(self, q, current, quantum_used, time):
        """Verifica si un proceso recien llegado debe preemptar al actual (STCF)."""
        best = None
        for p in q.ready:
            if (p.remaining_time < current.remaining_time or
                (p.remaining_time == current.remaining_time and
                 p.priority > current.priority)):
                if best is None or p.remaining_time < best.remaining_time:
                    best = p

        if best:
            q.ready.remove(best)
            q.ready.append(current)
            if not best.started:
                best.response_time = time - best.arrival_time
                best.started = True
            return best, 0

        return current, quantum_used