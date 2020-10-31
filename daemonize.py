import os
import sys
import signal
import atexit
def daemonize(pid_file, *, stdin = '/dev/null', stdout = '/dev/null', stderr = '/dev/null'):
    if os.path.exists(pid_file):
        raise RuntimeError('already running.')
    try:
        if os.fork() > 0:
            raise SystemExit(0)
    except OSError as e:
        raise RuntimeError('fork #1 child process error.')
    os.chdir('/')
    os.umask(0)
    os.setsid()
    try:
        if os.fork() > 0:
            raise SystemExit(0)
    except OSError as e:
        raise RuntimeError('fork #2 child process error.')
    sys.stdout.flush()
    sys.stderr.flush()
    with open(stdin, 'rb', 0) as f:
        os.dup2(f.fileno(), sys.stdin.fileno())
    with open(stdout, 'ab', 0) as f:
        os.dup2(f.fileno(), sys.stdout.fileno())
    with open(stderr, 'ab', 0) as f:
        os.dup2(f.fileno(), sys.stderr.fileno())
    with open(pid_file, 'w') as f:
        print(os.getpid(), file = f)
    atexit.register(lambda : os.remove(pid_file))
    def sigterm_handler(signo, frame):
        raise SystemExit(1)
    signal.signal(signal.SIGTERM, sigterm_handler)

