# Configuração do Ambiente

Este guia fornece instruções detalhadas para configurar o ambiente de desenvolvimento e execução do JulIA.

## Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Git (opcional, para controle de versão)

## Instalação das Dependências

1. Clone o repositório (se ainda não o fez):
   ```bash
   git clone https://github.com/seu-usuario/JulIA.git
   cd JulIA
   ```

2. Crie um ambiente virtual (recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

## Configuração das Variáveis de Ambiente

1. Crie um arquivo `.env` na raiz do projeto.
2. Adicione as seguintes variáveis (se necessário):
   ```env
   OPENAI_API_KEY=your_openai_api_key
   HUGGINGFACEHUB_API_TOKEN=your_huggingface_token
   ```

## Executando a Aplicação

Para iniciar a aplicação, execute:
```bash
streamlit run main.py
```

A aplicação estará disponível em `http://localhost:8501`.

## Testando a Configuração

1. Acesse a interface web no navegador.
2. Tente carregar um vídeo do YouTube e fazer algumas perguntas.
3. Verifique se as respostas são geradas corretamente.
