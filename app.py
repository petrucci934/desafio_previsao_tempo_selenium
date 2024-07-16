import os
from time import sleep
import schedule
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from dotenv import load_dotenv
from email_sender import Emailer

def iniciar_driver():
    chrome_options = Options()
    chrome_options.add_argument("--lang=pt-BR")
    chrome_options.add_argument("--window-size=800,1000")
    chrome_options.add_experimental_option(
        "prefs",
        {
            "download.default_directory": "desafio_selenium/download",
            "download.directory_upgrade": True,
            "download.prompt_for_download": False,
            "profile.default_content_setting_values.notifications": 2,
            "profile.default_content_setting_values.automatic_downloads": 1,
        }
    )
    try:
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
        wait = WebDriverWait(driver, 10, poll_frequency=1, ignored_exceptions=[NoSuchElementException])
        return driver, wait
    except Exception as e:
        print("Ocorreu um erro ao iniciar o driver:", e)
        return None, None

def obter_informacoes_climaticas(driver):
    try:
        elementos = {
            "current_date": "//span[contains(@class,'module-header sub date')]",
            "current_day": "//span[contains(@class,'module-header dow date')]",
            "current_temp": "//span[contains(@class, 'high')]",
            "current_condition": "//div[contains(@class, 'phrase')]"
        }
        info = {key: driver.find_element(By.XPATH, xpath).text for key, xpath in elementos.items()}
        
        daily_cards_info = []
        for i in range(1, 4):
            daily_card = driver.find_element(By.XPATH, f"//*[@data-qa='dailyCard{i}']")
            daily_info = {
                "next_date": daily_card.find_element(By.XPATH, ".//span[contains(@class, 'module-header sub date')]").text,
                "next_day": daily_card.find_element(By.XPATH, ".//span[contains(@class, 'module-header dow date')]").text,
                "next_temp": daily_card.find_element(By.XPATH, ".//span[contains(@class, 'high')]").text,
                "next_condition": daily_card.find_element(By.XPATH, ".//div[contains(@class, 'phrase')]").text,
            }
            daily_cards_info.append(daily_info)

        return info, daily_cards_info
    except NoSuchElementException as e:
        print(f"Erro: elemento não encontrado - {e}")
        return None, None

def imprimir_informacoes(info, daily_cards_info, driver):
    print("##########################################################")
    print("Título da página:", driver.title)
    print("----------------------------------------------------------")
    print(info['current_date'], info['current_day'])
    print("Tempo agora em Igaratá, SP:", info['current_temp'])
    print("Condição atual:", info['current_condition'])
    print("#########################################################")
    sleep(6)
    print("Condições para os próximos 3 dias")
    for card in daily_cards_info:
        print("#########################################################")
        print(card['next_date'], card['next_day'])
        print("Tempo Igaratá, SP:", card['next_temp'])
        print("Condição no dia:", card['next_condition'])

def enviar_email(info, daily_cards_info):
    load_dotenv()
    EMAIL_ADDRESS = os.getenv("EMAIL_USER")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASS")

    email = Emailer(EMAIL_ADDRESS, EMAIL_PASSWORD)
    lista_contatos = ["petrucci.lucenaplc@gmail.com"]

    try:
        daily_cards_html = "".join([
            f"""
            ####################################################<br>
            Data: {card['next_date']}<br>
            Dia: {card['next_day']}<br>
            Tempo em Igaratá, SP: {card['next_temp']}<br>
            Condição no dia: {card['next_condition']}<br>
            """ for card in daily_cards_info
        ])
        mensagem = f"""
        <html>
        <body>
        <h1>Previsão do Tempo Atual</h1><br>
        Data: {info['current_date']}<br>
        Dia: {info['current_day']}<br>
        Tempo em Igaratá, SP: {info['current_temp']}<br>
        Condição no dia: {info['current_condition']}<br>
        ####################################################<br>
        <h2>Previsão do Tempo para os Próximos 3 Dias:</h2><br>
        {daily_cards_html}
        </body>
        </html>
        """
        email.definir_conteudo(
            topico="Previsão do Tempo Igaratá-SP!",
            email_remetente=EMAIL_ADDRESS,
            lista_contatos=lista_contatos,
            conteudo_email=mensagem,
        )
        email.enviar_email(intervalo_em_segundos=30)
        print(f"Email enviado para {lista_contatos}")
    except Exception as e:
        print(f"Erro ao enviar email para {lista_contatos}: {e}")
        

def executar_tarefa():
    driver, wait = iniciar_driver()
    if driver is not None:
        driver.get("https://www.accuweather.com/pt/br/igarat%C3%A1/36614/daily-weather-forecast/36614")
        info, daily_cards_info = obter_informacoes_climaticas(driver)
        if info and daily_cards_info:
            imprimir_informacoes(info, daily_cards_info, driver)
            enviar_email(info, daily_cards_info)
        driver.quit()

def main():
    # Executar a tarefa imediatamente ao iniciar o script
    executar_tarefa()
    # Agendar a tarefa para ser executada diariamente às 07:00
    schedule.every().day.at("07:00").do(executar_tarefa)
    # Teste para envio a cada minuto
    # schedule.every(1).minute.do(executar_tarefa)

    # Executar o agendador
    while True:
        schedule.run_pending()
        sleep(30)

if __name__ == "__main__":
    main()
