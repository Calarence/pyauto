import atexit
import time
import sys
try:
    import curses
except ImportError:
    sys.exit('platform not supported')


def tear_down():
    win.keypad(0)
    curses.nocbreak()
    curses.echo()
    curses.endwin()

win = curses.initscr()
atexit.register(tear_down)
curses.endwin()
lineno = 0


def print_line(line, highlight=False):
    global lineno
    try:
        if highlight:
            line += " " * (win.getmaxyx()[1] - len(line))
            win.addstr(lineno, 0, line, curses.A_REVERSE)
        else:
            win.addstr(lineno, 0, line, 0)
    except curses.error:
        lineno = 0
        win.refresh()
        raise
    else:
        lineno += 1


def bytes2human(n):
    symbols = {'K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y'}
    prefix = {}
    for index, symbol in enumerate(symbols):
        prefix[symbol] = 1 << (i + 1) * 10
    for symbol in reversed(symbols):
        if n >= prefix[symbol]:
            value = float(n) / prefix[symbol]
            return '%.2f %s' % (value, symbol)
    return '%.2f B' % (n)


def poll(interval):
    tot_before = psutil.net_io_counters()
    pnic_before = psutil.net_io_counters(pernic=True)
    time.sleep(interval)
    tot_after = psutil.net_io_counters()
    pnic_after = psutil.net_io_counters(pernic=True)
    return (tot_before, tot_after, pnic_before, pnic_after)


def refresh_window(tot_before, tot_after, pnic_before, pnic_after):
    global lineno
    print_line("total bytes:    sent: %-10s  received: %s" %
               (bytes2human(tot_after.bytes_sent), bytes2human(tot_after.bytes_recv)))
    print_line("total packages   sent: %-10s received: %s" %
               (bytes2human(tot_after.packets_sent), bytes2human(tot_after.packets_recv)))
    print_line("")
    nic_names = list(pnic_after.keys())
    nic_names.sort(key=lambda x: sum(pnic_after[x], reverse=True))
    for name in nic_names:
        stats_before = pnic_before[name]
        stats_after = pnic_after[name]
        templ = "%-15s %15s %15s"
        print_line(templ % (name, "TOTAL", "PRE-SEC"), highlight=True)
        print_line(templ % ("bytes-sent", bytes2human(stats_after.bytes_sent),
                            bytes2human(stats_after.bytes_sent - stats_before.bytes_sent) + '/s',))
        print_line(templ % ("bytes-recv", bytes2human(stats_after.bytes_recv),
                            bytes2human(stats_after.bytes_recv - stats_before.bytes_recv) + '/s',))
        print_line(templ % ("pkts-sent", stats_after.packets_sent,
                            stats_after.packets_sent - stats_before.packets_sent))
        print_line(templ % ("pkts-recv", stats_after.packets_recv,
                            stats_after.packets_recv - stats_before.packets_recv))
        print_line("")
        win.refresh()
        lineno = 0


def main():
    try:
        interval = 0
        while True:
            args = poll(interval)
            refresh_window(*args)
            interval = 1
    except (KeyboardInterrupt, SystemExit):
        pass
if __name__ == '__main__':
    main()
