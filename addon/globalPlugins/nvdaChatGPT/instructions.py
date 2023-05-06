# Translators: Instruction of how to get and set chatGPT api key.
HOW_TO_GET_KEY = _("""
1. Go to [here](https://platform.openai.com/account/api-keys)
2. Login (make an account, if you don't have one)
3. Press the button "Create new secret key"
4. Go to nvda - preference - settings - askChatGPT, and put the api key.

You get free credits when you create a new chatGPT account, but it expires in several months.
So when it expires, you need to set up your payment method to keep using this add-on.
You can set it up from [here](https://platform.openai.com/account/billing/overview)
It should cost less than $5 a month for normal usage.
""")

API_KEY_NOT_SET_ERROR = _(
    # Translators:Error when text box of api key is empty
    "Your api key is not set! You need to do the following.\n {HOW_TO_GET_KEY}").format(HOW_TO_GET_KEY=HOW_TO_GET_KEY)
API_KEY_INCORRECT_ERROR = _(
    # Translators:Error when api key is set but incorrect.
    "Your api key is incorrect, Check it again! You need to do the following.\n {HOW_TO_GET_KEY}").format(HOW_TO_GET_KEY=HOW_TO_GET_KEY)

# Translators:Error when you run out of credits which you get when creating an account.
INSUFFICIENT_QUOTA_ERROR = _("""You ran out of your free credits, or your credits expired! Now you have to start paying. Below is how you set up your payment method.  

1. Go to [here](https://platform.openai.com/account/billing/overview)
2. Press "Set up payment method" button.

The cost should be less than $3 a month for normal usage.  
But I highly reccomend set usage limit from [here](https://platform.openai.com/account/billing/limits)  

Also, if you are doing well financially, consider donating to this add-on's author.  
You can send your love from [here](https://paypal.me/satoshi26).  
I would really appreciate it, and it would make my day!  
""")
