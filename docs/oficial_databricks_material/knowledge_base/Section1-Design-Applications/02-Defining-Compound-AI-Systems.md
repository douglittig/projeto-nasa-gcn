# 02 - Defining Compound AI Systems

**Source:** `02-Defining Compound AI Systems.mp4`
**Duration:** 07:43
**Language:** en (detected with 100.0% confidence)

---

## Full Transcription

What is a compound AI system? So you've probably been talking about models over the last few years. But when you look at it, real complex systems that achieve state of the art results aren't just models. They're not just a large language model working on its own. It's typically a large language model in conjunction with other components, things like databases, the ability for it to search on the internet, things like that, into a system or a chain that allows it to achieve its state of the art results. So what are some examples of compound AI systems? We've actually already talked about a few of them in our other courses. For example, prompt engineering is an example of a really simple compound AI system. You're combining an LLM with prompt generation logic, whether that is a template, whether that is auto-generated via frameworks and libraries. But the idea here is through prompt engineering, we're able to improve the output of the model versus just giving the questions directly to the model. We have RAG, where we boost the performance of a large language model by adding and combining it with an external data store, whether that is a vector database or a structured database that we connect to with some type of text to SQL system or something like that in conjunction with it. And today, we're going to be talking about a couple more different architectures, things like agent-based chains and orchestration chains, where instead of us defining every step in a workflow or a pipeline that we're traditionally used to in a lot of software and application, these LLMs are able to do a little bit of planning and reasoning. So we want to take advantage of that. And what we can do is let the LLM figure out the plan and observations and execution path to go and solve some of our problems. So let's go and talk about one system that we already know. That one is RAG, which is really an example of a simple AI system. And if you think about RAG, it's combining two things. It's combining prompt engineering, the idea of few-shot learning and context-driven learning to improve the performance of the model and to pull in an external data store to provide as that context to that prompt. And with that, we can improve the overall system's performance, to be able to answer questions that are more relevant or more domain-specific. So really, if you think about it, a compound AI system is defined as a system that tackles AI tasks using multiple interactioning components, including multiple calls to models, retrievers, and external tools, or even other models, agent-based communication where they're talking with other agents. How do we go and break down or think about decomposing these AI tasks into these systems and components? For example, we're going to use an example here, which is given the objective of building a system to analyze sentiment for Japanese customer reviews, you can think about this problem at a high level, which is that's what we're trying to do. But in order to engineer a system or solution, we need to break it down into smaller pieces. And typically, one way we can think about that is intents and tasks. So you think of an intent as a single objective that we have, that has multiple intents, and an intent is something that consists of one to many tasks. And those tasks can then align to particular things that an LLM or a model or a system can do, for example, things like translation or summarization. So in this example for Japanese customer reviews, some intents that we might have is translation, right? In order to go and calculate the sentiment of this review, we first need to translate the Japanese customer review into English, right? That's one intent. We can then from there take the translation and summarize it, right? A lot of these LLMs can't just take unlimited sizes of data as input or context. So it's very common to compress that with some type of summarization intent. Then analyzing its sentiment could be a different intent. And then once we have the sentiment, we can then classify the type of feedback provided based on our business logic, right? Is that good feedback or is that negative feedback? And all of this would then be put together into a pipeline to go and complete these. So let's dive a little bit deeper on the concept, right? If we look at it, we have a system that we're trying to build, right? That system could be to go and do the Japanese customer reviews, or in this case, it could be used to create personalized responses to customer questions or a QA chat bot. And then that system would be comprised of multiple intents, right? So each intent would be one of those objectives that we're doing, such as translation, summarization, sentiment analysis, classification, things like that. And then each of those intents might require tasks for us to go and do, right? We might need to go and retrieve some information about the customer before we can create the message and things like that. So when you're looking at AI systems, the power of LLMs is that we can go and use them to do a lot of these tasks. And a lot of these agents can do multiple tasks, but what we've found is they do better when we design the LLM to do one task at a time, right? The more constrained the task, the better the performance typically, right? So, for example, we can have them do things like summarization, sentiment analysis, translation, zero-shot, few-shot learning, conversation chat, QA, the list goes on, right? Today, we almost have models and tasks for almost anything that you want to go and do. Especially now, we have things like image generation, video generation models, all those kind of cool things. So if we really look at it today, we're no longer really just building applications that just do a single task. We're actually building applications that do a pipeline or a chain of tasks that are combined together in order to complete those more complex intents and objectives. So in this case, you can see that we, instead of a single task, we have multiple tasks, right? This could be a task to do summarization, and then we might go and then use that summarization to go and do sentiment analysis, and then we might go and do something else after that, compound AI systems. Why would we want to do that? And what are some reasons of why we want to do that? One, I think at the high levels, it makes it easier for us to grasp these complex systems and break them down into pieces that we can manage and develop. But the other thing also is when it comes to LLMs, if we go and just build a solution, for example, here, get the sentiment of many articles on a topic, and we just send all the articles and ask it to go and generate the sentiment, that's going to overload most LLMs, right? We have context windows of limited size, right? And we can't just throw everything at it, right? It's going to lead to an issue where it runs out of context length, right? So that can be a problem. So another reason why we do this is by breaking it down, we can also get better performance, we can also get better latency out of it, right? So in this case, we can break it down into two stages, one in which we summarize the articles first, right? Basically reducing the amount of data that we send into the context, and then by sending only the summaries, the sentiment LLM can then process all those articles. That's an example of how we can get better performance, better modularity by doing all. So this helps us build reusable workflows, right? We might have these tasks being used elsewhere in the organization, so we can share that with others. And it also allows us to optimize those individual components separately, right? And apply these best practices when it comes to engineering. Now we need to look at the outputs from our engineered prompts, look at inputs, and look at, now that we understand the ideas of chaining and how do we go and do this, how do we actually go and design this, right? And what does actually get involved?

