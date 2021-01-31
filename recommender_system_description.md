A short description of the recommender system
=============================================

The goal of our recommender system is to suggest the recipes based on the preferences of the user. The type of our recommender system will be **Collaborative Filtering** – the method which makes recommendations based on group of people which has similar tastes to concrete user. 

This method has two approaches:
 - **user-based** - prompts based on similarities to users: “users who are similar to you like also:”,
 - **item-based** - prompts items which was rated in similar way to specific item: “users who like this item like also:". 

In our project we will use approach similar to **user-based** one of collaborative filtering because in this method recommendations are more diverse than in item-based approach. Besides, our user database is small in comparison to recipes database.   

Libraries which will be used in recommender system:
- **Numpy** to handle with ratings data

The ratings database will be created with special model which will contain information about:
- **recipe** which was rated
- **score** given to this recipe
- **user** who rated this recipe

Recommendation is created based on potetial rating which user would give to the recipe. Potential rating is calculated by the formula:
potential_rating = sum_of_weigthed_ratings_for_the_recipe/sum_of_similarities_to_the_other_user,

wherein weighted_rating_for_the_recipe is calculated by: 
weighted_rating_for_the_recipe = rating_for_the_recipe * similarity_to_the_other_user

To find the similarities the system creates group of users who rated recipes in common with our user. For all users belonging to this group the similarity index is calculated by the **Pearson Correlation**. After finding similarities, the system sorts them descending. 

The **weighted rating** for each recipe is the product of rating which other user gave to one recipe and similarity index.

To calculate the **potential rating** which user would give to recommended recipe, the system divides *sum of weighted ratings* for the recipe by the *sum of similarities of users* who rated given recipe. Next, potential ratings are sorted descending.

As a result, the recommended recipes are these whose potential rating score is the highest.


