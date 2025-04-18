import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import logging


class ax2:

    def check_login(_chorme, host_login, port_login, username_login, password_login):
        try:
            _chorme.get("http://"+host_login+":"+port_login)
            WebDriverWait(_chorme, 10).until(
                EC.presence_of_element_located((By.ID, "userpassword_ctrl"))
            )

            _chorme.find_element(By.ID, "userpassword_ctrl").clear()
            _chorme.find_element(By.ID, "userpassword_ctrl").send_keys(password_login)
            _chorme.find_element(By.ID, "loginbtn").click()        

            WebDriverWait(_chorme, 20).until(
                EC.presence_of_element_located((By.ID, "wifi"))
            )
            
            return True

        except Exception as e:
            print("❌ Erro ao configurar o Wi-Fi:", e)
            return False

    def change_password(_chorme, newNameSSID, newPasswordSSID, unificarRedes):
        try:

            _chorme.refresh()
            _chorme.switch_to.default_content()

            time.sleep(1)
            logging.info("4 - Verificando se pagina já está logada!")
            WebDriverWait(_chorme, 30).until(
                EC.element_to_be_clickable((By.ID, "wifi"))
            ).click()

            # MODAL #
            WebDriverWait(_chorme, 30).until(
                EC.invisibility_of_element_located((By.ID, "loading"))
            )

            if unificarRedes : 
                
                time.sleep(1)
                logging.info("4.1 - Verificando se deve unificar as redes wifi.")
                if esta_visivel(_chorme, By.ID, "dbhoOff_btnId") :
                    check = _chorme.find_element(By.ID, "dbhoOff_btnId")
                    classes = check.get_attribute("class")
                    if "btn_on" not in classes.split():
                        check.click()

                    # MODAL - para confirmar que deseja unificar mesmo.
                    if esta_visivel(_chorme, By.ID, "wlandbhonoticewin") : 
                        WebDriverWait(_chorme, 30).until(
                            EC.element_to_be_clickable((By.ID, "wlandbhonoticewin"))
                        ).click()

                    if esta_visivel(_chorme, By.ID, "wifi_dbhoonnoticecontinue") : 
                        WebDriverWait(_chorme, 30).until(
                            EC.element_to_be_clickable((By.ID, "wifi_dbhoonnoticecontinue"))
                        ).click()
                
                # MODAL - Loading
                WebDriverWait(_chorme, 30).until(
                    EC.invisibility_of_element_located((By.ID, "loading"))
                )

                WebDriverWait(_chorme, 15).until(
                    EC.presence_of_element_located((By.ID, "content_wifi_name2G_ctrl"))
                )

                logging.info("4.2 - Informando o novo nome da rede wifi")
                ssid_input = _chorme.find_element(By.ID, "content_wifi_name2G_ctrl")
                for _ in range(150):
                    ssid_input.send_keys(Keys.BACKSPACE)
                ssid_input.send_keys(newNameSSID)

                logging.info("4.3 - Informando a nova senha para as redes unificadas.")
                senha_input = _chorme.find_element(By.ID, "content_wifi_password2G_ctrl")
                senha_input.clear()
                senha_input.send_keys(newPasswordSSID)

            else :
                time.sleep(3)
                logging.info("4.1 - Verificando se deve desfazer a unificação das redes wifi.")
                if esta_visivel(_chorme, By.ID, "dbhoOn_btnId") :
                    check = _chorme.find_element(By.ID, "dbhoOn_btnId")
                    classes = check.get_attribute("class")
                    if "btn_on" in classes.split():
                        check.click()

                    # MODAL - Loading
                    WebDriverWait(_chorme, 30).until(
                        EC.invisibility_of_element_located((By.ID, "loading"))
                    )
                
                WebDriverWait(_chorme, 15).until(
                    EC.presence_of_element_located((By.ID, "content_wifi_name2G_ctrl"))
                )

                # 2.4 Ghz
                time.sleep(1)
                logging.info("4.2 - Iniciando configuração do ssid wifi 2.4 Ghz.")
                ssid_24_input = _chorme.find_element(By.ID, "content_wifi_name2G_ctrl")
                for _ in range(150):
                    ssid_24_input.send_keys(Keys.BACKSPACE)
                ssid_24_input.send_keys(newNameSSID)

                time.sleep(1)
                logging.info("4.3 - Iniciando configuração do pass wifi 2.4 Ghz.")
                senha_24_input = _chorme.find_element(By.ID, "content_wifi_password2G_ctrl")
                senha_24_input.clear()
                senha_24_input.send_keys(newPasswordSSID)


                # 5.0 Ghz
                time.sleep(1)
                logging.info("4.4 - Iniciando configuração do ssid wifi 5.0 Ghz.")
                ssid_50_input = _chorme.find_element(By.ID, "content_wifi_name5G_ctrl")
                for _ in range(150):
                    ssid_50_input.send_keys(Keys.BACKSPACE)
                ssid_50_input.send_keys(newNameSSID+"_5G")
                
                time.sleep(1)
                logging.info("4.5 - Iniciando configuração do pass wifi 5.0 Ghz.")
                senha_50_input = _chorme.find_element(By.ID, "content_wifi_password5G_ctrl")
                senha_50_input.clear()
                senha_50_input.send_keys(newPasswordSSID)
            

            time.sleep(1)
            logging.info("5 - Verificando se botão está disponivel para click.")
            WebDriverWait(_chorme, 30).until(
                EC.element_to_be_clickable((By.ID, "SsidSettings_submitbutton"))
            ).click()

            # MODAL #
            WebDriverWait(_chorme, 30).until(
                EC.invisibility_of_element_located((By.ID, "loading"))
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
    
def aguardar_modem_pos_envio(driver, botao_id, cooldown=20, timeout=20):
    
    WebDriverWait(driver, timeout).until(
        EC.invisibility_of_element_located((By.ID, "waiting_animation"))
    )

    WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((By.ID, botao_id))
    )

    time.sleep(cooldown)