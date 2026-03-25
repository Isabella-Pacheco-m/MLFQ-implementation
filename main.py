import sys
from parser import parse_input
from mlfq import MLFQ
from metrics import write_output


def main():
    if len(sys.argv) < 3:
        print("Uso: python main.py <archivo_entrada> <esquema (1-3)>")
        print("\nEsquemas disponibles:")
        print("  1 -> RR(1), RR(3), RR(4), SJF")
        print("  2 -> RR(2), RR(3), RR(4), STCF")
        print("  3 -> RR(3), RR(5), RR(6), RR(20)")
        sys.exit(1)

    input_file = sys.argv[1]
    scheme_num = int(sys.argv[2])

    if scheme_num not in (1, 2, 3):
        print("Error: el esquema debe ser 1, 2 o 3.")
        sys.exit(1)


    processes = parse_input(input_file)

    scheduler = MLFQ(scheme_num)
    scheduler.run(processes)

    output_path = write_output(input_file, processes, scheme_num)
    print(f"Resultado guardado en: {output_path}")


if __name__ == "__main__":
    main()
