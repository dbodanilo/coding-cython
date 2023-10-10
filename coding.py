from queue import PriorityQueue


def fano_rec(q: PriorityQueue, cs: dict[str, int]) -> dict[str, int]:
    qsize = q.qsize()
    if (qsize <= 1):
        return cs

    zero = [q.get()]
    zero_cs, zero_bs = zip(*zero)

    one = []
    while not q.empty():
        one.append(q.get())

    one_cs, one_bs = zip(*one)

    # minimize absolute value, not avoid crossing the line.
    while abs(sum(zero_cs) + one_cs[0] - sum(one_cs[1:])) < abs(sum(zero_cs) - sum(one_cs)):
        zero.append(one.pop(0))
        zero_cs, zero_bs = zip(*zero)
        one_cs, one_bs = zip(*one)

    for b in zero_bs:
        cs[b] = cs.get(b, "") + "0"

    for b in one_bs:
        cs[b] = cs.get(b, "") + "1"

    if qsize > 2:
        zero_q = PriorityQueue()
        for z in zero:
            zero_q.put(z)

        one_q = PriorityQueue()
        for o in one:
            one_q.put(o)

        cs = fano_rec(zero_q, cs)
        cs = fano_rec(one_q, cs)

    return cs


def fano(bs: str) -> tuple[dict[str, str], str]:
    counts: dict[str, int] = {}
    for b in bs:
        counts[b] = counts.get(b, 0) + 1

    counts_q = PriorityQueue()
    total = 0
    for b, c in counts.items():
        total += c

        counts_q.put((-c, b))

    codes = {}
    codes = fano_rec(counts_q, codes)

    cs = ""
    for b in bs:
        cs += codes[b]

    return codes, cs


def fixed(bs: str) -> tuple[dict[str, str], str]:
    symbols = set()
    for b in bs:
        symbols.add(b)

    length = len(symbols)
    bin_len = len(f"{length:b}")
    fmt = "{:0LENb}".replace("LEN", str(bin_len))

    codes = {}
    for i, s in enumerate(symbols):
        codes[s] = fmt.format(i)

    encoded = "".join(map(lambda b: codes[b], bs))

    return codes, encoded


def main():
    symbols = "A"*15 + "B"*7 + "C"*6 + "D"*6 + "E"*5
    codes, dest = fano(symbols)

    source = symbols
    for s, c in [("A", "000"), ("B", "001"), ("C", "010"),
                 ("D", "011"), ("E", "100")]:
        source = source.replace(s, c)

    print("symbols:", symbols)
    print("fixed encoding:", source)
    print("codewords:", codes)
    print("encoded:", dest)
    print("len(fixed):", len(source))
    print("len(fano):", len(dest))


if __name__ == "__main__":
    main()
