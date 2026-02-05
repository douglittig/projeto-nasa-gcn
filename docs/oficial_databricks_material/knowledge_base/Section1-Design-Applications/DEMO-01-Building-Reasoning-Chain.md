# 07 - Demo Building Multi - stage Reasoning Chain in Databricks

**Source:** `07-Demo_ Building Multi-stage Reasoning Chain in Databricks.mp4`
**Duration:** 12:36
**Language:** en (detected with 100.0% confidence)

---

## Full Transcription

Let's go and jump in and talk about and build some of this, right? So let's actually go and build a multi-stage reasoning chain in Databricks. So in the demo, we're going to cover some components, right? So we're going to look at prompts, LLMs, retrievers, tools and chaining, right? And then we're going to take all those ideas and start building a multi-stage chain. We're going to go and create a vector store, build our chain, build our second chain, and then we're going to talk about connecting those chains together, right? And you remember, we can think of chains as intense and then connecting those together into a system, right? In our case, we're going to be building this kind of rag-like system. So we just talked about multi-stage AI systems and talked about building multi-stage applications. So in this demo, we're going to talk about building a multi-stage AI system, so going away from kind of high-level architecture and actually getting into it and writing some code. So in this stage, we're going to start building a multi-stage reasoning system using Databricks features. In this case, we're going to be using Langchain as our framework of choice, but there are also other frameworks out there that I want everyone to know about. There's things like Llama Index, AutoGBT, AutoGen, and tons of other projects out there that are going to continue to come onto the field as this whole industry keeps growing. But we're going to stick to Langchain here because it's been around there for a while and Databricks has already built a lot of support into Langchain with integrations with Databricks inside of the framework. So that's what we're going to use in our demonstration. So in the main section of this demo, we're going to be building a multi-stage system. We're going to be building each of those components. We're going to build the prompt, the LMs, the retriever, the tools, and then we're going to chain them together. And then we're going to build a multi-stage chain to connect it together. And in this case, our example is going to be going and looking at YouTube videos and then combine that together. So by the end of this demo, you should be able to identify a Langchain, can use stages and tasks that are not just LLMs. So the idea of these systems that go and talk to other components that are not just language models. We're going to be talking about basic LLM chains to connect with prompts and we'll be talking about tools to go and complete other tasks and look at how we combine them together. In this case, we're just going to do a simple sequential chain, right? Let's go ahead and get started. The first thing is getting our requirements installed. So I've already ran this earlier today, but installing our libraries and then configuring the configurations for our lab environment. So making sure you always run these before you run the demos in the labs because this is needed to download all the packages as well as any additional data sets and configuration settings for your environment. So that's out of the way. Let's go ahead and jump in. So this is the configuration settings it sets up. So it actually creates a catalog and some schemas for us that it uses in the lab environment. And we'll come back to that in a bit. So let's jump into our component. So we're building a couple of components. We're going to build a prompt component, a LLM component, a retriever, tool integration, and then we're going to create a chain to go and connect them together. The first one's pretty straightforward. It's a prompt. It's a basic building block when we're looking at generative AI applications and it's pretty straightforward. It's the prompt or the input to our large language model and what that should look like. And very common when it comes to prompts is prompt engineering and with prompt engineering, prompt templates or the structure of that prompt. So here we have an example of a prompt template. So tell me about a genre, movie, which actor is one of the actors. And we have a placeholder for the genre and the actor. And then we can instantiate this prompt with a specific genre and actor when we go and use the object here. So you can see here with romance and Brad Pritt. So here, tell me a romance movie, which Brad Pritt is one of the actors. So really common practice is building a convention around how we go and capture these prompts that work really well that we can share with our organization. In this case, Lang chain provides things like the prompt template then that we can reuse and share as well as use as a piece to go and prepare our data or our input to go and pass through an LLM. That's our prompt. Now, the next piece is the LLM itself. So you can think of the LLM as the computer project or the business logic that actually processes the prompt. And there's different options. There's tons of different models out there. I think everyone last year has been talking about all the different models that are out there from llama to open AIs models to Databricks as DBR X model and MPT and llama three models that we have in our foundational models API. So in this case, we're going to actually go and connect to one of the models that Databricks has and that model is going to be DBR X instruct. So here we're going to bring in the chat models component in Lang chain and we're going to bring in the chat Databricks. So this actually allows Lang chain to talk to the Databricks endpoint. That's what we're doing here. And we're configuring the chat Databricks to go and connect to Databricks instruct. And then now what we can do is we can go and send that data over there and get an output. So here's just an example of us sending who is Brad Pitt to it. And then you can see here kind of the tokens that it generated out. Is that Brad Pitt is an American actor and film producer. So you can see the output there. So we have our LLM configured. So we have our prompt, our LLM. The next one we're going to do is a retriever. In this case, instead of using a private retriever like we did in the last demo with Databricks Vector Search, in this case, we're going to use a community given retriever. And a common thing to retrieve against is online resources. In this case, Wikipedia. We're going to load in the Wikipedia retriever. And you can see here it's very easy to go and load because Lang chain the community has already contributed and built a retriever for Wikipedia. We can go and do that. And then we can use that to go and do a search for Brad Pitt. We have that. And then we're just returning one of the documents. And you can see here we have the article for Brad Pitt on Wikipedia here. So pretty predictable and what we were expecting there. So we have a retriever. All right. So finally, what's next? Next, we're going to have a tool. So tools are interesting. So whereas retrievers are really built to go and pull information from databases and search systems that could collect a lot of data, tools can be used to invoke other functions such as running code, writing math expressions, sending out emails, things like that. Now, in this case, the tool that we're going to use is tool that was built by the community to do a search on YouTube. So that's what we're doing here. We're going to go and search YouTube. So YouTube search tool. And then in this case, Brad Pitt movie trailer. And you can see here it returns this link for YouTube videos that are related to it. So we can get some details on that here as well. So search for video person, comma separate. So this is if you want to know what the tool does, we can get descriptions of the tool here. So the description and then arguments. And this is something when it comes to lane chain that they developed, which is one of the ideas is how do we integrate LLMs with tools? And one of the things is one is actually connecting the tool to the service, writing the code to make it happen. But the other also is defining that interface. What does it look like to work with a tool? What can the tool do so that the LLM can then know how to use the tool? In this case, this tells us what the tool does. The LLM can understand that. And then the structure for the queries. So that's there, the description and the argument. So we have our components. Now we can go and chain them together. So this is an example of using lane chain to do a chain. In this case, the chain that we're doing is prompt to the model and then pulling the output. So just a sequential chain. So remember, if we looked at our prompt template, again, earlier the prompt template was find me movies, romance movies with Brad Pitt in them. And then LLM can process that. So this is an example of that. So Brad Pitt has been in a few romance films, but most noticeably is the curious case of Benjamin Button. You can see here an example of that. But there's no retrieval in this case. We're really just having two pieces, which is the prompt and the LLM. So let's go and build a more complex chain. So let's go and do more other chains where we're gonna go and connect to things like vector stores or something like that. So let's jump over to multi-stage. In this case, we're gonna do something that's a little bit more complicated. Instead of using built-in tools and things like that, in this case, we're gonna show an example of RAG, but in which we're actually gonna connect to a vector search database endpoint. So that's what we're gonna do here. We're gonna go define our vector search endpoint. So this code here is just selecting a pre-built endpoint if it's already built in your environment or falling back to a backup. So in this case, it's found that we have vector search endpoint number three, what it's gonna use. Now that we have that endpoint, the next thing we're gonna do is we're gonna go and load data into that endpoint. So here is some code identifying our tables, DAS text, DAS embedding. We have a whole bunch of text data that's already been loaded up into, that we're gonna load into this table. And then we're gonna use that table to create an index on top of, that's gonna be used by the vector search database. You can see here's some code to load the data. And then we're gonna go and override it if it exists already. And then once we have that table created, we're gonna create an index on the DAS text data. And then that's gonna make it all good to go. So I ran this earlier, so it's all good to go, but it'll create these two tables. So we jump over here, we have the text table that you can see here, this is all the DAS talks that happened last year and the titles and the abstract of those that we have. So here's a sample set of that. And then what we did was we created index on top of this inside of vector search. So you can see here, our vector search endpoint, you can see our index. And if you look at this index actually points to this table here, and you can see this table is very similar to our text table, except instead of just title and abstract, we also now have these embeddings that the vector search database is using or Daybrick's vector search is using to do that similarity search. And we have that there. Our table is ready to go. Now we can use that to go and do a query. Now to set up the query, we're gonna go and create parts of our chain again. We're gonna create, we're gonna load up our model, our tool, so this is our YouTube search tool, our model. And then we're gonna go set up our prompt template. So this one's a little bit different. Instead of the model asking about a movie, we're gonna be asking about Databricks. So you are a Databricks expert. You have question about Databricks, try to give simple answers and be professional. And then we pass through the question and then get some answers. So we define this chain as pass through the question, pass through the question here, and then our prompt template, then the model, then we get our output. So here's an example of how machine learning models are stored in Unity catalog. And then here you can see the answer. Machine learning models in Databricks can be stored in Unity catalog as MLflow model artifacts. So we have that, our first chain that we built. So this is chain number one. And this chain is a combination of the question, the prompt template, the model, then the output. So we're combining that into this component. And then the second chain here is we're gonna use that information and we're gonna augment that with another chain in which this chain, what we're gonna do is we're gonna use our vector search index and we're gonna use that to grab titles of talks that were done at DAS and then find the YouTube video related to it. So that's what we're gonna do here. So here's our vector search client, our index that we defined earlier. The query we're gonna ask is how do I use Databricks SQL? And then we're gonna load in our Databricks vector search client. Here's our similarity search that's going on and then our video search tool here and then our prompt. So you will get a list of videos related to the user questions that are recorded at DAS, encourage the user to watch the videos, list the videos with YouTube links and then we have that through here. So here you can see we have this go through the prompt, videos, so here we're pulling in the videos from our YouTube videos and then we pass through the model and then the model gives us the output. So you can see that. I don't think we run it here. We don't see the output. We don't run it here and then we're gonna put that together to go and do a multi-chain where we actually have two chains running together. So the first chain about the question and then the second chain doing that video lookup. So here that's what we have and you can see here machine learning models are part of the Lakehouse platform and then you can also see here some code and then you can also see some related videos that we have that's received from the second chain. So you can see here how we can build up from a very simple application, build up the simple components, combine those components into complex systems or chains then we can even combine chains together into multi-stage chains or AI systems. That's what we have here. Showing you that really quick of what it looks like and building on and using lane chain as an example of one of the frameworks and how those frameworks can make things a little bit easier.

