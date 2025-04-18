from netmiko import ConnectHandler, NetMikoAuthenticationException, NetMikoTimeoutException
import pandas as pd
import re
import json


def getCpuUsage(host, port, user, password):
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

        # 1) Separar em linhas
        lines = output.splitlines()

        # Dicionário final
        stats = {
            "timestamp": None,
            "system_cpu_use_rate": None,
            "cpu_util_5s": None,
            "cpu_util_1m": None,
            "cpu_util_5m": None,
            "max_cpu_usage": None,
            "max_cpu_usage_time": None,
            "cpu_services": [],
            "cpu_details": [],
            "memory_details": [],
            "temperature_router": [],
            "info_router": [],
        }

        # 2) Regex para capturar as linhas principais
        re_timestamp    = re.compile(r"^Cpu utilization statistics at (.+)$")
        re_sys_cpu_rate = re.compile(r"^System cpu use rate is :\s*(\d+)%")
        re_cpu_util     = re.compile(
            r"^Cpu utilization for five seconds:\s*(\d+)%\s*;\s*one minute:\s*(\d+)%\s*;\s*five minutes:\s*(\d+)%\.$"
        )
        re_max_cpu      = re.compile(r"^Max CPU Usage :\s*(\d+)%")
        re_max_cpu_time = re.compile(r"^Max CPU Usage Stat. Time :\s*(.+)$")

        in_service_table = False
        in_cpu_table = False

        re_service_line = re.compile(r"^(\S[^\d%]+)\s+(\d+)%$")
        re_cpu_line = re.compile(
            r"^(cpu\d+)\s+(\d+)%\s+(\d+)%\s+(\d+)%\s+(\d+)%\s+(\d+)%\s+(.*)$"
        )

        for line in lines:
            line = line.strip()

            m_ts = re_timestamp.match(line)
            if m_ts:
                stats["timestamp"] = m_ts.group(1).strip()
                continue

            m_sys = re_sys_cpu_rate.match(line)
            if m_sys:
                stats["system_cpu_use_rate"] = m_sys.group(1)
                continue

            m_util = re_cpu_util.match(line)
            if m_util:
                stats["cpu_util_5s"] = m_util.group(1)
                stats["cpu_util_1m"] = m_util.group(2)
                stats["cpu_util_5m"] = m_util.group(3)
                continue

            m_max = re_max_cpu.match(line)
            if m_max:
                stats["max_cpu_usage"] = m_max.group(1)
                continue

            m_max_t = re_max_cpu_time.match(line)
            if m_max_t:
                stats["max_cpu_usage_time"] = m_max_t.group(1).strip()
                continue

            # 2) Detecta se começamos ou terminamos a tabela de serviços
            if "ServiceName" in line and "UseRate" in line:
                # A partir daqui, estamos na tabela de serviços
                in_service_table = True
                in_cpu_table = False
                continue
            if in_service_table and ("CPU Usage Details" in line or line.startswith("CPU Usage Details")):
                # tabela de serviços acabou
                in_service_table = False
                in_cpu_table = True
                continue

            # 4) Parse da tabela de serviços
            if in_service_table:
                m_svc = re_service_line.match(line)
                if m_svc:
                    service_name = m_svc.group(1).strip()
                    usage = m_svc.group(2)
                    stats["cpu_services"].append({
                        "service": service_name,
                        "usage": usage
                    })
                continue

            # 5) Parse da tabela de CPU usage
            if in_cpu_table:
                
                parts = line.split()
                if ( (len(parts) >= 6) and (not "current" in line.lower()) and ( not "fivesec" in line.lower()) ):
                    cpu_id = parts[0]
                    current = parts[1].rstrip('%')
                    five_sec = parts[2].rstrip('%')
                    one_min = parts[3].rstrip('%')
                    five_min = parts[4].rstrip('%')
                    max_val = parts[5].rstrip('%')
                    
                    max_time = ""
                    if len(parts) > 6:
                        max_time = " ".join(parts[6:])
                    
                    stats["cpu_details"].append({
                        "cpu_id": cpu_id,
                        "current": current,
                        "five_sec": five_sec,
                        "one_min": one_min,
                        "five_min": five_min,
                        "max": max_val,
                        "max_time": max_time
                    })
                continue

        return stats
    
    except NetMikoTimeoutException:
        print(f"Timeout ao tentar conectar ao dispositivo {host}:{port}")
        return (f"Timeout ao tentar conectar ao dispositivo {host}:{port}")

    except NetMikoAuthenticationException:
        print(f"Falha de autenticação ao tentar conectar ao dispositivo {host}:{port}")
        return (f"Falha de autenticação ao tentar conectar ao dispositivo {host}:{port}")

    except Exception as e:
        print(f"Erro inesperado ao conectar no dispositivo {host}:{port}: {e}")
        return (f"Erro inesperado ao conectar no dispositivo {host}:{port}: {e}")

