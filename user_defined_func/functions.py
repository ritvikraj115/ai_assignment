

def greet():
    return 'hello'


def get_disk_space():
    import shutil
    def get_disk_space():
        total, used, free = shutil.disk_usage("/")
        return f'Total: {total // (2**30)} GB, Used: {used // (2**30)} GB, Free: {free // (2**30)} GB'
