# Demo LLM - a

**Source:** `Generative AI Application Evaluation and Governance - Demo LLM-a.mp4`
**Duration:** 10:15
**Language:** en (detected with 100.0% confidence)

---

## Full Transcription

We're going to do LM as a judge. In this case, in that LM as a judge, I'm going to show how we can use that to go and create a custom metric called professionalism. We're going to define some examples, define the rubric for it, and then we're going to let LM go and use that rubric to go and evaluate our own examples that we have, right? So we're going to go and do that. Okay, so in this demo, it's continuation for the evaluation demos. And in the last demo we showed, how do we evaluate when we have a ground truth or a benchmark data set that we can use to compare against and use that to compare different models. But the problem with a lot of generative AI applications is in a lot of cases, the task or what we're trying to do, there isn't a benchmark to use to work with or the benchmarks that do exist don't align either deep enough or specific enough to the task that we're trying to do. So one strategy that is evolved is using an LM to judge the output of an LM. The LM's have this reasoning capability and we found that they're actually quite good in some cases as good as humans when it comes to judging the output of another LM. So in this demo, we're going to show how to use LM to evaluate using another LM. And then we're going to look at how we can define a custom metric using that and we're going to show how we can do this all using MLflow. The new MLflow evaluate has support for LM's as a judge and we'll talk about how we can go and define them. So I ran this before making sure again, run your requirements, run your setup. We're good to go. So why go and do LM's as a judge? I talked about it before, but really, we found that there's three main things. Even if you can do human eval is more costly in a lot of cases. Using LM as a judge is just a much more economical way to go and scale evaluation for LM based applications. But you can save us time, humans take time, they're busy. We have a lot of things that we're trying to do. So whereas LM is on command, we can have it go and do things and we can automate on it, which is really big. So in a lot of cases, it's a great piece to help us automate our testing and evaluation and then really putting humans where the LM can't figure it out. So LM is a judge really popular strategy. We can also do custom metrics as well. So in this case, we're going to consider a custom metric called professionalism where we measure the style of the output of the LM and check it for professionalism. Is it professional or not? And that's really useful for a lot of us that are building chatbots to customers where we want to make sure that the chat style is reflective of our customers, of our company's branding and things like that. Okay, so for this demo, we'll be using a chatbot system so for our chatbot system, we have here. We can answer simple questions like what is the expected search and then it goes and answers that. And we're really less worried about the system and really more about evaluating the system. So I'm not going to go into details of this chatbot system. Here we're really concerned about is evaluating its response. And in this case, defining a custom metric that we're going to use in LLM to go and generate measurements. So we're going to define what a professionalism metric we're going to go and define how to compute that in a few examples. And then we're going to define some best practices when using LLM's value here. So let's go into find a metric. So when we use LLM to evaluate a common metric, we need to create our own custom metric. So to this, we need a definition of what professionalism is. We need a greeting prompt or a rubric. We need examples of those responses, of human-graded responses. And then we can then define the LLM and pass that to the LLM so that it can use to go and create our response. So let's establish the definition. So before we create the metric, we need to understand what professionalism is and how it will be scored. So let's use a definition. Professionalism refers to the use of formal, respectful, and appropriate style communication that is tailored to the context and audience. It often involves avoiding overly casual language, playing or localisms. And instead, use clear concise and respectful language. So here's our greeting prompt. So based on that definition, a low score is something that is extremely casual, informal, and may include slang or colloquialisms. Where something professional is known as the formal, respectful avoids casual elements and appropriate for formal business and economic setting. So that's what we want the model kind of a high score is leaning towards this definition and a low score is leaning towards this definition. But this rubric is gonna be used by the language model to understand what is good and what is bad and how to scale between good and bad. Okay, so we have that. The next thing we're gonna do is generate some human-graded responses. So then it has an example to work with, even though we have this scoring in this rubric, it's always good to have a example. So that's what we'll do too, is we'll generate two examples with the input, output, the score, and the justification. But the model can use this context. So then when it goes and sees a new example, it can figure out how to do that. So if you think about it, it's a few-shot example technique. So let's define two examples. So here's one, what is MLflow? MLflow is like your friendly neighborhood toolkit for managing your machine learning projects. So this scores is a two. And the reason here is it's a casual tone, uses contradictions, filler words, and exclamation parts, which makes it less professional. And then here's another example. What is MLflow? MLflow is an open-source toolkit for managing machine learning projects. It can be used to track experiments, project code, models of value performance. And then this example is a written in a professional tone. It is not used filler words or unprofessional proxiation is matter of fact, but it's not particularly advanced or academic. So this we give it as a score of four. So it gives us examples the model can work with. So now that we have all kind of the ingredients, the MLflow needs to go and use LMs as a judge, we can then finally make this custom metric. So we're creating the custom metric. We need to find a couple of things, arguments. So the name of the metric, professional, a definition of it. So the definition we had earlier, the grading prompt that we defined from one to five, two examples, and then the model that we want to use, DVRX Instruct, configurations for the model, and then our aggregations that we might want for it. So what's mean and the variance for it, and then greater is better. Basically higher numbers mean better, lower numbers mean less. In this case, higher numbers do mean better. Sometimes our scoring might mean opposite. So that's just to help it out. So we've now defined the metric. The next thing we can go do is now jump into actually using it. So let's go and grab some evaluation data that we want to go and evaluate. So here's our evaluation data to samples. Be very unprofessional in your response. What is Apache Spark? And then what is Apache Spark? Is there inputs? And then we'll pass that to our chatbot system to generate some outputs that then we're going to evaluate. So let's go and do that. So here we're creating iteration. So it's passing it to the model, have it go and generate the answer. And then we're testing that here, making sure we get an answer. So you can see the first one, a little more casual, where the last second one is a little more professional. It's staying with the style of the way the question was asked. And then we can go and send it to MLflow evaluate. And you'll see here with MLflow evaluate, a similar to before, we have our question iteration, the eval data. And then the thing here is because we're not measuring it to a target data set, you'll notice that's not here. There's no target that we're trying to hit. And the model type here is question answering. And then the metric we're using is the professional metric that we defined earlier. So it's going to go and run an experiment. It's going to go and evaluate it against that. And then it's going to log that out. So here we can see the results of that. So let's go and look at it in MLflow. So you can see here, the last run, you can see the experiment, the notebook, you can see the values for this, you can see the score one and three. I think we only ran on two samples. We don't see the toxicity scores. We can look at the artifacts. Right, and you can see here, the example and the outputs that we got. So here you can see the outputs, token count, professionalism, and then you can see the reasoning that's here. So you can see that for each example. We can also pull that up in our notebook as well. So here I'm pulling it up as a table. So here's our results. You can see same thing, similar as what we saw in MLflow. And then you can see here the responses. If we look at the first one, pay their buddy, really casual and a response. The response, usually casual, it includes the phrase like, hey, they're buddy, and closing sense slice spread, whereas the second one is in a formal respectful tone. That gets the score of. That's really cool. So basically, what it means is, if we have a task that we don't have a benchmark, what it allows us to do is start using LLMs as a way to scale and automate our evaluations. Right, on custom tasks that otherwise would be very difficult to go and do and get this process started in cases where we either don't have a ground-truve data set or we don't have human bandwidth to go and do that or human capital to go and do that and we can leverage an LLM to do that for it. Now, a couple of things as LLM best practices, you small rubric scales, what we found is evaluation scale that are small, like one to three or one to five, don't do a one to 10. It's a lot harder for the LLM to pick between those. So that's typically something. Provide a variety of examples, typically examples, not just a lot, but variety you want. It's a good example and bad examples for the model so that it can get a better understanding of what is a one, what is a two, what is a three. Consider an additive scale. The one point for X, one point for Y, zero points for Z and then adding those up. That might be a way to break down the evaluation actually. That might be a great way so that we can then decompose the evaluation and then use a high token LL if you're able to use more tokens, you can provide more context. So when it comes to that, we're talking about context windows, the models that have a larger context window mean that we can provide them more examples so that we can get better results out of it. So that is LLM as a judge. Pretty cool, another strategy when it comes to evaluating generative AI applications, especially when we don't have a ground truth or a data set to work with and how we can do that on Databricks with MLflow in its integrations to the platform.