---

## Timestamped Segments

**[00:00]** Let's go and jump in and talk about and build some of this, right?

**[00:03]** So let's actually go and build a multi-stage reasoning chain in Databricks.

**[00:06]** So in the demo, we're going to cover some components, right?

**[00:10]** So we're going to look at prompts, LLMs, retrievers, tools and chaining, right?

**[00:14]** And then we're going to take all those ideas and start building a multi-stage chain.

**[00:17]** We're going to go and create a vector store, build our chain, build our second chain,

**[00:22]** and then we're going to talk about connecting those chains together, right?

**[00:24]** And you remember, we can think of chains as intense

**[00:26]** and then connecting those together into a system, right?

**[00:28]** In our case, we're going to be building this kind of rag-like system.

**[00:32]** So we just talked about multi-stage AI systems

**[00:37]** and talked about building multi-stage applications.

**[00:40]** So in this demo, we're going to talk about building a multi-stage AI system,

**[00:44]** so going away from kind of high-level architecture

**[00:47]** and actually getting into it and writing some code.

**[00:50]** So in this stage, we're going to start building a multi-stage reasoning system

**[00:53]** using Databricks features.

**[00:56]** In this case, we're going to be using Langchain as our framework of choice,

**[00:59]** but there are also other frameworks out there that I want everyone to know about.

