# 2016 US Election Sentiment Map

![Clinton vs Trump](/Clinton_Trump_Overall.png)

I wrote this code for a group project last semester. It uses Matplotlib and the Basemap toolkit to overlay a 2D histogram over a map of the United States. The hexbin is populated from tweets in JSON format, which we divided into positive and negative sentiment using a Support Vector Machine from the scikit-learn library.

Also included is an example of how a map can be animated. Unfortunately at the time we did not have data over the right time period to create an animated map illustrating changes in sentiment over several days. 
