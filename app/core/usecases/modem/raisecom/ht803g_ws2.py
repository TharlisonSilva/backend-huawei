import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import logging

class ht803g_ws2:

    def change_password(_chorme, newNameSSID, newPasswordSSID):
        try:

            logging.info("4 - Verificando se pagian já está logada!")
            iframe = _chorme.find_element(By.NAME, "topFrame")
            _chorme.switch_to.frame(iframe)

            logging.info("4.1 - Acessando menu de configuração WLAN ")
            _chorme.find_element(By.XPATH, "//tr[@id='topmenu']/td[2]").click()

            logging.info("4.1 - Acessando mainFrame para conseguir acessar os inputs")
            _chorme.switch_to.default_content()
            iframe = _chorme.find_element(By.NAME, "mainFrame")
            _chorme.switch_to.frame(iframe)
            
            WebDriverWait(_chorme, 20).until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='text' and @name='ssid']"))
            )

            logging.info("4.2 - Acessando campo ssid do WIFI 2.4ghz.")
            ssid_24_input = _chorme.find_element(By.XPATH, "//input[@type='text' and @name='ssid']")
            for _ in range(150):
                ssid_24_input.send_keys(Keys.BACKSPACE)
            ssid_24_input.send_keys(newNameSSID)
            
            logging.info("4.3 - Informando a nova senha no input!")
            senha_booth_input = _chorme.find_element(By.ID, "wpapsk")
            senha_booth_input.clear()
            senha_booth_input.send_keys(newPasswordSSID)

            logging.info("4.4 - Aplicando as alterações WIFI 2.4ghz.")
            _chorme.find_element(By.XPATH, "//input[@type='button' and @value='Confirm']").click()

            _chorme.switch_to.default_content()
            
            # WIFI 5.0 # 

            logging.info("5 - Acenssando menu WIFI 5.0Ghz.")
            iframe = _chorme.find_element(By.NAME, "topFrame")
            _chorme.switch_to.frame(iframe)

            logging.info("5.1 - clicando no item do menu WIFI 5.0Ghz.")
            _chorme.find_element(By.XPATH, "//tr[@id='submenu']/td[5]/p/a").click()
            
            logging.info("5.2 - carregando mainFrame para acessar os inputs")
            _chorme.switch_to.default_content()
            iframe = _chorme.find_element(By.NAME, "mainFrame")
            _chorme.switch_to.frame(iframe)

            logging.info("5.3 - Aguardando os campos carregarem.")
            if esperar_texto_em_tag(_chorme, "td", "-5G") :
                WebDriverWait(_chorme, 20).until(
                    EC.presence_of_element_located((By.XPATH, "//input[@type='text' and @name='ssid']"))
                )
            
            logging.info("5.4 - Informando o SSID do wifi 5.0Ghz.")
            ssid_50_input = _chorme.find_element(By.XPATH, "//input[@type='text' and @name='ssid']")
            for _ in range(150):
                ssid_50_input.send_keys(Keys.BACKSPACE)
            ssid_50_input.send_keys(newNameSSID)
            
            logging.info("5.5 - Informando a nova senha no input!")
            senha_50_input = _chorme.find_element(By.ID, "wpapsk")
            senha_50_input.clear()
            senha_50_input.send_keys(newPasswordSSID)

            logging.info("5.6 - Aplicando as alterações!")
            _chorme.find_element(By.XPATH, "//input[@type='button' and @value='Confirm']").click()
            
            time.sleep(6)
            _chorme.switch_to.default_content()

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