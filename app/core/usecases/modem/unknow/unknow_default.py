from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import logging


class unknow_default:

    def force_close(_chorme):
        try:
            WebDriverWait(_chorme, 5).until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='submit' and @value='Sair']"))
            ).click()
            logging.info("Close 1 - Deslogado!")

        except Exception as e:
            logging.info("Close 1 - Não logado!")

        try:
            
            iframe = _chorme.find_element(By.NAME, "topFrame")
            _chorme.switch_to.frame(iframe)

            WebDriverWait(_chorme, 5).until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='submit' and @value='Logout']"))
            ).click()
            logging.info("Close 2 - Deslogado!")

        except Exception as e:
            logging.info("Close 2 - Não logado!")

        try:
            WebDriverWait(_chorme, 5).until(
                EC.presence_of_element_located((By.ID, "Logout_button"))
            ).click()
            logging.info("Close 3 - Deslogado!")

        except Exception as e:
            logging.info("Close 3 - Não logado!")

    def check_login_v__AX1500ONT(_chorme, host_login, port_login, username_login, password_login):
        try:
            urlLogin = "http://"+host_login+":"+port_login
            _chorme.get(urlLogin)

            if esta_visivel(_chorme, By.ID, "canvas") and esta_visivel(_chorme, By.ID, "text") :
                return False
            
            _chorme.find_element(By.XPATH, "//input[@type='text']").clear()
            _chorme.find_element(By.XPATH, "//input[@type='text']").send_keys(username_login)
            
            _chorme.find_element(By.XPATH, "//input[@type='password']").clear()
            _chorme.find_element(By.XPATH, "//input[@type='password']").send_keys(password_login)
            _chorme.find_element(By.XPATH, "//input[@type='submit']").click()
            
            WebDriverWait(_chorme, 10).until(
                EC.invisibility_of_element_located((By.XPATH, "//input[@type='password']"))
            )

            if "Erro" in _chorme.page_source or "ERROR" in _chorme.page_source  or "bad password" in _chorme.page_source: 
                _chorme.get(urlLogin)
                return False
            
            else:
                try:

                    tryVersion = _chorme.title.replace(" ","")
                    if(tryVersion in "AX1500ONT"):
                        return True
                    
                except Exception as e:
                    return ""

        except Exception as e:
            return False
        
    def check_login_raisecom_v__HT803G_WS2(_chorme, host_login, port_login, username_login, password_login):
        try:
            urlLogin = "http://"+host_login+":"+port_login
            _chorme.get(urlLogin)

            if esta_visivel(_chorme, By.ID, "canvas") and esta_visivel(_chorme, By.ID, "text") :
                return False

            _chorme.find_element(By.XPATH, "//input[@id='username1']").clear()
            _chorme.find_element(By.XPATH, "//input[@id='username1']").send_keys(username_login)

            _chorme.find_element(By.XPATH, "//input[@id='psd1']").clear()
            _chorme.find_element(By.XPATH, "//input[@id='psd1']").send_keys(password_login)
            _chorme.find_element(By.XPATH, "//input[@type='button' and @value='Login']").click()
            
            WebDriverWait(_chorme, 10).until(
                EC.presence_of_element_located((By.XPATH, "//frame[@name='mainFrame']"))
            )

            iframe = _chorme.find_element(By.NAME, "mainFrame")
            _chorme.switch_to.frame(iframe)

            WebDriverWait(_chorme, 10).until(
                EC.presence_of_element_located((By.XPATH, "//table[@class='flat']/tbody/tr/td[text()='HT803G-WS2']"))
            )

            _chorme.switch_to.default_content()

            return True

        except Exception as e:
            return False
        
    def check_login_Think_v__TKONU2PDPX(_chorme, host_login, port_login, username_login, password_login):
        try:
            urlLogin = "http://"+host_login+":"+port_login
            _chorme.get(urlLogin)

            if esta_visivel(_chorme, By.ID, "canvas") and esta_visivel(_chorme, By.ID, "text") :
                return False

            _chorme.find_element(By.XPATH, "//input[@type='text']").clear()
            _chorme.find_element(By.XPATH, "//input[@type='text']").send_keys(username_login)
            
            _chorme.find_element(By.XPATH, "//input[@type='password']").clear()
            _chorme.find_element(By.XPATH, "//input[@type='password']").send_keys(password_login)
            _chorme.find_element(By.ID, "LoginId").click()
            
            WebDriverWait(_chorme, 10).until(
                EC.invisibility_of_element_located((By.ID, "mainFrame']"))
            )

            tryVersion = _chorme.title.replace(" ","")
            if(tryVersion in "TKONU2PDPX"):
                return True

        except Exception as e:
            return False

    def check_login_VSOL_v__V2804AX(_chorme, host_login, port_login, username_login, password_login):
        try:

            if esta_visivel(_chorme, By.ID, "basic_info_row") :
                td = _chorme.find_element(By.XPATH, "//table[@id='basic_info_table']/tbody/tr/td[2]")
                if td.text == "V2804AX" :
                    return True
                
            urlLogin = "http://"+host_login+":"+port_login
            _chorme.get(urlLogin)

            WebDriverWait(_chorme, 10).until(
                EC.presence_of_element_located((By.ID, "login_username"))
            )

            WebDriverWait(_chorme, 15).until(
                lambda d: _chorme.execute_script("return typeof show_num !== 'undefined';")
            )
            
            WebDriverWait(_chorme, 15).until(
                lambda d: _chorme.execute_script("return typeof show_num !== [];")
            )

            itens_captcha = []
            while itens_captcha == [] :
                itens_captcha = _chorme.execute_script("return show_num;")
                CAPTCHA = ""
                for i in itens_captcha :
                    CAPTCHA += i

            logging.info("CAPTCHA: ["+CAPTCHA+"]")
            _chorme.find_element(By.ID, "login_username").clear()
            _chorme.find_element(By.ID, "login_username").send_keys(username_login)

            _chorme.find_element(By.ID, "login_password").clear()
            _chorme.find_element(By.ID, "login_password").send_keys(password_login)

            _chorme.find_element(By.ID, "text").clear()
            _chorme.find_element(By.ID, "text").send_keys(CAPTCHA)

            _chorme.find_element(By.ID, "Login_Button").click()
            
            WebDriverWait(_chorme, 10).until(
                EC.presence_of_element_located((By.ID, "basic_info_row"))
            )

            td = _chorme.find_element(By.XPATH, "//table[@id='basic_info_table']/tbody/tr/td[2]")
            if td.text == "V2804AX" :
                return True
            
            return False        

        except Exception as e:
            return False
            
    def check_login_VSOL_v__V2804AC_Z(_chorme, host_login, port_login, username_login, password_login):
        try:

            if esta_visivel(_chorme, By.ID, "dataTable") :
                td = _chorme.find_element(By.ID, "devModel")
                if td.text == "V2804AC-Z" :
                    return True
                
            urlLogin = "http://"+host_login+":"+port_login
            _chorme.get(urlLogin)

            WebDriverWait(_chorme, 10).until(
                EC.presence_of_element_located((By.ID, "login_username"))
            )

            WebDriverWait(_chorme, 15).until(
                lambda d: _chorme.execute_script("return typeof show_num !== 'undefined';")
            )
            
            WebDriverWait(_chorme, 15).until(
                lambda d: _chorme.execute_script("return typeof show_num !== [];")
            )

            itens_captcha = []
            while itens_captcha == [] :
                itens_captcha = _chorme.execute_script("return show_num;")
                CAPTCHA = ""
                for i in itens_captcha :
                    CAPTCHA += i

            logging.info("CAPTCHA: ["+CAPTCHA+"]")
            _chorme.find_element(By.ID, "login_username").clear()
            _chorme.find_element(By.ID, "login_username").send_keys(username_login)

            _chorme.find_element(By.ID, "login_password").clear()
            _chorme.find_element(By.ID, "login_password").send_keys(password_login)

            _chorme.find_element(By.ID, "text").clear()
            _chorme.find_element(By.ID, "text").send_keys(CAPTCHA)

            _chorme.find_element(By.ID, "Login_Button").click()
            
            WebDriverWait(_chorme, 10).until(
                EC.presence_of_element_located((By.ID, "basic_info_row"))
            )

            td = _chorme.find_element(By.ID, "devModel")
            if td.text == "V2804AC-Z" :
                return True
            
            return False        

        except Exception as e:
            return False
        

def esta_visivel(driver, by, seletor):
    try:
        elemento = driver.find_element(by, seletor)
        return elemento.is_displayed()
    except Exception as e:
        return False