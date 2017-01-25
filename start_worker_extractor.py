import sys,dva,os

if __name__ == '__main__':
    import dva
    Q_EXTRACTOR = dva.settings.Q_EXTRACTOR
    if len(sys.argv) > 1:
        concurrency = int(sys.argv[1])
    else:
        concurrency = 1
    command = 'celery -A dva worker -l info -c {} -Q {} -n {}.%h -f logs/{}.log'.format(concurrency,Q_EXTRACTOR,Q_EXTRACTOR,Q_EXTRACTOR)
    print command
    os.system(command)
