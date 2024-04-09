#SMC

It's - easy **server-machine-communication**.

SMC - is built solely on mutual trust of sources, therefore all data transmitted through tcp-channel are encrypted with **AES-256** algorithm, without a true "**key**" file, which is generated automatically at the first start of the server, all clients that connect to the socket and try to send any data to it - will not be able to cause any harm to your machine.
The server logic is based on a simple principle - if you can't decrypt the received data bytes, you reject the connection.
To start the server correctly, you need to read the recommendations in the **readme file**.

Just hover over the linux service or any other **server.py** file to keep the server active.

After starting the server, you will get an encryption key "**key**", this should be placed on all clients that will communicate with the server.
Pay attention to the secure transmission of this key.

Also, for convenience, make changes directly to the file **server_functions.py** in python, so that the server can handle your data from clients.

Remember that the client only sends requests, but in any other case, if you add some code, the client can process the server's responses.

Also before starting the server, you need to create a configuration file "options_server", in which you must be sure to put the following parameters:

    host = 127.0.0.1
    port = 20001

And then save the changes.

You may not create the **server_options** file, then when you initialize the application **start()** in the **server.py** file, the application itself will create the server settings file.
To change it, open the file as a text file, e.g. with the **nano** utility. By default, the application will create a socket and put it in listening mode at 127.0.0.1 on port 20001.

After modification, do not forget to restart the server.

#
###Service for *unix-systems

If you are on a linux (unix-like) system, you will probably find it useful to create a service to automatically start **server.py** login point.
Below are the basic settings for the service:

    [Unit]
    Description=SMC socket server
    After=network.target
    
    [Service]
    User=root
    Group=www-data
    WorkingDirectory=/SMC
    ExecStart=/usr/bin/python3.9 /SMC/server.py
    StandardOutput=append:/var/log/SMC.log
    StandardError=append:/var/log/SMC.log
    
    [Install]
    WantedBy=multi-user.target

Note that you can create a service file with the command:

    nano /etc/systemd/system/System/SMC.service

And then:

    systemctl daemon-reload

This will only work on systems where the systemd-service exists.

And also, notice the line:

    ExecStart=/usr/bin/python3.9

This assumes that you are using python **version 3.9**.

Since the **requirements.txt** dependency uses 
**cryptography**-module to securely encrypt/decrypt traffic between client and server, you need to use **python version >= 3.9.10**.

#
###Example using SMC

Here is an example of sending a request from a client to an already running (deploined server):

    from client import get_connect, request
    
    
    connect = get_connect('ip_your_server', port_you_server)
    response = request(connect, {'call_func': 'test1', 'data': {'1': 2, '2': 3}})
    
In this example:

    # this is the name of the called server processing function
    # you wrote in the server_functions.py file
    'call_func': 'test1'
    
    # is the data, in this case {'1': 2, '2': 3}, that will be passed to the called
    # function on the server, in this case the 'test1' function
    'data': {'1': 2, '2': 3}

If we look at the original "**test**" set of functions in the **server_functions.py** file, we see that all the functions written there take the "**data**" argument.

This must be strictly observed when writing your own processing functions for the server part, otherwise, the data coming from the client in the "**data**" field will not be able to be passed to the server for processing. You will get the answer: "**incorrect data**". Since the construction of the specified function call looks as follows (in server.py):

`response(connection, server_functions.names.get(client_request[conf.call_func])(client_request.get(conf.data)))`

In this line, the following happens:
1. the function of sending a response by the server accepts 2 arguments, where 1 argument is the connection object, the 2nd argument is the received function name from the variable "**names**".
2. receives the name of the function specified in the request "**client_request[conf.call_func]**".
3. calls the received function, if it exists in **server_functions.py** passing the request body from the client request from the "**data**" field.
- If you specify the function name incorrectly and it is not found, the server will return the response "**call_func not found**".
- If you don't specify the "**data**" field in the request to the server, nothing happens, you just call the function by name, which processes some data and returns it to the client.
4. "**server_functions.names**" is a global visibility variable in **server_functions.py** that collects the names of custom functions that were written in **server_functions.py**, the construct forming the dictionary object **{'name function': your_function, ...}** looks like this:

        # get names functions and links to functions for import
        names = {name: obj for name, obj in frame().f_locals.items() if callable(obj) and obj.__module__ == __name__}

#
#End

Great, you can start the server and handle client requests.