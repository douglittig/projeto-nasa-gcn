# 04 - Demo Deconstruct and Plan a Use Case

**Source:** `04-Demo_ Deconstruct and Plan a Use Case.mp4`
**Duration:** 14:35
**Language:** en (detected with 100.0% confidence)

---

## Full Transcription

All right, so that's what we're gonna do here. We're actually gonna jump into a demo. I'm gonna go jump into the notebooks. We're gonna go through each of these kind of components or intents and look at how do we define the APIs, interfaces, understand the dependencies and the components needed to go and build that. Right, so in that, we're gonna talk about how what it looks like to build the run search, run summary, run get context, run QA stage, and then we'll look at full multi-end point car architecture where we have identified at the end of this kind of the interfaces, the flow, as well as other dependencies that our system might rely on. All right, let's jump into a demo. And this demo is really talking about what we just talked about in our slides, which is how to plan a compound AI system architecture. So we're gonna go over that architecture diagram and then dive a little bit deeper into how do we go and look at each of those components and stages and then what would that kind of look at like the high level when you look at the code. So that's one of the things we wanna think about when it comes to building out a system. In this demo, we'll talk about doing that in Python. We'll talk about really the goal here is to scope the functionalities and strengths of each of the components in the system and outline the structure and relationship of each of those components and address some of the technical challenges. So then when it comes to implementation, we know everything that's involved before we start building it. So by the end of this demo, you should be able to apply a class architecture in the composition phase. We'll be able to explain the conventions that map the stages to class methods and then plan what methods and attributes are used to write a compound application and the various components in a compound app. All right, so to start off, we're gonna run some of the requirements. I've already ran this earlier. So it's basically gonna install some libraries. In this case, we're using GraphViz to visualize the architecture to make it easier for you to see in HTML. And then we're gonna install a couple of libraries right here. And then we define two functions here that are gonna be used to visualize that graphic that you saw on the slide. So it's just some HTML code that defines the graph that you see. So I'm not gonna go into it here, but it's just all the HTML code that's used to generate that. So this is to create the HTML, and then this is to highlight a particular stage in the HTML. So they're helper methods to help us visualize what we're doing. All right, overview of the application. So when we're looking at an application, today, modern generative AI applications aren't just a single LLM call. They're actually an LLM call comprised of other functions that might be involved in order to go and make that happen, such as a vector database or a rag or something like that. So really that's the focus of this is how do we go and take those complex systems and break them down into their individual components so one, we can better understand how those components are connected together and to understand the separation between those components and the interfaces and those things. So that's really the thing that we're gonna focus here. And when you're looking at each of these stages, the things we wanna consider is intent. What is the goal of each component? Naming, how do we wanna name it? There are conventions around this. I think if you look at the documentation on the Python documentation, there's actually conventions around this in the world of Python, such as run underscore for everything that we're gonna use in our examples here. When we're writing software, we need to also be aware of the dependencies or the libraries that we're using when we're building the application. Without that awareness, then when it comes to deployment, there can be a lot of challenges and things. So the goal here is to understand what do those components depend on? And then the actual thing that we think of when we think about coding, which is the signature, which is the input and the output arguments for all of that. What do we need to feed the function and then what does the function respond to or the output? All right, okay, so let's go through it. So let's go through the high level architecture first again, and then we can dive into kind of the individual components. So again, this is the compound application. We have the beginning with a question and the end is the answer that we want. So if you think about it, it could be something like a chat bot that we use or a chat assistant. Right now for this to work though, there's actually a couple of pieces that are gonna happen. We're first gonna go and do a search. So if we're building kind of an application like this, a rag is a very common application architecture. If you actually look at it, this is actually a rag architecture. We need to go and search for relevant documents. So in that case, go and retrieve some external information and grab that. So that's our retrieval piece. We then have right here our summary piece. Very often, we can't just feed the data as is to the large language model. So what we're actually gonna do here is we're gonna go and compress the original documents by running a summary function on top of it. So we'll talk about that. And once we have that, we can then grab the summaries, compile those into the context that we're gonna use to then feed to our model. So here, we're gonna take it, compile it into a context, and then we're gonna use that context and then feed to our model to actually answer the question. And then we get that as output. So really, if you look at this, the QA chatbot is actually comprised of a couple of different steps here. And what we're gonna do is we're gonna go into each of those steps. So the first step is that run search stage. If we think about run search, that's our retrieval piece of our rag architecture. So here, we're gonna define the run search. We're gonna give it the name. Search seems appropriate here. If we look at search, what are we gonna do or how are we gonna perform that search? And very common when it comes to rag architectures is using something like a vector database. Now in Databricks, the vector database that we might use might be Databricks vector search. Now, if we're using Databricks vector search, then we might use something like vector search client to go and perform a search. If we're performing search, we typically need to perform that against a vector search index. What are some of the methods and things that we would use to go and do that? I'm gonna go ahead and show the solution here, but the practice here would be, we would want you to go and figure this out yourself. You might go to the documentation, but for vector search, that would be vector search index get index and vector search index similarity search to perform the search. When we have that, what are the arguments for our application? If you're working with Databricks vector search, we need to have the endpoint. What's the vector search endpoint? That's why we do this vector search index is to maybe grab the endpoint information and the index name that we can then feed to our actual search method. The signature for this component, typically the input is gonna be the query from the user. So what is that query that the user is asking? We then pass that query over to our vector search API and it might take some additional parameters. What column we wanna search against, any filters, the results that we wanna go and configure. So those are just some other things that we might wanna add to that. And then the output, typically, if you're looking at Databricks vector search, it returns a dictionary and that dictionary is gonna include the results as well as pagination tokens if we get a lot of results back. So really, the key thing here is understanding how this works. What are the inputs and the outputs? And a lot of this is to help us understand what we need before we even getting to the coding phase. And one big thing here is the idea we need to go and connect to a vector database. I'll get back to that in a little bit. So that's one dependency we discovered as part of this. All right, let's jump into another component. Next one is summary. So run summary. The idea here is, in a lot of cases, when we're working with LLMs, especially in RAG, is that the LLMs have a limitation on the context window. We can't just feed it unlimited data. Typically, they have a limit on how much data they can process as input. So because of that, what we're gonna do here is we're gonna do some processing on the results from our search components. So instead of feeding the raw documents, we're gonna go and summarize those documents. And that's what this is doing here is we're actually gonna go do a summarization of the documents and I'll show the answers again here, but we're gonna do that. Now, how we're gonna do that in this case, our implementation is the idea is we're gonna use a LLM to summarize the material we get from our vector search. That's what we're gonna do. Now, if we wanna use an LLM in Databricks, we wanna use the Databricks deployment client to go and make a connection to the Databricks foundational models API. So we have these two dependencies. We need to know what model to actually go and talk to in the endpoint. So we have this dependency here we wanna go and use connecting the Databricks. And then once we have that, we're missing kind of the LLM here. That's something that would add here. And then signature inputs, typically that's gonna be the content and then the question. In our case, the question is summarize the input. And then here, these are additional, whenever you're working with LLM configurations around that LLM, the prompt, and then the results we should get back should be the text that we get back. That's an example for that. Here, the answers don't give us everything, but that's part of the process. The idea here is sometimes we might not catch everything. And as we go through this process, we're able to catch those pieces that we're missing. Now, in this case, the key thing that we identified is if we're using a large language model, we're gonna need this dependency of connecting to the Databricks client, MLflow client and configurations for that, as well as the prompt to go and do the summary and things like that. So defining those pieces. So that's a summary. And really here, we're just looking at how do we do a summary for a single record that comes from our search component that came earlier. So another thing we add here is this run augment stage. And what this does is this allows us to asynchronously parallelize that summary across multiple records. So instead of us having to do the summary one at a time, the idea here is to run them in parallel. So I'm not gonna go into details here, but this is something we would wanna define. So I'll give this as your homework to go and figure out here. But it uses something like async.io. You don't need to understand how that works, but it allows us to basically parallelize the task and track those tasks as we complete them all in parallel. But the inputs and outputs here are very similar, right? You would probably have input is the dictionary of all of our results from our run search component. And then the output here is going to probably be a dictionary as well that we're gonna feed in to our get context component, which is what I'm gonna talk about next. So next is our get context component. And the get context component really is how do we go and just take all of the information that we have summarized and compile that into a piece that we're actually gonna go and pass to our large language model to use to go and get an answer, that augmented prompt. So that's really what we're doing here. And there's different ways we can go and do that. In this case, we're also gonna go and do a sort. So we might sort the results based on that. And that's what we might go and do here and then concatenate it. So we're really taking in a dictionary as our input, and then we'll get out a plain text string that we can then use into our QA component. So we have that, right? But you can see here, really, there's no dependencies here. It's really just, we're just using the Python to do some concatenation, right? But you could make it more complex too. The idea here is it takes in a dictionary of results, summarized results, and it outputs a concatenated context that we pass through the model. And in this case, we're just implementing it with a simple sort. But imagine you could use other strategies. You might go and use Spark to go and do this sort at scale. You might go and do something else with this. It's up to you. But the idea is by modularizing this and defining what the inputs and outputs are, it lets us hide away that and abstract that complexity. But anyways, input, our augmented search results, and our context is a string as output. So once we have that, then the last piece of this is the QA piece, which is where we actually use a chat model to go and answer the question finally. All of that was really like, if you think about just data preparation to give to the LLM to think about it, that's what we have here. So very similar because we're using LLM model, can be similar to that run summary. And then we're going to pull in the Databricks deployment client. For our configuration here, we need our endpoint just like before. But instead, when we look at these parameters for using it, our context and our question is going to be a little bit different. Our context here will typically be the context from our previous component. Our question might be the user question that we had from the very beginning. And then our QA prompt might be providing that in to tell the model that, hey, based on this context, can you answer using the context? And then we get the results out and then we can grab the message. All in all, we went high level of what are all the components in a RAG system. We talked about the different pieces, how we need to think about each component, what the inputs and outputs of each of those components look like, what the logic or intent of each of these components of what they're supposed to do. And by decoupling or decomposing that into those pieces, it can make it easier for us to understand what's going on and wrap our heads around the complexity of the system. By breaking down the smaller pieces, they become more manageable. That also makes it very easy when we look at our code that finally we put it all together, you can see the code that's very easy to understand. We're doing a search, we're augmenting the search results by doing our summary compression. We then generate the context then we pass the context to our model to get a question. And then once it processes the question with the context, we get an answer back that we can then respond back. And that's our main method that puts together the entire RAG architecture. And if you look at it, it's pretty simple. The question is the input, the answer is the output as a string. But behind the scenes, there's all of these components working together to make that happen. All right, other thing that we wanted to talk about here is overall with our application, we also identified dependency, which are very important because if it comes to productionizing, we need to know if it depends on other systems and services. And what we found also during our component, the composition process, we found that the run search depends on a search database, or in this case, data expector search. So that's something that we need to be aware about. Our summary component here is using an LLM to perform that summarization. So we need to think about model serving and what model we're using for that summarization process. And then for our run QA, we're using a chat bot or a chat model to go and process the question and the prompt. So we also need to think about in model serving and what model we're using for that as well. So with that in conclusion, really high level looking at a simple compound AI system, in this case, a rag system. That's what we're working with. That's very familiar, but really breaking it down into its individual components and understanding what each of those components are and then the dependencies that they may have. And it's very important when we're working with software architecture and design to be aware about this. And that's one of the new things when it comes to generative AI is that we're no longer just building models, we're building these systems and it's good to have a high level understanding of what the system looks like before we go and start building it.