**[01:03]** There's things like Llama Index, AutoGBT, AutoGen,

**[01:07]** and tons of other projects out there

**[01:09]** that are going to continue to come onto the field

**[01:12]** as this whole industry keeps growing.

**[01:14]** But we're going to stick to Langchain here

**[01:16]** because it's been around there for a while

**[01:18]** and Databricks has already built a lot of support into Langchain

**[01:22]** with integrations with Databricks inside of the framework.

**[01:24]** So that's what we're going to use in our demonstration.

**[01:27]** So in the main section of this demo,

**[01:29]** we're going to be building a multi-stage system.

**[01:32]** We're going to be building each of those components.

**[01:34]** We're going to build the prompt, the LMs, the retriever, the tools,

**[01:37]** and then we're going to chain them together.

**[01:39]** And then we're going to build a multi-stage chain to connect it together.

**[01:42]** And in this case, our example is going to be going and looking at YouTube videos

**[01:46]** and then combine that together.

**[01:47]** So by the end of this demo, you should be able to identify a Langchain,

**[01:51]** can use stages and tasks that are not just LLMs.

**[01:54]** So the idea of these systems that go and talk to other components

**[01:58]** that are not just language models.

**[01:59]** We're going to be talking about basic LLM chains to connect with prompts

**[02:04]** and we'll be talking about tools to go and complete other tasks

