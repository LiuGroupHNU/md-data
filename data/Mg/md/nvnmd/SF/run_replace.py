
import sys


def process(fn, nr, nc, value):
    with open(fn, 'r') as fr:
        lines = fr.readlines()
    line = lines[nr]
    pars = line.split()
    if value is not None:
        pars[nc] = value
        line = " ".join(pars)
        lines[nr] = line
        with open(fn, 'w') as fw:
            fw.writelines(lines)
    else:
        print(pars[nc])

if __name__ == "__main__":
    argvs = sys.argv[1:]
    # print(argvs)
    fn = argvs[0]
    nr = int(argvs[1]) - 1
    nc = int(argvs[2]) - 1
    value = argvs[3] if (len(argvs) == 4) else None
    process(fn, nr, nc, value)