---

## Timestamped Segments

**[00:00]** All right, so that's what we're gonna do here.

**[00:01]** We're actually gonna jump into a demo.

**[00:03]** I'm gonna go jump into the notebooks.

**[00:04]** We're gonna go through each of these kind of components

**[00:08]** or intents and look at how do we define the APIs,

**[00:12]** interfaces, understand the dependencies

**[00:14]** and the components needed to go and build that.

**[00:16]** Right, so in that, we're gonna talk about

**[00:18]** how what it looks like to build the run search,

**[00:20]** run summary, run get context, run QA stage,

**[00:23]** and then we'll look at full multi-end point

**[00:26]** car architecture where we have identified

**[00:29]** at the end of this kind of the interfaces,

**[00:30]** the flow, as well as other dependencies

**[00:33]** that our system might rely on.

**[00:36]** All right, let's jump into a demo.

**[00:38]** And this demo is really talking about

**[00:40]** what we just talked about in our slides,

**[00:41]** which is how to plan a compound AI system architecture.

**[00:45]** So we're gonna go over that architecture diagram

**[00:48]** and then dive a little bit deeper into

**[00:50]** how do we go and look at each of those components

**[00:52]** and stages and then what would that kind of look at

**[00:55]** like the high level when you look at the code.

**[00:59]** So that's one of the things we wanna think about

