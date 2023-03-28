# nvda-chatGPT

## Sobre

Este complemento fornece acesso ao chatGPT. através de combinações de teclas, para que você possa perguntar o significado de qualquer palavra ou fazer qualquer pergunta.
Especialmente útil para perguntar palavras difíceis que você não conhece ou fazer perguntas simples de programação.
Você precisa da chave da API (é grátis), mas acho que vale a pena.
Você pode ler radme em [japonês](https://github.com/mo29cg/nvda-chatGPT/blob/main/README.ja.md).

## Download

[nvda-chatGPT](https://github.com/mo29cg/nvda-chatGPT/releases/latest/download/nvdaChatGPT.nvda-addon)

## Configuração (VOCÊ PRECISA FAZER ISSO)

Você precisa da chave de API do chatGPT para usar este complemento (você pode obtê-lo gratuitamente).
Abaixo está como obter a chave de API e configurar.

1. vá para o [chatGPT](https://platform.openai.com/account/api-keys)
2. Faça login (ou crie uma conta, caso não tenha uma)
3. pressione o botão "Criar nova chave secreta‍"
4. vá para nvda - preferências - configurações - askChatGPT e coloque a chave api.

## Teclas de atalho

Primeiro, selecione as palavras que deseja saber o significado ou as perguntas que deseja fazer.
Em seguida, use um dos atalhos abaixo.

- NVDA+shift+W Pergunta o significado da palavra selecionada.

- NVDA+shift+L Faça uma pergunta.

Você pode obter respostas em 3 a 30 segundos, dependendo da dificuldade das perguntas.
Você pode configurar essas ligações de teclas na configuração, você precisa reiniciar o nvda para aplicar novas ligações de teclas.

## contribuidor
- wrapper para acessar o chatGPT [revChatGPT](https://github.com/acheong08/ChatGPT)

- Descobrindo como importar módulos corretamente [@sarnex](https://github.com/sarnex)