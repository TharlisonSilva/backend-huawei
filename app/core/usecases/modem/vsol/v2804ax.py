import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import logging


class v2804ax:
    def change_password(_chorme, newNameSSID, newPasswordSSID):
        try:

            _chorme.refresh()
            _chorme.switch_to.default_content()

            time.sleep(1)
            logging.info("4 - Verificando se pagian já está logada!")
            WebDriverWait(_chorme, 30).until(
                EC.presence_of_element_located((By.ID, "LANG_NETWORK"))
            )
            
            time.sleep(1)
            logging.info("4.1 - Clicando no menu de configuração de INTERNET")
            WebDriverWait(_chorme, 30).until(
                EC.element_to_be_clickable((By.ID, "LANG_NETWORK"))
            ).click()

            time.sleep(1)
            listMenu = _chorme.find_element(By.ID, "collapseLANG_NETWORK")
            classes = listMenu.get_attribute("class")
            if "show" not in classes.split():
                _chorme.find_element(By.ID, "LANG_NETWORK").click()
            
            time.sleep(1)
            WebDriverWait(_chorme, 30).until(
                EC.element_to_be_clickable((By.ID, "net_2g"))
            ).click()

            WebDriverWait(_chorme, 30).until(
                EC.element_to_be_clickable((By.ID, "2_4g_Start_PIN_submit"))
            ).click()

            # 2.4 Ghz wifi
            time.sleep(1)
            logging.info("4.2 - Clicando no item WLAN 2.4 config")
            _chorme.find_element(By.ID, "net_2g").click()
            WebDriverWait(_chorme, 30).until(
                EC.presence_of_element_located((By.ID, "B_ssid"))
            )
            
            time.sleep(1)
            logging.info("4.3 - Alterando o ssid do wifi")
            ssid_input = _chorme.find_element(By.ID, "B_ssid")
            for _ in range(150):
                ssid_input.send_keys(Keys.BACKSPACE)
            ssid_input.send_keys(newNameSSID)
            
            time.sleep(1)
            WebDriverWait(_chorme, 30).until(
                EC.presence_of_element_located((By.ID, "2G_BASIC_SUBMIT"))
            )

            time.sleep(1)
            logging.info("4.4 - Salvando o novo ssid")
            WebDriverWait(_chorme, 30).until(
                EC.element_to_be_clickable((By.ID, "2G_BASIC_SUBMIT"))
            ).click()

            # MODAL #
            WebDriverWait(_chorme, 30).until(
                EC.invisibility_of_element_located((By.ID, "waiting_animation"))
            )

            time.sleep(1)
            logging.info("4.5 - informando a nova senha do wifi 2.4")
            senha_booth_input = _chorme.find_element(By.ID, "B_pskValue")
            senha_booth_input.clear()
            senha_booth_input.send_keys(newPasswordSSID)

            WebDriverWait(_chorme, 30).until(
                EC.invisibility_of_element_located((By.ID, "waiting_animation"))
            )

            time.sleep(1)
            logging.info("4.6 - Salvando a nova senha")
            WebDriverWait(_chorme, 30).until(
                EC.element_to_be_clickable((By.ID, "2G_SECURITY_CONFIG_SUBMIT"))
            ).click()

            # MODAL #
            WebDriverWait(_chorme, 30).until(
                EC.invisibility_of_element_located((By.ID, "waiting_animation"))
            )
            

            # 5.0 Ghz wifi
            time.sleep(1)
            logging.info("5 - Acessando item do menu para config do wifi 5.0 Ghz")
            WebDriverWait(_chorme, 30).until(
                EC.presence_of_element_located((By.ID, "net_5g"))
            )
            WebDriverWait(_chorme, 30).until(
                EC.element_to_be_clickable((By.ID, "net_5g"))
            ).click()

            WebDriverWait(_chorme, 30).until(
                EC.presence_of_element_located((By.ID, "B_ssid"))
            )

            WebDriverWait(_chorme, 30).until(
                EC.presence_of_element_located((By.ID, "EM_Config_submit"))
            )

            time.sleep(1)
            logging.info("5.1 - Alterando o ssid para o novo wifi 5.0 Ghz")
            ssid_input = _chorme.find_element(By.ID, "B_ssid")
            for _ in range(150):
                ssid_input.send_keys(Keys.BACKSPACE)
            ssid_input.send_keys(newNameSSID+"_5G")

            WebDriverWait(_chorme, 30).until(
                EC.invisibility_of_element_located((By.ID, "waiting_animation"))
            )

            WebDriverWait(_chorme, 30).until(
                EC.presence_of_element_located((By.ID, "5G_BASIC_SUBMIT"))
            )

            time.sleep(1)
            logging.info("5.2 - Salvando o novo ssid")
            WebDriverWait(_chorme, 30).until(
                EC.element_to_be_clickable((By.ID, "5G_BASIC_SUBMIT"))
            ).click()

            # MODAL #
            WebDriverWait(_chorme, 30).until(
                EC.invisibility_of_element_located((By.ID, "waiting_animation"))
            )

            time.sleep(1)
            logging.info("5.3 - Informando a nova senha do wifi 5.0 Ghz")
            senha_booth_input = _chorme.find_element(By.ID, "B_pskValue")
            senha_booth_input.clear()
            senha_booth_input.send_keys(newPasswordSSID)

            time.sleep(1)
            logging.info("5.4 - Salvando a nova senha")
            WebDriverWait(_chorme, 30).until(
                EC.element_to_be_clickable((By.ID, "5G_SECURITY_CONFIG_SUBMIT"))
            ).click()
            
            # MODAL #
            WebDriverWait(_chorme, 30).until(
                EC.invisibility_of_element_located((By.ID, "waiting_animation"))
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

def esta_visivel(driver, by, seletor):
    try:
        elemento = driver.find_element(by, seletor)
        return elemento.is_displayed()
    except Exception as e:
        return False