---

## Timestamped Segments

**[00:00]** We're going to do LM as a judge.

**[00:01]** In this case, in that LM as a judge,

**[00:03]** I'm going to show how we can use that to go

**[00:05]** and create a custom metric called professionalism.

**[00:07]** We're going to define some examples,

**[00:09]** define the rubric for it,

**[00:10]** and then we're going to let LM go

**[00:12]** and use that rubric to go and evaluate

**[00:14]** our own examples that we have, right?

**[00:16]** So we're going to go and do that.

**[00:18]** Okay, so in this demo,

**[00:21]** it's continuation for the evaluation demos.

**[00:24]** And in the last demo we showed,

**[00:26]** how do we evaluate when we have a ground truth

**[00:29]** or a benchmark data set that we can use

**[00:31]** to compare against and use that

**[00:33]** to compare different models.

**[00:35]** But the problem with a lot of generative AI applications

**[00:38]** is in a lot of cases,

**[00:40]** the task or what we're trying to do,

**[00:43]** there isn't a benchmark to use to work with

**[00:46]** or the benchmarks that do exist

**[00:48]** don't align either deep enough

**[00:50]** or specific enough to the task that we're trying to do.

**[00:53]** So one strategy that is evolved

**[00:55]** is using an LM to judge the output of an LM.

