from subprocess import Popen, PIPE

class Plugin:
    def __init__(self, name:str, paramenters:str, description:str) -> None:
        self.name = name
        self.description = description
        pars = paramenters.split(':')
        self.command = pars[0].split(' ')
        if self.command[-1] == '':
            del self.command[-1]

        self.parameters = pars[1].split(' ')
        if self.parameters[-1] == '':
            del self.parameters[-1]

    def __call__(self, args: list[str]) -> str:
        n_args = len(args)
        n_pars = len(self.parameters)
        if n_args != n_pars:
            return f'ERROR: expected {len(self.parameters)} arguments but got {len(args)} parameters'
        command = []
        for i in range(n_args):
            if self.parameters[i][0] == '-':
                command.append(self.parameters[i])
            command.append(args[i])
        command = self.command + command
        process = Popen(command, stdout=PIPE, stderr=PIPE, text=True)
        out, err = process.communicate()
        if err != "":
            return err
        return out

    def __str__(self) -> str:
        pars = '  '.join(self.parameters) if len(self.parameters) > 0 else '(None)'
        return self.description + '.usage = \n\t' + self.name + ': ' + pars
