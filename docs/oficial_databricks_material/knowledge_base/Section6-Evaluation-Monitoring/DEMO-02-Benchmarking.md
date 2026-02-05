# Demo Bench

**Source:** `Generative AI Application Evaluation and Governance - Demo Bench.mp4`
**Duration:** 09:30
**Language:** en (detected with 100.0% confidence)

---

## Full Transcription

stop talking about it was jump to a demo where what I'll do in this demo is I'll show two demos right to the one is going to be about using a benchmark evaluation where we can use MLflow to go and measure the performance of two different LLMs against the Rouge scores right on summarization tasks right that's we're going to do and then we're going to compare the two. So we talked about evaluation we talked about the history evaluation and different metrics we can use such as Rouge and Blue and LLMs as a judge right now if you can the the best thing to do is have a benchmark to do your evaluation against and that's what we're going to talk about first and then if you don't have that we'll do a demo where you talk LLMs as a judge next so benchmark evaluation in this demo we'll be focusing especially using a benchmark to compare our models performance against now in this case we're going to be doing specifically summarization so at the end of this demo we'll talk about how to obtain a benchmark data set right for task specific LLM evaluation which is really common with a lot of LLMs today with a lot of common benchmarks out there it's the same strategy we're going to be doing particularly just one task here which is summarization then we're going to evaluate the LLM performance using task specific metrics we're going to be using MLflow to calculate the Rouge scores and then we're going to compare that performance on two LLMs using benchmark set but go and do that getting started run the requirements in the classroom set up again and then we're going to set up the models that we're going to use we're going to compare two different models in this Databricks says DVRX and LOMA 270B check that what we're going to do is we're going to load those two models in so that's what we're doing here we're going to pull in the Databricks model serving and the workspace client and then we're going to define the first model here as a function queries summary system the message here you can see the system prompt and then the user input and then here is it sent to the endpoint so this is LOMA2 70B and then here's our second one which is our challenger model and in this case similar prompt as we have for the first one except the difference here is we're going to be talking to DVRX so you can see here we have a challenger and then we have the non-challenger so very common is the challenger champion test that's what we're doing here right so we have our models let's see a quick test to make sure they work this is the best frozen pizza overhead running that against that endpoint looks like it works running against this one point looks like it works awesome so at this point we have our models and these are the two models that we're going to be using to compare against our benchmark so the next thing that we want to do is we want to pull in our benchmark so the benchmark we're going to be using is a generic benchmark for new summarization and we can go and take a look at the data set here or the paper here so this is a paper for it if you want to go and take a look but at this day set has a bunch of records in it and it's basically news articles and it has a ground truth summary written by authors so the author is actually wrote the summaries for the article so pretty good summary because it's the writer for it so it's a human based data set so we have that here's our input the article here is the summary from the human writer and that's provided as a CSB so quickly we pull down that data set so you can take a look at but that's what it looks like we have our articles or summary right and we have all right with the scrolling here so the next thing we're going to do is we're going to go and evaluate one of our models right now what we're going to do is we're going to evaluate using Rouge so one of the cool things MLflow is MLflow has added the capability for element evaluations and with that is the ability to go and calculate Rouge scores and do things for text summarization and things like that so that's what we're going to do here is we're going to use MLflow to go and define evaluation so custom fix to iterate through our data frame and generate some summaries and then once we have that we're going to pass that data set to MLflow evaluate to then generate statistics so that's what we're doing here we're going to go through our inputs we're going to go and generate summaries for each of those from model go we can then compare against right so we have go here pass make sure it works and that works we can then go and now use MLflow to go and do that so here you can see MLflow has done the evaluate it's going to go and go through each of our sample items generating output and then it's going to go and evaluate that we're only going to do the first 50 and then we're going to go and evaluate against a target column that writer summary column so this is the good output that it's going to go measure against and then we're going to have it do a text summarization measurement so in that MLflow there's different tasks that you can have it evaluate against and text summarization one of them and behind the scenes that means that it's going to go and run Rouge scores since here that it ran earlier it took about two minutes to go and do that's why I'm not going to run it again because it does take a little bit of time and the cool thing about this is MLflow integrates with MLflow experiments so with that we actually get this logged as an experiment inside of Databricks so you can see here we have our experiment and we have some runs so this was ran earlier today and you can see that we can see the run and the scores with it you can see here it's run we can see the results here so you can see here that's our original data then you can see here this is output from the model that we have and then if we go down and we look at the results we can see the metrics for it so you can see here our run and I think if we take a look I believe this is the actual one itself leave this is the run that ran earlier today and then here you get you can see the metrics and if you're familiar with MLflow this is MLflow experiments this is a run you can see the notebooks and the information with that the metrics were logged here you can also see the artifacts and that's that table that we showed earlier and these are the artifacts for those tables so here we have the run things here inputs outputs and then all the scores that were calculated as part of it so pretty cool all right so we did one run now we only did this run against one model which is the llama demdb model that we just did let's go and take a look at it more into those results and see what good looks like so we look at the results we can take a look so here you can see with a .4 score this is our input and this is our output you can see quite good actually ultimate pair letting it need for change and you can see that ends up pretty good so we have there and when we're looking at Rouge Force typically zero is it is in matching and one is perfect match so typically if you're hitting anywhere in 30 to about 30% or 40% then you're actually really close that there but something you look at I would recommend that everyone go in and take a look at these scores and play deeper into all of that that's there we can look at but really what we're here for is to compare the performance between models it's great to go and look at a single model and be able to evaluate its results and look at all the individual sample outputs but really what we're trying to do here is compare two different models so let's do the same thing again let's go and load up our challenger model so here's our code to do an iteration for it and we're going to go and do the same thing so we're going to have MLflow go through use the challenger and it's going to go and do the same thing generate predictions for 50 rows and then compare it and then calculate the text summarization metrics so it goes through and does that and then it has our run and then here you can see the run for that model run you can see our outputs you can see our scores it looks a little higher than our previous example so that's pretty good to see here we can look at the artifacts and we can see the table so we can see here the table for the outputs and the scores just like the other run but let's actually go and compare the two so well let's go down we can see the metrics let's go and compare the two so one of the cool things in MLflow the new UI inside of the abrix is the ability to chart these results as well as show the evaluations right so I'm going to go pull up the runs here so I'm going to go and hide that one so one thing that we can do is we can see all the runs with this experiment so I've rammed this demo multiple times well let's just highlight two of them and you can see here the scores so we can hear quickly look at the Rouge one scores Rouge two scores Rouge Alstom and we can quickly compare between the challenger model and the old model I believe the brown here's the new one and the green one is the older one and you can see here there is a slight improvement on some of those scores that we have another cool view that we can show is not only can we see a scores and look at them but we can also go and compare visually so with the new evaluations preview I can pull that up and I can actually look at the outputs so let me go and hide one that we just ran you can actually look at the outputs so here you can see the inputs the outputs and we can see really quickly those all right so here if we want to actually put the summary so here's the gold standard and we can compare directly to the generations that's also very useful because sometimes the numbers are the numbers but I like to jump in and actually take a look at why what we actually got right so pretty cool okay so that wrap things up with benchmark evaluation powerful and great especially we do have a ground truth but what happens if we don't so that's why I'm going to show in the next demo with LLMS as a judge is what is it we don't how do we deal with that

