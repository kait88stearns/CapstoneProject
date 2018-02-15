# Know Your Likes

The Drift Collective is a sustainable clothing and handmade bikini company very close to my heart. (Check them out [here](https://www.thedriftcollective.com/)!) In addition to being a kick-ass company, their founder, owner and CEO is none other than my sister Emily Stearns. So I was thrilled at the oportunity to team up with Drift and offer up my skills as a data scientist. 

  As a young startup with a young customer base, Instagram provides Drift an ideal platform for reaching new audiences of potential customers. However, Instagram also offers Drift an increadibly effective marketing platform. Infact, over a third of Drift's web traffic in 2017 was pushed directly from Instagram. Other interesting things I found:
  * On average, there are 25% increase in online shop visits on days Drift posts vs days they don't.
  * For a 50 like increase on a day's Instagram post, there is an expected 15% increase in daily visits.   
  
![alt text](https://github.com/kait88stearns/CapstoneProject/blob/master/pics/visits_days_posted_vs_not.png "Logo Title Text 1")  

Knowing this, I set out to optimize their use of Instagram. 


## Part 1: Data Collection 
I collected data from two main sources, Shopify and Instagram.   

   For shopify, I used Selenium to log into Drift's account and pull information about Daily web traffic and order history. The functions I wrote for this are in **src/shopify_scrape.py**. 
   
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
  
  Additionally, I went through and manually classified posts with a series of 16 qualitative features. As you might think, this took some time. Moving forward my hope is Drift classifies each post with these categories upon posting it, something that should only take around 30 seconds in the moment for a single post. The categories I evaluated for  are:
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
The first thing I did in data preparation was remove any factors not controlled by the Drift Collective and determined at the time of posting (excluding number of likes i.e the response). This mainly consisted of information about comments. Next I restricted my data to only that from 2017 onward. This decision was based on intuition of Drift's growth and development: their physical shop only opened in the Fall of 2016, and apparel was introduced around this time. I suspected content from Drift's strictly online and bikini days would not be as predictive of content coming out today as the more recent posts. This theory was confirmed with much improved accuracy for both linear and gradient-boosted regression tree based models predicting number of likes for a given post. 

Below are other major feature engineering steps I took:
* From the time posted information, I extracted day of the week, hour, and month details. 
* Using a sentiment analysis tool Word2Vec, I created a 100 element array for each caption.
* Using natural language processing, I created a TF-IDF matrix for hashtags
i.e comment  machine learning and statistic tools used are gradient boosted regression modeling, K-Means clustering, natural language processing and frequentist hypothesis testing

## Part 3: Data Modeling 
I produced a model that predicts the number of likes a post will get with a RMSE of 46 likes, and ran hypothesis tests to determine whether certain post qualities are more successful than others

## Part 4: Hypothesis Testing 