**[02:07]** and look at how we combine them together.

**[02:10]** In this case, we're just going to do a simple sequential chain, right?

**[02:13]** Let's go ahead and get started.

**[02:14]** The first thing is getting our requirements installed.

**[02:17]** So I've already ran this earlier today, but installing our libraries

**[02:20]** and then configuring the configurations for our lab environment.

**[02:24]** So making sure you always run these before you run the demos in the labs

**[02:27]** because this is needed to download all the packages

**[02:30]** as well as any additional data sets and configuration settings for your environment.

**[02:35]** So that's out of the way.

**[02:36]** Let's go ahead and jump in.

**[02:40]** So this is the configuration settings it sets up.

**[02:42]** So it actually creates a catalog and some schemas for us

**[02:45]** that it uses in the lab environment.

**[02:46]** And we'll come back to that in a bit.

**[02:48]** So let's jump into our component.

**[02:50]** So we're building a couple of components.

**[02:51]** We're going to build a prompt component, a LLM component, a retriever, tool integration,

**[02:57]** and then we're going to create a chain to go and connect them together.

**[02:59]** The first one's pretty straightforward.

**[03:01]** It's a prompt.

**[03:01]** It's a basic building block when we're looking at generative AI applications

**[03:05]** and it's pretty straightforward.

**[03:06]** It's the prompt or the input to our large language model

**[03:10]** and what that should look like.

**[03:11]** And very common when it comes to prompts is prompt engineering

**[03:14]** and with prompt engineering, prompt templates or the structure of that prompt.

**[03:18]** So here we have an example of a prompt template.

**[03:20]** So tell me about a genre, movie, which actor is one of the actors.

**[03:25]** And we have a placeholder for the genre and the actor.

**[03:28]** And then we can instantiate this prompt with a specific genre and actor

**[03:32]** when we go and use the object here.

**[03:34]** So you can see here with romance and Brad Pritt.

**[03:36]** So here, tell me a romance movie, which Brad Pritt is one of the actors.

**[03:40]** So really common practice is building a convention around how we go

**[03:44]** and capture these prompts that work really well

**[03:47]** that we can share with our organization.

**[03:49]** In this case, Lang chain provides things like the prompt template

**[03:52]** then that we can reuse and share as well as use as a piece to go

**[03:55]** and prepare our data or our input to go and pass through an LLM.

