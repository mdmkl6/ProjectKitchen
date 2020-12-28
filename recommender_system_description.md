A short description of the recommender system
=============================================

The goal of our recommender system is to suggest the recipes based on the preferences of the user. The type of our recommender system will be Collaborative Filtering – the method which makes recommendations based on group of people which has similar tastes to concrete user. 

This method has two approaches:
 - user-based - prompts based on similarities to users: “users who are similar to you like also:”,
 - item-based - prompts items which was rated in similar way to specific item: “users who like this item like also:". 

In our project we will use the approach similar to item-based one of collaborative filtering because this approach works faster with large database and it is usually makes more accurate recommendations than user-based one.

Libraries which will be used in recommender system:
- Pandas to handle with databases
 
We create separate ratings database in which there will be all given ratings for each recipe (rows – users, columns – ratings for recipe). 

First of all, we find the most similar recipes to the recipe user has recently rated. 
In order to do that we use statistical tools like Cosine Similarity or Pearson Correlation. After calculating similarities, we sort them descending.

Later, we calculate the ratings mean and number of ratings for each recipe - they are important determinants in our recommender system, because similarity alone is not good enough determinant because it can prompt recipes which has a few ratings and this small number of ratings could be unreliable.
For example, we have two recipes which has the same rating and one has 50 ratings and the other one has only 3 ratings – in this situation is more naturally to recommend more popular one. That is why we take number of ratings for each recipe into consideration.

As a result, more popular recipes - even having less similarity value - will show up first. The recommender system ignores recipes which has less than some number of ratings. 