---

## Timestamped Segments

**[00:00]** stop talking about it was jump to a demo where what I'll do in this demo is I'll show two demos right

**[00:04]** to the one is going to be about using a benchmark evaluation where we can use MLflow to go and

**[00:10]** measure the performance of two different LLMs against the Rouge scores right on summarization tasks

**[00:16]** right that's we're going to do and then we're going to compare the two. So we talked about evaluation

**[00:20]** we talked about the history evaluation and different metrics we can use such as Rouge and Blue

**[00:28]** and LLMs as a judge right now if you can the the best thing to do is have a benchmark to do your

**[00:34]** evaluation against and that's what we're going to talk about first and then if you don't have that

**[00:39]** we'll do a demo where you talk LLMs as a judge next so benchmark evaluation in this demo we'll be

**[00:44]** focusing especially using a benchmark to compare our models performance against now in this case

**[00:52]** we're going to be doing specifically summarization so at the end of this demo we'll talk about how to

**[00:56]** obtain a benchmark data set right for task specific LLM evaluation which is really common with a lot

**[01:03]** of LLMs today with a lot of common benchmarks out there it's the same strategy we're going to be doing

**[01:08]** particularly just one task here which is summarization then we're going to evaluate the LLM performance

**[01:13]** using task specific metrics we're going to be using MLflow to calculate the Rouge scores and then

