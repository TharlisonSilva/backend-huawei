from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import logging

class shoreline_default:

    def check_login(_chorme, host_login, port_login, username_login, password_login):
        try:
            urlLogin = "http://"+host_login+":"+port_login
            _chorme.get(urlLogin)

            if "user_name" in _chorme.page_source :    
                WebDriverWait(_chorme, 10).until(
                    EC.presence_of_element_located((By.ID, "user_name"))
                )

                _chorme.find_element(By.ID, "user_name").send_keys(username_login)
                _chorme.find_element(By.XPATH, "//input[@type='password']").send_keys(password_login)
                _chorme.find_element(By.ID, "btn_login").click()
            
            WebDriverWait(_chorme, 20).until(
                EC.presence_of_element_located((By.ID, "DiagnosticRefresh"))
            )
            
            return True

        except Exception as e:
            print("❌ Erro ao configurar o Wi-Fi:", e)
            return False
        
    def change_password_SH1505W(_chorme, host_login, port_login, username_login, password_login, newNameSSID, newPasswordSSID):
        try:

            urlLogin = "http://"+host_login+":"+port_login
            _chorme.get(urlLogin)
            logging.info("4 - Acessando pagina de login: [ "+urlLogin+" ]")
            
            if "user_name" in _chorme.page_source :
                
                logging.info("4.1 - Efetuando login na página")
                WebDriverWait(_chorme, 10).until(
                    EC.presence_of_element_located((By.ID, "user_name"))
                )

                _chorme.find_element(By.ID, "user_name").send_keys(username_login)
                _chorme.find_element(By.XPATH, "//input[@type='password']").send_keys(password_login)
                _chorme.find_element(By.ID, "btn_login").click()

                logging.info("4.2 - Login efetuado!")
            else:
                logging.info("4.1 - Página já estava autenticada, com login feito!")


            logging.info("5 - Acessando menu de configuração WLAN ")
            _chorme.find_element(By.XPATH, "//ul[@id='nav']/li/a[text()='WLAN']").click()
            WebDriverWait(_chorme, 20).until(
                EC.presence_of_element_located((By.ID, "side"))
            )

            logging.info("5.1 - Acessando regra de configuração dupla de WIFI 2.4ghz e 5ghz ")
            iframe = _chorme.find_element(By.ID, "contentIframe")
            _chorme.switch_to.frame(iframe)

            WebDriverWait(_chorme, 20).until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='text' and @name='bsSSID']"))
            )

            logging.info("5.2 - Verificando o checkbox de unificar redes ")
            _chorme.find_element(By.XPATH, "//input[@name='bsEnabled' and @value='1']").click()

            logging.info("5.3 - Acessando o campo SSID para por o novo nome!")
            ssid_booth_input = _chorme.find_element(By.XPATH, "//input[@type='text' and @name='bsSSID']")
            for _ in range(150):
                ssid_booth_input.send_keys(Keys.BACKSPACE)
            ssid_booth_input.send_keys(newNameSSID)
            
            logging.info("5.4 - Informando a nova senha no input!")
            senha_booth_input = _chorme.find_element(By.XPATH, "//input[@type='password' and @name='bsPSK']")
            senha_booth_input.clear()
            senha_booth_input.send_keys(newPasswordSSID)
            
            logging.info("5.5 - Aplicando as alterações!")
            _chorme.find_element(By.XPATH, "//input[@type='submit' and @name='apply']").click()
            WebDriverWait(_chorme, 25).until(
                EC.presence_of_element_located((By.XPATH, "//blockquote//input[@type='button' and @value='OK']"))
            ).click()

            logging.info("5.6 - Modificações aplicadas!")
            _chorme.switch_to.default_content()

            logging.info("6 - Modificações feitas com sucesso!")
            return True
        
        except Exception as e:
            print("❌ Erro ao configurar o Wi-Fi:", e)
            return False
        
        finally:
            _chorme.quit()

    def change_password_SH1015W_and_SH3000WF(_chorme, host_login, port_login, username_login, password_login, newNameSSID, newPasswordSSID, unificarRedes):
        try:

            urlLogin = "http://"+host_login+":"+port_login
            _chorme.get(urlLogin)
            logging.info("4 - Acessando pagina de login: [ "+urlLogin+" ]")
            
            if "user_name" in _chorme.page_source :
                
                logging.info("4.1 - Efetuando login na página")
                WebDriverWait(_chorme, 10).until(
                    EC.presence_of_element_located((By.ID, "user_name"))
                )

                _chorme.find_element(By.ID, "user_name").send_keys(username_login)
                _chorme.find_element(By.XPATH, "//input[@type='password']").send_keys(password_login)
                _chorme.find_element(By.ID, "btn_login").click()

                logging.info("4.2 - Login efetuado!")
            else:
                logging.info("4.1 - Página já estava autenticada, com login feito!")

            WebDriverWait(_chorme, 20).until(
                EC.presence_of_element_located((By.ID, "DiagnosticRefresh"))
            )

            logging.info("5 - Acessando menu de configuração WLAN ")
            _chorme.find_element(By.XPATH, "//ul[@id='menu1levelNavlist']/li/a[text()='Wlan']").click()
            WebDriverWait(_chorme, 20).until(
                EC.presence_of_element_located((By.ID, "Menu3_WLAN_BandSteering"))
            )

            if unificarRedes:
                
                logging.info("5.1 - Acessando regra de configuração dupla de WIFI 2.4ghz e 5ghz ")
                iframe = _chorme.find_element(By.ID, "mainFrame")
                _chorme.switch_to.frame(iframe)

                WebDriverWait(_chorme, 20).until(
                    EC.presence_of_element_located((By.ID, "ssid"))
                )

                logging.info("5.2 - Verificando o checkbox de unificar redes ")
                check = _chorme.find_element(By.ID, "bandsteering")
                if not check.is_selected():
                    _chorme.find_element(By.ID, "bandsteering").click()


                logging.info("5.3 - Acessando o campo SSID para por o novo nome!")
                ssid_booth_input = _chorme.find_element(By.ID, "ssid")
                for _ in range(150):
                    ssid_booth_input.send_keys(Keys.BACKSPACE)
                ssid_booth_input.send_keys(newNameSSID)
                
                logging.info("5.4 - Informando a nova senha no input!")
                senha_booth_input = _chorme.find_element(By.ID, "wapiPskValue")
                senha_booth_input.clear()
                senha_booth_input.send_keys(newPasswordSSID)
                
                logging.info("5.5 - Aplicando as alterações!")
                _chorme.find_element(By.ID, "ApplyChanges").click()
                WebDriverWait(_chorme, 25).until(
                    EC.invisibility_of_element_located((By.ID, "progressBox"))
                )

                logging.info("5.6 - Modificações aplicadas!")
                _chorme.switch_to.default_content()

            else:
                
                ## WIFI 2.4Gz
                ## SSID
                logging.info("5.1 - Acessando menu de configuração WLAN 2.4ghz ")
                _chorme.find_element(By.ID, "Menu2_WLAN_2GHz").click()

                logging.info("5.2 - Acessando Acessando iframe ")
                iframe = _chorme.find_element(By.ID, "mainFrame")
                _chorme.switch_to.frame(iframe)
                WebDriverWait(_chorme, 20).until(
                    EC.presence_of_element_located((By.ID, "ApplyChanges"))
                )

                logging.info("5.3 - Acessando campon ssid para por o novo nome da rede wifi")
                ssid_24_input = _chorme.find_element(By.XPATH, "//input[@name='ssid']")
                for _ in range(150):
                    ssid_24_input.send_keys(Keys.BACKSPACE)
                ssid_24_input.send_keys(newNameSSID)

                logging.info("5.4 - Salvando o novo nome da rede wifi 2.4ghz")
                _chorme.find_element(By.ID, "ApplyChanges").click()
                WebDriverWait(_chorme, 25).until(
                    EC.invisibility_of_element_located((By.ID, "progressBox"))
                )

                ## WIFI 2.4Gz
                ## PASSWORD
                logging.info("5.5 - Saindo do iframe para clicar no item do menu password")
                _chorme.switch_to.default_content()
                _chorme.find_element(By.ID, "Menu3_WLAN_Security").click()
                iframe = _chorme.find_element(By.ID, "mainFrame")
                _chorme.switch_to.frame(iframe)
                
                logging.info("5.6 - Acessando campon password[wpapsk] para por a nova senha")
                sleep(1)
                senha_24_input = _chorme.find_element(By.ID, "wpapsk")
                senha_24_input.clear()
                senha_24_input.send_keys(newPasswordSSID)

                logging.info("5.7 - Salvando a nova configuração de senha da rede 2.4ghz")
                _chorme.find_element(By.ID, "ApplyChanges").click()
                WebDriverWait(_chorme, 25).until(
                    EC.invisibility_of_element_located((By.ID, "progressBox"))
                )



                ## WIFI 5Gz
                ## SSID
                logging.info("5.8 - Acessando menu de configuração WLAN 5.0ghz ")
                _chorme.switch_to.default_content()
                _chorme.find_element(By.ID, "Menu2_WLAN_5GHz").click()

                logging.info("5.9 - Acessando Acessando iframe ")
                iframe = _chorme.find_element(By.ID, "mainFrame")
                _chorme.switch_to.frame(iframe)
                WebDriverWait(_chorme, 25).until(
                    EC.presence_of_element_located((By.ID, "ApplyChanges"))
                )

                logging.info("5.10 - Acessando campon ssid para por o novo nome da rede wifi")
                ssid_25_input = _chorme.find_element(By.XPATH, "//input[@name='ssid']")
                for _ in range(150):
                    ssid_25_input.send_keys(Keys.BACKSPACE)
                ssid_25_input.send_keys(newNameSSID)

                logging.info("5.11 - Salvando o novo nome da rede wifi 5.0ghz")
                _chorme.find_element(By.ID, "ApplyChanges").click()
                WebDriverWait(_chorme, 25).until(
                    EC.invisibility_of_element_located((By.ID, "progressBox"))
                )
                
                ## WIFI 5Gz
                ## PASSWORD
                logging.info("5.12 - Saindo do iframe para clicar no item do menu password")
                _chorme.switch_to.default_content()
                _chorme.find_element(By.ID, "Menu3_WLAN_Security").click()
                iframe = _chorme.find_element(By.ID, "mainFrame")
                _chorme.switch_to.frame(iframe)
                sleep(1)
                
                logging.info("5.13 - Acessando campon password[wpapsk] para por a nova senha")
                senha_25_input = _chorme.find_element(By.ID, "wpapsk")
                senha_25_input.clear()
                senha_25_input.send_keys(newPasswordSSID)

                logging.info("5.14 - Salvando a nova configuração de senha da rede 5.0ghz")
                _chorme.find_element(By.ID, "ApplyChanges").click()
                WebDriverWait(_chorme, 25).until(
                    EC.invisibility_of_element_located((By.ID, "progressBox"))
                )

            logging.info("6 - Modificações feitas com sucesso!")
            return True
        
        except Exception as e:
            print("❌ Erro ao configurar o Wi-Fi:", e)
            return False
        
        finally:
            _chorme.quit()