**[01:02]** when it comes to building out a system.

**[01:04]** In this demo, we'll talk about doing that in Python.

**[01:07]** We'll talk about really the goal here is to scope

**[01:09]** the functionalities and strengths

**[01:11]** of each of the components in the system

**[01:13]** and outline the structure and relationship

**[01:15]** of each of those components

**[01:16]** and address some of the technical challenges.

**[01:19]** So then when it comes to implementation,

**[01:20]** we know everything that's involved

**[01:22]** before we start building it.

**[01:23]** So by the end of this demo,

**[01:25]** you should be able to apply a class architecture

**[01:27]** in the composition phase.

**[01:28]** We'll be able to explain the conventions

**[01:30]** that map the stages to class methods

**[01:32]** and then plan what methods and attributes are used

**[01:35]** to write a compound application

**[01:36]** and the various components in a compound app.

**[01:39]** All right, so to start off,

**[01:40]** we're gonna run some of the requirements.

**[01:42]** I've already ran this earlier.

**[01:43]** So it's basically gonna install some libraries.

**[01:45]** In this case, we're using GraphViz

**[01:47]** to visualize the architecture

**[01:48]** to make it easier for you to see in HTML.

**[01:51]** And then we're gonna install a couple of libraries

**[01:54]** right here.

**[01:55]** And then we define two functions here

