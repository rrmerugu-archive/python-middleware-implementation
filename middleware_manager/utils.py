import importlib


def import_class(cls_string):
    module_name, class_name = cls_string.rsplit(".", 1)
    module = importlib.import_module(module_name)
    cls = getattr(module, class_name)
    if cls is not None:
        return cls
    else:
        raise Exception("{} not Found", cls)


def try_except(func, *args, **kwargs):
    try:
        return func(*args, **kwargs), None
    except Exception as e:
        return None, e
