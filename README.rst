subwrap - A very thin wrapper for subprocesses
==============================================

This is a very thin layer on top of stdlib's subprocess module. It is simply
for some convenient functions that are needed in many of my projects. 

Full documentation could come later but if you really want something that makes
using subprocess much easier I would personally try envoy. However, at this
time envoy seemed a bit too early in it's development to use so I created my
own very thin layer to satisfy my needs for the time being.

If you'd like something with higher aspirations please check out envoy.

Examples
--------

Simple example::
    
    import subwrap

    response = subwrap.run(['echo', 'hello'])
    
    # Display hello
    print response.std_out

By default subwrap throws a ``CommandError`` if the command being run exits with an exit
code that is not zero. To catch default command errors::

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

License
-------

MIT License
