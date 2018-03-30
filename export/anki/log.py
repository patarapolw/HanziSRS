from datetime import datetime
import yaml
import inspect


class Logger:
    def __init__(self, filename):
        self.filename = filename
        try:
            with open(self.filename) as f:
                self.log = yaml.safe_load(f)
        except FileNotFoundError:
            self.log = dict()

    def dump(self):
        with open(self.filename, 'w') as f:
            yaml.safe_dump(self.log, f, allow_unicode=True)

    def save_var(self, **value):
        self.log[datetime.now()] = {
            self.get_caller(): value
        }
        self.dump()

    def load_var(self, var_name):
        for v1 in self.log.values():
            for k2, v2 in v1.items():
                if k2 == self.get_caller():
                    yield v2[var_name]

    @staticmethod
    def get_caller():
        parent_stack = inspect.stack()[2]
        module_name = parent_stack[3]
        class_name = parent_stack[0].f_locals['self'].__class__.__name__
        return '{}.{}'.format(class_name, module_name)


if __name__ == '__main__':
    print(str(datetime.now()))