**[01:58]** that are gonna be used to visualize that graphic

**[02:00]** that you saw on the slide.

**[02:02]** So it's just some HTML code

**[02:03]** that defines the graph that you see.

**[02:05]** So I'm not gonna go into it here,

**[02:07]** but it's just all the HTML code

**[02:09]** that's used to generate that.

**[02:11]** So this is to create the HTML,

**[02:13]** and then this is to highlight a particular stage

**[02:15]** in the HTML.

**[02:16]** So they're helper methods

**[02:17]** to help us visualize what we're doing.

**[02:19]** All right, overview of the application.

**[02:20]** So when we're looking at an application,

**[02:22]** today, modern generative AI applications

**[02:24]** aren't just a single LLM call.

**[02:27]** They're actually an LLM call comprised of other functions

**[02:30]** that might be involved in order to go and make that happen,

**[02:34]** such as a vector database or a rag or something like that.

**[02:37]** So really that's the focus of this

**[02:39]** is how do we go and take those complex systems

**[02:41]** and break them down into their individual components

**[02:43]** so one, we can better understand

**[02:45]** how those components are connected together

**[02:47]** and to understand the separation between those components

**[02:51]** and the interfaces and those things.

**[02:53]** So that's really the thing that we're gonna focus here.

**[02:55]** And when you're looking at each of these stages,

**[02:56]** the things we wanna consider is intent.

**[02:59]** What is the goal of each component?

**[03:01]** Naming, how do we wanna name it?

**[03:02]** There are conventions around this.

**[03:03]** I think if you look at the documentation

