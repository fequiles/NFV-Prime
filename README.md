
# NFV-Prime

A plataforma NFV-Prime foi construída com o objetivo de introduzir, de forma prática e facilitada, o paradigma NFV para novos desenvolvedores e usuários. A NFV-Prime simplifica o processo de criar, instanciar e visualizar resultados de execução das VNFs em uma rede de testes, sendo adequada para a prototipação de VNFs.


## Requisitos Mínimos

Os requisitos mínimos (recomendações) para acessar localmente o NFV-Prime

    1. Sistema Operacional: Linux Mint 20 Cinnamon
    2. Docker: 27.0.3
    3. Docker-compose: 1.25.0
    4. Usuário: permissões administrativas
    5. Google Chrome: Versão 126.0.6478.126
    6. Python: 3.8.10

## Rodando localmente

Clone o projeto
```bash
  git clone https://github.com/fequiles/NFV-Prime.git
```
Entre no diretório do projeto

```bash
  cd NFV-Prime
```

No diretório do projeto, será necessário subir o docker do banco de dados, instância do postgres, que a plataforma NFV-Prime utilizará para armazenamento e consulta de dados, sendo necessário executar em um terminal
```bash
sudo docker-compose -f docker-compose-postgres.yml up --build
```

Após, em outro terminal, acesse a pasta do backend da aplicação
```bash
cd NFVPrimeBack
```

Crie uma instância virtual do Python3
```bash
python3 -m venv venv
```

Instale os requisitos do Python3 no ambiente virtual
```bash
pip3 install -r requirements.txt
```

Inicialize o backend da aplicação
```bash
sudo python3 main.py
```

A partir da raiz, acesse a pasta do frontend da aplicação
```bash
cd NFVPrimeFront
```

Instale as dependências
```bash
npm i
```

Inicie o projeto
```bash
npm run dev
```

Por fim, o acesse a plataforma
https://localhost:3000


Clone o projeto

```bash
  git clone https://github.com/fequiles/NFV-Prime.git
```

Entre no diretório do projeto

```bash
  cd NFV-Prime
```

No diretório do projeto, será necessário subir o docker do banco de dados, instância do postgres, que a plataforma NFV-Prime utilizará para armazenamento e consulta de dados, sendo necessário executar em um terminal: 

    $ sudo docker-compose -f docker-compose-postgres.yml up --build

Após, em outro terminal, é necessário executar o docker-compose para inicializar a aplicação Web da NFV-Prime e o backend da plataforma:

    $ sudo docker-compose -f docker-compose.yml up --build

Por fim, o acesso a plataforma ocorre através do link:

    https://localhost:23621


## Demonstração

Segue abaixo um vídeo demo da plataforma NFV-Prime.


## Documentação NFV-Prime

A documentação da Plataforma pode ser acessada no seguinte link: [Documentação](https://docs.google.com/document/d/1px9SR90iJHylnYZHP7F1b6iJTrY2Zfrp7TYmC4MK6hg/edit?usp=sharing)


## Uso/Exemplos

Clique [aqui](https://github.com/fequiles/NFV-Prime/tree/master/NFVPrimeExemplos) para ter acesso a arquivos ".json" que configuram a NFV-Prime com cenários de teste, para que se tenha maior familiaridade e facilidade ao utilizar a ferramenta a primeira vez com a plataforma. Além disso, também é possível verificar resultados obtidos e armazenados em arquivos ".csv" da execução das VNFs que estão disponíveis na plataforma, com as configurações escolhidas.


## Licença

MIT License

Copyright (c) 2025 NFV-Prime

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
