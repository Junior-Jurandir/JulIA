# Exemplos de Uso

Este documento fornece exemplos práticos de como utilizar o JulIA para diferentes cenários.

## 1. Carregando um Vídeo do YouTube

1. Insira a URL de um vídeo do YouTube na barra lateral.
2. Clique em "Carregar Transcrição".
3. Aguarde o processamento e verifique a mensagem de sucesso.

**Exemplo de URL:**
```
https://www.youtube.com/watch?v=exemplo123
```

## 2. Fazendo Upload de Documentos

1. Na barra lateral, clique em "Escolher arquivos".
2. Selecione um ou mais arquivos (PDF, TXT, XLS/XLSX).
3. Aguarde o processamento dos arquivos.

**Exemplo de Arquivos:**
- `documento.pdf`
- `relatorio.txt`
- `dados.xlsx`
- `anotações.md`
- `mensagem.json`

## 3. Interagindo com o Chat

1. No campo de chat, digite sua pergunta.
2. Pressione Enter ou clique no ícone de enviar.
3. Aguarde a resposta do assistente.

**Exemplos de Perguntas:**
- "Qual é o tema principal deste vídeo?"
- "Me mostre os dados da planilha sobre vendas."
- "Resuma os pontos principais do documento."

## 4. Selecionando o Modelo de Linguagem

1. No código fonte, localize a variável `model_class`.
2. Altere o valor para o modelo desejado:
   - `"hf_hub"`: Hugging Face
   - `"openai"`: OpenAI
   - `"ollama"`: Ollama
3. Reinicie a aplicação para aplicar as mudanças.

## 5. Verificando as Fontes

1. Após receber uma resposta, clique nas referências abaixo da resposta.
2. Visualize o conteúdo original que foi usado para gerar a resposta.

**Exemplo de Referência:**
```
:link: Fonte 1: documento.pdf - p. 2
```

## 6. Gerenciando o Histórico

- O histórico de conversas é mantido durante a sessão.
- Para limpar o histórico, reinicie a aplicação.