**[03:05]** on the Python documentation,

**[03:07]** there's actually conventions around this

**[03:09]** in the world of Python, such as run underscore

**[03:11]** for everything that we're gonna use in our examples here.

**[03:14]** When we're writing software,

**[03:16]** we need to also be aware of the dependencies

**[03:18]** or the libraries that we're using

**[03:20]** when we're building the application.

**[03:21]** Without that awareness,

**[03:22]** then when it comes to deployment,

**[03:23]** there can be a lot of challenges and things.

**[03:25]** So the goal here is to understand

**[03:27]** what do those components depend on?

**[03:29]** And then the actual thing that we think of

**[03:31]** when we think about coding, which is the signature,

**[03:33]** which is the input and the output arguments

**[03:35]** for all of that.

**[03:36]** What do we need to feed the function

**[03:39]** and then what does the function respond to

**[03:41]** or the output?

**[03:42]** All right, okay, so let's go through it.

**[03:44]** So let's go through the high level architecture

**[03:47]** first again, and then we can dive

**[03:50]** into kind of the individual components.

**[03:52]** So again, this is the compound application.

**[03:55]** We have the beginning with a question

**[03:57]** and the end is the answer that we want.

**[04:00]** So if you think about it,

**[04:01]** it could be something like a chat bot that we use

**[04:03]** or a chat assistant.

**[04:05]** Right now for this to work though,

**[04:06]** there's actually a couple of pieces

**[04:07]** that are gonna happen.

**[04:08]** We're first gonna go and do a search.

**[04:10]** So if we're building kind of an application like this,

**[04:14]** a rag is a very common application architecture.

**[04:16]** If you actually look at it,

**[04:17]** this is actually a rag architecture.

**[04:18]** We need to go and search for relevant documents.

**[04:21]** So in that case,

**[04:22]** go and retrieve some external information and grab that.

**[04:24]** So that's our retrieval piece.

**[04:26]** We then have right here our summary piece.

**[04:28]** Very often, we can't just feed the data as is

**[04:32]** to the large language model.

**[04:34]** So what we're actually gonna do here

**[04:36]** is we're gonna go and compress the original documents

**[04:39]** by running a summary function on top of it.

**[04:41]** So we'll talk about that.

**[04:42]** And once we have that,

**[04:43]** we can then grab the summaries,

**[04:46]** compile those into the context that we're gonna use

**[04:49]** to then feed to our model.

**[04:51]** So here, we're gonna take it, compile it into a context,

**[04:55]** and then we're gonna use that context

**[04:56]** and then feed to our model

**[04:57]** to actually answer the question.

**[04:59]** And then we get that as output.

**[05:00]** So really, if you look at this,

**[05:02]** the QA chatbot is actually comprised

**[05:05]** of a couple of different steps here.

**[05:06]** And what we're gonna do

**[05:07]** is we're gonna go into each of those steps.

**[05:08]** So the first step is that run search stage.

**[05:11]** If we think about run search,

**[05:12]** that's our retrieval piece of our rag architecture.

**[05:15]** So here, we're gonna define the run search.

**[05:18]** We're gonna give it the name.

**[05:19]** Search seems appropriate here.

**[05:21]** If we look at search, what are we gonna do

**[05:23]** or how are we gonna perform that search?

**[05:25]** And very common when it comes to rag architectures

**[05:27]** is using something like a vector database.

**[05:29]** Now in Databricks,

**[05:30]** the vector database that we might use

**[05:32]** might be Databricks vector search.

**[05:34]** Now, if we're using Databricks vector search,

**[05:36]** then we might use something like vector search client

**[05:38]** to go and perform a search.

**[05:39]** If we're performing search,

**[05:40]** we typically need to perform that

**[05:41]** against a vector search index.

**[05:43]** What are some of the methods and things

**[05:44]** that we would use to go and do that?

**[05:46]** I'm gonna go ahead and show the solution here,

**[05:48]** but the practice here would be,

**[05:49]** we would want you to go and figure this out yourself.

