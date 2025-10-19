#!/usr/bin/env python3
# tradutor_mt_final_v2.py
# Tradutor I <-> S garantindo completude determinística e compatibilidade com simulador Sipser

import sys

# Constantes
BLANK = '_'
LIMIT_MARKER = 'M'
WILDCARD = '*'
SYMBOLS_BASE = ['0', '1', BLANK]
Q_OLD_START = 'Q_ORIGINAL_0'

# Controle de nomes de estados
estado_counter = 1
estado_map = {}

def get_estado_name(original_name):
    """Mapeia nomes de estados antigos para 'estadoX' de forma consistente."""
    global estado_counter, estado_map
    if original_name == '0':
        return '0'
    if original_name not in estado_map:
        estado_map[original_name] = f"estado{estado_counter}"
        estado_counter += 1
    return estado_map[original_name]

def parse_line(line):
    """Divide linha em partes válidas."""
    parts = line.strip().split()
    return parts if len(parts) == 5 else None

def get_unique_elements(program_lines_raw):
    """Identifica todos os estados e símbolos do programa original."""
    states = set()
    symbols = set(SYMBOLS_BASE)
    for line in program_lines_raw:
        parts = parse_line(line)
        if not parts:
            continue
        q_in, s_in, s_out, d_in, q_out = parts
        states.add(q_in)
        states.add(q_out)
        if s_in != WILDCARD:
            symbols.add(s_in)
        if s_out != WILDCARD:
            symbols.add(s_out)
    states.discard('0')
    states.add(Q_OLD_START)
    return states, symbols

def translate_i_to_s(program_lines_raw, all_states, all_symbols):
    """Traduz máquina de fita duplamente infinita (I) para formato Sipser (S)."""
    translated = []
    translated.append(';S')
    translated.append(';I (Duplamente Infinita) -> S (Sipser) - Simulação Determinística')
    translated.append(';Entrada esperada: sequência de 0s e 1s (sem marcador M)')

    simbolos_trabalho = sorted(list(all_symbols))
    simbolos_simulados = sorted(list(all_symbols.union({LIMIT_MARKER})))

    # Regras originais
    original_rules = {}
    for line in program_lines_raw:
        parts = parse_line(line)
        if not parts:
            continue
        q_in, s_in, s_out, d_in, q_out = parts
        if q_in == '0':
            q_in = Q_OLD_START
        if q_out == '0':
            q_out = Q_OLD_START
        original_rules[(q_in, s_in)] = (s_out, d_in, q_out)

    # 1) Estado inicial 0 -> escreve M e vai para Q_ORIGINAL_0_R
    q_start_sim = f"{Q_OLD_START}_R"
    q_start_sim_mapped = get_estado_name(q_start_sim)
    for s in simbolos_trabalho:
        translated.append(f"0 {s} {LIMIT_MARKER} R {q_start_sim_mapped}")

    # 2) Traduzir regras originais
    for (q_in, s_in), (s_out, d_in, q_out) in original_rules.items():
        q_in_R = get_estado_name(f"{q_in}_R")
        q_in_L = get_estado_name(f"{q_in}_L")

        if q_out.lower().startswith('halt_accept'):
            q_out_R = q_out_L = 'halt_accept'
        elif q_out.lower().startswith('halt_reject'):
            q_out_R = q_out_L = 'halt_reject'
        else:
            q_out_R = get_estado_name(f"{q_out}_R")
            q_out_L = get_estado_name(f"{q_out}_L")

        s_out_real = s_out if s_out != WILDCARD else s_in

        # Criação determinística das transições
        if d_in == 'R':
            translated.append(f"{q_in_R} {s_in} {s_out_real} R {q_out_R}")
            translated.append(f"{q_in_L} {s_in} {s_out_real} L {q_out_L}")
        elif d_in == 'L':
            translated.append(f"{q_in_R} {s_in} {s_out_real} L {q_out_R}")
            translated.append(f"{q_in_L} {s_in} {s_out_real} R {q_out_L}")
        else:  # parada (*)
            translated.append(f"{q_in_R} {s_in} {s_out_real} * {q_out_R}")
            translated.append(f"{q_in_L} {s_in} {s_out_real} * {q_out_L}")

    # 3) Completude determinística
    all_symbols_full = SYMBOLS_BASE + [LIMIT_MARKER]
    existentes = set()
    for ln in translated:
        if ln.startswith(';'):
            continue
        parts = ln.split()
        if len(parts) >= 2:
            existentes.add((parts[0], parts[1]))

    # Determinar todos os estados conhecidos
    estados_conhecidos = set()
    for ln in translated:
        if ln.startswith(';'):
            continue
        parts = ln.split()
        if len(parts) == 5:
            estados_conhecidos.add(parts[0])
            estados_conhecidos.add(parts[4])

    # Adicionar regras faltantes
    for estado in sorted(estados_conhecidos):
        if estado in ('halt_accept', 'halt_reject', '0'):
            continue
        for s in all_symbols_full:
            if (estado, s) not in existentes:
                translated.append(f"{estado} {s} {s} * halt_reject")

    # 4) Estados finais auto-absorventes
    translated.append("halt_accept * * * halt_accept")
    translated.append("halt_reject * * * halt_reject")

    # 5) Remover duplicatas mantendo a ordem
    seen = set()
    final_lines = []
    for ln in translated:
        if ln not in seen:
            seen.add(ln)
            final_lines.append(ln)

    return final_lines

def translate_s_to_i(program_lines):
    """Tradução S -> I (identidade simples)."""
    return [';I', ';S (Sipser) -> I (Duplamente Infinita) - Tradução Identidade'] + program_lines

def translator(input_file, output_file):
    """Lê arquivo .in e gera .out traduzido."""
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = [l.strip() for l in f if l.strip()]
    except FileNotFoundError:
        print(f"[ERRO] Arquivo não encontrado: {input_file}")
        sys.exit(1)

    if not lines or not lines[0].startswith(';'):
        print("[ERRO] Formato inválido: primeira linha deve ser ;I ou ;S")
        sys.exit(1)

    mode = lines[0][1].upper()
    program = [l for l in lines[1:] if not l.startswith(';')]

    all_states, all_symbols = get_unique_elements(program)

    if mode == 'I':
        out_lines = translate_i_to_s(program, all_states, all_symbols)
    elif mode == 'S':
        out_lines = translate_s_to_i(program)
    else:
        print(f"[ERRO] Modelo desconhecido: {mode}")
        sys.exit(1)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(out_lines) + '\n')

    print(f"[OK] Gerado: {output_file} ({len(out_lines)} linhas)")

if __name__ == "__main__":
    in_file = sys.argv[1] if len(sys.argv) > 1 else 'codigo.in'
    out_file = sys.argv[2] if len(sys.argv) > 2 else in_file.replace('.in', '.out')
    translator(in_file, out_file)
