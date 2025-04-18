from netmiko import ConnectHandler, NetMikoAuthenticationException, NetMikoTimeoutException
import pandas as pd
import re
import json
import concurrent.futures

import app.core.usecases.status_router_service as status_router_service
import app.core.usecases.interface_router_service as interface_router_service

class huaweirouterservice:
    
    def getUsersPPOE(host, port, username, password):
        try:
            objConnection = {'host': host,
                            'username': username,
                            'password': password,
                            'port': int(port)
                        }
        
            connection = ConnectHandler(device_type='huawei', **objConnection)
            connection.send_command('screen-length 0 temporary')            
            output = connection.send_command("display access-user user-type pppoe", read_timeout=60)
            connection.disconnect()

            usersData = []
            lines = output.strip().split("\n")
            
            for i in range(0, len(lines), 2):
                main_line = lines[i].split()
                second_line = lines[i+1].strip().split() if i+1 < len(lines) else []
                
                if len(main_line) >= 5:
                    user = {
                        "id": main_line[0],
                        "username": main_line[1],
                        "interface": main_line[2],
                        "ipv4": main_line[3],
                        "mac": main_line[4],
                        "ipv6": second_line[1] if len(second_line) > 1 and second_line[1] != '-' else None,
                        "connection_type": second_line[2] if len(second_line) > 2 else None
                    }
                    usersData.append(user)

            return usersData
        
        except NetMikoTimeoutException:
            print(f"Timeout ao tentar conectar ao dispositivo {host}:{port}")
            return (f"Timeout ao tentar conectar ao dispositivo {host}:{port}")

        except NetMikoAuthenticationException:
            print(f"Falha de autenticação ao tentar conectar ao dispositivo {host}:{port}")
            return (f"Falha de autenticação ao tentar conectar ao dispositivo {host}:{port}")

        except Exception as e:
            print(f"Erro inesperado ao conectar no dispositivo {host}:{port}: {e}")
            return (f"Erro inesperado ao conectar no dispositivo {host}:{port}: {e}")

    def getRouterDetails(host, port, username, password):
        try:
            objConnection = {'host': host,
                            'username': username,
                            'password': password,
                            'port': int(port)
                        }
        
            connection = ConnectHandler(device_type='huawei', **objConnection)
            connection.send_command('screen-length 0 temporary')            
            temperature = connection.send_command("display temperature", read_timeout=60)

            connection.send_command('screen-length 0 temporary')            
            version = connection.send_command("display version", read_timeout=60)
            connection.disconnect()

            temperatureReturn = formatDataTemperature(temperature)
            versionReturn = formatDataVersion(version)
            detailsReturn = []

            detailsReturn.append({"Temperature" : temperatureReturn})
            detailsReturn.append({"Version" : versionReturn})

            return detailsReturn

        
        except Exception as e:
            print(f"Erro ao executar comando: {e}")
            raise

    def getInterfaceDetails(host, port, username, password, interfaceName):
        objConnection = {'host': host,
                            'username': username,
                            'password': password,
                            'port': int(port)
                        }
        try:
            print(interfaceName)
            connection = ConnectHandler(device_type='huawei', fast_cli=True, **objConnection)
            connection.send_command('screen-length 0 temporary')            
            output = connection.send_command("display interface "+interfaceName, read_timeout=60)
            connection.disconnect()
            
            lines = output.split("\n")
            print(lines)

            # Dicionário que vai conter todos os campos
            details = {
                "name": None,
                "current_state": None,
                "ifindex": None,
                "line_protocol": None,
                "link_quality_grade": None,
                "description": None,
                "max_transmit_unit": None,
                "internet_protocol_processing": None,
                "hardware_address": None,
                "factor_module": None,
                "factor_standard": None,
                "fec_mode": None,
                "vendor_pn": None,
                "vendor_name": None,
                "port_bw": None,
                "transceiver_max_bw": None,
                "transceiver_mode": None,
                "connector_type": None,
                "transmission_distance": None,
                "wave_length": None,
                "rx_warning_range": None,
                "tx_warning_range": None,
                "rx0_power": None,
                "tx0_power": None,
                "rx1_power": None,
                "tx1_power": None,
                "rx2_power": None,
                "tx2_power": None,
                "rx3_power": None,
                "tx3_power": None,
                "loopback": None,
                "duplex_mode": None,
                "pause_flowcontrol": None,
                "last_up_time": None,
                "last_down_time": None,
                "current_system_time": None,
                "stats_last_cleared": None,
                "last_300s_input_bits": None,
                "last_300s_input_bits_converted": None,
                "last_300s_input_pkts": None,
                "last_300s_output_bits": None,
                "last_300s_output_bits_converted": None,
                "last_300s_output_pkts": None,
                "input_peak_bits": None,
                "output_peak_bits": None,
                "input_bytes": None,
                "input_packets": None,
                "output_bytes": None,
                "output_packets": None,

                # Contadores do bloco "Input:"
                "input_unicast": None,
                "input_multicast": None,
                "input_broadcast": None,
                "input_jumbo": None,

                # Contadores do bloco "Output:"
                "output_unicast": None,
                "output_multicast": None,
                "output_broadcast": None,
                "output_jumbo": None,
                "local_fault": None,
                "remote_fault": None,
                "last_300s_input_utility_rate": None,
                "last_300s_output_utility_rate": None,
            }

            # Exemplos de regex para capturar informações de cada linha
            regex_name_state_ifindex = re.compile(r"""
                ^(?P<name>\S+)        # ex.: 100GE0/5/1
                \s+current\s+state\s+: \s+
                (?P<state>\S+)        # ex.: UP
                \s+\(ifindex:\s*(?P<ifindex>\d+)\)
            """, re.VERBOSE)

            regex_line_protocol = re.compile(r"^Line protocol current state : (?P<line_state>\S+)")
            regex_link_quality = re.compile(r"^Link quality grade : (?P<quality>\S+)")
            regex_description = re.compile(r"^Description:\s*(?P<desc>.+)")
            regex_mtu = re.compile(r"The Maximum Transmit Unit is (?P<mtu>\d+)")
            regex_internet_processing = re.compile(r"^Internet protocol processing : (?P<val>\S+)")
            regex_hw_address = re.compile(r".*Hardware address is (?P<mac>\S+)")
            regex_factor = re.compile(r"^Factor/Module:\s*(?P<factor>[^,]+),\s*Standard:\s*(?P<std>[^,]+),\s*FecMode:\s*(?P<fec>\S+)")
            regex_vendor_pn = re.compile(r"^The Vendor PN is (?P<pn>\S+)")
            regex_vendor_name = re.compile(r"^The Vendor Name is (?P<name>\S+)")
            regex_bw = re.compile(r"^Port BW:\s*(?P<pbw>\S+),\s*Transceiver max BW:\s*(?P<maxbw>\S+),\s*Transceiver Mode:\s*(?P<mode>\S+)")
            regex_connector_dist = re.compile(r"^Connector Type:\s*(?P<connector>[^,]+),\s*Transmission Distance:\s*(?P<dist>\S+)")
            regex_wave = re.compile(r"^WaveLength:\s*(?P<wave>.+)")

            regex_warn_range = re.compile(r"^Rx Warning range:\s*(?P<rxWarn>[^\]]+\]dBm),\s*Tx Warning range:\s*(?P<txWarn>[^\]]+\]dBm)")
            regex_rx0_tx0 = re.compile(r"^Rx0 Power:\s*(?P<rx0>[^,]+),\s*Tx0 Power:\s*(?P<tx0>.+)")
            regex_rx1_tx1 = re.compile(r"^Rx1 Power:\s*(?P<rx1>[^,]+),\s*Tx1 Power:\s*(?P<tx1>\S+)")
            regex_rx2_tx2 = re.compile(r"^Rx2 Power:\s*(?P<rx2>[^,]+),\s*Tx2 Power:\s*(?P<tx2>\S+)")
            regex_rx3_tx3 = re.compile(r"^Rx3 Power:\s*(?P<rx3>[^,]+),\s*Tx3 Power:\s*(?P<tx3>\S+)")
            

            # Você pode criar regex parecidas para Rx1/Tx1, Rx2/Tx2, Rx3/Tx3
            regex_loopback = re.compile(r"^Loopback:\s*(?P<loop>[^,]+),\s*(?P<duplex>[^,]+),\s*Pause Flowcontrol:\s*(?P<pause>.+)")
            regex_last_up = re.compile(r"^Last physical up time\s*:\s*(?P<datetime>.+)")
            regex_last_down = re.compile(r"^Last physical down time\s*:\s*(?P<datetime>.+)")
            regex_current_time = re.compile(r"^Current system time:\s*(?P<datetime>.+)")
            regex_stats_cleared = re.compile(r"^Statistics last cleared:(?P<datetime>.*)")
            regex_input_rate = re.compile(r"^Last 300 seconds input rate:?\s*(?P<bits>\d+)\s*bits/sec,\s*(?P<pkts>\d+)\s*packets/sec")
            regex_output_rate = re.compile(r"^Last 300 seconds output rate:?\s*(?P<bits>\d+)\s*bits/sec,\s*(?P<pkts>\d+)\s*packets/sec")
            regex_peak_input = re.compile(r"^Input peak rate\s*(?P<bits>\d+)\s*bits/sec")
            regex_peak_output = re.compile(r"^Output peak rate\s*(?P<bits>\d+)\s*bits/sec")
            regex_in_bytes_packets = re.compile(r"^Input:\s*(?P<bytes>\d+)\s*bytes,\s*(?P<packets>\d+)\s*packets")
            regex_in_packets_bytes = re.compile(r"^Input:\s*(?P<packets>\d+)\s*packets,\s*(?P<bytes>\d+)\s*bytes")

            regex_out_bytes_packets = re.compile(r"^Output:\s*(?P<bytes>\d+)\s*bytes,\s*(?P<packets>\d+)\s*packets")
            regex_out_packts_bytes = re.compile(r"^Output:\s*(?P<packets>\d+)\s*packets,\s*(?P<bytes>\d+)\s*bytes")

            regex_unicast_multicast = re.compile(r"^\s*Unicast:\s*(?P<unicast>\d+)\s*packets,\s*Multicast:\s*(?P<mcast>\d+)\s*packets")   # "Unicast: 27312472608 packets, Multicast: 16726 packets"
            regex_bcast_jumbo = re.compile(r"^\s*Broadcast:\s*(?P<bcast>\d+)\s*packets,\s*JumboOctets:\s*(?P<jumbo>\d+)\s*packets") # "Broadcast: 0 packets, JumboOctets: 2657994 packets"
            regex_local_remote_fault = re.compile(r"^Local fault:\s*(?P<local>\S+),\s*Remote fault:\s*(?P<remote>[^\.]+).*")
            regex_util_in = re.compile(r"^Last 300 seconds input utility rate:\s*(?P<rate>\S+)")
            regex_util_out = re.compile(r"^Last 300 seconds output utility rate:\s*(?P<rate>\S+)")

            # Flags para sabermos se estamos na seção "Input:" ou "Output:"
            in_input_section = False
            in_output_section = False
            in_port_table = False
            port_entries = []
            value_metryc_temp = ""
            for line in lines:
                line = line.strip()

                # 1) Checar cada regex e atribuir no dicionário se casar
                m = regex_name_state_ifindex.match(line)
                if m:
                    details["name"] = m.group("name")
                    details["current_state"] = m.group("state")
                    details["ifindex"] = m.group("ifindex")
                    continue
                
                m = regex_line_protocol.match(line)
                if m:
                    details["line_protocol"] = m.group("line_state")
                    continue

                m = regex_link_quality.match(line)
                if m:
                    details["link_quality_grade"] = m.group("quality")
                    continue

                m = regex_description.match(line)
                if m:
                    details["description"] = m.group("desc").strip()
                    continue

                m = regex_mtu.search(line)
                if m:
                    details["max_transmit_unit"] = m.group("mtu")
                    continue

                m = regex_internet_processing.match(line)
                if m:
                    details["internet_protocol_processing"] = m.group("val")
                    continue

                m = regex_hw_address.search(line)
                if m:
                    details["hardware_address"] = m.group("mac")
                    continue

                m = regex_factor.match(line)
                if m:
                    details["factor_module"] = m.group("factor").strip()
                    details["factor_standard"] = m.group("std").strip()
                    details["fec_mode"] = m.group("fec").strip()
                    continue

                m = regex_vendor_pn.match(line)
                if m:
                    details["vendor_pn"] = m.group("pn")
                    continue

                m = regex_vendor_name.match(line)
                if m:
                    details["vendor_name"] = m.group("name")
                    continue

                m = regex_bw.match(line)
                if m:
                    details["port_bw"] = m.group("pbw")
                    details["transceiver_max_bw"] = m.group("maxbw")
                    details["transceiver_mode"] = m.group("mode")
                    continue

                m = regex_connector_dist.match(line)
                if m:
                    details["connector_type"] = m.group("connector")
                    details["transmission_distance"] = m.group("dist")
                    continue

                m = regex_wave.match(line)
                if m:
                    details["wave_length"] = m.group("wave")
                    continue

                m = regex_warn_range.match(line)
                if m:
                    details["rx_warning_range"] = m.group("rxWarn").strip()
                    details["tx_warning_range"] = m.group("txWarn").strip()
                    continue

                m = regex_rx0_tx0.match(line)
                if m:
                    details["rx0_power"] = m.group("rx0")
                    details["tx0_power"] = m.group("tx0")
                    continue

                m = regex_rx1_tx1.match(line)
                if m:
                    details["rx1_power"] = m.group("rx1")
                    details["tx1_power"] = m.group("tx1")
                    continue

                m = regex_rx2_tx2.match(line)
                if m:
                    details["rx2_power"] = m.group("rx2")
                    details["tx2_power"] = m.group("tx2")
                    continue

                m = regex_rx3_tx3.match(line)
                if m:
                    details["rx3_power"] = m.group("rx3")
                    details["tx3_power"] = m.group("tx3")
                    continue
                
                m = regex_loopback.match(line)
                if m:
                    details["loopback"] = m.group("loop")
                    details["duplex_mode"] = m.group("duplex")
                    details["pause_flowcontrol"] = m.group("pause")
                    continue

                m = regex_last_up.match(line)
                if m:
                    details["last_up_time"] = m.group("datetime").strip()
                    continue

                m = regex_last_down.match(line)
                if m:
                    details["last_down_time"] = m.group("datetime").strip()
                    continue

                m = regex_current_time.match(line)
                if m:
                    details["current_system_time"] = m.group("datetime").strip()
                    continue
                
                m = regex_stats_cleared.match(line)
                if m:
                    details["stats_last_cleared"] = m.group("datetime").strip()
                    continue

                m = regex_input_rate.match(line)
                if m:
                    details["last_300s_input_bits"] = m.group("bits")
                    value_converted = format_traffic(m.group("bits"), "")
                    value_metryc_temp = value_converted.split()[1]
                    details["last_300s_input_bits_converted"] = value_converted
                    details["last_300s_input_pkts"] = m.group("pkts")
                    continue
                
                m = regex_output_rate.match(line)
                if m:
                    details["last_300s_output_bits"] = m.group("bits")
                    details["last_300s_output_bits_converted"] = format_traffic(m.group("bits"), value_metryc_temp)                   
                    details["last_300s_output_pkts"] = m.group("pkts")
                    continue

                m = regex_peak_input.match(line)
                if m:
                    details["input_peak_bits"] = m.group("bits")
                    continue
                
                m = regex_peak_output.match(line)
                if m:
                    details["output_peak_bits"] = m.group("bits")
                    continue
                
                m = regex_in_bytes_packets.match(line)
                if m:
                    details["input_bytes"] = m.group("bytes")
                    details["input_packets"] = m.group("packets")
                    continue
                
                m = regex_in_packets_bytes.match(line)
                if m:
                    details["input_bytes"] = m.group("bytes")
                    details["input_packets"] = m.group("packets")
                    continue
                
                m = regex_out_bytes_packets.match(line)
                if m:
                    details["output_bytes"] = m.group("bytes")
                    details["output_packets"] = m.group("packets")
                    continue
                
                m = regex_out_packts_bytes.match(line)
                if m:
                    details["output_bytes"] = m.group("bytes")
                    details["output_packets"] = m.group("packets")
                    continue
                
                # Verifica se a linha nos indica que estamos entrando ou saindo da seção Input/Output
                if line.startswith("Input:"):
                    in_input_section = True
                    in_output_section = False
                    continue
                if line.startswith("Output:"):
                    in_input_section = False
                    in_output_section = True
                    continue

                # Se estivermos na seção Input, tentamos casar os regex que pegam unicast/multicast etc.
                if in_input_section:
                    m = regex_unicast_multicast.match(line)
                    if m:
                        details["input_unicast"] = m.group("unicast")
                        details["input_multicast"] = m.group("mcast")
                        continue
                    m = regex_bcast_jumbo.match(line)
                    if m:
                        details["input_broadcast"] = m.group("bcast")
                        details["input_jumbo"] = m.group("jumbo")
                        continue
                    # Se tiver mais contadores (CRC, etc.), faça regex ou split também

                # Se estivermos na seção Output
                if in_output_section:
                    m = regex_unicast_multicast.match(line)
                    if m:
                        details["output_unicast"] = m.group("unicast")
                        details["output_multicast"] = m.group("mcast")
                        continue
                    m = regex_bcast_jumbo.match(line)
                    if m:
                        details["output_broadcast"] = m.group("bcast")
                        details["output_jumbo"] = m.group("jumbo")
                        continue
                    # E assim por diante

                m = regex_local_remote_fault.match(line)
                if m:
                    details["local_fault"] = m.group("local")
                    details["remote_fault"] = m.group("remote").strip()
                    continue

                m = regex_util_in.match(line)
                if m:
                    details["last_300s_input_utility_rate"] = m.group("rate")
                    continue

                m = regex_util_out.match(line)
                if m:
                    details["last_300s_output_utility_rate"] = m.group("rate")
                    continue
                
                if "PortName" in line and "Status" in line and "Weight" in line:
                    in_port_table = True
                    continue
                
                if in_port_table:
                    if line.startswith("---"):  # separador de tabela
                        continue
                    if line.strip().startswith("The Number of Ports in Trunk"):
                        in_port_table = False
                        continue
                    
                    parts = line.split()
                    if len(parts) >= 3:
                        iface = parts[0]
                        status = parts[1]
                        weight = parts[2]
                        port_entries.append({
                            "iface": iface,
                            "status": status,
                            "weight": weight
                        })

            details["slave_ports"] = port_entries
            
            print(details)
            return details
    
        except Exception as e:
            print(f"Erro ao executar comando: {e}")
            raise
    
    def getInterfaces(host, port, username, password):
        try:
            return interface_router_service.getAll(host, port, username, password)
        except Exception as e:
            print(f"Erro ao executar comando: {e}")
            raise
    
    def getStatusRouter(host, port, username, password):
        # 1) Cria um executor de threads
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            # 2) Agenda as chamadas
            future_cpu = executor.submit(
                status_router_service.getCpuUsage,
                host, port, username, password
            )
            future_mem = executor.submit(
                status_router_service.getMemoryUsage,
                host, port, username, password
            )
            future_temp = executor.submit(
                status_router_service.getTemperature,
                host, port, username, password
            )
            future_info = executor.submit(
                status_router_service.getInfoRouter,
                host, port, username, password
            )

            # 3) Obtém os resultados (bloqueia até cada um terminar)
            cpuUsage = future_cpu.result()
            memoryUsage = future_mem.result()
            temperature = future_temp.result()
            infoRouter = future_info.result()

        # 4) Monta o JSON final
        cpuUsage["memory_details"].append(memoryUsage)
        cpuUsage["temperature_router"].extend(temperature)
        cpuUsage["info_router"].append(infoRouter)
            
        return json.dumps(cpuUsage, indent=2)