**[05:51]** You might go to the documentation,

**[05:53]** but for vector search,

**[05:55]** that would be vector search index get index

**[05:58]** and vector search index similarity search

**[06:00]** to perform the search.

**[06:02]** When we have that,

**[06:03]** what are the arguments for our application?

**[06:05]** If you're working with Databricks vector search,

**[06:07]** we need to have the endpoint.

**[06:08]** What's the vector search endpoint?

**[06:09]** That's why we do this vector search index

**[06:11]** is to maybe grab the endpoint information

**[06:13]** and the index name that we can then feed

**[06:15]** to our actual search method.

**[06:17]** The signature for this component,

**[06:19]** typically the input is gonna be the query from the user.

**[06:21]** So what is that query that the user is asking?

**[06:24]** We then pass that query over to our vector search API

**[06:29]** and it might take some additional parameters.

**[06:31]** What column we wanna search against, any filters,

**[06:33]** the results that we wanna go and configure.

**[06:35]** So those are just some other things

**[06:37]** that we might wanna add to that.

**[06:39]** And then the output, typically,

**[06:40]** if you're looking at Databricks vector search,

**[06:43]** it returns a dictionary

**[06:44]** and that dictionary is gonna include the results

**[06:46]** as well as pagination tokens

**[06:47]** if we get a lot of results back.

**[06:49]** So really, the key thing here

**[06:51]** is understanding how this works.

**[06:53]** What are the inputs and the outputs?

**[06:55]** And a lot of this is to help us understand

**[06:57]** what we need before we even getting to the coding phase.

**[07:00]** And one big thing here is the idea

**[07:02]** we need to go and connect to a vector database.

**[07:04]** I'll get back to that in a little bit.

**[07:05]** So that's one dependency we discovered

**[07:07]** as part of this.

**[07:08]** All right, let's jump into another component.

**[07:10]** Next one is summary.

**[07:12]** So run summary.

**[07:13]** The idea here is, in a lot of cases,

**[07:15]** when we're working with LLMs, especially in RAG,

**[07:18]** is that the LLMs have a limitation on the context window.

**[07:21]** We can't just feed it unlimited data.

**[07:23]** Typically, they have a limit

**[07:24]** on how much data they can process as input.

**[07:27]** So because of that, what we're gonna do here

**[07:29]** is we're gonna do some processing

**[07:30]** on the results from our search components.

**[07:32]** So instead of feeding the raw documents,

**[07:34]** we're gonna go and summarize those documents.

**[07:36]** And that's what this is doing here

**[07:38]** is we're actually gonna go do

**[07:39]** a summarization of the documents

**[07:41]** and I'll show the answers again here,

**[07:43]** but we're gonna do that.

**[07:44]** Now, how we're gonna do that in this case,

**[07:45]** our implementation is the idea is we're gonna use a LLM

**[07:48]** to summarize the material we get from our vector search.

**[07:53]** That's what we're gonna do.

**[07:54]** Now, if we wanna use an LLM in Databricks,

**[07:56]** we wanna use the Databricks deployment client

**[07:58]** to go and make a connection

**[08:00]** to the Databricks foundational models API.

**[08:02]** So we have these two dependencies.

**[08:05]** We need to know what model

**[08:06]** to actually go and talk to in the endpoint.

**[08:08]** So we have this dependency here

**[08:10]** we wanna go and use connecting the Databricks.

**[08:13]** And then once we have that,

**[08:14]** we're missing kind of the LLM here.

**[08:15]** That's something that would add here.

**[08:16]** And then signature inputs,

**[08:18]** typically that's gonna be the content

**[08:20]** and then the question.

**[08:21]** In our case, the question is summarize the input.

**[08:26]** And then here, these are additional,

**[08:28]** whenever you're working with LLM configurations

**[08:29]** around that LLM, the prompt,

**[08:31]** and then the results we should get back

**[08:33]** should be the text that we get back.

**[08:36]** That's an example for that.

**[08:37]** Here, the answers don't give us everything,

**[08:39]** but that's part of the process.

