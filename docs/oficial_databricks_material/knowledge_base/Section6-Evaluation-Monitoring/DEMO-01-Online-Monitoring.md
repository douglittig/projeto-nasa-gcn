# Demo Onlin

**Source:** `Generative AI Application Deployment and Monitoring - Demo Onlin.mp4`
**Duration:** 21:05
**Language:** en (detected with 100.0% confidence)

---

## Full Transcription

So let's illustrate this in action in the next demo where we will walk through unpacking the role payload from the JSON, calculate additional eliminated metrics, materialize this as a table, create Lake House Monitor, either via the UI or API, we'll show both experiences, navigate the generated dashboard and show how one can potentially create a SQL alert on top of a specific metric of interest. So let's jump to the last demo to showcase how we can unpack that inference table, compute some metrics, walk you through what a monitor creates and enable that on our inference table. So first thing first, so you do remember that inference table that we created previously, let's do a quick check and you can see that in the meantime I've run some batch inferences on that table. So I have a couple of requests which came in which are ready for me for to be unpacked. So unpacking the table will also depend on the input signature of the model. Here this is where there might be some different nuances on how the input request JSON past should be here because we were following for our model, the TensorFlow input serving format, which usually the format will look like you would have an input and then an array of queries containing the user questions. This is how we define the JSON past but we do provide well detailed explanations in our documentation on how depending on the format of the inputs, how to pre-define the input request JSON past and type and if potentially it is a multi-turn conversational chatbot, you also want to ensure that you're only keeping like the last exchange of the history because usually the content of the whole conversation is always persisted as part of prompts. Defining what column contains, let's say the key for the outputs. So here again because our output format is predictions containing the list of answers, so it's prediction and informing it that inside it is an array of string. So that's where you might potentially given how you format the DDI messages and signature, you might need to modify things in the provided template. But once you define that, you feed it to an unpacking helper method that we've pre-created for you and again made available in the documentation notebooks. So here we'll just do a quick test on a sample of 10 observations. So here technically we can see that after unpacking we have the model identifier as we know we can use as a grouping variable. We can see the different the inputs and the outputs. That's it. Now for sake of simplicity we did not persist the sources even though it is a rack chain. Again you could parse and have an additional source field as part of your unpacking logic if you've persisted that in the output of the system. So now that we have an inference table this is where you can bring in all the metrics of interests and run these at scale using pandas user defined function. So here what we will do is we'll use common open source Python packages to calculate the number of tokens, the fleshkincade grade, the automated reliability index, the toxicity and the perplexed. Both on the inputs and the outputs. And this is where again these are provided in the template notebook. This is where you can also add in your own metrics as well and we'll wrap everything in a nice and easy method called compute metrics which will take the request data spark data from input tell it on which column we want to apply these measures and every time append a new column run the pandas udf to calculate all the metrics of interests. So that's it. So that's like the second step on packing defining the functions for the LLM related metrics of interest and schedule this to run as a streaming job. So again whether you're familiar or not with spark structure streaming that's really not a block or an issue here. The good thing is that delta tables can be used as an input for source for a streaming job. So here what we're telling here we're going to create a streaming job which will just look at the source inference table unpack the request. We'll drop the columns that are not necessary for monitoring. We'll compute the metrics and we'll use an initial helper function to pre-create the new unpack table with the metrics if that table does not exist and persist this into a new table in our catalog called rag app process inference. And usually this whole piece happening here where we are reading the stream unpacking the requests dropping the column computing the metrics and writing the stream back to a delta table in an append fashion to our new process table. These like two three sections of the notebook this is what you would usually schedule to run either as a trigger job or a continuous streaming job. So in a sense that as new payloads gets persisted to the inference table they will be automatically read the stream will pick it up based on the previous checkpoint location and do all the unpacking calculating the metrics and then just persisting writing the stream back to a delta table and that's pretty much it. So while our processed table with the metrics is calculated let's talk about to review the basics of the chaos monitoring. So again the way it works it is a data centric solution which you enable at a table level and here our starting point table is going to be that unpacked inference table with the LLM related metrics of interest. And so once we have that inference table ready we can enable the monitoring on top. Now usually we have three types of monitor that can be created on top of a table. So time series is just through is let's say the default profile where again we are going to profile the data and look at drift from a time series perspective given the granularity that you set at the monitor creation. inference log is the format specific to machine or supervised machine learning system like classification and regression and snapshot is just if you want to asynchronously compare different versions of a table at manually defined one in time. Now when it comes to monitoring our LLM system the time series profile is the type of profile that you will be using on the inference table. So now that the inference table has been created let's just take a look at again what table is being populated in at the pace of the streaming job. So we have the prompts the completions and all the metrics the toxicity perplexity token count can cater of the input to realize the reliability index and the same for all the outputs. And so what's going to be of interest is to monitor all those potential model from a time series perspective how all these metrics might be changing through time. So how can we enable a monitor? There are two options. The first one is to do it via the UI. So let's start with that experience because it can be the most easy one to show and to demonstrate. So if I go to my processed inference table right here any table under unity catalog will have a quality tab available for it. If a monitor exists then you will already have information here. If a monitor does not exist you will see this gets started wizard. So here first you pick a profile. So here we open the time series we'll define the granularity. So here again given like the the reality of the data and that I've batched my requests in five minute windows I'm going to pick the smallest granularity supported which is five minute but usually in real time in a more common situation you might be looking at things maybe hourly or daily or whatnot. Defining which call and represents your timestamp is important and that's it there's nothing more to add. Now you can also set the schedule for refreshing the monitoring metrics or just have it done manually. You can set notifications on failures of refreshes. What's also important is to define in which schema under which schema are database you want those profile and drift metrics table to be created. You can also define a baseline table for if you want to compare drift or let's say you have a baseline model which has specific for your evaluation set or test set has specific values for all these tests that you did and want to compare how far we are from the baseline you can point it to that same let's say unprocessed inference table for the baseline model on baseline data set. We won't be doing that today but because it's optional but this will allow you to measure things such as drift compared to a baseline model. You can add slicing expressions so slicing expression let's say for example that I want to look at performance per model ID so you can usually you can either just say list the name of the categorical column but you can also use you can also create use equalities or inequalities. Let's say it doesn't apply to our table here but if you want to look at I don't know metrics where maybe you have an input where the age of the user is higher or lower than that you can define those like slicing expressions using in equal SQL inequalities and that's pretty much it so once you do that you hit the create button and the monitor will be created. So that's how you do it via the UI while the monitor gets created and we can we'll get back to it. Let's also see how you can do exactly the same using the the Databricks SDK. So with the Databricks SDK there is under the service class and the catalog you can define which profile you want to use whether it's a monitor time series or an inference log or a snapshot and with that same workspace client which exposes we saw serving endpoint it also exposes a quality monitor API. So that's the quality monitor this is how we can create an endpoint sorry and that's how we can create a monitor using the create method. So the starting point that it needs is the table name and always make sure to use the three level namespace otherwise the default schema and catalog will be used and here I'm telling it I want time series profile that is my timestamp colon and this is the granularities that I want. Note that you can have multiple granularities at a time it doesn't have to be one defining your slicing expressions and telling it once you're going to create those this profile metrics table and the Durstmetrics table store these under that specific output schema and that's it. So I won't run this command because my monitor already exists but you can do a quick status check on the table to see if the monitor already exists. So normally I do that yeah I should have probably imported my client first so once I'll do the essentially the client there we go okay so now we can do a quick get monitor so it's telling me that the status is active and that it's not pending so it sounds like my monitor has been created. So let's do a quick status to make sure do a quick pulse check to ensure that the monitor has been created looks like it did. Now one thing to ensure the success of the creation of the dashboard is to make sure that you have an accessible Databricks SQL cluster up and running because the for the dashboard to be created and create the queries and execute them and populate the graph a Databricks SQL cluster must be up and running ahead of time. Let's go and and take a quick check at our created monitor so that's what we're expecting to see once the monitor has been created successfully so you could have a link to the dashboard a link to the different profile and Durstmetrics table and what not so we can quickly try to query those tables so from the monitor info there will be a link to the profile metrics table name and also a link to the Durstmetrics table name now that the monitor has been set up and the refresh of the table as ran I can take a look at my profile metrics table so the way to interpret this is that for every five minute time window that was found inside the process different stable for the given model ID value you can look at there's going to be different types of metrics such as length, non-null columns, frequent items, median etc and same for the Durstmetrics table but what's going to be important is not how the row information is going to being laid out is how you can query it and get a sense out of it so for that we are going to examine the dashboard board that specific monitor so let's jump back into the catalog and our processed inference table so now you can see in the quality tab that I have all my different monitoring metrics when the last three fresh happened and I can trigger refresh manually I can enter the monitor configuration and I can also see my dashboard and you can also see here those the two newly created tables the drift metrics and the profile metrics and the link to the dashboard so let's take a quick look at that dashboard and see how we can use that to monitor our system let's give it a couple of minutes to spin off the warehouse so you can see on the top left of that dashboard you can choose the inspection windows you can look at specific granularities you can decide if you want to look at metrics for a specific model identifier so let's take a look at what's inside that dashboard so most of the information up here are let's say genai agnostic and ascent that we just have we can see the count of the requests happening every five minutes if there's any high zeros or null zeros are probably irrelevant in text but at least the number of nulls can be important is there any high drift in numerical columns looking at again high nulls in specific columns looking at data integrity over time for any given column of interest that we can put here and you can also see that again for every column every inspection window what the data integrity information is given that we don't have a baseline table let's take a look at for example consecutive drift and let's see for example since we're interested primarily in numerical drift is there any significant change in maybe the toxicity of your output so let's we can take a quick look at the time series of the toxicity compared to previous window and when we think about an numerical drift you can look at the p-value of the ks test or maybe looking at population stability indexes so that this for example will give us chart on is there like a high drift in the toxicity of my output in between consecutive windows categorical drift is probably here meaningless because we only have purely unstructured text but other things that for time series that are provided out of the box so let's say again I want to plot the time series of the toxicity maybe of my input this time look at the average toxicity on five-minute windows of my input so I can see the chart of this toxicity metric and let's say I want to be alerted in case the toxicity value goes beyond the specific threshold what I can do here is I can go to the specific query which is automatically generated on top of the drift metric stable and so here I can see the query I can rerun it I can parameterize it but what I can do on top of that query is create an alert and usually the way alerts get created is you can give it a name you can tell it that again is the metric which is in our case our toxicity is it higher than if is the average value for example higher than 0.1 you can decide how you want to be notified if you know this rule is violated once or multiple time you can define notification and you can use custom template in the body of the email and then that's it you can create your alert and you can add schedules and then you can add destinations so the destinations could be an email address the Slack webhook team is webhook a page or duty etc there's a list of supported integration with the Databricks and thousands platform geore integration is also coming soon so that's it so this is how you could self-serve yourself and create a feedback loop to proactively be alerted on potential and on metrics exceeding specific dangerous thresholds so to conclude on Lake House Monitoring so the way we set it up today is on a single table because this is how usually things work but making sure you want to use this as part of a more general workflow when you're dealing with AI system with multiple components you can run you can enable this monitoring at the different stages of the development so whether you're doing this in development you're doing this in test or even in production so you don't necessarily have to only monitor what's happening at the production level you can also start doing some pre-monitoring in your testing in development environment and some other tips that you can also do you can also use this tools to so it is again recommended to monitor the tables of all the components you could also monitor how the embeddings are changing through time for example you could monitor not only the inference tables but maybe monitoring any type of other feature table that you also might be looking at you can also use this tool to monitor costs so we didn't touch upon it today during the module but all the Databricks associated costs for any system that you're using in the platform is logged automatically in a unity catalog called system tables and you can create your own queries or views on top of these cost component and create the monitor on top of that view or table make sure to refresh the table and dashboards regularly because the dashboards usually they'll query what's their static you can set a schedule for them to refresh themselves or refresh the queries powering each one of the chart so make sure you set a schedule for that and also make sure that the monitor schedule refresh is in sync with the pace at which the monitor table is changing so if you know that the monitor table is changing or is getting requests maybe every five minutes or so and you're not really interested in seeing what's happening every five minutes but maybe every half hour so set your schedule for the monitor to be for example every 30 minutes such as a refresh will have in every 30 minute and only process incrementally the latest 30 minutes of data because that's how the monitoring system work it is an incremental runner so it doesn't scan the full table every time it will only scan what has changed in the table between last three fresh and current three fresh and to run things in an optimized and cost-efficient fashion

