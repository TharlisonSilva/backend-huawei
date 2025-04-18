import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import logging

class tkonu2pdpx:

    def change_password(_chorme, newNameSSID, newPasswordSSID):
        try:

            logging.info("4 - Verificando se pagian já está logada!")
            WebDriverWait(_chorme, 20).until(
                EC.presence_of_element_located((By.ID, "mainFrame"))
            )

            iframe = _chorme.find_element(By.ID, "mainFrame")
            _chorme.switch_to.frame(iframe)

            logging.info("4.1 - Acessando menu de configuração INTERFACE ")
            _chorme.find_element(By.ID, "mmNet").click()
            WebDriverWait(_chorme, 20).until(
                EC.presence_of_element_located((By.ID, "smWLAN"))
            )

            logging.info("4.2 - Acessando menu de configuração WLAN ")
            _chorme.find_element(By.ID, "smWLAN").click()

            WebDriverWait(_chorme, 20).until(
                EC.presence_of_element_located((By.ID, "ssmWLANMul"))
            )
            
            logging.info("4.3 - Acessando menu de configuração SSID WLAN ")
            _chorme.find_element(By.ID, "ssmWLANMul").click()

            WebDriverWait(_chorme, 10).until(
                EC.presence_of_element_located((By.ID, "Frm_ESSID"))
            )

            WebDriverWait(_chorme, 10).until(
                EC.presence_of_element_located((By.ID, "Btn_Submit"))
            )

            logging.info("4.4 - Informando novo nome do WIFI.")
            ssid_booth_input = _chorme.find_element(By.ID, "Frm_ESSID")
            for _ in range(150):
                ssid_booth_input.send_keys(Keys.BACKSPACE)
            ssid_booth_input.send_keys(newNameSSID)

            logging.info("4.5 - Aplicando as alterações SSID WIFI.")
            _chorme.find_element(By.ID, "Btn_Submit").click()
            
            logging.info("5 - Aguardando pagina recarregar.")
            if aguardar_valor_input(_chorme, By.ID, "Frm_ESSID", newNameSSID) : 
                _chorme.find_element(By.ID, "ssmWLANSec").click()
                WebDriverWait(_chorme, 20).until(
                    EC.presence_of_element_located((By.ID, "Frm_KeyPassphrase"))
                )

            logging.info("5.1 - Informando a nova senha no input!")
            senha_booth_input = _chorme.find_element(By.ID, "Frm_KeyPassphrase")
            senha_booth_input.clear()
            senha_booth_input.send_keys(newPasswordSSID)

            logging.info("5.2 - Aplicando as alterações de password do WIFI")
            _chorme.find_element(By.ID, "Btn_Submit").click()

            logging.info("5.3 - Aguardando pagina recarregar.")
            WebDriverWait(_chorme, 20).until(
                EC.presence_of_element_located((By.ID, "Frm_KeyPassphrase"))
            )        

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