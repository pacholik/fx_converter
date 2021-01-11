I'm going with exchangeratesapi. Simple API with no api key needed.

#Workflow might be like this:

First, download a lot of data at once to populate db.

Do we have rates for the date in query?
 - Yes: search our db
 - No: download data from exchangeratesapi, populate db and return data.


#Notes:

I think the entire template schema is useless. I don't want direct db queries
and I don't want any mutations.
