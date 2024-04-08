#SMC

Is a easy **server-machine-communication**.

Just hover over the linux service or any other **server.py** file to keep the server active.

After starting the server, you will get an encryption key "**key**", this should be placed on all clients that will communicate with the server.
Pay attention to the secure transmission of this key.

Also, for convenience, make changes directly to the file **server_functions.py** in python, so that the server can handle your data from clients.

Remember that the client only sends requests, but in any other case, if you add some code, the client can process the server's responses.

Also before starting the server, you need to create a configuration file "options_server", in which you must be sure to put the following parameters:

    host = 127.0.0.1
    port = 20001

And then save the changes.

Great, you can start the server and handle client requests.