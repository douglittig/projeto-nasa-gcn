# 06 - Introduction to Multi - stage Reasoning Chains

**Source:** `06-Introduction to Multi-stage Reasoning Chains.mp4`
**Duration:** 13:20
**Language:** en (detected with 100.0% confidence)

---

## Full Transcription

So introduction to multi-stage reasoning chains, right, when you think about traditional software and you think about software that we build today, we're really moving into a different era and paradigm of how we go and develop and build our applications, right? If you think about it, a lot of the things that we've built up to this point are really retrieval systems, right? Everything we built, all the software, the stacks, is how do we scale and build global systems for information retrieval, whether that's retrieving information about my shopping history or my orders or retrieving information about some historical figure or something for research that I'm trying to do. But a lot of it for the most part are really powerful systems that we built to search and find information, right? And with generative AI, the reason we call it generative is we're moving into an order of magnitude where now these systems not only can retrieve information, but they can look at that information that they retrieved and reason on that and synthesize that information into something new or something different, right, or generation, right? We're really moving into a new paradigm where now we're building systems that generate information, and with that comes new challenges. So here we have a graphic of some things. If you think about we used to have retrieval, now we have tools, we used to have tasks, now the systems are trying to figure out how to combine these tools together to do more complex tasks, where we used to have questions and answers, now we have intents and routes. We have these, the systems now trying to figure out how to solve some problems that hasn't seen before, whereas before we had very defined problems, things like that. So when it comes to building SDKs and frameworks to actually implement these multi-stage reasoning systems, it's a big challenge right now, right? There's a lot of different frameworks that are trying to tackle this at different, in different levels, right? So when we look at it, there's a lot of compositional frameworks out there. Now one that we're going to be focusing on in this course, and one of the early ones that came to the field that became really popular when it came to generative AI is lane chain, right? So that's what we're going to be talking about. And we also talk about it because Databricks has contributed and added a lot of integrations to the lane chain framework, but we expect that there's going to be more and more frameworks as we go on and on, right? Which kind of leads to, there's a lot more frameworks out there, right? Building AI systems require new tools because of this new paradigm, right? These compositional frameworks are becoming more popular, and in conjunction with lane chain, other popular ones are things like Llama Index, Paystack, and DSPY, or DSPY, some people will call it that way. And then there's also things like agent libraries, like lane chain agents, AutoGBT, right? AutoGen, and a whole bunch of others as well. I expect this to explode over the next few years. So just a quick overview of some of them. Lane chain, right, was the first to the field. It came out at the same time around when a major LLM was released to the world. It is a software framework to help us build generative AI applications. It was developed from the ground up to really support the LLM kind of development where we're really taking prompts and text as input and dealing with text and prompts as output. And this enables our applications to be context aware, to reason and interact dynamically with various sources and environments. They brought in the concepts of kind of this prompt engineering and templating. They brought in ideas of controlling the flow of those prompts and templates right into these pipelines and workflows, right? As well as the idea of tools integrating your large language models with external systems, right? So there are a lot of things that kind of were inspired by lane chain and brought to the world to elevate language models to more than just text prediction tools, right? Now, when we look at building these compound AI systems and using lane chain in the world, lane chain, we have things like prompts, which are those specific tasks or queries of a language model that we're trying to build. Like how do we actually go and guide the model? So what's that prompt look like? We've already, we talked about it in another course, but that's very important in getting good performance. Then there's the chain. So how do we connect these things together to complete some tasks? So typically we have a whole bunch of different prompts that we combine together or tools. We have retrievers, which is very popular now with RAG, connecting our language model to external data source, whether that's the internet or that's a vector database or whatever other information store that we have. And then we have tools, functionality or resource that an agent can activate such as APIs, database, function calls, things like that, right? So really these are some of the ideas that lane chain brought to the world. And a lot of other frameworks are also trying to solve it, but opinionated on actually how do we write the APIs and things like that, right? I like to think of the front end software development world. There's so many frameworks out there of how to do the same thing, but everyone has different opinions on the conventions and the best way to go and do that. So with that, there's other ones as well. So there's Lama index, right? So whereas lane chain is really built with kind of more of the idea of orchestration and managing complex tasks and decoupling them and integrating them with other components, Lama index is more about that information retrieval and RAG system, right? So it's really about how do we structure and index data to make it easy for our LLMs to consume and look for, right? So it has components like models, prompts, indexing, querying and agents as well, but it's really powerful capabilities, really popular when it comes to indexing, storing and querying and building a great retrieval component to integrate with our large language models, right? Therefore, Lama index, the way I remember it's index database index, way for me to remember it. Another one that is worth mentioning is Haystack, right? Haystack's actually been around for quite longer than the other two, right? It's open source Python framework for building custom applications, right? And it also has tons of integrations and things like that as well. But being out there for a little bit longer, the API is a little bit more stable and things like that, but it might not support things like agents and things like that. So it's really great for things like workflows and things like that, right? Whereas Langchain is moving towards those agents and things like that, right? Where we're giving that orchestration away. So different frameworks for different things that are there. Now, another one worth mentioning is when it comes to prompt engineering, a lot of people think it's like these templates that you write to get this output, right? DSPY throws that out the window and looks at the idea of instead of us manually writing the prompts, could we go and build a framework or a system where the library or the framework figures out what the best prompt is for you? So the idea DSPY is you write signature. What's the input output kind of signature that you want for your system? And then DSPY will use teleprompters to optimize or compile those prompts, right? And then generate that for you to go and build the system, right? So there's a little bit of higher learning curve with it, but it's really popular for people that are trying to move beyond just prompts, right? So it's another popular framework worth looking into, right? And we have a lot of engineers at Databricks that do like DSPY. But when it comes to choosing libraries, things to think like features, right? Or do you want stability? Do you want control, right? Do you want integrations, right? All these libraries have different trade-offs with each of them. So looking into them and figuring out which one you like, right? Performance and scalability. Performance is a tricky thing with a lot of these frameworks because a lot of them do abstract away the LLM. So when it comes to knowing how many tokens each of these calls are going to take, the latency and the performance it could be difficult, right? To optimize the tokens that are being used there. So when it comes to performance and scalability, that might be one thing to consider when choosing one framework worth as another, especially DSPY where it's generating those prompts dynamically, right? Then that's hard for us to go and control that. But the idea is hopefully that gives us better performance, right? And then you have stability and complexity, right? Remember we're only a couple years into the generative AI development movement, right? And expect that there's going to be new frameworks. These APIs are going to change. So do understand that a lot of this is experimental and a lot of it is going to be changing very quickly, right? Okay. So with that, we talked about frameworks. We talked about ways that we can implement it. Let's talk about what Databricks offers to help you out with it. Now, when it comes to Databricks, right? On a platform, you're able to use whatever framework you want. That's why we talked about all those frameworks just now. Now, when it comes to those framework connecting and building those individual tasks and components, we provide different things for that. So the first is you typically need an LLM if you're building generative AI. And one of those things inside of Databricks is the foundational models API. And what that is, it is a managed service for popular language models that are out there, right? So instead of you having to go and figure out how to go and deploy a lot of popular open source state of the art models, think things like Llama 3, Mextral, DBRX, all of these kinds of models, right? The foundational model API and Databricks, we went out there and deployed them all are ready for you. It can be provided as a paper token service that you can use, that you can get started very quickly. And we also support provision throughput for once you get into production and your workload size, you can optimize it later, right? The foundational model API also supports proxies to external models as well. So you actually use it to connect to other models like AWS Fedrock models, or Azure OpenAI, GPT models, right? And it's useful because then it provides us this unified interface for deploying, governing, and controlling AI models. So not only does it make it easy for us to go and get started, but also allows us to get from that point and go into production, right? And provide a unified interface so that if we need to swap out models, we can easily do that as well, right? So that's one thing that we have. Now, we also have a model as well. That model is called DBRX. It's a new open LLM by Databricks, right? That we developed earlier this year, and it's our very own open source LLM. Now, DBRX is available in two different flavors. We have DBRX base, which is a pre-trained model. Now, if you're not familiar, base models are just that autocomplete model. So it generates the next token, but it isn't trained to do anything like particular tasks or something. So it's not going to be able to do, give me instructions for a recipe to make a cake, right? It's not going to go and do things like that. That's typically a fine-tuned model. And we also provide that as well. That would be DBRX instruct, which is our fine-tuned model that's been trained to do various different tasks, right? And it's built on DBRX, and we designed it specifically to be good for enterprise tasks. So when it comes to enterprise tasks, what are some of the things that we designed and optimized DBRX for? So in enterprise, we found that there's three really main things that our customers are concerned about. The first is language understanding. So being able to do RAG, right? When you think about RAG, what is it? It's look at this context, understand that context, align it to its own understanding of language, and then give me an answer, right? So when we look at language understanding, that's one thing that we designed and optimized DBRX for. So you can see here at the time when DBRX came out, it did really well in MMLU against other open source models at the time, right? The other one is programming. Very common. A lot of our customers are using models to drive internal assistance for coding and for software development, or if you're doing things like text to SQL, this is also a very important metric, right? So DBRX is also really good at programming, and you can see here it does really well comparatively to other open source models as well. And then finally, we have reasoning. If we're going to be using it for orchestration or for agent-based workflows, the model needs to be able to reason on the task and be able to look at observations and then reason on those observations to figure out what to do next. So that was also another thing that we optimized for. So if you think about it, the ability to understand language, the ability to write software, and the ability to reason are the three things that we optimized DBRX for on, because we thought that was very important for a lot of customers. So DBRX. Now finally, with that we also have is, RAG is so popular out there, right? It's very common to go and build an external data store with a vector database. DBRX has that as well, and that is vector search, right? So vector search is our own implementation of a vector database, and it's built on top of the DBRX intelligence platform, meaning that it's integrated with the platform and it makes it really easy for you to go and implement a vector search index on your data inside a Unity catalog, whether that is a Delta table or a Unity catalog volume, right? So it stores vector representations of your data plus metadata. It integrates tightly with Lake House. It's fully managed, so you don't have to worry about scaling it. So it's built for production, and you don't have to really worry about scaling and infrastructure for it. It is integrated with Unity catalog, so it supports ACLs, and we provide it, once you set it up, you can access it via an API, whether that is a REST API or our SDK that you can use, and we'll show an example of that in the demos later. Now other things to think about, DBRX is a major contributor of the MLflow project, so with that we have a lot of integrations of MLflow inside the DBRX platform. So other things that we'll talk about in other courses are things like MLflow tracking, which is great for logging our chains and pipelines during development, model serving for building custom models and deploying our applications, MLflow evaluation, very useful when it comes to getting that iterative development cycle and feedback loop started, and then things like Lake House monitoring to go and monitor our applications in production.

