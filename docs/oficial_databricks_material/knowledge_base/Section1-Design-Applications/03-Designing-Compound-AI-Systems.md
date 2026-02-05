# 03 - Designing Compound AI Systems

**Source:** `03-Designing Compound AI Systems.mp4`
**Duration:** 03:42
**Language:** en (detected with 100.0% confidence)

---

## Full Transcription

Designing compound AI systems now that we understand why we want to go and do this and the things of how we want to decompose and get better performance and reliability out of it. What's the process of how we do this? When you look at software engineering, we can take a lot of the ideas from the software engineering world, such as the application development life cycle. So if you ever have built software before, typically we start with analysis. The idea with analysis is we need to go and work with our business and stakeholders to understand what's the objectives and requirements for our application. We need to define the scope, functionality, constraints, and success criteria for the system that we want to develop. Once we get that business level understanding, then we can go into the engineering, which is the design. So what's the architecture going to look like? What's the structure? What are those intents that we're going to go and choose and the behavior of the system? And then we can look at the technical challenges and constraints, right? What APIs, SDKs, what frameworks are we going to use to go and implement? Then once we understand that, then we can actually get into the development. That's where we actually get our hands on the keyboard, write the code, build the system, test the system, make sure that it works. Now, in general, I test things a little bit more challenging. We have another module to talk about that. And then we can talk about things like production, how we get into production, develop the system, productionize it, scale it, and then monitor that system in production to make sure that it's performing well, that it's working, and that our customers are getting value out of it. A lot of things that we don't cover production and monitoring in this module. It's something we cover in our other modules in the course. So with that, let's go and jump into intent classification and chain building. I like to think of intents and chains similar, but in the world of generative AI, those intents are typically implemented as chains. The first is identify the intents. If we look at the system design, what are the high level intents or tasks or components that we are trying to go and do? It's typically one defined task that we're trying to do. Whether that's summer translation, that's something you need to define for your organization and what you think that level of abstraction should be. So we can define those possible intents based on the user queries or based on our requirements. Then we need to look at those intents and what are the dependencies, like is this need to happen before another? Can they happen in parallel? Things like that. Once we understand a high level logic, then we can look at how do we implement that. So identify the tools. How do we actually accomplish that task? Is it a web search? Is it an API call to a database? Is it running code? Is it a model that's going to be doing text to speech or speech to text? Whatever that might be. Once we have that, we can then build the chain to complete that workflow. That might be a RAG, text to SQL, whatever that's needed. We're going to go through an example in a bit. We talked about RAG. Here's an example of an architectural design for RAG. If you look at RAG at a high level, it's really three main intents that we have. We can break them down a little bit more. The first intent is that retrieval piece or that search piece. We then have the middle piece, which is taking those requests and those responses from our search and then building the prompt or the augmentation of the prompt. That's what we're doing here. Grabbing the summaries and then generating those summaries and then building the context. Then once we have the context, we have that generation piece of RAG where we pass that augmented prompt or context to the model to then generate the answer for us.

---

## Timestamped Segments

**[00:00]** Designing compound AI systems now that we understand why we want to go and do this

**[00:04]** and the things of how we want to decompose and get better performance and reliability out of it.

**[00:10]** What's the process of how we do this? When you look at software engineering,

**[00:13]** we can take a lot of the ideas from the software engineering world,

**[00:16]** such as the application development life cycle. So if you ever have built software before,

**[00:21]** typically we start with analysis. The idea with analysis is we need to go and work with

**[00:26]** our business and stakeholders to understand what's the objectives and requirements

**[00:30]** for our application. We need to define the scope, functionality,

**[00:33]** constraints, and success criteria for the system that we want to develop.

**[00:37]** Once we get that business level understanding, then we can go into the engineering,

**[00:41]** which is the design. So what's the architecture going to look like? What's the structure?

**[00:44]** What are those intents that we're going to go and choose and the behavior of the system?

**[00:48]** And then we can look at the technical challenges and constraints, right? What APIs, SDKs,

**[00:54]** what frameworks are we going to use to go and implement? Then once we understand that,

**[00:58]** then we can actually get into the development. That's where we actually get our hands on the

**[01:01]** keyboard, write the code, build the system, test the system, make sure that it works.

**[01:06]** Now, in general, I test things a little bit more challenging. We have another

**[01:09]** module to talk about that. And then we can talk about things like production,

**[01:13]** how we get into production, develop the system, productionize it, scale it,

**[01:17]** and then monitor that system in production to make sure that it's performing well,

**[01:22]** that it's working, and that our customers are getting value out of it.

**[01:26]** A lot of things that we don't cover production and monitoring in this module.

**[01:29]** It's something we cover in our other modules in the course.

**[01:35]** So with that, let's go and jump into intent classification and chain building.

**[01:40]** I like to think of intents and chains similar, but in the world of generative AI,

**[01:44]** those intents are typically implemented as chains.

**[01:48]** The first is identify the intents. If we look at the system design,

**[01:53]** what are the high level intents or tasks or components that we are trying to go and do?

**[02:00]** It's typically one defined task that we're trying to do. Whether that's summer translation,

**[02:06]** that's something you need to define for your organization and what you think that level of

**[02:10]** abstraction should be. So we can define those possible intents based on the user queries or

**[02:16]** based on our requirements. Then we need to look at those intents and what are the dependencies,

**[02:21]** like is this need to happen before another? Can they happen in parallel? Things like that.

**[02:26]** Once we understand a high level logic, then we can look at how do we implement that.

**[02:32]** So identify the tools. How do we actually accomplish that task?

**[02:35]** Is it a web search? Is it an API call to a database? Is it running code?

**[02:39]** Is it a model that's going to be doing text to speech or speech to text? Whatever that

**[02:43]** might be. Once we have that, we can then build the chain to complete that workflow.

**[02:49]** That might be a RAG, text to SQL, whatever that's needed.

**[02:53]** We're going to go through an example in a bit. We talked about RAG. Here's an example

**[02:58]** of an architectural design for RAG. If you look at RAG at a high level, it's really

**[03:03]** three main intents that we have. We can break them down a little bit more.

**[03:07]** The first intent is that retrieval piece or that search piece.

**[03:11]** We then have the middle piece, which is taking those requests and those responses from our

**[03:18]** search and then building the prompt or the augmentation of the prompt. That's what we're

**[03:24]** doing here. Grabbing the summaries and then generating those summaries and then building the

**[03:29]** context. Then once we have the context, we have that generation piece of RAG where we pass

**[03:34]** that augmented prompt or context to the model to then generate the answer for us.

