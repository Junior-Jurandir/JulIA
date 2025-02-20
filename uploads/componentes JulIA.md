# Componentes Principais

Este documento descreve os principais componentes técnicos do JulIA e como eles interagem entre si.

## 1. Carregamento de Vídeos

### Funcionalidade
- Extrai transcrições de vídeos do YouTube
- Coleta metadados (título, autor, descrição, duração)
- Armazena as informações em arquivos de texto

### Tecnologias Utilizadas
- `yt-dlp`: Para extração de informações e legendas
- `YoutubeLoader` (LangChain): Para processamento das transcrições

## 2. Carregamento de Documentos

### Formatos Suportados
- PDF: Extração de texto e metadados
- TXT: Processamento direto do conteúdo
- XLS/XLSX: Leitura de planilhas e conversão para texto
- JSON: Leitura e processamento de dados estruturados em formato de pares chave-valor
- MD (Markdown): Processamento de texto formatado em Markdown, incluindo cabeçalhos, listas e links

### Tecnologias Utilizadas
- `PyPDFLoader`: Para processamento de PDFs
- `pandas`: Para leitura de arquivos Excel
- `RecursiveCharacterTextSplitter`: Para divisão do texto em chunks
- `json`: Para leitura e manipulação de arquivos JSON
- `markdown`: Para processamento de arquivos Markdown

## 3. Modelos de Linguagem

### Provedores Suportados
- **Hugging Face**: Modelos como Meta-Llama-3-8B-Instruct
- **OpenAI**: Integração com modelos GPT
- **Ollama**: Suporte para modelos locais

### Configuração
- Seleção do modelo através da variável `model_class`
- Parâmetros ajustáveis (temperatura, max_tokens)

## 4. Recuperação de Informações

### Funcionalidade
- Indexação do conteúdo usando FAISS
- Busca semântica com embeddings BGE-M3
- Técnicas de RAG (Retrieval-Augmented Generation)

### Tecnologias Utilizadas
- `FAISS`: Para armazenamento e busca vetorial
- `HuggingFaceEmbeddings`: Para geração de embeddings
- `create_retrieval_chain`: Para integração com LangChain

## 5. Interface do Usuário

### Funcionalidades
- Upload de arquivos
- Chat interativo
- Exibição de fontes e referências

### Tecnologias Utilizadas
- `Streamlit`: Framework para interface web
- `st.chat_input`: Para entrada de mensagens
- `st.session_state`: Para gerenciamento de estado