**[03:59]** That's our prompt.

**[04:01]** Now, the next piece is the LLM itself.

**[04:04]** So you can think of the LLM as the computer project

**[04:07]** or the business logic that actually processes the prompt.

**[04:10]** And there's different options.

**[04:11]** There's tons of different models out there.

**[04:13]** I think everyone last year has been talking about all the different models

**[04:15]** that are out there from llama to open AIs models to Databricks

**[04:20]** as DBR X model and MPT and llama three models that we have

**[04:24]** in our foundational models API.

**[04:26]** So in this case, we're going to actually go and connect

**[04:28]** to one of the models that Databricks has

**[04:30]** and that model is going to be DBR X instruct.

**[04:32]** So here we're going to bring in the chat models component in Lang chain

**[04:37]** and we're going to bring in the chat Databricks.

**[04:39]** So this actually allows Lang chain to talk to the Databricks endpoint.

**[04:43]** That's what we're doing here.

**[04:43]** And we're configuring the chat Databricks to go

**[04:45]** and connect to Databricks instruct.

**[04:47]** And then now what we can do is we can go and send that data over there

**[04:51]** and get an output.

**[04:53]** So here's just an example of us sending who is Brad Pitt to it.

**[04:57]** And then you can see here kind of the tokens that it generated out.

**[05:00]** Is that Brad Pitt is an American actor and film producer.

**[05:04]** So you can see the output there.

**[05:05]** So we have our LLM configured.

**[05:09]** So we have our prompt, our LLM.

**[05:11]** The next one we're going to do is a retriever.

**[05:12]** In this case, instead of using a private retriever

**[05:17]** like we did in the last demo with Databricks Vector Search,

**[05:20]** in this case, we're going to use a community given retriever.

**[05:22]** And a common thing to retrieve against is online resources.

**[05:26]** In this case, Wikipedia.

**[05:28]** We're going to load in the Wikipedia retriever.

**[05:30]** And you can see here it's very easy to go and load

**[05:32]** because Lang chain the community has already contributed

**[05:34]** and built a retriever for Wikipedia.

**[05:36]** We can go and do that.

**[05:37]** And then we can use that to go and do a search for Brad Pitt.

**[05:41]** We have that.

**[05:41]** And then we're just returning one of the documents.

**[05:43]** And you can see here we have the article for Brad Pitt

**[05:45]** on Wikipedia here.

**[05:46]** So pretty predictable and what we were expecting there.

**[05:50]** So we have a retriever.

**[05:51]** All right.

**[05:51]** So finally, what's next?

**[05:54]** Next, we're going to have a tool.

**[05:56]** So tools are interesting.

**[05:57]** So whereas retrievers are really built to go

**[05:59]** and pull information from databases and search systems

**[06:04]** that could collect a lot of data,

**[06:05]** tools can be used to invoke other functions

**[06:08]** such as running code, writing math expressions,

**[06:12]** sending out emails, things like that.

**[06:13]** Now, in this case, the tool that we're going to use

**[06:15]** is tool that was built by the community

**[06:17]** to do a search on YouTube.

**[06:18]** So that's what we're doing here.

**[06:20]** We're going to go and search YouTube.

**[06:21]** So YouTube search tool.

**[06:23]** And then in this case, Brad Pitt movie trailer.

**[06:25]** And you can see here it returns this link

**[06:27]** for YouTube videos that are related to it.

**[06:30]** So we can get some details on that here as well.

**[06:34]** So search for video person, comma separate.

**[06:37]** So this is if you want to know what the tool does,

**[06:39]** we can get descriptions of the tool here.

**[06:41]** So the description and then arguments.

**[06:43]** And this is something when it comes to lane chain

**[06:45]** that they developed, which is one of the ideas is

**[06:47]** how do we integrate LLMs with tools?

**[06:50]** And one of the things is one is actually connecting

**[06:52]** the tool to the service,

**[06:53]** writing the code to make it happen.

**[06:54]** But the other also is defining that interface.

