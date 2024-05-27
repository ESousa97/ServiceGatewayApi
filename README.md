# Service Gateway Api

Esta API serverless é projetada para automatizar o processo de agrupamento (clustering) de tickets de suporte técnico baseado em suas descrições textuais. Utilizando uma sequência de serviços externos para normalização, vetorização e clustering de texto, esta aplicação identifica padrões e agrupa tickets semelhantes, facilitando a organização e a priorização de problemas recorrentes.

### Funcionalidades

- **Normalização de Texto:** A API primeiro normaliza os textos dos tickets usando um serviço externo, garantindo que os dados estejam formatados consistentemente para análise.
- **Vetorização de Texto:** Após a normalização, os textos são convertidos em vetores numéricos, permitindo que sejam processados por algoritmos de machine learning.
- **Clustering de Tickets:** Finalmente, os vetores são enviados para um serviço de clustering, que agrupa os tickets com base em suas semelhanças.

### Como Instalar e Rodar Localmente

#### **Pré-requisitos:**

- Python 3.12
- Pip (gerenciador de pacotes Python)

### Instalação:

**1. Clone o repositório para sua máquina local usando Git:**

```php

git clone <url-do-repositorio>
cd <nome-do-diretorio>

```
**2. Crie um ambiente virtual para instalar as dependências:**

```bash

python -m venv env
source env/bin/activate  # No Windows use `env\Scripts\activate`

```

**3. Instale as dependências necessárias usando `pip`:**

```

pip install -r requirements.txt

```

O arquivo `requirements.txt` deve conter:

```makefile

Flask==2.1.2
requests==2.27.1
Flask-CORS==3.0.10
Werkzeug==2.1.1

```

### Execução:

- Execute a aplicação

```bash

python api/app.py

```

A API estará disponível em `http://localhost:5001/`.

### Uso da API

#### Endepoint `/cluster-tickets` (POST):

- Envie uma requisição POST para `http://localhost:5001/cluster-tickets` com um JSON contendo a lista de tickets. Cada ticket deve incluir as chaves `cause_by`, `testes_realizados_by`, `solution_by`, e `validated_by`.

Exemplo de corpo da requisição:

```json

[
    {
        "cause_by": "Erro de conexão",
        "testes_realizados_by": "Verificação de cabo",
        "solution_by": "Troca de cabo",
        "validated_by": "Cliente confirma solução"
    }
]

```

- A resposta será um JSON com os tickets agrupados por categorias de problemas.

#### Configuração com Vercel

Este projeto é configurado para deploy no Vercel com as seguintes especificações em `vercel.json`:

```json

{
  "version": 2,
  "builds": [
    {
      "src": "api/app.py",
      "use": "@vercel/python",
      "config": { "runtime": "python-3.12" }
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "/api/app.py"
    },
    {
      "src": "/cluster-tickets",
      "dest": "/api/app.py"
    }
  ]
}

```

Para deploy no Vercel, siga as instruções da documentação oficial para configurar seu projeto e faça o deploy utilizando a interface do Vercel ou a CLI.

### Conclusão

Esta API facilita a gestão de tickets de suporte, permitindo que equipes técnicas se concentrem nos problemas mais prementes e reduzam o tempo de resolução. Ideal para empresas que buscam otimizar suas operações de suporte técnico.