---

## Timestamped Segments

**[00:00]** So let's illustrate this in action in the next demo where we will walk through unpacking the

**[00:08]** role payload from the JSON, calculate additional eliminated metrics, materialize this as a table,

**[00:14]** create Lake House Monitor, either via the UI or API, we'll show both experiences, navigate the

**[00:21]** generated dashboard and show how one can potentially create a SQL alert on top of a specific metric

**[00:27]** of interest. So let's jump to the last demo to showcase how we can unpack that inference table,

**[00:36]** compute some metrics, walk you through what a monitor creates and enable that on our inference

**[00:42]** table. So first thing first, so you do remember that inference table that we created previously,

**[00:47]** let's do a quick check and you can see that in the meantime I've run some batch inferences on that

**[00:54]** table. So I have a couple of requests which came in which are ready for me for to be unpacked.

**[01:01]** So unpacking the table will also depend on the input signature of the model. Here this is where

**[01:08]** there might be some different nuances on how the input request JSON past should be here because

**[01:14]** we were following for our model, the TensorFlow input serving format, which usually the format

**[01:20]** will look like you would have an input and then an array of queries containing the user questions.

**[01:25]** This is how we define the JSON past but we do provide well detailed explanations in our

**[01:30]** documentation on how depending on the format of the inputs, how to pre-define the input request

