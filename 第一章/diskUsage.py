import sys
import os
import psutil


class DiskUsage:

    def bytes2human(self, n):
        symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
        prefix = {}
        for index, symbol in enumerate(symbols):
            prefix[symbol] = 1 << (index+1)*10
        for symbol in reversed(symbols):
            if n > prefix[symbol]:
                value = float(n) / prefix[symbol]
                return '%.1f%s' % (value, symbol)
        return '%sB' % n

    def main(self):
        templ = "%-17s %8s %8s %8s %5s%% %9s %s"
        print(templ % ("Device", "Total", "Used", "Free",
            "Use", "Type", "Mount"))
        for part in psutil.disk_partitions(all=False):
            if os.name == 'nt':
                if 'cdrom' in part.opts or part.fstype == '':
                    continue
            usage = psutil.disk_usage(part.mountpoint)
            print(templ % (
                part.device,
                self.bytes2human(usage.total),
                self.bytes2human(usage.used),
                self.bytes2human(usage.free),
                int(usage.percent),
                part.fstype,
                part.mountpoint
                ))
if __name__ == '__main__':
    DiskUsage().main()