def getMemoryUsage(host, port, user, password):
    stats = {
            "timestamp": None,
            "system_total_memory": None,
            "system_memory_used": None,
            "memory_using_percentage": None,
            }

    try:
        objConnection = {'host': host,
                            'username': user,
                            'password': password,
                            'port': int(port)
                        }
        
        connection = ConnectHandler(device_type='huawei', **objConnection)
        connection.send_command('screen-length 0 temporary')            
        output = connection.send_command("display memory-usage", read_timeout=60)
        connection.disconnect()

        # Regex para cada linha de interesse
        re_timestamp = re.compile(r"^Memory utilization statistics at (.+)$")
        re_total_mem = re.compile(r"^System Total Memory Is:\s*(\d+)\s*Kbytes")
        re_used_mem  = re.compile(r"^Total Memory Used Is:\s*(\d+)\s*Kbytes")
        re_mem_perc  = re.compile(r"^Memory Using Percentage Is:\s*(\d+)%")

        for line in output.splitlines():
            line = line.strip()

            m_ts = re_timestamp.match(line)
            if m_ts:
                stats["timestamp"] = m_ts.group(1).strip()
                continue

            m_total = re_total_mem.match(line)
            if m_total:
                stats["system_total_memory"] = m_total.group(1)
                continue

            m_used = re_used_mem.match(line)
            if m_used:
                stats["system_memory_used"] = m_used.group(1)
                continue

            m_perc = re_mem_perc.match(line)
            if m_perc:
                stats["memory_using_percentage"] = m_perc.group(1)
                continue

    except NetMikoTimeoutException:
        print(f"Timeout ao tentar conectar ao dispositivo {host}:{port}")
        return (f"Timeout ao tentar conectar ao dispositivo {host}:{port}")

    except NetMikoAuthenticationException:
        print(f"Falha de autenticação ao tentar conectar ao dispositivo {host}:{port}")
        return (f"Falha de autenticação ao tentar conectar ao dispositivo {host}:{port}")

    except Exception as e:
        print(f"Erro inesperado ao conectar no dispositivo {host}:{port}: {e}")
        return (f"Erro inesperado ao conectar no dispositivo {host}:{port}: {e}")

    return stats