**[01:18]** we're going to compare that performance on two LLMs using benchmark set but go and do that getting started

**[01:24]** run the requirements in the classroom set up again and then we're going to set up the models

**[01:28]** that we're going to use we're going to compare two different models in this Databricks says DVRX

**[01:32]** and LOMA 270B check that what we're going to do is we're going to load those two models in so that's

**[01:37]** what we're doing here we're going to pull in the Databricks model serving and the workspace client

**[01:43]** and then we're going to define the first model here as a function queries summary system the message

**[01:50]** here you can see the system prompt and then the user input and then here is it sent to the endpoint

**[01:58]** so this is LOMA2 70B and then here's our second one which is our challenger model and in this case

**[02:05]** similar prompt as we have for the first one except the difference here is we're going to be talking to

**[02:10]** DVRX so you can see here we have a challenger and then we have the non-challenger so very common is

**[02:16]** the challenger champion test that's what we're doing here right so we have our models let's see

**[02:21]** a quick test to make sure they work this is the best frozen pizza overhead running that against that

**[02:26]** endpoint looks like it works running against this one point looks like it works awesome so at this point

**[02:32]** we have our models and these are the two models that we're going to be using to compare against our

**[02:37]** benchmark so the next thing that we want to do is we want to pull in our benchmark so the benchmark

**[02:43]** we're going to be using is a generic benchmark for new summarization and we can go and take a look at

**[02:48]** the data set here or the paper here so this is a paper for it if you want to go and take a look

**[02:53]** but at this day set has a bunch of records in it and it's basically news articles and it has a ground

**[03:00]** truth summary written by authors so the author is actually wrote the summaries for the article so

**[03:05]** pretty good summary because it's the writer for it so it's a human based data set so we have that

**[03:11]** here's our input the article here is the summary from the human writer and that's provided as

**[03:18]** a CSB so quickly we pull down that data set so you can take a look at but that's what it looks like

**[03:22]** we have our articles or summary right and we have all right with the scrolling here so the next

**[03:28]** thing we're going to do is we're going to go and evaluate one of our models right now what we're

**[03:33]** going to do is we're going to evaluate using Rouge so one of the cool things MLflow is MLflow has

**[03:38]** added the capability for element evaluations and with that is the ability to go and calculate

**[03:44]** Rouge scores and do things for text summarization and things like that so that's what we're going to do

**[03:48]** here is we're going to use MLflow to go and define evaluation so custom fix to iterate through our

**[03:54]** data frame and generate some summaries and then once we have that we're going to pass that data set

**[04:00]** to MLflow evaluate to then generate statistics so that's what we're doing here we're going to go

**[04:04]** through our inputs we're going to go and generate summaries for each of those from model go we can

**[04:10]** then compare against right so we have go here pass make sure it works and that works we can then go

**[04:18]** and now use MLflow to go and do that so here you can see MLflow has done the evaluate it's going to

**[04:24]** go and go through each of our sample items generating output and then it's going to go and evaluate that

**[04:31]** we're only going to do the first 50 and then we're going to go and evaluate against a target column

**[04:36]** that writer summary column so this is the good output that it's going to go measure against and then

**[04:41]** we're going to have it do a text summarization measurement so in that MLflow there's different tasks

**[04:46]** that you can have it evaluate against and text summarization one of them and behind the scenes that

**[04:50]** means that it's going to go and run Rouge scores since here that it ran earlier it took about two

**[04:54]** minutes to go and do that's why I'm not going to run it again because it does take a little bit of

**[04:57]** time and the cool thing about this is MLflow integrates with MLflow experiments so with that we

