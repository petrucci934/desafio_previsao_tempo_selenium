# Previsão do Tempo Igaratá-SP

Este projeto coleta informações climáticas da cidade de Igaratá, SP, utilizando Selenium para automação do navegador. Os dados são então enviados por e-mail para uma lista de contatos especificada.

## Pré-requisitos

- Python 3.7+
- Navegador Google Chrome
- ChromeDriver (gerenciado automaticamente pelo `webdriver_manager`)

## Instalação

1. Clone o repositório:

   ```sh
   git clone https://github.com/petrucci934/desafio_previsao_tempo_selenium.git
   cd desafio_selenium
   ```

2. Crie um ambiente virtual:

   ```sh
   python -m venv venv
   source venv/bin/activate  # No Windows, use `venv\Scripts\activate`
   ```

3. Instale as dependências:

   ```sh
   pip install -r requirements.txt
   ```

4. Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo, substituindo pelos seus dados:

   ```env
   EMAIL_USER=seu-email@gmail.com
   EMAIL_PASS=sua-senha
   ```

## Uso

Para iniciar a coleta de dados e envio de e-mail, execute:

```sh
python main.py
```

## Estrutura do Projeto

```
.
├── desafio_selenium/
│   ├── email_sender.py         # Módulo para envio de e-mails
│   ├── main.py                 # Script principal do projeto
│   ├── requirements.txt        # Arquivo com as dependências do projeto
│   ├── .env                    # Arquivo de configuração com as credenciais de e-mail
│   ├── README.md               # Este arquivo

```

## desafio_selenium/email_sender.py

Este é o script principal que:
1. Inicia o driver do Selenium.
2. Coleta as informações climáticas da página do AccuWeather.
3. Formata essas informações.
4. Envia um e-mail com os dados coletados.
5. Fecha o navegador e encerra o programa

## Autor
Petrucci Lucena - @petrucci934

## Licença


Este `README.md` agora reflete a estrutura do projeto onde a pasta principal é `desafio_selenium` e menciona o seu usuário do GitHub. Certifique-se de ajustar os detalhes conforme necessário para refletir com precisão o seu projeto.
