#!/usr/bin/env python
import sys, getopt
import pika

class Rabbit_producer_basic():
    user = None
    passwd = None
    host = None
    queue = None
    exchange = None
    connection = None
    channel = None
    message = None

    def connect_to_rabbit(self):

        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host, credentials=pika.PlainCredentials(self.user, self.passwd)))

        self.channel = self.connection.channel()

        if self.exchange:
            self.channel.exchange_declare(exchange=self.exchange, exchange_type='fanout', durable=True)
        else:
            self.channel.queue_declare(queue=self.queue, durable=True)


    def disconnect_rabbit(self):
        self.connection.close()


    def show_usage(self):
        print ('notify_by_telegram.py --host HOST_NAME --user USER --pw PASSWORD [--exchange EXCHANGE_NAME | --queue QUEUE_NAME] --message MESSAGE')


    def main(self, argv):
        try:
            opts, args = getopt.getopt(argv,"",["host=","queue=","exchange=","message=","user=","pw="])
            pass
        except getopt.GetoptError as ex:
            print('[ERROR] Params received not correct (%s).' % ex.msg)
            self.show_usage()
            sys.exit(2)
        for opt, arg in opts:
            if opt == "--host":
               self.host = arg
            elif opt == "--queue":
               self.queue = arg
            elif opt == "--exchange":
               self.exchange = arg
            elif opt == "--message":
                self.message = arg
            elif opt == "--user":
               self.user = arg
            elif opt == "--pw":
               self.passwd = arg

        if (not self.host or not self. message or (not self.exchange and not self.queue)):
            print('[ERROR] Mandatory param empty.\nHOST: %s\nEXCHANGE: %s\nQUEUE: %s\nUSER: %s\nMESSAGE: %s\n' % (self.host, self.exchange, self.queue, self.user, self.message))
            self.show_usage()
            sys.exit(2)

        self.connect_to_rabbit()

        if self.exchange:
            self.channel.basic_publish(exchange=self.exchange,
                                       routing_key='',
                                       body=self.message)
        else:
            self.channel.basic_publish(exchange='',
                                       routing_key=self.queue,
                                       body=self.message)

        self.disconnect_rabbit()
        print(' [*] Connected to RabbitMQ on %s and try to sent message "%s"' % (self.host, self.message))


if __name__ == "__main__":
    app = Rabbit_producer_basic()
    params = sys.argv[1:]
    app.main(params)
