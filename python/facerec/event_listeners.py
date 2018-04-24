import modules.hello_module as hello_module


def register():
    """register event listeners"""

    return {
        'on_face_appear': [hello_module.hello],
        'on_start': [hello_module.on_start],
        'on_stop': [hello_module.on_stop],
    }