---

## Timestamped Segments

**[00:00]** So introduction to multi-stage reasoning chains, right, when you think about traditional software

**[00:05]** and you think about software that we build today, we're really moving into a different era and

**[00:11]** paradigm of how we go and develop and build our applications, right? If you think about it,

**[00:17]** a lot of the things that we've built up to this point are really retrieval systems,

**[00:21]** right? Everything we built, all the software, the stacks, is how do we scale and build global

**[00:26]** systems for information retrieval, whether that's retrieving information about my shopping history

**[00:32]** or my orders or retrieving information about some historical figure or something for research

**[00:37]** that I'm trying to do. But a lot of it for the most part are really powerful systems that we

**[00:43]** built to search and find information, right? And with generative AI, the reason we call it

**[00:47]** generative is we're moving into an order of magnitude where now these systems not only

**[00:51]** can retrieve information, but they can look at that information that they retrieved and reason

**[00:56]** on that and synthesize that information into something new or something different,

**[01:00]** right, or generation, right? We're really moving into a new paradigm where now we're

**[01:04]** building systems that generate information, and with that comes new challenges. So here we have

**[01:09]** a graphic of some things. If you think about we used to have retrieval, now we have tools,

**[01:13]** we used to have tasks, now the systems are trying to figure out how to combine these