**[00:59]** The LM's have this reasoning capability

**[01:01]** and we found that they're actually quite good

**[01:04]** in some cases as good as humans

**[01:07]** when it comes to judging the output of another LM.

**[01:10]** So in this demo,

**[01:11]** we're going to show how to use LM to evaluate

**[01:14]** using another LM.

**[01:15]** And then we're going to look at how we can define

**[01:18]** a custom metric using that

**[01:20]** and we're going to show how we can do this all using MLflow.

**[01:23]** The new MLflow evaluate has support for LM's as a judge

**[01:26]** and we'll talk about how we can go and define them.

**[01:28]** So I ran this before making sure again,

**[01:30]** run your requirements, run your setup.

**[01:32]** We're good to go.

**[01:35]** So why go and do LM's as a judge?

**[01:38]** I talked about it before, but really,

**[01:39]** we found that there's three main things.

**[01:41]** Even if you can do human eval is more costly in a lot of cases.

**[01:45]** Using LM as a judge

**[01:47]** is just a much more economical way

**[01:49]** to go and scale evaluation for LM based applications.

**[01:54]** But you can save us time, humans take time, they're busy.

**[01:56]** We have a lot of things that we're trying to do.

**[01:58]** So whereas LM is on command,

**[02:00]** we can have it go and do things

**[02:02]** and we can automate on it, which is really big.

**[02:04]** So in a lot of cases,

**[02:05]** it's a great piece to help us automate our testing

**[02:10]** and evaluation and then really putting humans

**[02:12]** where the LM can't figure it out.

**[02:14]** So LM is a judge really popular strategy.

**[02:17]** We can also do custom metrics as well.

**[02:19]** So in this case, we're going to consider a custom metric

**[02:21]** called professionalism

**[02:22]** where we measure the style of the output of the LM

**[02:26]** and check it for professionalism.

**[02:27]** Is it professional or not?

**[02:28]** And that's really useful for a lot of us

**[02:30]** that are building chatbots to customers

**[02:33]** where we want to make sure that the chat style

**[02:36]** is reflective of our customers,

**[02:38]** of our company's branding and things like that.

**[02:41]** Okay, so for this demo,

**[02:43]** we'll be using a chatbot system

**[02:45]** so for our chatbot system,

**[02:47]** we have here.

**[02:49]** We can answer simple questions

**[02:50]** like what is the expected search

**[02:52]** and then it goes and answers that.

**[02:54]** And we're really less worried about the system

**[02:57]** and really more about evaluating the system.

**[03:00]** So I'm not going to go into details of this chatbot system.

**[03:02]** Here we're really concerned about is evaluating its response.

**[03:06]** And in this case, defining a custom metric

**[03:08]** that we're going to use in LLM to go and generate measurements.

**[03:11]** So we're going to define what a professionalism metric

**[03:14]** we're going to go and define how to compute that

**[03:16]** in a few examples.

**[03:17]** And then we're going to define some best practices

**[03:20]** when using LLM's value here.

**[03:22]** So let's go into find a metric.

**[03:23]** So when we use LLM to evaluate a common metric,

**[03:26]** we need to create our own custom metric.

**[03:27]** So to this, we need a definition of what professionalism is.

**[03:30]** We need a greeting prompt or a rubric.

**[03:33]** We need examples of those responses,

**[03:36]** of human-graded responses.

**[03:37]** And then we can then define the LLM and pass that to the LLM

**[03:41]** so that it can use to go and create our response.

**[03:44]** So let's establish the definition.

**[03:46]** So before we create the metric,

**[03:47]** we need to understand what professionalism is

**[03:49]** and how it will be scored.

**[03:50]** So let's use a definition.

