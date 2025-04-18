import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import logging


def check_login(_chorme, host_login, port_login, username_login, password_login):
    try:
        urlLogin = "http://"+host_login+":"+port_login
        _chorme.get(urlLogin)

        WebDriverWait(_chorme, 10).until(
            EC.presence_of_element_located((By.ID, "Frm_Username"))
        )
        
        _chorme.find_element(By.ID, "Frm_Username").clear()
        _chorme.find_element(By.ID, "Frm_Username").send_keys(username_login)

        _chorme.find_element(By.ID, "Frm_Password").clear()
        _chorme.find_element(By.ID, "Frm_Password").send_keys(password_login)
        _chorme.find_element(By.ID, "LoginId").click()
        
        WebDriverWait(_chorme, 20).until(
            EC.presence_of_element_located((By.ID, "homePage"))
        )
        
        return True

    except Exception as e:
        print("❌ Erro ao configurar o Wi-Fi:", e)
        return False
    

def change_password(_chorme, newNameSSID, newPasswordSSID):
    try:
    
        logging.info("4 - Verificando se pagian já está logada!")
        WebDriverWait(_chorme, 20).until(
            EC.presence_of_element_located((By.ID, "localnet"))
        )

        logging.info("4.1 - Clicando no menu de configuração de INTERNET")
        _chorme.find_element(By.ID, "localnet").click()
        WebDriverWait(_chorme, 20).until(
            EC.presence_of_element_located((By.ID, "wlanConfig"))
        )

        logging.info("4.2 - Clicando no intem WLAN config")
        _chorme.find_element(By.ID, "wlanConfig").click()
        WebDriverWait(_chorme, 20).until(
            EC.presence_of_element_located((By.ID, "WLANSSIDConfBar"))
        )
        
        logging.info("4.3 - Clicando na config SSID.")
        _chorme.find_element(By.ID, "WLANSSIDConfBar").click()
        
        logging.info("5 - Iniciando processo de alterações das informações WIFI")
        for i in range(8) :
            
            logging.info(f"5.{i} - INICIO PROCESSO")

            elementWait = f"instName_WLANSSIDConf:{i}"
            WebDriverWait(_chorme, 10).until(
                EC.presence_of_element_located((By.ID, elementWait))
            )

            # MODAL #
            WebDriverWait(_chorme, 25).until(
                EC.invisibility_of_element_located((By.ID, "blackMask"))
            )

            logging.info(f"5.{i}.1 - Expandir item config")
            idLine = f"instName_WLANSSIDConf:{i}"
            line = _chorme.find_element(By.ID, idLine )
            classes = line.get_attribute("class")
            if "instNameExp" not in classes.split():
                line.click()

            logging.info(f"5.{i}.2 - Alterando SSID")
            ssid = f"ESSID:{i}"
            ssid_input = _chorme.find_element(By.ID, ssid)
            for _ in range(150):
                ssid_input.send_keys(Keys.BACKSPACE)
            ssid_input.send_keys(newNameSSID)

            logging.info(f"5.{i}.3 - Alterando PASSWORD")
            senhaId = f"KeyPassphrase:{i}"
            senha_booth_input = _chorme.find_element(By.ID, senhaId)
            senha_booth_input.clear()
            senha_booth_input.send_keys(newPasswordSSID)

            logging.info(f"5.{i}.4 - Salvando ajustes")
            buttonSave = f"Btn_apply_WLANSSIDConf:{i}"
            _chorme.find_element(By.ID, buttonSave).click()

            # MODAL #
            WebDriverWait(_chorme, 25).until(
                EC.invisibility_of_element_located((By.ID, "blackMask"))
            )

            logging.info(f"5.{i} - FIM PROCESSO")

        logging.info("6 - Modificações feitas com sucesso!")
        return True
    
    except Exception as e:
        print("❌ Erro ao configurar o Wi-Fi:", e)
        return False
    
    finally:
        _chorme.quit()


def esperar_texto_em_tag(driver, tagType, texto_procurado, timeout=30, intervalo=0.5):
    fim = time.time() + timeout

    while time.time() < fim:
        try:
            tds = driver.find_elements(By.TAG_NAME, tagType)
            for td in tds:
                if texto_procurado in td.text:
                    return True
        except Exception:
            pass

        time.sleep(intervalo)

    return False


def aguardar_valor_input(driver, by, seletor, valor_esperado, timeout=30, intervalo=0.5):
    fim = time.time() + timeout
    while time.time() < fim:
        try:
            input_element = driver.find_element(by, seletor)
            valor_atual = input_element.get_attribute("value")

            if valor_atual == valor_esperado:
                return True
            return False

        except Exception:
            pass
        time.sleep(intervalo)
    
    return False