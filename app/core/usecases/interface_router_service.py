from netmiko import ConnectHandler, NetMikoAuthenticationException, NetMikoTimeoutException
import pandas as pd
import re
import json


def getAll(host, port, username, password):
    try:

        # 1) list1 vem do método getInterfaceStep1() => lista de dicionários
            list1 = getInterfaceStep1(host, port, username, password)  # cada item tem "name", "description", etc.
            list2 = getInterfaceStep2(host, port, username, password)

            # 4) Localiza o cabeçalho
            header_line = None
            for idx, line in enumerate(list2):
                if line.startswith("Interface"):
                    header_line = idx
                    break

            if header_line is None:
                raise ValueError("Não foi possível encontrar o cabeçalho na lista de strings.")

            header_cols = list2[header_line].split()  # ex.: ["Interface","PHY","Protocol","InUti","OutUti","inErrors","outErrors"]

            # 5) Monta a tabela de dados
            data = []
            for line in list2[header_line+1:]:
                cols = line.split()
                if len(cols) == len(header_cols):
                    data.append(cols)
                # se não tiver o mesmo número de colunas, ignora

            # 6) Cria DataFrame
            df = pd.DataFrame(data, columns=header_cols)

            # 7) Converte DF para lista de dicts (cada linha é um dict)
            df_records = df.to_dict(orient="records")
        
            # 8) Cria dicionário de lookup, chave = valor da coluna "Interface"
            lookup = { row["Interface"]: row for row in df_records }

            # 9) Percorre list1 (principal) => se o item tiver "name" igual a "Interface" do lookup, copia infos
            for p_item in list1:
                interface_name = p_item.get("name")
                if interface_name in lookup:
                    s_item = lookup[interface_name]
                    # Copiamos as chaves que quisermos de s_item para p_item
                    p_item["PHY"] = s_item.get("PHY")
                    p_item["Protocol"] = s_item.get("Protocol")
                    p_item["InUti"] = s_item.get("InUti")
                    p_item["OutUti"] = s_item.get("OutUti")
                    p_item["inErrors"] = s_item.get("inErrors")
                    p_item["outErrors"] = s_item.get("outErrors")
                    # e assim por diante

            # b) Criar DF e usar to_json
            df_merged = pd.DataFrame(list1)
            return df_merged.to_json(orient="records")
    
    except NetMikoTimeoutException:
        print(f"Timeout ao tentar conectar ao dispositivo {host}:{port}")
        return (f"Timeout ao tentar conectar ao dispositivo {host}:{port}")

    except NetMikoAuthenticationException:
        print(f"Falha de autenticação ao tentar conectar ao dispositivo {host}:{port}")
        return (f"Falha de autenticação ao tentar conectar ao dispositivo {host}:{port}")

    except Exception as e:
        print(f"Erro inesperado ao conectar no dispositivo {host}:{port}: {e}")
        return (f"Erro inesperado ao conectar no dispositivo {host}:{port}: {e}")
        
def getInterfaceStep1(host, port, username, password):
    try:
        objConnection = {'host': host,
                        'username': username,
                        'password': password,
                        'port': int(port)
                    }
    
        connection = ConnectHandler(device_type='huawei', **objConnection)
        connection.send_command('screen-length 0 temporary')            
        output = connection.send_command("dis curr int", read_timeout=60)
        connection.disconnect()
        
        # 1) Quebrar por linha, limpar espaços
        lines = [line.strip() for line in output.splitlines()]

        # 2) Separar em blocos com base no "#"
        blocks = []
        current_block = []
        for line in lines:
            if line == "#":
                # Encontramos um delimitador de bloco
                if current_block:
                    blocks.append(current_block)
                    current_block = []
            else:
                if line:  # se não for linha vazia
                    current_block.append(line)
        # Se sobrar bloco no final, adiciona
        if current_block:
            blocks.append(current_block)

        # 3) Regex para capturar interface, descrição, IP
        regex_interface = re.compile(r"^interface\s+(\S+)", re.IGNORECASE)
        regex_desc = re.compile(r"^description\s+(.*)", re.IGNORECASE)
        regex_ip = re.compile(r"^ip\s+address\s+(\S+)\s+(\S+)", re.IGNORECASE)
        
        parsed = []

        for block in blocks:
            name = None
            description = None
            ip_address = None
            ip_mask = None
            iface_type = None  # Pode ficar como None se não achar config

            for line in block:
                # 1) Interface
                m_int = regex_interface.match(line)
                if m_int:
                    name = m_int.group(1)  # ex.: "Eth-Trunk1.99"
                    continue

                # 2) Description
                m_desc = regex_desc.match(line)
                if m_desc:
                    description = m_desc.group(1).strip()
                    continue

                # 3) IP address
                m_ip = regex_ip.match(line)
                if m_ip:
                    ip_address = m_ip.group(1)
                    ip_mask = m_ip.group(2)
                    continue

                # 4) Checar vlan-type dot1q
                if "vlan-type dot1q" in line:
                    iface_type = "vlan"

                # 5) Checar user-vlan
                if "user-vlan" in line:
                    iface_type = "authentication"

            # Só adiciona se achamos uma linha "interface X"
            if name:
                parsed.append({
                    "name": name,
                    "description": description,
                    "ip_address": ip_address,
                    "ip_mask": ip_mask,
                    "type": iface_type
                })

    except NetMikoTimeoutException:
        print(f"Timeout ao tentar conectar ao dispositivo {host}:{port}")
        raise Exception(f"Timeout ao tentar conectar ao dispositivo {host}:{port}")

    except NetMikoAuthenticationException:
        print(f"Falha de autenticação ao tentar conectar ao dispositivo {host}:{port}")
        raise Exception(f"Falha de autenticação ao tentar conectar ao dispositivo {host}:{port}")

    except Exception as e:
        print(f"Erro inesperado ao conectar no dispositivo {host}:{port}: {e}")
        raise Exception(f"Erro inesperado ao conectar no dispositivo {host}:{port}: {e}")
    
    return parsed
        
def getInterfaceStep2(host, port, username, password):
    try:
        objConnection = {'host': host,
                        'username': username,
                        'password': password,
                        'port': int(port)
                    }
    
        connection = ConnectHandler(device_type='huawei', **objConnection)
        connection.send_command('screen-length 0 temporary')
        output = connection.send_command("display interface brief", read_timeout=60)
        connection.disconnect()
        lines = output.strip().split("\n")
        return lines
    
    except NetMikoTimeoutException:
        print(f"Timeout ao tentar conectar ao dispositivo {host}:{port}")
        raise Exception(f"Timeout ao tentar conectar ao dispositivo {host}:{port}")

    except NetMikoAuthenticationException:
        print(f"Falha de autenticação ao tentar conectar ao dispositivo {host}:{port}")
        raise Exception(f"Falha de autenticação ao tentar conectar ao dispositivo {host}:{port}")

    except Exception as e:
        print(f"Erro inesperado ao conectar no dispositivo {host}:{port}: {e}")
        raise Exception(f"Erro inesperado ao conectar no dispositivo {host}:{port}: {e}")