**[01:37]** JSON past and type and if potentially it is a multi-turn conversational chatbot, you also want to

**[01:47]** ensure that you're only keeping like the last exchange of the history because usually the content

**[01:53]** of the whole conversation is always persisted as part of prompts. Defining what column contains,

**[02:00]** let's say the key for the outputs. So here again because our output format is predictions

**[02:05]** containing the list of answers, so it's prediction and informing it that inside it is an array of

**[02:13]** string. So that's where you might potentially given how you format the DDI messages and signature,

**[02:20]** you might need to modify things in the provided template. But once you define that,

**[02:25]** you feed it to an unpacking helper method that we've pre-created for you and again made available

**[02:32]** in the documentation notebooks. So here we'll just do a quick test on a sample of 10 observations.

**[02:38]** So here technically we can see that after unpacking we have the model identifier as we know we can

**[02:45]** use as a grouping variable. We can see the different the inputs and the outputs. That's it. Now for

**[02:52]** sake of simplicity we did not persist the sources even though it is a rack chain. Again you could parse

**[02:59]** and have an additional source field as part of your unpacking logic if you've persisted that in the

**[03:05]** output of the system. So now that we have an inference table this is where you can bring in

**[03:12]** all the metrics of interests and run these at scale using pandas user defined function. So here