**[06:57]** What does it look like to work with a tool?

**[06:59]** What can the tool do so that the LLM

**[07:01]** can then know how to use the tool?

**[07:03]** In this case, this tells us what the tool does.

**[07:05]** The LLM can understand that.

**[07:06]** And then the structure for the queries.

**[07:08]** So that's there, the description and the argument.

**[07:12]** So we have our components.

**[07:14]** Now we can go and chain them together.

**[07:16]** So this is an example of using lane chain to do a chain.

**[07:18]** In this case, the chain that we're doing

**[07:19]** is prompt to the model and then pulling the output.

**[07:23]** So just a sequential chain.

**[07:25]** So remember, if we looked at our prompt template,

**[07:27]** again, earlier the prompt template was

**[07:29]** find me movies, romance movies with Brad Pitt in them.

**[07:32]** And then LLM can process that.

**[07:34]** So this is an example of that.

**[07:35]** So Brad Pitt has been in a few romance films,

**[07:38]** but most noticeably is the curious case of Benjamin Button.

**[07:42]** You can see here an example of that.

**[07:44]** But there's no retrieval in this case.

**[07:45]** We're really just having two pieces,

**[07:46]** which is the prompt and the LLM.

**[07:49]** So let's go and build a more complex chain.

**[07:52]** So let's go and do more other chains

**[07:54]** where we're gonna go and connect to things

**[07:57]** like vector stores or something like that.

**[07:59]** So let's jump over to multi-stage.

**[08:01]** In this case, we're gonna do something

**[08:02]** that's a little bit more complicated.

**[08:04]** Instead of using built-in tools and things like that,

**[08:07]** in this case, we're gonna show an example of RAG,

**[08:09]** but in which we're actually gonna connect

**[08:11]** to a vector search database endpoint.

**[08:14]** So that's what we're gonna do here.

**[08:15]** We're gonna go define our vector search endpoint.

**[08:18]** So this code here is just selecting

**[08:20]** a pre-built endpoint if it's already built

**[08:21]** in your environment or falling back to a backup.

**[08:24]** So in this case, it's found that we have

**[08:27]** vector search endpoint number three,

**[08:28]** what it's gonna use.

**[08:30]** Now that we have that endpoint,

**[08:31]** the next thing we're gonna do is we're gonna go

**[08:33]** and load data into that endpoint.

**[08:34]** So here is some code identifying our tables,

**[08:38]** DAS text, DAS embedding.

**[08:40]** We have a whole bunch of text data

**[08:41]** that's already been loaded up into,

**[08:43]** that we're gonna load into this table.

**[08:45]** And then we're gonna use that table

**[08:46]** to create an index on top of,

**[08:48]** that's gonna be used by the vector search database.

**[08:50]** You can see here's some code to load the data.

**[08:52]** And then we're gonna go and override it

**[08:55]** if it exists already.

**[08:56]** And then once we have that table created,

**[08:58]** we're gonna create an index on the DAS text data.

**[09:01]** And then that's gonna make it all good to go.

**[09:03]** So I ran this earlier, so it's all good to go,

**[09:06]** but it'll create these two tables.

**[09:07]** So we jump over here, we have the text table

**[09:10]** that you can see here, this is all the DAS talks

**[09:13]** that happened last year and the titles

**[09:16]** and the abstract of those that we have.

**[09:19]** So here's a sample set of that.

**[09:20]** And then what we did was we created index

**[09:22]** on top of this inside of vector search.

**[09:25]** So you can see here, our vector search endpoint,

**[09:28]** you can see our index.

**[09:29]** And if you look at this index

**[09:30]** actually points to this table here,

**[09:33]** and you can see this table is very similar

**[09:34]** to our text table, except instead of just title

**[09:38]** and abstract, we also now have these embeddings

**[09:40]** that the vector search database is using

**[09:42]** or Daybrick's vector search is using

**[09:44]** to do that similarity search.

**[09:46]** And we have that there.

