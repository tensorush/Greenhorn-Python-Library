from timeit import timeit
from functools import wraps
from inspect import signature


def cache_results_decorator(func):
    '''
    Decorates function for caching results.
    '''
    cache = dict()

    @wraps(func)
    def cache_results_wrapper(*args, **kwargs):
        '''
        Wraps specific function signature for caching results.
        '''
        nonlocal cache
        params_hash = hash((*args, *kwargs.items()))
        if params_hash not in cache:
            cache[params_hash] = func(*args, **kwargs)
        return cache[params_hash]

    return cache_results_wrapper


def check_types_decorator_creator(*arg_types, **kwarg_types):
    '''
    Creates decorator for checking function parameter types against provided types.
    '''
    def check_types_decorator(func):
        '''
        Decorates function for checking function parameter types against provided types.
        '''
        func_signature = signature(func)
        bound_args = func_signature.bind_partial(*arg_types, **kwarg_types)

        def check_types(params):
            '''
            Checks function parameter types against provided types.
            '''
            for name, value in params.items():
                if name in bound_args.arguments and type(value) is not bound_args.arguments[name]:
                    raise TypeError(f'Argument {name} must be of type {bound_args.arguments[name]}')

        @wraps(func)
        def check_types_wrapper(*args, **kwargs):
            '''
            Wraps specific function signature for checking function parameter types against provided types.
            '''
            bound_args = func_signature.bind(*args, **kwargs)
            bound_args.apply_defaults()
            check_types(bound_args.arguments)
            return func(*args, **kwargs)

        return check_types_wrapper

    return check_types_decorator


@cache_results_decorator
def test_results_caching(number: int) -> int:
    if number == 0:
        return 0
    elif number == 1:
        return 1
    else:
        return test_results_caching(number - 1) + test_results_caching(number - 2)


@check_types_decorator_creator(bool, int, c=float, d=list)
def test_type_checking(a, b, *, c=13.37, d=list()) -> None:
    d.append(a * b + c)


if __name__ == '__main__':
    print('Test results caching:')
    print('First launch execution time: ')
    print(timeit('test_results_caching(33)', number=1, globals=globals()))
    print('Second launch execution time: ')
    print(timeit('test_results_caching(33)', number=1, globals=globals()))
    print('Done!')

    print('\nTest type checking:')
    test_type_checking(True, 33)
    print('Done!')
