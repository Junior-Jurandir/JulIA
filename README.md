# JulIA - Assistente Virtual Inteligente

JulIA é uma aplicação web construída com Streamlit que permite aos usuários interagir com um assistente virtual capaz de responder perguntas baseadas no ambiente técnico da sua empresa, para isso ela só precisa ser alimentada com uma base de conhecimentos fornecida pelo usuário e em documentos adicionais que podem ser inseridos posteriormente durante o uso.

## Funcionalidades Principais

- **Carregamento de Vídeos do YouTube**: Ao inserir a url de um video do youtube, se o mesmo possuir legendas, o video será carregado para a base de conhecimentos da IA de forma temporária e poderá ser consultado.
- **Carregamento de Documentos**: Suporte para PDF, TXT, MD, JSON e XLSX. O conteúdo é processado e indexado para consultas.
- **Modelos de Linguagem**: Escolha entre diferentes provedores de modelos (Hugging Face, OpenAI, Ollama) para gerar respostas.
- **Recuperação de Informações**: O sistema utiliza técnicas de RAG (Retrieval-Augmented Generation) para fornecer respostas precisas baseadas no conteúdo carregado.
- **Interface Intuitiva**: Interface simples e intuitiva construída com Streamlit para facil utilização por parte do usuário.

## Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/JulIA.git
   cd JulIA
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure as variáveis de ambiente:
   - Crie um arquivo `.env` na raiz do projeto e adicione suas chaves de API (se necessário).

4. Execute a aplicação:
   ```bash
   streamlit run main.py
   ```

## Uso

1. Insira a URL de um vídeo do YouTube no campo de texto na barra lateral.
2. Faça upload de documentos (PDF, TXT, XLSX) para adicionar mais conteúdo.
3. Digite suas perguntas no campo de chat e receba respostas baseadas no conteúdo carregado.

## Tecnologias Utilizadas

- **Streamlit**: Framework para criação de aplicações web interativas.
- **LangChain**: Biblioteca para construção de aplicações com modelos de linguagem.
- **Hugging Face**: Modelos de linguagem de última geração.
- **OpenAI**: Integração com modelos GPT.
- **Ollama**: Suporte para modelos locais.
- **FAISS**: Biblioteca para busca vetorial eficiente.

## Contribuição

Contribuições são bem-vindas! Siga os passos abaixo:

1. Faça um fork do projeto.
2. Crie uma branch para sua feature (`git checkout -b feature/NovaFeature`).
3. Commit suas mudanças (`git commit -m 'Adicionando nova feature'`).
4. Faça push para a branch (`git push origin feature/NovaFeature`).
5. Abra um Pull Request.