**[01:17]** tools together to do more complex tasks, where we used to have questions and answers,

**[01:20]** now we have intents and routes. We have these, the systems now trying to figure out how to

**[01:26]** solve some problems that hasn't seen before, whereas before we had very defined problems,

**[01:30]** things like that. So when it comes to building SDKs and frameworks to actually implement these

**[01:36]** multi-stage reasoning systems, it's a big challenge right now, right? There's a lot

**[01:40]** of different frameworks that are trying to tackle this at different, in different levels,

**[01:43]** right? So when we look at it, there's a lot of compositional frameworks out there.

**[01:46]** Now one that we're going to be focusing on in this course, and one of the early ones that

**[01:50]** came to the field that became really popular when it came to generative AI is lane chain,

**[01:54]** right? So that's what we're going to be talking about. And we also talk about it because

**[01:58]** Databricks has contributed and added a lot of integrations to the lane chain framework,

**[02:03]** but we expect that there's going to be more and more frameworks as we go on and on,

**[02:06]** right? Which kind of leads to, there's a lot more frameworks out there, right? Building

**[02:10]** AI systems require new tools because of this new paradigm, right? These compositional

**[02:15]** frameworks are becoming more popular, and in conjunction with lane chain, other popular

**[02:19]** ones are things like Llama Index, Paystack, and DSPY, or DSPY, some people will call it that

