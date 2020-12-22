application.py -> Implementation to Discord
rinabot.py -> The AI
editor_database.py -> Clean data and implement it using pymongo, run using localhost (NEED MONGO DB) 
model
|
|-chatbotmodel.h5 -> The weights for the AI
|-intentions.json -> Text that can be recognized by AI
data
|
|-data_toko.csv -> Data for our shop (we will convert this to data_toko.json because we'll be using MONGO DB)
|-data_toko.json -> We'll be using several rows, in this case the id, name, stock, price, and url of the product