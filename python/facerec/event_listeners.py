# import sample module "hello" to demonstrate 
# event listeners mechanism.
import modules.hello_module as hello_module


def register():

    # register your event listeners here
    return {
        'on_face_unknown': [hello_module.hello_unknown],
        'on_face_appear': [hello_module.hello],
        'on_start': [hello_module.on_start],
        'on_stop': [hello_module.on_stop],
    }