**[02:25]** way. And then there's also things like agent libraries, like lane chain agents, AutoGBT,

**[02:30]** right? AutoGen, and a whole bunch of others as well. I expect this to explode over the

**[02:34]** next few years. So just a quick overview of some of them. Lane chain, right, was the

**[02:39]** first to the field. It came out at the same time around when a major LLM was released to

**[02:44]** the world. It is a software framework to help us build generative AI applications. It was

**[02:48]** developed from the ground up to really support the LLM kind of development where we're really

**[02:55]** taking prompts and text as input and dealing with text and prompts as output.

**[03:00]** And this enables our applications to be context aware, to reason and interact

**[03:04]** dynamically with various sources and environments. They brought in the concepts of

**[03:08]** kind of this prompt engineering and templating. They brought in ideas of controlling the flow

**[03:13]** of those prompts and templates right into these pipelines and workflows, right? As well as the

**[03:19]** idea of tools integrating your large language models with external systems, right? So there

**[03:24]** are a lot of things that kind of were inspired by lane chain and brought to the world to

**[03:29]** elevate language models to more than just text prediction tools, right?

**[03:35]** Now, when we look at building these compound AI systems and using lane chain in the world,

**[03:42]** lane chain, we have things like prompts, which are those specific tasks or queries

**[03:47]** of a language model that we're trying to build. Like how do we actually go and guide

**[03:50]** the model? So what's that prompt look like? We've already, we talked about it in another

**[03:53]** course, but that's very important in getting good performance. Then there's the chain.

**[03:57]** So how do we connect these things together to complete some tasks? So typically we have

**[04:03]** a whole bunch of different prompts that we combine together or tools. We have retrievers,

**[04:07]** which is very popular now with RAG, connecting our language model to external data source,

**[04:12]** whether that's the internet or that's a vector database or whatever other information

**[04:17]** store that we have. And then we have tools, functionality or resource that an agent can

**[04:21]** activate such as APIs, database, function calls, things like that, right? So really

**[04:26]** these are some of the ideas that lane chain brought to the world. And a lot of other

**[04:30]** frameworks are also trying to solve it, but opinionated on actually how do we write the

**[04:34]** APIs and things like that, right? I like to think of the front end software development

**[04:38]** world. There's so many frameworks out there of how to do the same thing,

**[04:41]** but everyone has different opinions on the conventions and the best way to go and do that.

**[04:46]** So with that, there's other ones as well. So there's Lama index, right? So whereas

**[04:50]** lane chain is really built with kind of more of the idea of orchestration and managing

**[04:54]** complex tasks and decoupling them and integrating them with other components,

**[04:58]** Lama index is more about that information retrieval and RAG system, right? So it's

**[05:02]** really about how do we structure and index data to make it easy for our LLMs to consume

**[05:08]** and look for, right? So it has components like models, prompts, indexing,

**[05:12]** querying and agents as well, but it's really powerful capabilities, really popular when it

**[05:17]** comes to indexing, storing and querying and building a great retrieval component

**[05:21]** to integrate with our large language models, right? Therefore, Lama index,

**[05:25]** the way I remember it's index database index, way for me to remember it.