**[05:03]** actually get this logged as an experiment inside of Databricks so you can see here we have our experiment

**[05:09]** and we have some runs so this was ran earlier today and you can see that we can see the run

**[05:14]** and the scores with it you can see here it's run we can see the results here so you can see here

**[05:21]** that's our original data then you can see here this is output from the model that we have and then if

**[05:27]** we go down and we look at the results we can see the metrics for it so you can see here our run

**[05:31]** and I think if we take a look I believe this is the actual one itself leave this is the run that ran

**[05:40]** earlier today and then here you get you can see the metrics and if you're familiar with MLflow this is

**[05:46]** MLflow experiments this is a run you can see the notebooks and the information with that the metrics

**[05:50]** were logged here you can also see the artifacts and that's that table that we showed earlier and these are

**[05:55]** the artifacts for those tables so here we have the run things here inputs outputs and then all the

**[06:01]** scores that were calculated as part of it so pretty cool all right so we did one run now we only did

**[06:07]** this run against one model which is the llama demdb model that we just did let's go and take a look at it

**[06:15]** more into those results and see what good looks like so we look at the results we can take a look so here

**[06:20]** you can see with a .4 score this is our input and this is our output you can see quite good actually

**[06:28]** ultimate pair letting it need for change and you can see that ends up pretty good so we have there

**[06:35]** and when we're looking at Rouge Force typically zero is it is in matching and one is perfect match so

**[06:41]** typically if you're hitting anywhere in 30 to about 30% or 40% then you're actually really close

**[06:46]** that there but something you look at I would recommend that everyone go in and take a look at these

**[06:51]** scores and play deeper into all of that that's there we can look at but really what we're here for

**[06:58]** is to compare the performance between models it's great to go and look at a single model and be able to

**[07:02]** evaluate its results and look at all the individual sample outputs but really what we're trying to do here

**[07:08]** is compare two different models so let's do the same thing again let's go and load up our challenger model

**[07:13]** so here's our code to do an iteration for it and we're going to go and do the same thing so

**[07:18]** we're going to have MLflow go through use the challenger and it's going to go and do the same thing

**[07:22]** generate predictions for 50 rows and then compare it and then calculate the text summarization metrics

**[07:28]** so it goes through and does that and then it has our run and then here you can see the run for that

**[07:32]** model run you can see our outputs you can see our scores it looks a little higher than our previous

**[07:40]** example so that's pretty good to see here we can look at the artifacts and we can see the table

**[07:47]** so we can see here the table for the outputs and the scores just like the other run but let's actually

**[07:53]** go and compare the two so well let's go down we can see the metrics let's go and compare the two so

**[08:00]** one of the cool things in MLflow the new UI inside of the abrix is the ability to chart these results as

**[08:05]** well as show the evaluations right so I'm going to go pull up the runs here so I'm going to go and hide

**[08:11]** that one so one thing that we can do is we can see all the runs with this experiment so I've rammed

**[08:15]** this demo multiple times well let's just highlight two of them and you can see here the scores so we can

**[08:19]** hear quickly look at the Rouge one scores Rouge two scores Rouge Alstom and we can quickly compare

**[08:25]** between the challenger model and the old model I believe the brown here's the new one and the green

**[08:31]** one is the older one and you can see here there is a slight improvement on some of those scores

**[08:36]** that we have another cool view that we can show is not only can we see a scores and look at them

**[08:43]** but we can also go and compare visually so with the new evaluations preview I can pull that up and

**[08:48]** I can actually look at the outputs so let me go and hide one that we just ran you can actually look at

**[08:53]** the outputs so here you can see the inputs the outputs and we can see really quickly those all right so

**[08:58]** here if we want to actually put the summary so here's the gold standard and we can compare directly to

**[09:02]** the generations that's also very useful because sometimes the numbers are the numbers but I like to

**[09:07]** jump in and actually take a look at why what we actually got right so pretty cool okay so that wrap

**[09:14]** things up with benchmark evaluation powerful and great especially we do have a ground truth but what

**[09:20]** happens if we don't so that's why I'm going to show in the next demo with LLMS as a judge is what

**[09:25]** is it we don't how do we deal with that