def getTemperature(host, port, user, password):
    
    try:
        objConnection = {'host': host,
                            'username': user,
                            'password': password,
                            'port': int(port)
                        }
        
        connection = ConnectHandler(device_type='huawei', **objConnection)
        connection.send_command('screen-length 0 temporary')            
        output = connection.send_command("display temperature", read_timeout=60)
        connection.disconnect()

        lines = output.splitlines()

        # Regex para capturar algo como: "Base-Board, Unit:C, Slot 9"
        slot_regex = re.compile(r"^Base-Board,\s*Unit:\S+,\s*Slot\s+(\d+)$")

        # Estrutura final
        result = []

        current_slot = None
        current_boards = []  # armazena as linhas de PCB do slot atual
        collecting_table = False

        for line in lines:
            line = line.strip()

            # 1) Detecta início de slot
            m_slot = slot_regex.match(line)
            if m_slot:
                # Se já estávamos em um slot, salvar o anterior
                if current_slot is not None:
                    result.append({
                        "slot": current_slot,
                        "boards": current_boards
                    })

                # Começa um novo slot
                current_slot = m_slot.group(1)
                current_boards = []
                collecting_table = False
                continue

            # 2) Se vier uma linha vazia ou algo que não é parte da tabela, e estivermos coleteando
            if not line:
                continue

            # 3) Detecta o cabeçalho da tabela (outra forma: se começa com "PCB" e "Temp(C)")
            if line.startswith("PCB") and "Temp(C)" in line:
                # Próximas linhas (até um "----" ou novo slot) serão dados da tabela
                collecting_table = True
                continue

            # 4) Se for linha de separador "----", podemos pular
            if set(line) == {"-"}:
                # É um separador
                continue

            # 5) Se estamos coletando as linhas da tabela, parse
            if collecting_table:
                # Exemplo de linha de dados:
                # "CR81IPU480DS   255 73   0   NORMAL   75    85    90    50       60       32"
                # Precisamos splitar. Vamos supor que cada coluna
                # esteja separada por espaços. 
                parts = line.split()
                if len(parts) < 11:
                    # Pode haver variações, ajusta se precisar
                    continue

                # Mapeia cada parte para a respectiva coluna
                row_data = {
                    "PCB": parts[0],
                    "I2C": parts[1],
                    "Addr": parts[2],
                    "Chl": parts[3],
                    "Status": parts[4],
                    "Minor": parts[5],
                    "Major": parts[6],
                    "Fatal": parts[7],
                    "FanTMin": parts[8],
                    "FanTMax": parts[9],
                    "Temp(C)": parts[10]
                }
                current_boards.append(row_data)

        # Se acabar o arquivo e tivermos um slot em aberto
        if current_slot is not None:
            result.append({
                "slot": current_slot,
                "boards": current_boards
            })

        return result

    except NetMikoTimeoutException:
        print(f"Timeout ao tentar conectar ao dispositivo {host}:{port}")
        return (f"Timeout ao tentar conectar ao dispositivo {host}:{port}")

    except NetMikoAuthenticationException:
        print(f"Falha de autenticação ao tentar conectar ao dispositivo {host}:{port}")
        return (f"Falha de autenticação ao tentar conectar ao dispositivo {host}:{port}")

    except Exception as e:
        print(f"Erro inesperado ao conectar no dispositivo {host}:{port}: {e}")
        return (f"Erro inesperado ao conectar no dispositivo {host}:{port}: {e}")

def getInfoRouter(host, port, user, password):
    # Dicionário final
    info = {
        "version_equipment": None,
        "model_equipment": None,
        "uptime": None,
        "patch_version": None
    }
    
    try:

        objConnection = {'host': host,
                            'username': user,
                            'password': password,
                            'port': int(port)
                        }
        
        connection = ConnectHandler(device_type='huawei', **objConnection)
        connection.send_command('screen-length 0 temporary')            
        output = connection.send_command("display version", read_timeout=60)
        connection.disconnect()
    
        re_version_model = re.compile(
            r"^VRP.*Version\s+([^\s]+)\s*\(([^)]+)\)", re.IGNORECASE
        )
        
        re_uptime = re.compile(r"uptime\s+is\s+(.*)", re.IGNORECASE)

        re_patch = re.compile(r"^Patch Version:\s*(.+)$", re.IGNORECASE)

        # Processa cada linha
        for line in output.splitlines():
            line_strip = line.strip()

            # Tenta capturar versão & modelo
            vm = re_version_model.search(line_strip)
            if vm:
                version_value = vm.group(1)
                model_value = vm.group(2).strip()
                info["version_equipment"] = f"Version {version_value}"
                info["model_equipment"] = model_value
                continue

            # Tenta capturar uptime
            m_up = re_uptime.search(line_strip)
            if m_up:
                info["uptime"] = m_up.group(1).strip()  # ex.: "19 days, 3 hours, 57 minutes"
                continue

            # Tenta capturar patch
            m_patch = re_patch.search(line_strip)
            if m_patch:
                info["patch_version"] = m_patch.group(1).strip()
                continue

        return info
    
    except NetMikoTimeoutException:
        print(f"Timeout ao tentar conectar ao dispositivo {host}:{port}")
        return (f"Timeout ao tentar conectar ao dispositivo {host}:{port}")

    except NetMikoAuthenticationException:
        print(f"Falha de autenticação ao tentar conectar ao dispositivo {host}:{port}")
        return (f"Falha de autenticação ao tentar conectar ao dispositivo {host}:{port}")

    except Exception as e:
        print(f"Erro inesperado ao conectar no dispositivo {host}:{port}: {e}")
        return (f"Erro inesperado ao conectar no dispositivo {host}:{port}: {e}")