# nvda-chatGPT

### About

This add-on provides an access to chatGPT. through key bindings, so you can ask meanings of any words, or ask anyquestions.  
Especially useful for asking difficult words that you don't know, or asking simple programming questions.  
You need api key (it is free), but I think it's worth time.  
You can read readme in, [Japanese](https://github.com/mo29cg/nvda-chatGPT/blob/main/README.ja.md).

### Download

[nvda-chatGPT](https://github.com/mo29cg/nvda-chatGPT/releases/latest/download/nvdaChatGPT.nvda-addon)

### Setup (YOU NEED TO DO THIS)

You need chatGPT api key to use this add-on, You get free credits, but it expires in several monthes.  
So, after it expires, you need to pay your actual money to keep using this add-on, it should be less than $2 a month for normal usage.  
Below is how to get api key and set up.

1. go to https://platform.openai.com/account/api-keys
2. login (make an account, if you don't have one)
3. press the button "Create new secret key‍"
4. go to nvda - preference - settings - askChatGPT, and put the api key.

### Key bindings

- NVDA+shift+W Ask the meaning of selected word, or open a dialog, if none is selected.

- NVDA+shift+L Open a dialog to ask a question.

Press ctrl + enter to send a request in the dialog.
You can get responses in 3 ~ 30 seconds, depends on difficulty of the questions.  
You can browse your conversation in the list above text box, pressing enter will open a dialog of a selected message.

### For people this add-on is not working

Assuming you correctly put your api key, most likely your chatGPT account is too old, so your free credits you got when you created your account expired.  
Now, you need to set up your payment method.  
Go to [here](https://platform.openai.com/account/billing/overview)

### For developer

To make a release, run below

```
git tag -a <release name>
git push --tags
```

Release will be created by github-action.

### I need your supports!

Due to my visual impairment, my capability for jobs is pretty limited.  
I'd really appreciate donations if anyone find my add-on useful.  
Here is the link: [paypal.me](https://paypal.me/satoshi26)

### contributor

- Figured out how to correctly import modules [@sarnex](https://github.com/sarnex)
