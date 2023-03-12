# nvda-chatGPT

## About

This add-on provides an access to chatGPT. through key bindings, so you can ask meanings of any words, or ask anyquestions.  
Especially useful for asking difficult words that you don't know, or asking simple programming questions.  
You need api key (it is free), but I think it's worth time.  
You can read radme in, [Japanese](https://github.com/mo29cg/nvda-chatGPT/blob/main/README.ja.md).

## Download

[nvda-chatGPT](https://github.com/mo29cg/nvda-chatGPT/releases/latest/download/nvdaChatGPT.nvda-addon)

## Setup (YOU NEED TO DO THIS)

You need chatGPT api key to use this add-on (you can get it for frree).  
Below is how to get api key and set up.

1. go to https://platform.openai.com/account/api-keys
2. login (make an account, if you don't have one)
3. press the button "Create new secret key‍"
4. go to nvda - preference - settings - askChatGPT, and put the api key.

## Key bindings

First, select any words you wish to know the meaning of, or questions you wish to ask.  
Then use the either of below.

- NVDA+shift+A Ask the meaning of selected word.

- NVDA+shift+L Ask the question.

You can get responses in 3 ~ 30 seconds, depends on difficulty of the questions.  
You can configure these key binding in setting, you need to restart nvda to apply new key bindings.

## contributor

- wrapper to access chatGPT [revChatGPT](https://github.com/acheong08/ChatGPT)

- Figureed out how to correctly import modules [@sarnex](https://github.com/sarnex)
