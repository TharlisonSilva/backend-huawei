import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoAlertPresentException
import logging

class eg8145x6_10:

    def check_login(_chorme, host_login, port_login, username_login, password_login):
        try:
            _chorme.get("http://"+host_login+":"+port_login)
            WebDriverWait(_chorme, 10).until(
                EC.presence_of_element_located((By.ID, "txt_Username"))
            )

            _chorme.find_element(By.ID, "txt_Username").clear()
            _chorme.find_element(By.ID, "txt_Username").send_keys(username_login)

            _chorme.find_element(By.ID, "txt_Password").clear()
            _chorme.find_element(By.ID, "txt_Password").send_keys(password_login)
            
            WebDriverWait(_chorme, 30).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@id='loginbuttondiv']/div/input[@id='loginbutton']"))
            ).click()

            try:
                alert = _chorme.switch_to.alert
                alert.accept()
            except NoAlertPresentException:
                pass

            WebDriverWait(_chorme, 20).until(
                EC.presence_of_element_located((By.ID, "menuIframe"))
            )
            
            return True

        except Exception as e:
            print("❌ Erro ao configurar o Wi-Fi:", e)
            return False

    def change_password(_chorme, newNameSSID, newPasswordSSID, unificarRedes):
        try:

            _chorme.switch_to.default_content()
            iframe = _chorme.find_element(By.ID, "menuIframe")
            _chorme.switch_to.frame(iframe)

            time.sleep(1)
            logging.info("4 - Verificando se pagina já está logada!")
            WebDriverWait(_chorme, 30).until(
                EC.element_to_be_clickable((By.ID, "WIFIIconInfo"))
            ).click()

            WebDriverWait(_chorme, 15).until(
                EC.presence_of_element_located((By.ID, "ConfigWifiPageSrc"))
            )

            iframe = _chorme.find_element(By.ID, "ConfigWifiPageSrc")
            _chorme.switch_to.frame(iframe)
            
            WebDriverWait(_chorme, 15).until(
                EC.presence_of_element_located((By.ID, "txt_2g_wifiname"))
            )

            logging.info("4.2 - Informando o novo nome da rede wifi")
            ssid_input = _chorme.find_element(By.ID, "txt_2g_wifiname")
            for _ in range(150):
                ssid_input.send_keys(Keys.BACKSPACE)
            ssid_input.send_keys(newNameSSID)

            time.sleep(1)
            logging.info("4.3 - Informando a nova senha para as redes unificadas.")
            senha_input = _chorme.find_element(By.ID, "pwd_2g_wifipwd")
            senha_input.clear()
            senha_input.send_keys(newPasswordSSID)
            
            time.sleep(1)
            logging.info("4.2 - Informando o novo nome da rede wifi")
            ssid_input = _chorme.find_element(By.ID, "txt_5g_wifiname")
            for _ in range(150):
                ssid_input.send_keys(Keys.BACKSPACE)
            ssid_input.send_keys(newNameSSID+"-5G")

            time.sleep(1)
            logging.info("4.3 - Informando a nova senha para as redes unificadas.")
            senha_input = _chorme.find_element(By.ID, "pwd_5g_wifipwd")
            senha_input.clear()
            senha_input.send_keys(newPasswordSSID)

            # WebDriverWait(_chorme, 30).until(
            #     EC.element_to_be_clickable((By.ID, "btnSave"))
            # ).click()
            
            time.sleep(3)
            
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
    
def aguardar_modem_pos_envio(driver, botao_id, cooldown=20, timeout=20):
    
    WebDriverWait(driver, timeout).until(
        EC.invisibility_of_element_located((By.ID, "waiting_animation"))
    )

    WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((By.ID, botao_id))
    )

    time.sleep(cooldown)