**[08:40]** The idea here is sometimes we might not catch everything.

**[08:43]** And as we go through this process,

**[08:45]** we're able to catch those pieces that we're missing.

**[08:47]** Now, in this case,

**[08:48]** the key thing that we identified is

**[08:49]** if we're using a large language model,

**[08:51]** we're gonna need this dependency of connecting

**[08:53]** to the Databricks client,

**[08:56]** MLflow client and configurations for that,

**[08:58]** as well as the prompt to go and do the summary

**[09:00]** and things like that.

**[09:01]** So defining those pieces.

**[09:03]** So that's a summary.

**[09:04]** And really here, we're just looking at

**[09:05]** how do we do a summary for a single record

**[09:08]** that comes from our search component that came earlier.

**[09:12]** So another thing we add here is this run augment stage.

**[09:15]** And what this does is this allows us

**[09:17]** to asynchronously parallelize that summary

**[09:21]** across multiple records.

**[09:23]** So instead of us having to do the summary one at a time,

**[09:26]** the idea here is to run them in parallel.

**[09:28]** So I'm not gonna go into details here,

**[09:29]** but this is something we would wanna define.

**[09:32]** So I'll give this as your homework

**[09:33]** to go and figure out here.

**[09:34]** But it uses something like async.io.

**[09:36]** You don't need to understand how that works,

**[09:37]** but it allows us to basically parallelize the task

**[09:40]** and track those tasks as we complete them all in parallel.

**[09:42]** But the inputs and outputs here are very similar, right?

**[09:45]** You would probably have input is the dictionary

**[09:48]** of all of our results from our run search component.

**[09:52]** And then the output here

**[09:53]** is going to probably be a dictionary as well

**[09:55]** that we're gonna feed in to our get context component,

**[09:58]** which is what I'm gonna talk about next.

**[10:01]** So next is our get context component.

**[10:04]** And the get context component really is

**[10:06]** how do we go and just take all of the information

**[10:09]** that we have summarized and compile that into a piece

**[10:12]** that we're actually gonna go and pass

**[10:14]** to our large language model to use

**[10:17]** to go and get an answer, that augmented prompt.

**[10:19]** So that's really what we're doing here.

**[10:21]** And there's different ways we can go and do that.

**[10:23]** In this case, we're also gonna go and do a sort.

**[10:25]** So we might sort the results based on that.

**[10:28]** And that's what we might go and do here

**[10:29]** and then concatenate it.

**[10:30]** So we're really taking in a dictionary as our input,

**[10:33]** and then we'll get out a plain text string

**[10:36]** that we can then use into our QA component.

**[10:39]** So we have that, right?

**[10:41]** But you can see here, really, there's no dependencies here.

**[10:43]** It's really just, we're just using the Python

**[10:45]** to do some concatenation, right?

**[10:46]** But you could make it more complex too.

**[10:48]** The idea here is it takes in a dictionary of results,

**[10:51]** summarized results,

**[10:52]** and it outputs a concatenated context

**[10:55]** that we pass through the model.

**[10:56]** And in this case,

**[10:57]** we're just implementing it with a simple sort.

**[10:59]** But imagine you could use other strategies.

**[11:01]** You might go and use Spark

**[11:03]** to go and do this sort at scale.

**[11:05]** You might go and do something else with this.

**[11:07]** It's up to you.

**[11:08]** But the idea is by modularizing this

**[11:10]** and defining what the inputs and outputs are,

**[11:12]** it lets us hide away that and abstract that complexity.

**[11:15]** But anyways, input, our augmented search results,

**[11:19]** and our context is a string as output.

**[11:24]** So once we have that,

**[11:25]** then the last piece of this is the QA piece,

**[11:28]** which is where we actually use a chat model

**[11:30]** to go and answer the question finally.

**[11:32]** All of that was really like,

**[11:33]** if you think about just data preparation

**[11:34]** to give to the LLM to think about it,

**[11:36]** that's what we have here.

**[11:36]** So very similar because we're using LLM model,