---

## Timestamped Segments

**[00:00]** What is a compound AI system?

**[00:03]** So you've probably been talking about models

**[00:06]** over the last few years.

**[00:07]** But when you look at it, real complex systems

**[00:10]** that achieve state of the art results aren't just models.

**[00:14]** They're not just a large language

**[00:16]** model working on its own.

**[00:17]** It's typically a large language model in conjunction

**[00:20]** with other components, things like databases, the ability

**[00:23]** for it to search on the internet, things

**[00:26]** like that, into a system or a chain that allows it

**[00:29]** to achieve its state of the art results.

**[00:32]** So what are some examples of compound AI systems?

**[00:37]** We've actually already talked about a few of them

**[00:39]** in our other courses.

**[00:40]** For example, prompt engineering is

**[00:42]** an example of a really simple compound AI system.

**[00:46]** You're combining an LLM with prompt generation logic,

**[00:50]** whether that is a template, whether that

**[00:52]** is auto-generated via frameworks and libraries.

**[00:56]** But the idea here is through prompt engineering,

**[00:58]** we're able to improve the output of the model

**[01:00]** versus just giving the questions directly to the model.

**[01:03]** We have RAG, where we boost the performance

**[01:06]** of a large language model by adding and combining it

**[01:11]** with an external data store, whether that

**[01:14]** is a vector database or a structured database

**[01:17]** that we connect to with some type of text

**[01:19]** to SQL system or something like that in conjunction

**[01:22]** with it.

**[01:24]** And today, we're going to be talking about a couple more

**[01:26]** different architectures, things like agent-based chains

**[01:30]** and orchestration chains, where instead of us defining

**[01:34]** every step in a workflow or a pipeline

**[01:36]** that we're traditionally used to in a lot of software

**[01:39]** and application, these LLMs are able to do

**[01:42]** a little bit of planning and reasoning.

**[01:44]** So we want to take advantage of that.

**[01:46]** And what we can do is let the LLM figure out

**[01:49]** the plan and observations and execution path

**[01:52]** to go and solve some of our problems.

**[01:54]** So let's go and talk about one system that we already know.

**[01:58]** That one is RAG, which is really

**[02:00]** an example of a simple AI system.

**[02:02]** And if you think about RAG, it's combining two things.

**[02:05]** It's combining prompt engineering,

**[02:06]** the idea of few-shot learning and context-driven learning

**[02:09]** to improve the performance of the model

**[02:12]** and to pull in an external data store

**[02:15]** to provide as that context to that prompt.

**[02:18]** And with that, we can improve the overall system's

**[02:21]** performance, to be able to answer

**[02:22]** questions that are more relevant or more domain-specific.

**[02:26]** So really, if you think about it,

**[02:27]** a compound AI system is defined as a system

**[02:30]** that tackles AI tasks using multiple

**[02:32]** interactioning components, including multiple calls

**[02:35]** to models, retrievers, and external tools,

**[02:38]** or even other models, agent-based communication

**[02:41]** where they're talking with other agents.

**[02:44]** How do we go and break down or think about

**[02:47]** decomposing these AI tasks

**[02:49]** into these systems and components?

**[02:52]** For example, we're going to use an example here,

**[02:54]** which is given the objective of building a system

**[02:57]** to analyze sentiment for Japanese customer reviews,

**[03:00]** you can think about this problem at a high level,

**[03:03]** which is that's what we're trying to do.

**[03:04]** But in order to engineer a system or solution,

**[03:07]** we need to break it down into smaller pieces.

**[03:10]** And typically, one way we can think about that

**[03:12]** is intents and tasks.

**[03:14]** So you think of an intent as a single objective

**[03:17]** that we have, that has multiple intents,

**[03:19]** and an intent is something that consists

**[03:21]** of one to many tasks.

**[03:23]** And those tasks can then align to particular things

**[03:26]** that an LLM or a model or a system can do,

**[03:29]** for example, things like translation or summarization.

**[03:33]** So in this example for Japanese customer reviews,

**[03:36]** some intents that we might have is translation, right?

**[03:38]** In order to go and calculate the sentiment

**[03:40]** of this review, we first need to translate

**[03:43]** the Japanese customer review into English, right?

**[03:46]** That's one intent.

