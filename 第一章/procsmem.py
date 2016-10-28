import psutil


def bytes2human(n):
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for index, symbol in enumerate(symbols):
        prefix[symbol] = 1 << (index + 1) * 10
    for symbol in reversed(symbols):
        if n >= prefix[symbol]:
            value = float(n) / prefix[symbol]
            return ("%.1f%s" % (value, symbol))
    return "%sB" % n


def print_info():
    for pid in psutil.pids():
        process = psutil.Process(pid)
        USS = bytes2human(process.memory_info()[7])
        PSS = bytes2human(process.memory_info()[8])
        Swap = bytes2human(process.memory_info()[9])
        RSS = bytes2human(process.memory_info()[0])
        print("%s %s %s %s %s %s %s" % (str(pid), process.name(),
                                        process.cmdline(), USS, PSS, Swap, RSS))
if __name__ == '__main__':
    print("pid    name     cmdline    USS     PSS    Swap     RSS")
    print_info()