**[03:21]** what we will do is we'll use common open source Python packages to calculate the number of tokens,

**[03:30]** the fleshkincade grade, the automated reliability index, the toxicity and the perplexed.

**[03:36]** Both on the inputs and the outputs. And this is where again these are provided in the template

**[03:42]** notebook. This is where you can also add in your own metrics as well and we'll wrap everything

**[03:48]** in a nice and easy method called compute metrics which will take the request data spark data from

**[03:54]** input tell it on which column we want to apply these measures and every time append a new column

**[04:01]** run the pandas udf to calculate all the metrics of interests. So that's it. So that's like the second

**[04:08]** step on packing defining the functions for the LLM related metrics of interest and schedule this to run

**[04:17]** as a streaming job. So again whether you're familiar or not with spark structure streaming that's

**[04:23]** really not a block or an issue here. The good thing is that delta tables can be used as an input

**[04:29]** for source for a streaming job. So here what we're telling here we're going to create a streaming job

**[04:35]** which will just look at the source inference table unpack the request. We'll drop the columns that are

**[04:42]** not necessary for monitoring. We'll compute the metrics and we'll use an initial helper function to

**[04:50]** pre-create the new unpack table with the metrics if that table does not exist and persist this into a

**[04:57]** new table in our catalog called rag app process inference. And usually this whole piece happening here