def formatDataTemperature(self, data):
    lines = data.strip().split("\n")
    fieldsList = []
    valuesList = []
    temperatureLists = []
    temperatureDictionary = []
    slotTemp = ""
    
    for line in lines:
        lineItems = line.strip().split(" ")
        if slotTemp == "":
            if "Slot" in lineItems[2]:
                slotTemp = "Slote "+lineItems[3]
                valuesList = []
                continue
        
        if "----" not in line and fieldsList == []:
            fields = line.strip().split(" ")
            for field in fields:
                if field != "":
                    fieldsList.append(field)
            continue

        if "----" not in line and fieldsList != []:
            values = line.strip().split(" ")
            valuesList = []
            for value in values:
                if value != "":
                    valuesList.append(value)

            dictionary = {chave: valor for chave, valor in zip(fieldsList, valuesList)}
            temperatureLists.append(dictionary)
            
        if "----" in line and valuesList != []:
            temperatureDictionary.append({slotTemp : temperatureLists})
            fieldsList = []
            temperatureLists = []
            slotTemp = ""

    return temperatureDictionary

def formatDataVersion(self, data):
    lines = data.strip().split("\n")
    name = lines[1]
    upTime = lines[3]
    version = lines[4]

    fields = []
    fields.append("name")
    fields.append("upTime")
    fields.append("version")
    
    values = []
    nameList = name.strip().split(" ")
    values.append(nameList[5].replace("(","")+" "+nameList[6]+" "+nameList[7].replace(")",""))

    upList = upTime.strip().split(" ")
    values.append(upList[6]+" "+upList[7]+" "+upList[8]+" "+upList[9].replace(",",""))
    values.append(version)

    versionDictionary = {chave: valor for chave, valor in zip(fields, values)}
    return versionDictionary

def format_traffic(bits: int, type_metric: str) -> str:
    value = float(bits)
    unit = ""

    if not type_metric:
        # Se type_metric for vazio, faz autodetecção
        if value >= 1_000_000_000:
            value /= 1_000_000_000
            unit = "Gbps"
        elif value >= 1_000_000:
            value /= 1_000_000
            unit = "Mbps"
        elif value >= 1_000:
            value /= 1_000
            unit = "Kbps"
        else:
            unit = "bps"
    else:
        # Se veio algo em type_metric, faz switch
        if type_metric == "Gbps":
            value /= 1_000_000_000
            unit = "Gbps"
        elif type_metric == "Mbps":
            value /= 1_000_000
            unit = "Mbps"
        elif type_metric == "Kbps":
            value /= 1_000
            unit = "Kbps"
        else:
            unit = "bps"

    formatted_value = f"{value:,.2f}"
    return f"{formatted_value} {unit}"