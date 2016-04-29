# MIDS_205_elections

**Code from UC-Berkeley MIDS program

Project Description:

In this project, I aim to use internet & social media data to generate a real-time interactive dashboard for tracking surges (or drops) in a candidate's popularity throughout the 2016 presidential primary election cycle. The candidates that I have focused on include: Donald Trump, Ted Cruz, & John Kasich for the Republican party & Hillary Clinton & Bernie Sanders on the Democratic side. Indicators for popularity were gathered from the following sources:

- Twitter's Public Streaming API -> Sample of tweets containing a candidate's name. Velocity of tweets recieved were measured for "mention rate" approximations and tweets were subjected to sentiment analysis (Limited to ~192 tweets/candidate/12 hours/day due to textprocessing.com public API limitations). More info on Twitter's streaming APIs here: https://dev.twitter.com/streaming/overview.

- textprocessing.com API (sentiment analysis) -> Public API (w/ 1000 calls/day limit) that classifies interpreted text as "positive", "negative", or "neutral".  The "positive" and "negative" classifiers were trained on movie reviews meaning there is a potential for some bias (an example of this is that character names for popular franchises (e.g. "Jason", "Bourne", "Neo", etc.) may have been miscategorized as being a positive or negative word depending on the success of the movie).  More info here: http://text-processing.com/docs/index.html.

- GoogleTrends weekly traffic results -> Normalized to peak Google search traffic in a particular group. Candidates were grouped by party affiliation. Results were gathered for the 7 days preceeding a primary election in the state that the election was held in. More info on GoogleTrends service can be found here: https://support.google.com/trends#topic=6248052.

Output:

A sample workbook (w/ data to date as of 4/28/2016) is available to view here: 

**To recreate this project, follow the "Instructions" document that I've included in the "build_scripts" folder.
