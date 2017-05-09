import psutil
import sys
if not (psutil.LINUX or psutil.WINDOWS or psutil.OSX):
    sys.exit("platform not supported")


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


def main():
    ad_pids = []
    procs = []
    for process in psutil.process_iter():
        try:
            memoInfo = process.memory_full_info()
            proInfo = process.as_dict(attrs=["cmdline", "username"])
        except psutil.AccessDenied:
            ad_pids.append(process.pid)
        except psutil.NoSuchProcess:
            pass
        else:
            process._uss = memoInfo.uss
            process._rss = memoInfo.rss
            if not process._uss:
                continue
            """ 
            OSX and windows do not have pss and swap metric
            """
            process._pss = getattr(memoInfo, 'pss', '')
            process._swap = getattr(memoInfo, 'swap', '')
            process._info = proInfo
            procs.append(process)
    procs.sort(key=lambda process: process._uss)
    templ = "%-7s %-7s %-30s %7s %7s %7s %7s"
    print(templ % ("PID", "User", "Cmdline", "USS", "PSS", "Swap", "RSS"))
    print("=" * 78)
    for process in procs:
        line = templ % (
            process.pid,
            process._info["username"][:7],
            " ".join(process._info['cmdline'])[:30],
            bytes2human(process._uss),
            bytes2human(process._pss) if process._pss else "",
            bytes2human(process._swap) if process._swap else "",
            bytes2human(process._rss) if process._rss else ""
        )
        print(line)
    if ad_pids:
        print("Warining: access denied for % pids" % len(ad_pids))

        # USS = bytes2human(process.memory_full_info()[7])
        # PSS = bytes2human(process.memory_full_info()[8])
        # Swap = bytes2human(process.memory_full_info()[9])
        # RSS = bytes2human(process.memory_full_info()[0])
        # print("%s %s %s %s %s %s %s" % (str(pid), process.name(),
        # process.cmdline(), USS, PSS, Swap, RSS))
if __name__ == '__main__':
    sys.exit(main())
