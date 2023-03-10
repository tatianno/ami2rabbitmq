import sys, os
from ami2rabbitmq import AMI2RabbitMQ
import settings




producer = AMI2RabbitMQ(
    ami_settings = settings.AMI_SETTINGS,
    rabbitmq_settings = settings.RABBITMQ_SETTINGS,
    debug=settings.DEBUG
)

def main():
    print(' [*] PRESS CTRL+C TO QUIT')
    producer.run()
    

if __name__ == '__main__':

    try:
        main()

    except KeyboardInterrupt:
        print('Interrupted')

        try:
            sys.exit(0)
        
        except SystemExit:
            os._exit(0)