**[11:39]** can be similar to that run summary.

**[11:41]** And then we're going to pull in

**[11:42]** the Databricks deployment client.

**[11:44]** For our configuration here,

**[11:46]** we need our endpoint just like before.

**[11:48]** But instead, when we look at these parameters

**[11:50]** for using it,

**[11:51]** our context and our question

**[11:52]** is going to be a little bit different.

**[11:53]** Our context here will typically be the context

**[11:55]** from our previous component.

**[11:57]** Our question might be the user question

**[11:59]** that we had from the very beginning.

**[12:01]** And then our QA prompt might be providing that in

**[12:04]** to tell the model that,

**[12:05]** hey, based on this context,

**[12:06]** can you answer using the context?

**[12:08]** And then we get the results out

**[12:11]** and then we can grab the message.

**[12:13]** All in all, we went high level

**[12:15]** of what are all the components in a RAG system.

**[12:19]** We talked about the different pieces,

**[12:21]** how we need to think about each component,

**[12:23]** what the inputs and outputs

**[12:24]** of each of those components look like,

**[12:25]** what the logic or intent of each of these components

**[12:28]** of what they're supposed to do.

**[12:29]** And by decoupling or decomposing that into those pieces,

**[12:34]** it can make it easier for us to understand

**[12:36]** what's going on and wrap our heads

**[12:38]** around the complexity of the system.

**[12:40]** By breaking down the smaller pieces,

**[12:42]** they become more manageable.

**[12:43]** That also makes it very easy

**[12:44]** when we look at our code

**[12:45]** that finally we put it all together,

**[12:47]** you can see the code that's very easy to understand.

**[12:49]** We're doing a search,

**[12:50]** we're augmenting the search results

**[12:52]** by doing our summary compression.

**[12:54]** We then generate the context

**[12:55]** then we pass the context to our model to get a question.

**[12:58]** And then once it processes the question with the context,

**[13:01]** we get an answer back that we can then respond back.

**[13:04]** And that's our main method

**[13:05]** that puts together the entire RAG architecture.

**[13:08]** And if you look at it, it's pretty simple.

**[13:09]** The question is the input,

**[13:11]** the answer is the output as a string.

**[13:13]** But behind the scenes,

**[13:14]** there's all of these components working together

**[13:17]** to make that happen.

**[13:19]** All right, other thing that we wanted to talk about here

**[13:21]** is overall with our application,

**[13:23]** we also identified dependency,

**[13:25]** which are very important

**[13:26]** because if it comes to productionizing,

**[13:28]** we need to know if it depends on other systems and services.

**[13:30]** And what we found also during our component,

**[13:33]** the composition process,

**[13:34]** we found that the run search depends on a search database,

**[13:37]** or in this case, data expector search.

**[13:39]** So that's something that we need to be aware about.

**[13:41]** Our summary component here is using an LLM

**[13:43]** to perform that summarization.

**[13:44]** So we need to think about model serving

**[13:46]** and what model we're using for that summarization process.

**[13:49]** And then for our run QA, we're using a chat bot

**[13:52]** or a chat model to go and process the question

**[13:54]** and the prompt.

**[13:55]** So we also need to think about in model serving

**[13:56]** and what model we're using for that as well.

**[13:59]** So with that in conclusion,

**[14:00]** really high level looking at a simple compound AI system,

**[14:04]** in this case, a rag system.

**[14:06]** That's what we're working with.

**[14:07]** That's very familiar,

**[14:08]** but really breaking it down into its individual components

**[14:11]** and understanding what each of those components are

**[14:13]** and then the dependencies that they may have.

**[14:15]** And it's very important

**[14:16]** when we're working with software architecture

**[14:18]** and design to be aware about this.

**[14:20]** And that's one of the new things

**[14:21]** when it comes to generative AI

**[14:22]** is that we're no longer just building models,

**[14:24]** we're building these systems

**[14:26]** and it's good to have a high level understanding

**[14:28]** of what the system looks like

**[14:29]** before we go and start building it.