**[05:05]** where we are reading the stream unpacking the requests dropping the column computing the metrics

**[05:12]** and writing the stream back to a delta table in an append fashion to our new process table.

**[05:21]** These like two three sections of the notebook this is what you would usually schedule to run either

**[05:26]** as a trigger job or a continuous streaming job. So in a sense that as new payloads gets persisted to

**[05:34]** the inference table they will be automatically read the stream will pick it up based on the previous

**[05:39]** checkpoint location and do all the unpacking calculating the metrics and then just persisting writing

**[05:47]** the stream back to a delta table and that's pretty much it. So while our processed table with the metrics

**[05:54]** is calculated let's talk about to review the basics of the chaos monitoring. So again the way it

**[06:01]** works it is a data centric solution which you enable at a table level and here our starting point table

**[06:08]** is going to be that unpacked inference table with the LLM related metrics of interest.

**[06:16]** And so once we have that inference table ready we can enable the monitoring on top. Now usually we

**[06:24]** have three types of monitor that can be created on top of a table. So time series is just through

**[06:32]** is let's say the default profile where again we are going to profile the data and look at drift

**[06:38]** from a time series perspective given the granularity that you set at the monitor creation.

**[06:45]** inference log is the format specific to machine or supervised machine learning system

**[06:52]** like classification and regression and snapshot is just if you want to asynchronously compare

**[06:58]** different versions of a table at manually defined one in time. Now when it comes to monitoring

**[07:06]** our LLM system the time series profile is the type of profile that you will be using on the inference

**[07:14]** table. So now that the inference table has been created let's just take a look at again what table is

**[07:20]** being populated in at the pace of the streaming job. So we have the prompts the completions

**[07:27]** and all the metrics the toxicity perplexity token count can cater of the input

**[07:33]** to realize the reliability index and the same for all the outputs. And so what's going to be

**[07:39]** of interest is to monitor all those potential model from a time series perspective how all these

**[07:45]** metrics might be changing through time. So how can we enable a monitor? There are two options.

**[07:52]** The first one is to do it via the UI. So let's start with that experience because

**[07:58]** it can be the most easy one to show and to demonstrate. So if I go to my processed inference table

**[08:05]** right here any table under unity catalog will have a quality tab available for it. If a monitor exists

**[08:14]** then you will already have information here. If a monitor does not exist you will see this gets

**[08:19]** started wizard. So here first you pick a profile. So here we open the time series we'll define the

**[08:25]** granularity. So here again given like the the reality of the data and that I've batched my requests

**[08:30]** in five minute windows I'm going to pick the smallest granularity supported which is five minute

**[08:36]** but usually in real time in a more common situation you might be looking at things maybe hourly or

**[08:42]** daily or whatnot. Defining which call and represents your timestamp is important and that's it there's

**[08:49]** nothing more to add. Now you can also set the schedule for refreshing the monitoring metrics or just

**[08:56]** have it done manually. You can set notifications on failures of refreshes. What's also important

**[09:02]** is to define in which schema under which schema are database you want those profile and drift metrics

**[09:11]** table to be created. You can also define a baseline table for if you want to compare drift or let's

**[09:20]** say you have a baseline model which has specific for your evaluation set or test set has specific values

**[09:27]** for all these tests that you did and want to compare how far we are from the baseline you can point

**[09:33]** it to that same let's say unprocessed inference table for the baseline model on baseline data set. We

**[09:40]** won't be doing that today but because it's optional but this will allow you to measure things such as

**[09:45]** drift compared to a baseline model. You can add slicing expressions so slicing expression let's say for

**[09:52]** example that I want to look at performance per model ID so you can usually you can either just say

**[09:59]** list the name of the categorical column but you can also use you can also create use equalities or

**[10:06]** inequalities. Let's say it doesn't apply to our table here but if you want to look at I don't know

**[10:11]** metrics where maybe you have an input where the age of the user is higher or lower than that you can

**[10:16]** define those like slicing expressions using in equal SQL inequalities and that's pretty much it

