from netmiko import ConnectHandler


def createUserRouter(host, port, user, password):
    try:

        objConnection = {'host': host,
                            'username': user,
                            'password': password,
                            'port': int(port)
                        }
        
        connection = ConnectHandler(device_type='huawei', **objConnection)
        connection.send_command('screen-length 0 temporary')            
        output = connection.send_command("display cpu-usage", read_timeout=60)
        connection.disconnect()
    
    except Exception as e:
        print(f"Erro ao executar comando: {e}")
        raise

