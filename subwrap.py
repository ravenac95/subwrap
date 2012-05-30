"""
subwrap - A thin layer on top of subprocess
===========================================

This is a very simple tool to call subprocesses. It assumes you want output. It
does not at this time do anything with stdin. This is not that kind of tool. It
was simply meant to be a facility to make calls to subprocess just a bit easier
to use and test.

If you'd like something with higher aspirations please check out envoy!

Simple example::
    
    import subwrap

    response = subwrap.run(['echo', 'hello'])
    
    # Display hello
    print response.std_out

By default subwrap throws a ``CommandError`` if the command being run exits
with an exit code that is not zero. To catch default command errors::

    import subwrap

    try:
        response = subwrap.run(['false'])
    except subwrap.CommandError, e:
        #this is the response, you can do what you want here
        response = e.response
    
However that's not always useful. You can have subwrap run your own custom exit
handle for each subprocess. Just do the following::
        
    import subwrap

    def my_exit_handle(response):
        if response.return_code == 0:
            print "HAPPY DAY!"
        else:
            print "Not as happy"

    # The next line will output "Not as happy" to stdout
    response = subwrap.run(['false'], exit_handle=my_exit_handle)
"""
import subprocess

def run(sub_command, exit_handle=None):
    """Run a command"""
    command = Command(sub_command, exit_handle)
    return command.run()

class CommandError(Exception):
    """Default exception called if command return code is not zero"""
    def __init__(self, response):
        self.response = response
        std_err = response.std_err
        command_std_err = ''
        if std_err:
            command_std_err = ': %s' % std_err
        message = 'Exit code [%d]%s' % (response.return_code, 
                command_std_err)
        super(CommandError, self).__init__(message)

def default_exit_handle(response):
    if response.return_code != 0:
        raise CommandError(response)

class Command(object):
    def __init__(self, command, exit_handle=None):
        self._command = command
        self._exit_handle = exit_handle or default_exit_handle

    def run(self):
        process = subprocess.Popen(self._command, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
        std_out, std_err = process.communicate()
        response = Response(self._command, std_out, std_err, process.returncode)
        self._exit_handle(response)
        return response
        
class Response(object):
    """Command response"""
    def __init__(self, command, std_out, std_err, return_code):
        self._command = command
        self.std_out = std_out
        self.std_err = std_err
        self.return_code = return_code

    def __repr__(self):
        return '<Response %r>' % self._command