**[10:22]** so once you do that you hit the create button and the monitor will be created. So that's how you do

**[10:30]** it via the UI while the monitor gets created and we can we'll get back to it. Let's also see how

**[10:36]** you can do exactly the same using the the Databricks SDK. So with the Databricks SDK there is under

**[10:48]** the service class and the catalog you can define which profile you want to use whether it's a

**[10:53]** monitor time series or an inference log or a snapshot and with that same workspace client

**[11:01]** which exposes we saw serving endpoint it also exposes a quality monitor API. So that's the quality

**[11:08]** monitor this is how we can create an endpoint sorry and that's how we can create a monitor using the

**[11:14]** create method. So the starting point that it needs is the table name and always make sure to use the

**[11:20]** three level namespace otherwise the default schema and catalog will be used and here I'm telling it I

**[11:26]** want time series profile that is my timestamp colon and this is the granularities that I want. Note

**[11:32]** that you can have multiple granularities at a time it doesn't have to be one defining your slicing

**[11:38]** expressions and telling it once you're going to create those this profile metrics table and the

**[11:45]** Durstmetrics table store these under that specific output schema and that's it. So I won't run

**[11:52]** this command because my monitor already exists but you can do a quick status check on the table to see

**[11:59]** if the monitor already exists. So normally I do that yeah I should have probably imported my client first

**[12:08]** so once I'll do the essentially the client there we go okay so now we can do a quick get monitor

**[12:15]** so it's telling me that the status is active and that it's not pending so it sounds like my monitor has

**[12:25]** been created. So let's do a quick status to make sure do a quick pulse check to ensure that the monitor

**[12:31]** has been created looks like it did. Now one thing to ensure the success of the creation of the dashboard

**[12:40]** is to make sure that you have an accessible Databricks SQL cluster up and running because

**[12:45]** the for the dashboard to be created and create the queries and execute them and populate the graph

**[12:52]** a Databricks SQL cluster must be up and running ahead of time. Let's go and and take a quick check

**[12:59]** at our created monitor so that's what we're expecting to see once the monitor has been created successfully

**[13:05]** so you could have a link to the dashboard a link to the different profile and Durstmetrics table

**[13:11]** and what not so we can quickly try to query those tables so from the monitor info

**[13:18]** there will be a link to the profile metrics table name and also a link to the Durstmetrics table name

**[13:25]** now that the monitor has been set up and the refresh of the table as ran I can take a look at my

**[13:30]** profile metrics table so the way to interpret this is that for every five minute time window that

**[13:37]** was found inside the process different stable for the given model ID value you can look at there's

**[13:44]** going to be different types of metrics such as length, non-null columns, frequent items, median etc

**[13:52]** and same for the Durstmetrics table but what's going to be important is not

**[13:58]** how the row information is going to being laid out is how you can query it and get a sense out of it

**[14:05]** so for that we are going to examine the dashboard board that specific monitor so let's jump

**[14:12]** back into the catalog and our processed inference table so now you can see in the quality tab that I have

**[14:25]** all my different monitoring metrics when the last three fresh happened and I can trigger refresh

**[14:31]** manually I can enter the monitor configuration and I can also see my dashboard and you can also see

**[14:37]** here those the two newly created tables the drift metrics and the profile metrics and the link to

**[14:43]** the dashboard so let's take a quick look at that dashboard and see how we can use that to monitor

**[14:50]** our system let's give it a couple of minutes to spin off the warehouse so you can see on the top left

**[15:02]** of that dashboard you can choose the inspection windows you can look at specific granularities you

**[15:09]** can decide if you want to look at metrics for a specific model identifier so let's take a look at

**[15:16]** what's inside that dashboard so most of the information up here are let's say

**[15:22]** genai agnostic and ascent that we just have we can see the count of the requests happening every

**[15:27]** five minutes if there's any high zeros or null zeros are probably irrelevant in text but at least

**[15:34]** the number of nulls can be important is there any high drift in numerical columns looking at

**[15:40]** again high nulls in specific columns looking at data integrity over time for any given column of

**[15:47]** interest that we can put here and you can also see that again for every column every inspection window