**[03:52]** Professionalism refers to the use of formal, respectful,

**[03:55]** and appropriate style communication

**[03:57]** that is tailored to the context and audience.

**[03:59]** It often involves avoiding overly casual language,

**[04:02]** playing or localisms.

**[04:04]** And instead, use clear concise and respectful language.

**[04:06]** So here's our greeting prompt.

**[04:08]** So based on that definition, a low score

**[04:10]** is something that is extremely casual, informal,

**[04:13]** and may include slang or colloquialisms.

**[04:15]** Where something professional is known as the formal,

**[04:17]** respectful avoids casual elements

**[04:19]** and appropriate for formal business and economic setting.

**[04:22]** So that's what we want the model kind of a high score

**[04:24]** is leaning towards this definition

**[04:26]** and a low score is leaning towards this definition.

**[04:28]** But this rubric is gonna be used by the language model

**[04:32]** to understand what is good and what is bad

**[04:34]** and how to scale between good and bad.

**[04:38]** Okay, so we have that.

**[04:40]** The next thing we're gonna do

**[04:41]** is generate some human-graded responses.

**[04:43]** So then it has an example to work with,

**[04:46]** even though we have this scoring in this rubric,

**[04:49]** it's always good to have a example.

**[04:51]** So that's what we'll do too,

**[04:52]** is we'll generate two examples with the input,

**[04:54]** output, the score, and the justification.

**[04:56]** But the model can use this context.

**[04:57]** So then when it goes and sees a new example,

**[05:00]** it can figure out how to do that.

**[05:01]** So if you think about it,

**[05:02]** it's a few-shot example technique.

**[05:04]** So let's define two examples.

**[05:07]** So here's one, what is MLflow?

**[05:09]** MLflow is like your friendly neighborhood toolkit

**[05:11]** for managing your machine learning projects.

**[05:13]** So this scores is a two.

**[05:14]** And the reason here is it's a casual tone,

**[05:16]** uses contradictions, filler words,

**[05:18]** and exclamation parts, which makes it less professional.

**[05:21]** And then here's another example.

**[05:23]** What is MLflow?

**[05:24]** MLflow is an open-source toolkit

**[05:25]** for managing machine learning projects.

**[05:27]** It can be used to track experiments,

**[05:28]** project code, models of value performance.

**[05:31]** And then this example is a written in a professional tone.

**[05:34]** It is not used filler words

**[05:35]** or unprofessional proxiation is matter of fact,

**[05:38]** but it's not particularly advanced or academic.

**[05:40]** So this we give it as a score of four.

**[05:42]** So it gives us examples the model can work with.

**[05:45]** So now that we have all kind of the ingredients,

**[05:47]** the MLflow needs to go and use LMs as a judge,

**[05:51]** we can then finally make this custom metric.

**[05:53]** So we're creating the custom metric.

**[05:55]** We need to find a couple of things, arguments.

**[05:57]** So the name of the metric, professional,

**[05:59]** a definition of it.

**[06:01]** So the definition we had earlier,

**[06:02]** the grading prompt that we defined from one to five,

**[06:05]** two examples, and then the model that we want to use,

**[06:09]** DVRX Instruct, configurations for the model,

**[06:11]** and then our aggregations that we might want for it.

**[06:14]** So what's mean and the variance for it,

**[06:16]** and then greater is better.

**[06:19]** Basically higher numbers mean better, lower numbers mean less.

**[06:21]** In this case, higher numbers do mean better.

**[06:23]** Sometimes our scoring might mean opposite.

**[06:25]** So that's just to help it out.

**[06:27]** So we've now defined the metric.

**[06:29]** The next thing we can go do is now jump into actually using it.

**[06:34]** So let's go and grab some evaluation data

**[06:35]** that we want to go and evaluate.

**[06:37]** So here's our evaluation data to samples.

**[06:39]** Be very unprofessional in your response.

**[06:41]** What is Apache Spark?

**[06:42]** And then what is Apache Spark?

**[06:44]** Is there inputs?

**[06:45]** And then we'll pass that to our chatbot system

**[06:48]** to generate some outputs that then we're going to evaluate.

**[06:51]** So let's go and do that.

**[06:53]** So here we're creating iteration.

**[06:56]** So it's passing it to the model,

**[06:57]** have it go and generate the answer.

**[06:59]** And then we're testing that here,

**[07:01]** making sure we get an answer.

**[07:02]** So you can see the first one,