**[09:47]** Our table is ready to go.

**[09:49]** Now we can use that to go and do a query.

**[09:52]** Now to set up the query,

**[09:53]** we're gonna go and create parts of our chain again.

**[09:55]** We're gonna create, we're gonna load up our model,

**[09:57]** our tool, so this is our YouTube search tool,

**[10:00]** our model.

**[10:01]** And then we're gonna go set up our prompt template.

**[10:03]** So this one's a little bit different.

**[10:04]** Instead of the model asking about a movie,

**[10:06]** we're gonna be asking about Databricks.

**[10:07]** So you are a Databricks expert.

**[10:09]** You have question about Databricks,

**[10:10]** try to give simple answers and be professional.

**[10:12]** And then we pass through the question

**[10:13]** and then get some answers.

**[10:15]** So we define this chain as pass through the question,

**[10:18]** pass through the question here,

**[10:20]** and then our prompt template,

**[10:22]** then the model, then we get our output.

**[10:23]** So here's an example of how machine learning models

**[10:26]** are stored in Unity catalog.

**[10:27]** And then here you can see the answer.

**[10:28]** Machine learning models in Databricks

**[10:30]** can be stored in Unity catalog as MLflow model artifacts.

**[10:33]** So we have that, our first chain that we built.

**[10:35]** So this is chain number one.

**[10:37]** And this chain is a combination of the question,

**[10:39]** the prompt template, the model, then the output.

**[10:42]** So we're combining that into this component.

**[10:44]** And then the second chain here

**[10:46]** is we're gonna use that information

**[10:48]** and we're gonna augment that with another chain

**[10:50]** in which this chain, what we're gonna do

**[10:52]** is we're gonna use our vector search index

**[10:54]** and we're gonna use that to grab titles of talks

**[10:59]** that were done at DAS

**[11:00]** and then find the YouTube video related to it.

**[11:02]** So that's what we're gonna do here.

**[11:03]** So here's our vector search client,

**[11:05]** our index that we defined earlier.

**[11:07]** The query we're gonna ask is how do I use Databricks SQL?

**[11:10]** And then we're gonna load in

**[11:12]** our Databricks vector search client.

**[11:14]** Here's our similarity search that's going on

**[11:17]** and then our video search tool here

**[11:19]** and then our prompt.

**[11:20]** So you will get a list of videos

**[11:21]** related to the user questions that are recorded at DAS,

**[11:23]** encourage the user to watch the videos,

**[11:25]** list the videos with YouTube links

**[11:27]** and then we have that through here.

**[11:28]** So here you can see we have this go through the prompt,

**[11:32]** videos, so here we're pulling in the videos

**[11:34]** from our YouTube videos

**[11:36]** and then we pass through the model

**[11:37]** and then the model gives us the output.

**[11:38]** So you can see that.

**[11:41]** I don't think we run it here.

**[11:44]** We don't see the output.

**[11:45]** We don't run it here

**[11:46]** and then we're gonna put that together

**[11:48]** to go and do a multi-chain

**[11:49]** where we actually have two chains running together.

**[11:51]** So the first chain about the question

**[11:53]** and then the second chain doing that video lookup.

**[11:55]** So here that's what we have

**[11:57]** and you can see here machine learning models

**[11:59]** are part of the Lakehouse platform

**[12:01]** and then you can also see here some code

**[12:04]** and then you can also see some related videos

**[12:06]** that we have that's received from the second chain.

**[12:09]** So you can see here how we can build up

**[12:11]** from a very simple application,

**[12:13]** build up the simple components,

**[12:14]** combine those components into complex systems or chains

**[12:17]** then we can even combine chains together

**[12:19]** into multi-stage chains or AI systems.

**[12:23]** That's what we have here.

**[12:24]** Showing you that really quick

**[12:25]** of what it looks like and building on

**[12:27]** and using lane chain as an example

**[12:29]** of one of the frameworks

**[12:30]** and how those frameworks

**[12:31]** can make things a little bit easier.

