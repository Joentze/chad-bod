
##  CHAD-BOD 💪🏼

Chad-bod is a student assistant built with OpenAI's LLM. It is built with a custom knowledge base of common Singapore Management University (SMU) FAQs to assist students in their daily activities. FAQs are scraped from various SMU-affiliate sites such as SMU Blog & SMU's main site

  

###  Tech Stack

**Frontend**

- Telegram bot (w/ webhooks)

  

**Backend**

- 🤖 OpenAI (LLM: *gpt-3.5-turbo-0613*, embedding: *text-embedding-ada-002*)

- ⚡️ Supabase (Vector Database)

- ☁️ Google Cloud Run (Hosting)

- 💾 Redis (Message Caching)



**FAQs**

**Will my messages be stored?**

Yes, but not all. In order to have context of message history, a small chunk of recent messages will be stored. This means that as more messages are sent, older messages will be deleted.

**Will Chad Bod hallucinate?**

Yes, all Large Language Models do to some extent. But we try to minimise it by giving Chad Bod context to your queries. To lower the chances of hallucinations taking place, we've got to add updated, quality information to the knowledge base. You can help with that [here](https://forms.gle/sTETrFTCkGUtr6eJ7)

**How does it work?**
-
![diagram of how CHAD BOD works](https://lh4.googleusercontent.com/YHkYZQFMKDhZPfoj5HoX4ivfz_9EfWzTwgmK4Ffrx8I_tvXDqaEgypsanAO0gT7tLH54V-7Y-k5yYFesPpstEdOFuSiCgnBuf7zsIasIcUWDPuCfDpflFYQ8n4A4td4TvA=w1098)