**[05:30]** Another one that is worth mentioning is Haystack, right? Haystack's actually been around for

**[05:34]** quite longer than the other two, right? It's open source Python framework for building custom

**[05:38]** applications, right? And it also has tons of integrations and things like that as well.

**[05:44]** But being out there for a little bit longer, the API is a little bit more stable

**[05:48]** and things like that, but it might not support things like agents and things like that. So it's

**[05:52]** really great for things like workflows and things like that, right? Whereas Langchain

**[05:56]** is moving towards those agents and things like that, right? Where we're giving that

**[06:00]** orchestration away. So different frameworks for different things that are there. Now,

**[06:03]** another one worth mentioning is when it comes to prompt engineering, a lot of people think

**[06:07]** it's like these templates that you write to get this output, right? DSPY throws that out

**[06:11]** the window and looks at the idea of instead of us manually writing the prompts, could we

**[06:16]** go and build a framework or a system where the library or the framework figures out what the

**[06:22]** best prompt is for you? So the idea DSPY is you write signature. What's the input output

**[06:28]** kind of signature that you want for your system? And then DSPY will use teleprompters

**[06:35]** to optimize or compile those prompts, right? And then generate that for you to go and build

**[06:41]** the system, right? So there's a little bit of higher learning curve with it, but it's

**[06:45]** really popular for people that are trying to move beyond just prompts, right? So it's another

**[06:50]** popular framework worth looking into, right? And we have a lot of engineers at Databricks that

**[06:55]** do like DSPY. But when it comes to choosing libraries, things to think like features, right?

**[07:00]** Or do you want stability? Do you want control, right? Do you want integrations, right? All these

**[07:05]** libraries have different trade-offs with each of them. So looking into them and figuring out

**[07:09]** which one you like, right? Performance and scalability. Performance is a tricky thing with

**[07:14]** a lot of these frameworks because a lot of them do abstract away the LLM. So when it comes to

**[07:20]** knowing how many tokens each of these calls are going to take, the latency and the performance

**[07:24]** it could be difficult, right? To optimize the tokens that are being used there. So when it

**[07:28]** comes to performance and scalability, that might be one thing to consider when choosing

**[07:32]** one framework worth as another, especially DSPY where it's generating those prompts

**[07:36]** dynamically, right? Then that's hard for us to go and control that. But the idea is

**[07:40]** hopefully that gives us better performance, right? And then you have stability and complexity,

**[07:44]** right? Remember we're only a couple years into the generative AI development movement, right?

**[07:50]** And expect that there's going to be new frameworks. These APIs are going to change.

**[07:55]** So do understand that a lot of this is experimental and a lot of it is going to

**[08:00]** be changing very quickly, right? Okay. So with that, we talked about frameworks. We

**[08:04]** talked about ways that we can implement it. Let's talk about what Databricks offers to

**[08:08]** help you out with it. Now, when it comes to Databricks, right? On a platform,

**[08:13]** you're able to use whatever framework you want. That's why we talked about all those

**[08:16]** frameworks just now. Now, when it comes to those framework connecting and building those

**[08:20]** individual tasks and components, we provide different things for that. So the first is

**[08:25]** you typically need an LLM if you're building generative AI. And one of those things inside

**[08:29]** of Databricks is the foundational models API. And what that is, it is a managed service

**[08:34]** for popular language models that are out there, right? So instead of you having to go and figure

**[08:39]** out how to go and deploy a lot of popular open source state of the art models, think things

**[08:44]** like Llama 3, Mextral, DBRX, all of these kinds of models, right? The foundational model

**[08:50]** API and Databricks, we went out there and deployed them all are ready for you.

**[08:53]** It can be provided as a paper token service that you can use, that you can get started

**[08:58]** very quickly. And we also support provision throughput for once you get into production

**[09:02]** and your workload size, you can optimize it later, right? The foundational model API also

**[09:06]** supports proxies to external models as well. So you actually use it to connect to other models

**[09:11]** like AWS Fedrock models, or Azure OpenAI, GPT models, right? And it's useful because then

**[09:16]** it provides us this unified interface for deploying, governing, and controlling AI models.

**[09:21]** So not only does it make it easy for us to go and get started, but also allows us to get

