# Python Imports
# Third-Party Imports
# Project Imports


def only_if_audio_engine_defined(wrapped_function):
    def function_handler(_widget, audio_engine, *_args, **_kwargs):
        if audio_engine is not None:
            return wrapped_function(_widget, audio_engine, *_args, **_kwargs)
    return function_handler
