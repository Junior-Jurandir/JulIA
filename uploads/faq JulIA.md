# Perguntas Frequentes (FAQ)

## 1. Quais formatos de arquivo são suportados?

O JulIA suporta os seguintes formatos:
- PDF: Para documentos textuais
- TXT: Para arquivos de texto simples
- XLS/XLSX: Para planilhas do Excel
- JSON: Para troca de dados estruturados
- MD: Para textos com formatação simples

## 2. Como faço para mudar o modelo de linguagem?

Edite o arquivo `main.py` e altere o valor da variável `model_class` para:
- `"hf_hub"`: Usa modelos do Hugging Face
- `"openai"`: Usa modelos da OpenAI
- `"ollama"`: Usa modelos locais via Ollama

## 3. Posso usar minha própria chave de API?

Sim, crie um arquivo `.env` na raiz do projeto e adicione suas chaves:
```env
OPENAI_API_KEY=sua_chave_aqui
HUGGINGFACEHUB_API_TOKEN=seu_token_aqui
```

## 4. Como posso melhorar a precisão das respostas?

- Certifique-se de que o conteúdo carregado seja relevante para as perguntas.
- Experimente diferentes modelos de linguagem.
- Ajuste os parâmetros como temperatura e max_tokens.

## 5. Onde posso ver o código fonte?

O código fonte está disponível no arquivo `main.py`. Você pode abrir e editar diretamente no seu editor de código.

## 6. Como contribuir para o projeto?

1. Faça um fork do repositório.
2. Crie uma branch para sua feature.
3. Envie um pull request com suas alterações.

## 7. Onde posso reportar problemas ou sugerir melhorias?

Abra uma issue no repositório do projeto no GitHub, descrevendo detalhadamente o problema ou sugestão.

## 8. Como posso limpar o histórico de conversas?

Reinicie a aplicação. O histórico é mantido apenas durante a sessão atual.

## 9. Posso usar o JulIA sem conexão com a internet?

Sim, se estiver usando o modelo Ollama com modelos locais. Para outros modelos, é necessária conexão com a internet.

## 10. Como posso melhorar o desempenho?

- Use hardware com GPU para modelos locais.
- Limite o tamanho dos arquivos carregados.
- Ajuste os parâmetros de chunk_size e chunk_overlap.

## 11. Por que meu video não está sendo carregado?

Possivelmente o video em questão não possui uma legenda disponivel, por favor considere usar um video com legenda.