**[09:25]** from that point and go into production, right? And provide a unified interface so that if we

**[09:29]** need to swap out models, we can easily do that as well, right? So that's one thing that we have.

**[09:34]** Now, we also have a model as well. That model is called DBRX. It's a new open LLM by Databricks,

**[09:39]** right? That we developed earlier this year, and it's our very own open source LLM. Now,

**[09:46]** DBRX is available in two different flavors. We have DBRX base, which is a pre-trained

**[09:51]** model. Now, if you're not familiar, base models are just that autocomplete model. So

**[09:56]** it generates the next token, but it isn't trained to do anything like particular tasks or something.

**[10:02]** So it's not going to be able to do, give me instructions for a recipe to make a cake,

**[10:06]** right? It's not going to go and do things like that. That's typically a fine-tuned model.

**[10:10]** And we also provide that as well. That would be DBRX instruct, which is our fine-tuned model

**[10:15]** that's been trained to do various different tasks, right? And it's built on DBRX,

**[10:19]** and we designed it specifically to be good for enterprise tasks. So when it comes to enterprise

**[10:25]** tasks, what are some of the things that we designed and optimized DBRX for? So in enterprise,

**[10:29]** we found that there's three really main things that our customers are concerned about. The

**[10:33]** first is language understanding. So being able to do RAG, right? When you think about RAG,

**[10:38]** what is it? It's look at this context, understand that context, align it to its own

**[10:42]** understanding of language, and then give me an answer, right? So when we look at language

**[10:46]** understanding, that's one thing that we designed and optimized DBRX for. So you can

**[10:51]** see here at the time when DBRX came out, it did really well in MMLU against other open source

**[10:56]** models at the time, right? The other one is programming. Very common. A lot of our customers

**[11:00]** are using models to drive internal assistance for coding and for software development,

**[11:06]** or if you're doing things like text to SQL, this is also a very important metric, right? So

**[11:10]** DBRX is also really good at programming, and you can see here it does really well

**[11:14]** comparatively to other open source models as well. And then finally, we have reasoning. If

**[11:20]** we're going to be using it for orchestration or for agent-based workflows, the model needs to be

**[11:24]** able to reason on the task and be able to look at observations and then reason on those

**[11:28]** observations to figure out what to do next. So that was also another thing that we optimized

**[11:32]** for. So if you think about it, the ability to understand language, the ability to write

**[11:36]** software, and the ability to reason are the three things that we optimized DBRX for on,

**[11:41]** because we thought that was very important for a lot of customers. So DBRX. Now finally,

**[11:46]** with that we also have is, RAG is so popular out there, right? It's very common to go and build

**[11:51]** an external data store with a vector database. DBRX has that as well, and that is vector search,

**[11:57]** right? So vector search is our own implementation of a vector database,

**[12:00]** and it's built on top of the DBRX intelligence platform, meaning that it's integrated with

**[12:05]** the platform and it makes it really easy for you to go and implement a vector search index

**[12:11]** on your data inside a Unity catalog, whether that is a Delta table or a Unity catalog volume,

**[12:18]** right? So it stores vector representations of your data plus metadata. It integrates tightly

**[12:22]** with Lake House. It's fully managed, so you don't have to worry about scaling it. So it's

**[12:27]** built for production, and you don't have to really worry about scaling and infrastructure

**[12:31]** for it. It is integrated with Unity catalog, so it supports ACLs, and we provide it,

**[12:36]** once you set it up, you can access it via an API, whether that is a REST API or our SDK

**[12:42]** that you can use, and we'll show an example of that in the demos later.

**[12:46]** Now other things to think about, DBRX is a major contributor of the MLflow project,

**[12:50]** so with that we have a lot of integrations of MLflow inside the DBRX platform. So other

**[12:55]** things that we'll talk about in other courses are things like MLflow tracking,

**[12:58]** which is great for logging our chains and pipelines during development, model serving

**[13:03]** for building custom models and deploying our applications, MLflow evaluation,

**[13:07]** very useful when it comes to getting that iterative development cycle and feedback loop

**[13:12]** started, and then things like Lake House monitoring to go and monitor our applications

**[13:16]** in production.