**[03:47]** We can then from there take the translation

**[03:51]** and summarize it, right?

**[03:52]** A lot of these LLMs can't just take unlimited sizes

**[03:56]** of data as input or context.

**[03:58]** So it's very common to compress that

**[04:00]** with some type of summarization intent.

**[04:02]** Then analyzing its sentiment could be a different intent.

**[04:05]** And then once we have the sentiment,

**[04:07]** we can then classify the type of feedback provided

**[04:10]** based on our business logic, right?

**[04:11]** Is that good feedback or is that negative feedback?

**[04:14]** And all of this would then be put together

**[04:16]** into a pipeline to go and complete these.

**[04:19]** So let's dive a little bit deeper on the concept, right?

**[04:22]** If we look at it, we have a system

**[04:24]** that we're trying to build, right?

**[04:26]** That system could be to go

**[04:28]** and do the Japanese customer reviews,

**[04:29]** or in this case, it could be used

**[04:30]** to create personalized responses

**[04:32]** to customer questions or a QA chat bot.

**[04:35]** And then that system would be comprised

**[04:36]** of multiple intents, right?

**[04:38]** So each intent would be one of those objectives

**[04:41]** that we're doing, such as translation,

**[04:43]** summarization, sentiment analysis, classification,

**[04:47]** things like that.

**[04:48]** And then each of those intents

**[04:49]** might require tasks for us to go and do, right?

**[04:52]** We might need to go and retrieve some information

**[04:54]** about the customer before we can create the message

**[04:56]** and things like that.

**[04:58]** So when you're looking at AI systems,

**[05:00]** the power of LLMs is that we can go

**[05:03]** and use them to do a lot of these tasks.

**[05:06]** And a lot of these agents can do multiple tasks,

**[05:08]** but what we've found is they do better

**[05:10]** when we design the LLM to do one task at a time, right?

**[05:14]** The more constrained the task,

**[05:15]** the better the performance typically, right?

**[05:17]** So, for example, we can have them do things

**[05:19]** like summarization, sentiment analysis,

**[05:21]** translation, zero-shot, few-shot learning,

**[05:24]** conversation chat, QA, the list goes on, right?

**[05:26]** Today, we almost have models and tasks

**[05:31]** for almost anything that you want to go and do.

**[05:33]** Especially now, we have things like image generation,

**[05:35]** video generation models, all those kind of cool things.

**[05:38]** So if we really look at it today,

**[05:41]** we're no longer really just building applications

**[05:44]** that just do a single task.

**[05:46]** We're actually building applications that do a pipeline

**[05:49]** or a chain of tasks that are combined together

**[05:53]** in order to complete those

**[05:54]** more complex intents and objectives.

**[05:56]** So in this case, you can see that we,

**[05:58]** instead of a single task, we have multiple tasks, right?

**[06:00]** This could be a task to do summarization,

**[06:02]** and then we might go and then use that summarization

**[06:05]** to go and do sentiment analysis,

**[06:07]** and then we might go and do something else after that,

**[06:09]** compound AI systems.

**[06:11]** Why would we want to do that?

**[06:12]** And what are some reasons of why we want to do that?

**[06:14]** One, I think at the high levels,

**[06:16]** it makes it easier for us to grasp these complex systems

**[06:18]** and break them down into pieces

**[06:20]** that we can manage and develop.

**[06:21]** But the other thing also is when it comes to LLMs,

**[06:24]** if we go and just build a solution, for example, here,

**[06:27]** get the sentiment of many articles on a topic,

**[06:29]** and we just send all the articles

**[06:31]** and ask it to go and generate the sentiment,

**[06:33]** that's going to overload most LLMs, right?

**[06:36]** We have context windows of limited size, right?

**[06:39]** And we can't just throw everything at it, right?

**[06:41]** It's going to lead to an issue

**[06:43]** where it runs out of context length, right?

**[06:46]** So that can be a problem.

**[06:47]** So another reason why we do this is by breaking it down,

**[06:50]** we can also get better performance,

**[06:51]** we can also get better latency out of it, right?

**[06:54]** So in this case, we can break it down into two stages,

**[06:56]** one in which we summarize the articles first, right?

**[07:00]** Basically reducing the amount of data

**[07:02]** that we send into the context,

**[07:03]** and then by sending only the summaries,

**[07:05]** the sentiment LLM can then process all those articles.

**[07:08]** That's an example of how we can get better performance,

**[07:10]** better modularity by doing all.

**[07:13]** So this helps us build reusable workflows, right?

**[07:16]** We might have these tasks being used elsewhere

**[07:18]** in the organization, so we can share that with others.

**[07:21]** And it also allows us to optimize

**[07:23]** those individual components separately, right?

**[07:25]** And apply these best practices

**[07:27]** when it comes to engineering.

**[07:29]** Now we need to look at the outputs

**[07:31]** from our engineered prompts, look at inputs,

**[07:33]** and look at, now that we understand the ideas of chaining

**[07:35]** and how do we go and do this,

**[07:37]** how do we actually go and design this, right?

**[07:38]** And what does actually get involved?

