### このアドオンについて

chatGPT に対して質問できるショートカットキーを追加します。

### ダウンロード

[nvda-chatGPT](https://github.com/mo29cg/nvda-chatGPT/releases/download/release/nvdaChatGPT-0.1.nvda-addon)

### 必要な初期設定

このアドオンを使うには chatGPT 公式から取得した API キー が必要です。これは無料で取得できます。
取得方法は以下です。

1. https://platform.openai.com/account/api-keys　にいく
2. ログイン（アカウントがなければ作る）
3. "Create new secret key‍"というボタンを押す

api キーが取得できたら、このアドオンをインストール後に現れる NVDA の設定のタブの askChatGPT に api キーを入れる

### 使い方

まず任意の文字列を選択します。その後、下記のショートカットキーのどちらかを使って chatGPT に送ります。
・NVDA+shift+A 選択した単語の意味を chatGPT に聞く（英単語の意味や難しい熟語を聞くのに便利だと思います）
・NVDA+shift+L 選択した文をそのまま chatGPT に送って返答を得る

ショートカットキーは設定で変更可能です。
変更した場合は反映させるのに NVDA の再起動が必要です。
存在しないキー等を設定してしまうと多分アドオンがぶっ壊れます。

### 貢献・協力者

・このアドオンで使っている chatGPT アクセスのためのモジュール [revChatGPT](https://github.com/acheong08/ChatGPT)

・import 周りの不具合を解決してくれた友達 [@sarnex](https://github.com/sarnex)
