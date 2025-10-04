def catch_exception(exception=Exception, is_async=False):
    def decorator(func):
        if is_async:
            async def async_wrapper(*args, **kwargs):
                try:
                    return await func(*args, **kwargs)
                except exception as e:
                    print(f"Exception {e} caught, don't worry, it's normal :)")

            return async_wrapper
        else:
            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except exception as e:
                    print(f"Exception {e} caught, don't worry, it's normal :)")

        return wrapper

    return decorator


def catch_exception_async(exception=Exception):
    return catch_exception(exception, is_async=True)


def catch_exception_sync(exception=Exception):
    return catch_exception(exception, is_async=False)
