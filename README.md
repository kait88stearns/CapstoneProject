# Know Your Likes

The Drift Collective is a sustainable clothing and handmade bikini company very close to my heart (Check them out [here](https://www.thedriftcollective.com/)!). In addition to being a kick-ass company, their founder, owner and CEO is my very own sister Emily Stearns. So I was thrilled at the oportunity to team up with Drift and offer up my skills as a data scientist. 

  As a young startup with a young customer base, Drift has found an increadibly effective marketing platform in Instagram. Infact, over a third of Drift's web traffic in 2017 was pushed directly from Instagram. Additionally I found:
  * On average, there are 25% increase in online shop visits on days Drift posts vs days they don't.
  * For a 50 like increase on a day's Instagram post, there is an expected 15% increase in daily visits.   
  
![alt text](https://github.com/kait88stearns/CapstoneProject/blob/master/pics/visits_days_posted_vs_not.png "Logo Title Text 1")  

Knowing this, I set out to determine what types of content maximize the number of likes Drift's posts recieve. I decided to measure success in likes in part due to its positive correlation with web traffic, but also because they reflect followers' engagement with and approval of content. 

[Staying true to authenticity is one of Drift's first priorities as a company, so in growing their brand I want to be sure to consider  ]

## Part 1: Data Collection 
I collected data from two main sources, Shopify and Instagram.   

   For Shopify, I used Selenium to log into Drift's account and pull information about Daily web traffic and order history. The functions I wrote for this are in **src/shopify_scrape.py**. 
   
   For Instagram, I used Requests and Beautiful Soup to scrape the attributes for all of Drift's posts (409 posts). These attributes looks like:
   * caption
   * number of likes
   * number of comments
   * comments
   * users who commented
   * users tagged 
   * number of users tagged 
   * hashtags
   * datetime when posted
  The functions I wrote for this are in **src/scrape_insta.py**.
  
  Additionally, I went through and manually classified posts with a series of 16 qualitative features. As you might think, this took some time. Moving forward my hope is Drift classifies each post with these categories upon posting it, something that should only take around 30 seconds in the moment for a single post. The categories I evaluated for are:
  * number of people photographed 
  * bikini shot vs. apparel shot ('a'= apparel, 'b' = bikini, 'c' = both, 'd' = neither)
  * male or female content (0 = male, 1 = female, 2 = both)
  * are faces visible 
  * is a sale mentioned 
  * is there graphic editing
  * are there explicit butts (maybe to be replace with sexuality score) 
  * is picture of the ocean 
  * is content skateboarding related 
  * is picture drift content 
  * is picture a clear product shot
  * is picture a lifestyle shot 
  * is picture taken in the shop 
  * is picture very proffesional/modelly/ posed
  * is picture taken in nature
  * is content surf related 
   
## Part 2: Data Preparation 
My first step towards data preparation was to remove any factors not controlled by the Drift Collective and determined at the time of posting (excluding number of likes, the response). This was to be careful of data leakage and mainly consisted of information about comments. Next, based on intuition of Drift's growth and development I restricted my data to only that from 2017 onward. Drift's physical shop opened in the Fall of 2016 and apparel was introduced at about this time. Due to this major shift, I suspected content from Drift's strictly online and bikini days would not be as predictive of content coming out today as more recent posts. This theory was confirmed with much improved accuracy in predicting number of likes.  Some other feature engineering performed include:
* Using panda's datetime feature, I extracted day of the week, hour, and month details for when content was posted. 
* Using a sentiment analysis tool Word2Vec, I created a 100 element array for each caption. Documentation for Word2Vec can be found [here](https://radimrehurek.com/gensim/models/word2vec.html). I also tried incorporating captions' lengths and average word lengths into my model, however neither of these steps proved helpful. 
* Using natural language processing, I created a TF-IDF matrix for hashtags. I tested out only incorporating hashtags frequently used, but found useing all of them was most successful. The function to incorporate this into my model, **make_hashtag_tfidf(),** can be found in **src/clean.py**.
* Next I created dummy variables for the most frequently tagged users in Drift's posts. I tinkered with where to set the threshold for which users to include, but settled on users who appear in ___ or more posts. This ended up being ___ of the 188 users ever tagged. 
* With the qualitative features and K-Means clustering, I group posts into like types. Considering silhouette and elbow plots, I decided to set k for ______ **7** clusters. My hope was to capture the nature of different frequently posted 'types' of pictures, like people-free product shots, bikinis on the beach shots, skateboarding shots etc. Some of the clusters successfully captured these nuances, while others weren't so successful. Posts from two more successful clusters are shown below. I found my model performed best when the original qualitative features and the clusters were both considered. 

i.e comment  machine learning and statistic tools used are gradient boosted regression modeling, K-Means clustering, natural language processing and frequentist hypothesis testing

## Part 3: Data Modeling 
I produced a model that predicts the number of likes a post will get with a RMSE of 46 likes, and ran hypothesis tests to determine whether certain post qualities are more successful than others

## Part 4: Hypothesis Testing 


Alternatively, I am considering training a neural network to process post images more efficiently.
