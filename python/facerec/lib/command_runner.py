
def list_commands(commands: dict):
    print('Available commands:')
    count = 0
    for name, cmd in commands.items():
        count += 1
        fn, description, usage = _cmd_attributes(commands, name)

        print('{}. {}: {}'.format(count, name, description))
        print('   {}'.format(usage))
        print()

def run(commands: dict, command: str, args: list):
    if command not in commands:
        print('[ERROR] invalid command:', command)
        
        print()
        list_commands(commands)
        exit(1)

    # execute command
    print('executing {} command..'.format(command))
    fn, _, _ = _cmd_attributes(commands, command)
    fn(args)

def _cmd_attributes(commands: dict, command) -> tuple:
    cmd = commands[command]

    fn = getattr(cmd, "command")
    description = getattr(cmd, "description", "(no description has been set)")
    usage = getattr(cmd, "usage", "usage: (not set)")

    return fn, description, usage
