# nvda-chatGPT

### Sobre

Este complemento fornece acesso ao chatGPT. através de combinações de teclas, para que você possa perguntar o significado de qualquer palavra ou fazer qualquer pergunta.
Especialmente útil para perguntar palavras difíceis que você não conhece ou fazer perguntas simples de programação.
Você precisa da chave da API (é grátis), mas acho que vale a pena.
Você pode ler o leia-me em [japonês](https://github.com/mo29cg/nvda-chatGPT/blob/main/README.ja.md).

### Download

[nvda-chatGPT](https://github.com/mo29cg/nvda-chatGPT/releases/latest/download/nvdaChatGPT.nvda-addon)

### Configuração (VOCÊ PRECISA FAZER ISSO)

Você precisa da chave de API do chatGPT para usar este complemento. Você obtém créditos gratuitos, mas expira em alguns meses.
Portanto, depois que expirar, você precisará pagar para continuar usando este complemento, que deve ser inferior a US$5 por mês para uso normal.
Abaixo está como obter a chave de API e configurar.

1. Vá para [https://platform.openai.com/account/api-keys](https://platform.openai.com/account/api-keys)
2. Faça login (ou crie uma conta, caso não tenha uma)
3. pressione o botão  "Create new secret key‍"
4. vá para nvda - preferências - configurações - askChatGPT e coloque a chave api.

### Combinações de teclas

- NVDA+shift+W Pergunta o significado da palavra selecionada ou abre uma caixa de diálogo, se nenhuma estiver selecionada.

- NVDA+shift+L Abre uma caixa de diálogo para fazer uma pergunta.

Pressione ctrl + enter para enviar uma solicitação na caixa de diálogo.
Você pode obter respostas em 3 a 30 segundos, dependendo da dificuldade das perguntas.
Você pode navegar na sua conversa na lista acima da caixa de texto, pressionando enter abrirá uma caixa de diálogo de uma mensagem selecionada.

### Para aquelas pessoas que este complemento não está funcionando

Supondo que você tenha colocado sua chave de API corretamente, provavelmente sua conta chatGPT é muito antiga, então seus créditos gratuitos que você obteve quando criou sua conta expiraram.
Agora, você precisa configurar sua forma de pagamento.
Acesse [aqui](https://platform.openai.com/account/billing/overview)

### Preciso do seu suporte!

Devido à minha deficiência visual, minha capacidade de trabalho é bastante limitada.
Eu realmente apreciaria doações se alguém achar meu complemento útil.
Aqui está o link: [paypal.me](https://paypal.me/satoshi26)

### colaborador

- wrapper para acessar o chatGPT [revChatGPT](https://github.com/acheong08/ChatGPT)

- Descobri como importar módulos corretamente [@sarnex](https://github.com/sarnex)