**[15:54]** what the data integrity information is given that we don't have a baseline table let's take a look

**[15:59]** at for example consecutive drift and let's see for example since we're interested primarily in

**[16:06]** numerical drift is there any significant change in maybe the toxicity of your output so let's

**[16:13]** we can take a quick look at the time series of the toxicity compared to previous window and when

**[16:19]** we think about an numerical drift you can look at the p-value of the ks test or maybe looking at

**[16:25]** population stability indexes so that this for example will give us chart on is there like a high

**[16:32]** drift in the toxicity of my output in between consecutive windows categorical drift is probably here

**[16:41]** meaningless because we only have purely unstructured text but other things that for time series that are

**[16:48]** provided out of the box so let's say again I want to plot the time series of the toxicity maybe

**[16:54]** of my input this time look at the average toxicity on five-minute windows of my input

**[17:00]** so I can see the chart of this toxicity metric and let's say I want to be alerted in case the toxicity

**[17:07]** value goes beyond the specific threshold what I can do here is I can go to the specific query which

**[17:16]** is automatically generated on top of the drift metric stable and so here I can see the query I can

**[17:23]** rerun it I can parameterize it but what I can do on top of that query is create an alert and usually

**[17:30]** the way alerts get created is you can give it a name you can tell it that again is the metric which is

**[17:37]** in our case our toxicity is it higher than if is the average value for example higher than 0.1 you

**[17:46]** can decide how you want to be notified if you know this rule is violated once or multiple time you

**[17:52]** can define notification and you can use custom template in the body of the email and then that's it

**[18:00]** you can create your alert and you can add schedules and then you can add destinations so the destinations

**[18:06]** could be an email address the Slack webhook team is webhook a page or duty etc there's a list of

**[18:13]** supported integration with the Databricks and thousands platform geore integration is also coming soon

**[18:19]** so that's it so this is how you could self-serve yourself and create a feedback loop to

**[18:24]** proactively be alerted on potential and on metrics exceeding specific dangerous thresholds

**[18:30]** so to conclude on Lake House Monitoring so the way we set it up today is on a single table because

**[18:37]** this is how usually things work but making sure you want to use this as part of a more general workflow

**[18:43]** when you're dealing with AI system with multiple components you can run you can enable this

**[18:49]** monitoring at the different stages of the development so whether you're doing this in development you're

**[18:55]** doing this in test or even in production so you don't necessarily have to only monitor what's

**[19:01]** happening at the production level you can also start doing some pre-monitoring in your testing in

**[19:06]** development environment and some other tips that you can also do you can also use this tools to so it

**[19:13]** is again recommended to monitor the tables of all the components you could also monitor how the

**[19:18]** embeddings are changing through time for example you could monitor not only the inference tables but

**[19:23]** maybe monitoring any type of other feature table that you also might be looking at you can also use

**[19:30]** this tool to monitor costs so we didn't touch upon it today during the module but all the Databricks

**[19:36]** associated costs for any system that you're using in the platform is logged automatically in a

**[19:42]** unity catalog called system tables and you can create your own queries or views on top of these

**[19:50]** cost component and create the monitor on top of that view or table make sure to refresh the table

**[19:56]** and dashboards regularly because the dashboards usually they'll query what's their static you can

**[20:04]** set a schedule for them to refresh themselves or refresh the queries powering each one of the chart

**[20:10]** so make sure you set a schedule for that and also make sure that the monitor schedule refresh

**[20:17]** is in sync with the pace at which the monitor table is changing so if you know that the monitor table

**[20:23]** is changing or is getting requests maybe every five minutes or so and you're not really interested in

**[20:30]** seeing what's happening every five minutes but maybe every half hour so set your schedule for the

**[20:35]** monitor to be for example every 30 minutes such as a refresh will have in every 30 minute and only

**[20:42]** process incrementally the latest 30 minutes of data because that's how the monitoring system work

**[20:47]** it is an incremental runner so it doesn't scan the full table every time it will only scan what has

**[20:53]** changed in the table between last three fresh and current three fresh and to run things in an

**[20:59]** optimized and cost-efficient fashion