**[07:04]** a little more casual,

**[07:06]** where the last second one is a little more professional.

**[07:09]** It's staying with the style of the way the question was asked.

**[07:12]** And then we can go and send it to MLflow evaluate.

**[07:15]** And you'll see here with MLflow evaluate,

**[07:17]** a similar to before,

**[07:18]** we have our question iteration,

**[07:21]** the eval data.

**[07:23]** And then the thing here is because we're not measuring it

**[07:27]** to a target data set,

**[07:28]** you'll notice that's not here.

**[07:29]** There's no target that we're trying to hit.

**[07:31]** And the model type here is question answering.

**[07:33]** And then the metric we're using

**[07:34]** is the professional metric that we defined earlier.

**[07:37]** So it's going to go and run an experiment.

**[07:38]** It's going to go and evaluate it against that.

**[07:40]** And then it's going to log that out.

**[07:42]** So here we can see the results of that.

**[07:44]** So let's go and look at it in MLflow.

**[07:46]** So you can see here, the last run,

**[07:49]** you can see the experiment,

**[07:51]** the notebook,

**[07:52]** you can see the values for this,

**[07:53]** you can see the score one and three.

**[07:56]** I think we only ran on two samples.

**[07:58]** We don't see the toxicity scores.

**[08:00]** We can look at the artifacts.

**[08:02]** Right, and you can see here,

**[08:03]** the example and the outputs that we got.

**[08:06]** So here you can see the outputs,

**[08:08]** token count, professionalism,

**[08:09]** and then you can see the reasoning that's here.

**[08:11]** So you can see that for each example.

**[08:13]** We can also pull that up in our notebook as well.

**[08:15]** So here I'm pulling it up as a table.

**[08:17]** So here's our results.

**[08:18]** You can see same thing,

**[08:19]** similar as what we saw in MLflow.

**[08:21]** And then you can see here the responses.

**[08:23]** If we look at the first one,

**[08:24]** pay their buddy, really casual and a response.

**[08:27]** The response, usually casual,

**[08:28]** it includes the phrase like,

**[08:29]** hey, they're buddy,

**[08:30]** and closing sense slice spread,

**[08:32]** whereas the second one is in a formal respectful tone.

**[08:34]** That gets the score of.

**[08:36]** That's really cool.

**[08:37]** So basically, what it means is,

**[08:39]** if we have a task that we don't have a benchmark,

**[08:41]** what it allows us to do is start using LLMs

**[08:44]** as a way to scale and automate our evaluations.

**[08:47]** Right, on custom tasks that otherwise

**[08:50]** would be very difficult to go and do

**[08:52]** and get this process started in cases

**[08:54]** where we either don't have a ground-truve data set

**[08:57]** or we don't have human bandwidth to go and do that

**[08:59]** or human capital to go and do that

**[09:01]** and we can leverage an LLM to do that for it.

**[09:04]** Now, a couple of things as LLM best practices,

**[09:07]** you small rubric scales, what we found is evaluation scale

**[09:10]** that are small, like one to three or one to five,

**[09:12]** don't do a one to 10.

**[09:13]** It's a lot harder for the LLM to pick between those.

**[09:16]** So that's typically something.

**[09:18]** Provide a variety of examples,

**[09:20]** typically examples, not just a lot,

**[09:23]** but variety you want.

**[09:24]** It's a good example and bad examples for the model

**[09:27]** so that it can get a better understanding of what is a one,

**[09:30]** what is a two, what is a three.

**[09:31]** Consider an additive scale.

**[09:33]** The one point for X, one point for Y,

**[09:35]** zero points for Z and then adding those up.

**[09:37]** That might be a way to break down the evaluation actually.

**[09:40]** That might be a great way

**[09:41]** so that we can then decompose the evaluation

**[09:44]** and then use a high token LL

**[09:45]** if you're able to use more tokens, you can provide more context.

**[09:48]** So when it comes to that,

**[09:49]** we're talking about context windows,

**[09:51]** the models that have a larger context window

**[09:52]** mean that we can provide them more examples

**[09:54]** so that we can get better results out of it.

**[09:57]** So that is LLM as a judge.

**[09:58]** Pretty cool, another strategy

**[10:00]** when it comes to evaluating generative AI applications,

**[10:03]** especially when we don't have a ground truth

**[10:06]** or a data set to work with

**[10:07]** and how we can do that on Databricks with MLflow

**[10:09]** in its integrations to the platform.

