# Demo Assembling and Evaluat

**Source:** `Generative AI Solution Development - Demo Assembling and Evaluat.mp4`
**Duration:** 20:45
**Language:** en (detected with 100.0% confidence)

---

## Full Transcription

So let's illustrate how we can assemble a chain and evaluate it in the Databricks intelligence platform for in this demo, we'll, we'll assemble a full rack pipeline with the different with the retriever and the choice of the correct model to do the at least the generation piece, we'll evaluate that chain offline, and we'll push once the evaluation offline evaluation is done, we'll initiate, like we'll pull the trigger to push this model down the registry within with an alias, such as it can be pushed down for staging and or production. So let's jump back to the Databricks environment. So if you want to follow along, it's notebook number four, or demo number four, assembling and evaluating a rag application. So again, it's, we're still working on building the same application system rack system using the archive paper. But now we're focusing on the right side of things on building the chain, which will allow us to execute the full full inference. And another term, what are we going to try to assemble together? Whenever a query comes in, we want to make sure that this query will get turned into its into its into the correct embedding using the same embedding model, run a real time similarity search on the created vector search index. Once the documents are retrieved, we'll inject these in our prompt using a specific prompt template, and then send the whole augmented prompt for generation to a Databricks model serving foundation model endpoint, which is going to be llama two to get our generation back. So first thing first is to set up the retriever set up the retriever. So for the retriever, I just need to make sure that I have my endpoints up and running. So we will be I'll be using that specific shared endpoint that I've been using all along the demo. And here we will quick do we will do a quick let's say sanity check on the on the embedding model itself. So let me do a quick shift enter to make sure that the embedding model is up and running. So yes, I can see that. Okay, so I'm testing my embeddings on the question, which is what so what is generative AI and I can see that I have an embedding back now, building the retriever as part of the chain. Here we are going to use line chain as our as to build our chain. And so line chain, especially in the community package, has a lot of let's say, integration with any source of existing Databricks components. So the one of them being the Databricks embedding model, and the other one being the Databricks vector search client. And so whether in your if you're familiar with line chain, so that the wrapping, wrapping the retrieval in a under a method called get retriever is like the preferred way to do things. So this is what we will create here. Within that get retriever method, what are we going to do? We're just going to call as we did in a previous labs and demo, we're going to initiate a vector search client and ask it to retrieve our index given the endpoint name, and the index the index name again, the index name is just pretty sure is the one we created previously. So let me just print that very quickly. It's under my catalog. So you should see you will see that under your catalog schema. It's the PDF self managed vector search index embedding. So we point to the index. And here we will we are going to use the let's say the line chain integration with Databricks vector search. So we're going to create a vector store by telling it to point to the index telling it which text column do we want to retrieve, and which embedding model to use. And here again, the embedding model to use like the format is accepted is accepted for the line chain is going to be the Databricks embedding wrapper on top of the on top of our very own embedding model. So that's pretty much the steps identify your index, create a line chain Databricks vector storage vector store client with the parameters and apply the as retriever method to which you can pass in search arguments. So here are only going to tell it like retrieve the first top two chunks or documents. And that's it. So that's how you set up the method just to show how it works in real time. So you instantiate it using the get you instantiate the get retriever and then you just invoke it by feeding it a given query. And then the output what you will receive will just print that in a second, we will see that it's going to be the relevant documents which are here, which were retrieved previous which were retrieved given the question, how is generative AI impacting humans? So that's step one, you need to create your retriever because we're going to use line chain. So we're going to wrap this or structure it in the format, which is let's say line chain friendly using this get retriever wrapper methods. So once you created the retriever, the second step is to tell to the chain what foundation models or what LLM do we want to use for the generation piece. And in this example, we'll be using Lana 270B, which is again made available by the Databricks foundation models API. But again, you're not like limited to use a foundation model API again, as we said, you can definitely use any other model of choice, whether it's served as an API or running locally, there's no right or wrong here. But it is a very common practice to again have the generation happen using an API. So since we're using line chain, line chain in the community, they're going to have a wrapper, they're going to expose a wrapper class, which points to the Databricks model serving endpoint. So usually the way you instantiate that chat, you just tell it the endpoint name, the base URL. But here in our case, when you don't set the base URL, it will get the current host URL. So it will automatically get the URL of all the my current workspace model serving endpoint and potential other let's say completion or generation parameters such as the max token. So here if again, just to show, you know how this client works, it's nothing more than just a wrapper on top of our on top of the REST API. And it will give you back the results using a specific, let's say format where you have the content and any other response metadata, if you want to do some ad hoc calculations. So we created our retriever as a line chain class, we've created our LLM endpoint again, as a line chain wrapper on top of our Databricks chat foundationals endpoint. So now let's put them all together as part of a single chain. So how to do that? The first thing whenever you want to build any chain is to think about the system prompt. Okay, once I'm retriever, I've chosen my model, how am I gonna, let's say, give the instructions to my model. And for that, we are also going to use one of LLM chain's prompt template capabilities. Again, if you're not, if you're familiar with it, then it's great. If you're not, we'll give you a feel of how it is to use it, but won't spend too much time explaining the semantics. So usually the way it works is you define a template, you define like a template as a free string. So in which you are going to put the instructions, like we're telling here, the assistant that they're a GenAI teaching class or TA, and they need to answer a question on generative AI and how it can impact human's life. If the question is not related, and then add some additional, let's say, instructions, just like we did in the first lab. So we do want to make sure we don't want the model to try to answer any question outside of this topic. And if they don't know, we don't want them to hallucinate or try to come up with something creative and keep them as concise as possible. And here, this is where we're gonna add, let's say, that additional, let's say, structure or layout to instruct the language model to use the following pieces of context only. Put in between those specific signs. Now, the way these needs to be defined really depend on which model you're using. For LAMA, for doing RAG, that's like the expected template. So that meta has been recommended to do so. Put your system prompts at the beginning and then at the end, use the specific formalism to delimit what has been retrieved by your retriever. And now watch in between curly brackets is technically going to be a variable which will be dynamically, let's say, modified by when we're gonna use the prompt template class. And so the prompt, first thing we're gonna create again are prompt templates. So the way it works, you just feed it a template and you tell it what are the potential input variables as part of those templates. So you just need to make sure to use the same variable names. So context here that we're gonna inject and the question here. And once you create the prompt template, putting all the different chains together, you can use a Lang chain LCL, Lang chain executable language, or you could use some pre-baked chain, some like pre-baked standard chain. Here, because we're doing something pretty vanilla, which is a retrieval Q&A without, it was like, it's a single turn thing. There's no history. We're not, it's not like conversational. We are using the retrieval QA chain and the retrieval QA chain is expecting a chat model. So that chat model, again, is that wrapper class on top of the chat Databricks model. There are different types of chains. Stuff is a default one. If again, it's specific to any free text, tell it what is our retriever class. So again, our retriever, which is gonna use the Databricks or Mosaic I Vector Search and any other input arguments for the chain. And in that case, the prompt being our prompt template. So that's how, again, it's not the only way to build a chain, but let's say it's one of the most easiest way out of the box because it's a vanilla chain to use one of those pre-baked chain templates. And so that chain will manage every time a question come running the retriever, getting them back as context, injecting them in the prompt here, injecting the user question here and packaging all that and sending it to the language model for completion. And here the way, once your chain is created, the way it's true to use it is by using the invoke method. So here, for example, let's say I'm again asking that same old question on how is generative AI impacting our lives? I can see the response, but in my response as well, we can also see what sources have been retrieved as well as part of the retriever. And that's also is going to be important for us to back up the response of the LLM, but also if you want to do ad hoc evaluation of our chain, at least we have the retrieved context. So that's it. And if you want to take a quick look at what is that, what's the type of that chain object, it is a Lang chain retrieval QA type class. And again, why are we showcasing that is because in the final step here, as we get to it, we are going to log that chain as is to the MLflow registry because MLflow supports now a model which can have a Lang chain flavor. So now that we have the chain, the next step before even trying to say, okay, do I have something good? Let me just pull the trigger to get it through the LLM Ops pipeline. This is an example of how you can quickly evaluate the chain. Again, here we're doing this as part of a single notebook, but it can be done separately. So in that step, what we are going to create, I'll skim over it very quickly, but it's something you might, it is recommended to have beforehand or think about building it in parallel as the development is happening is creating an evaluation data set where as explained in the theory, in that evaluation data set, it is recommended to have a list of questions. So here we have 12 questions that again, we hard coded them here, but you can be pulling them from something else. Again, you can be pulling them from a spreadsheet or a table. What would a ground truth answer look like? And here, for example, okay, what type of inquiry is it? Is it like simple? Is it reasoning? Simple is usually some sort of like closed factual or closed question. That's it. Now we don't have, let's say ground truths for context or ground truths for retrieved. But at this point, I don't think we need that. Again, we have the question, we have the ground truths, and from the chain, we are going to get the completions and the context. And we have all four elements to run our evaluations. So once we have that eval, let's say list of Q&A, we're going to assemble them together in a hugging face data set. So first, we are going to batch each question to the chain, store the responses and put everything, you know, structure everything back into a pandas data frame. Again, we're using the hugging face data set to facilitate this, but you're not forced to use hugging face data sets. Ultimately, in order to run your evaluation, what the expected variable to have is a table, a pandas data frame or spark data frame, containing all those four information. So for each inputs or questions, what was the answer or completion of the language model? What were retrieved context? And what is the ground truths? So again, let's take a quick look at what are the responses look like for the current chain on the current evaluation. So these are my questions. These are the answers from the rag chain. These were the retrieved context. So again, it is an array. I think we should expect two entries in every array. So this is entry number one and this entry number zero. And what the ground truths would be. So once we have these in a structured table, this is where you can apply the run your evaluation harness on it. And so for that, we are going to use MLflow and the MLflow evaluate API. Now the way the MLflow evaluate API works is you can create a bunch of, it will calculate a bunch of metrics out of the box and we'll list them. But if you can also bring in additional metrics, such as like answer similarity or the relevance that we talked about. And the way to create these metrics is via the metric.genai API. And then you're going to have a list of methods. Now these methods, again, they won't be calculated like they're not calculated automatically. You need to predefine them. Why? Because since we're going to use an LLM as a judge to assess the similarity of the answer and the relevance, you need to predefine those metrics yourself by telling it, okay, which model are you going to use as a judge? So here we are going to use our own Databricks DBRX model, DBRX instruct, which is available in our endpoints. And MLflow will automatically understand that because we told them that the set deployment target is Databricks. And when I just tell it endpoints with the model name, it will automatically know where the host URL is, what the model name is, and how to structure the prompt. You can also run these in open source world, but you're probably going to have to parameterize additional steps. So that's pretty much it. Again, what you need is let's say your evaluation data set as a Pandas data frame. You tell us at least the evaluate template. What are the ground truce colon? What is the prediction colon or completion? What are additional metrics that you want to calculate? And voila. So once you do that, it will create an experiment in the under the MLflow tracking server. So we'll be looking at that experiment in a couple of minutes. And let's just wait for a couple of seconds to see the outputs that are being generated by that eval framework. For every entry in your data set, it is going to append a bunch of scores. So answer similarity score with a potential justification given by the LLM and the relevant score, which are again the two metrics that we've asked the evaluate template to calculate. And again, now we're going to assume that we're happy with these results and things are at least in a good state to create a new version out of that model and push it to the registry. So this is what we are going to do here. So we're going to create a model, which will be called drag app demo four. And we're arguing to log the chain, that specific chain by feeding it the retriever and push it automatically to the model name and feeding it a specific question and an input example and an output. So once you do that, if I quickly go to my experiment tab, show you how things have happened. So here I'm in the MLflow tracking server. I have my two, I have the current experiment that I did, but I also have a previous one that I had cashed. And what you can do here, when we think about, let's say you want to, we were talking about using MLflow to evaluate or compare chains and runs and whatnot. What you can do automatically using the UI is compare different, all the different metrics of interest, maybe the variance, a couple of other things. But you can also, if I go back to my experiment, an interesting thing that you can do is, let's say, let's compare together our two models. For every one of the questions, I can compare, for example, the context. I can, so let's say I want to compare inputs and I want to compare and I want to look at answers. For example, I can compare, let's say the scores between specific chains or specific version of the chains. And for every one of the question, I can see what the answer is and I can compare the scores for each version of my chain. And I can also, if I want, I can also potentially manually create run with a new template. If I just remember how to do that. But yeah, let's, that's at least like showing the UI component of how experiments can be or different versions of your chain can be compared in terms of score. So going back, so let's just go to one run in particular. And so when we ran that MLflow evaluate call, it's automatically logging to the experiment all those specific metrics. So we can see them under the model metrics tab. So you can see for that specific run what all the metrics values are and pretty much it. And then the second run that we did, that's the one where we created that specific model. So if I go, so we logged the artifact and pushed it to the Unity catalog registry. So when I go here, I can see, so that's my model. I have version two, which has been created right now. I can also see the lineage of that chain. So when we talk about lineage, I can see that, okay, that chain is invoking that specific index and whatnot. So now that again, my model is, I've created this version. I can potentially tag it as, okay, my new champion version of the chain. Again, I do this via UI, but I can also do these things programmatically. And so I can trigger the LLM Ops chain of action.

---

## Timestamped Segments

**[00:00]** So let's illustrate how we can assemble a chain and evaluate it in the Databricks intelligence

**[00:05]** platform for in this demo, we'll, we'll assemble a full rack pipeline with the different with the

**[00:14]** retriever and the choice of the correct model to do the at least the generation piece, we'll

**[00:21]** evaluate that chain offline, and we'll push once the evaluation offline evaluation is done,

**[00:27]** we'll initiate, like we'll pull the trigger to push this model down the registry within with an

**[00:34]** alias, such as it can be pushed down for staging and or production. So let's jump back to the

**[00:41]** Databricks environment. So if you want to follow along, it's notebook number four,

**[00:47]** or demo number four, assembling and evaluating a rag application. So again, it's, we're still

**[00:56]** working on building the same application system rack system using the archive paper. But now we're

**[01:02]** focusing on the right side of things on building the chain, which will allow us to execute the

**[01:11]** full full inference. And another term, what are we going to try to assemble together? Whenever a

**[01:16]** query comes in, we want to make sure that this query will get turned into its into its into

**[01:22]** the correct embedding using the same embedding model, run a real time similarity search on the

**[01:28]** created vector search index. Once the documents are retrieved, we'll inject these in our prompt

**[01:34]** using a specific prompt template, and then send the whole augmented prompt for generation to a

**[01:42]** Databricks model serving foundation model endpoint, which is going to be llama two to

**[01:48]** get our generation back. So first thing first is to set up the retriever set up the retriever.

**[01:56]** So for the retriever, I just need to make sure that I have my endpoints up and running. So we

**[02:02]** will be I'll be using that specific shared endpoint that I've been using all along the

**[02:07]** demo. And here we will quick do we will do a quick let's say sanity check on the on the

**[02:16]** embedding model itself. So let me do a quick shift enter to make sure that the embedding model

**[02:24]** is up and running. So yes, I can see that. Okay, so I'm testing my embeddings on the question,

**[02:31]** which is what so what is generative AI and I can see that I have an embedding back now,

**[02:34]** building the retriever as part of the chain. Here we are going to use line chain as our as

**[02:41]** to build our chain. And so line chain, especially in the community package, has a lot of let's say,

**[02:47]** integration with any source of existing Databricks components. So the one of them

**[02:54]** being the Databricks embedding model, and the other one being the Databricks vector search

**[02:59]** client. And so whether in your if you're familiar with line chain, so that the wrapping,

**[03:07]** wrapping the retrieval in a under a method called get retriever is like the preferred way to do

**[03:15]** things. So this is what we will create here. Within that get retriever method, what are we

**[03:20]** going to do? We're just going to call as we did in a previous labs and demo, we're going

**[03:25]** to initiate a vector search client and ask it to retrieve our index given the endpoint name,

**[03:33]** and the index the index name again, the index name is just pretty sure is the one we created

**[03:38]** previously. So let me just print that very quickly. It's under my catalog. So you should

**[03:44]** see you will see that under your catalog schema. It's the PDF self managed vector search index

**[03:49]** embedding. So we point to the index. And here we will we are going to use the let's say the

**[03:56]** line chain integration with Databricks vector search. So we're going to create a vector

**[04:00]** store by telling it to point to the index telling it which text column do we want to retrieve,

**[04:05]** and which embedding model to use. And here again, the embedding model to use like the

**[04:10]** format is accepted is accepted for the line chain is going to be the Databricks embedding

**[04:15]** wrapper on top of the on top of our very own embedding model. So that's pretty much the

**[04:21]** steps identify your index, create a line chain Databricks vector storage vector store client

**[04:27]** with the parameters and apply the as retriever method to which you can pass in search arguments.

**[04:34]** So here are only going to tell it like retrieve the first top two chunks or documents. And that's

**[04:41]** it. So that's how you set up the method just to show how it works in real time. So you

**[04:46]** instantiate it using the get you instantiate the get retriever and then you just invoke it

**[04:51]** by feeding it a given query. And then the output what you will receive will just print that in a

**[04:58]** second, we will see that it's going to be the relevant documents which are here, which were

**[05:03]** retrieved previous which were retrieved given the question, how is generative AI impacting

**[05:08]** humans? So that's step one, you need to create your retriever because we're going to use

**[05:13]** line chain. So we're going to wrap this or structure it in the format, which is let's

**[05:20]** say line chain friendly using this get retriever wrapper methods. So once you created the

**[05:26]** retriever, the second step is to tell to the chain what foundation models or what LLM do we

**[05:32]** want to use for the generation piece. And in this example, we'll be using Lana 270B, which

**[05:38]** is again made available by the Databricks foundation models API. But again, you're not

**[05:44]** like limited to use a foundation model API again, as we said, you can definitely

**[05:49]** use any other model of choice, whether it's served as an API or running locally, there's no

**[05:56]** right or wrong here. But it is a very common practice to again have the generation happen

**[06:02]** using an API. So since we're using line chain, line chain in the community,

**[06:07]** they're going to have a wrapper, they're going to expose a wrapper class, which points

**[06:12]** to the Databricks model serving endpoint. So usually the way you instantiate that chat,

**[06:17]** you just tell it the endpoint name, the base URL. But here in our case, when you don't set

**[06:22]** the base URL, it will get the current host URL. So it will automatically get the URL

**[06:27]** of all the my current workspace model serving endpoint and potential other let's say

**[06:33]** completion or generation parameters such as the max token. So here if again, just to show,

**[06:40]** you know how this client works, it's nothing more than just a wrapper on top of our on top

**[06:45]** of the REST API. And it will give you back the results using a specific, let's say format

**[06:51]** where you have the content and any other response metadata, if you want to do some

**[06:57]** ad hoc calculations. So we created our retriever as a line chain class, we've created our

**[07:04]** LLM endpoint again, as a line chain wrapper on top of our Databricks chat foundationals

**[07:10]** endpoint. So now let's put them all together as part of a single chain. So how to do that?

**[07:16]** The first thing whenever you want to build any chain is to think about the system prompt. Okay,

**[07:23]** once I'm retriever, I've chosen my model, how am I gonna, let's say, give the instructions

**[07:29]** to my model. And for that, we are also going to use one of LLM chain's prompt template

**[07:35]** capabilities. Again, if you're not, if you're familiar with it, then it's great. If you're

**[07:39]** not, we'll give you a feel of how it is to use it, but won't spend too much time explaining

**[07:44]** the semantics. So usually the way it works is you define a template, you define like a template

**[07:50]** as a free string. So in which you are going to put the instructions, like we're telling here,

**[07:56]** the assistant that they're a GenAI teaching class or TA, and they need to answer a question

**[08:01]** on generative AI and how it can impact human's life. If the question is not related,

**[08:07]** and then add some additional, let's say, instructions, just like we did in the first lab.

**[08:12]** So we do want to make sure we don't want the model to try to answer any question outside of

**[08:17]** this topic. And if they don't know, we don't want them to hallucinate or try to come up

**[08:22]** with something creative and keep them as concise as possible. And here, this is where we're

**[08:27]** gonna add, let's say, that additional, let's say, structure or layout to instruct the

**[08:35]** language model to use the following pieces of context only. Put in between those specific signs.

**[08:43]** Now, the way these needs to be defined really depend on which model you're using.

**[08:49]** For LAMA, for doing RAG, that's like the expected template. So that meta has been

**[08:55]** recommended to do so. Put your system prompts at the beginning and then at the end, use the

**[08:59]** specific formalism to delimit what has been retrieved by your retriever. And now watch in

**[09:04]** between curly brackets is technically going to be a variable which will be dynamically,

**[09:11]** let's say, modified by when we're gonna use the prompt template class. And so the prompt,

**[09:17]** first thing we're gonna create again are prompt templates. So the way it works,

**[09:21]** you just feed it a template and you tell it what are the potential input variables as

**[09:26]** part of those templates. So you just need to make sure to use the same variable names.

**[09:29]** So context here that we're gonna inject and the question here. And once you create the

**[09:34]** prompt template, putting all the different chains together, you can use a Lang chain

**[09:40]** LCL, Lang chain executable language, or you could use some pre-baked chain, some like pre-baked

**[09:47]** standard chain. Here, because we're doing something pretty vanilla, which is a retrieval

**[09:50]** Q&A without, it was like, it's a single turn thing. There's no history. We're not,

**[09:55]** it's not like conversational. We are using the retrieval QA chain and the retrieval QA

**[10:01]** chain is expecting a chat model. So that chat model, again, is that wrapper class on top of the

**[10:09]** chat Databricks model. There are different types of chains. Stuff is a default one.

**[10:14]** If again, it's specific to any free text, tell it what is our retriever class. So again,

**[10:20]** our retriever, which is gonna use the Databricks or Mosaic I Vector Search and

**[10:26]** any other input arguments for the chain. And in that case, the prompt being our prompt template.

**[10:34]** So that's how, again, it's not the only way to build a chain, but let's say it's one of the

**[10:38]** most easiest way out of the box because it's a vanilla chain to use one of those pre-baked

**[10:44]** chain templates. And so that chain will manage every time a question come running the

**[10:49]** retriever, getting them back as context, injecting them in the prompt here, injecting

**[10:54]** the user question here and packaging all that and sending it to the language model for completion.

**[11:01]** And here the way, once your chain is created, the way it's true to use it is by using the

**[11:08]** invoke method. So here, for example, let's say I'm again asking that same old question on

**[11:13]** how is generative AI impacting our lives? I can see the response, but in my response as

**[11:19]** well, we can also see what sources have been retrieved as well as part of the retriever.

**[11:27]** And that's also is going to be important for us to back up the response of the LLM,

**[11:32]** but also if you want to do ad hoc evaluation of our chain, at least we have the retrieved

**[11:38]** context. So that's it. And if you want to take a quick look at what is that, what's the

**[11:44]** type of that chain object, it is a Lang chain retrieval QA type class. And again,

**[11:49]** why are we showcasing that is because in the final step here, as we get to it,

**[11:54]** we are going to log that chain as is to the MLflow registry because MLflow supports now a model

**[12:01]** which can have a Lang chain flavor. So now that we have the chain, the next step before

**[12:06]** even trying to say, okay, do I have something good? Let me just pull the trigger to get it

**[12:13]** through the LLM Ops pipeline. This is an example of how you can quickly evaluate the chain. Again,

**[12:20]** here we're doing this as part of a single notebook, but it can be done separately.

**[12:24]** So in that step, what we are going to create, I'll skim over it very quickly,

**[12:28]** but it's something you might, it is recommended to have beforehand or think about building it

**[12:33]** in parallel as the development is happening is creating an evaluation data set where

**[12:39]** as explained in the theory, in that evaluation data set, it is recommended to have a list of

**[12:46]** questions. So here we have 12 questions that again, we hard coded them here, but you can

**[12:50]** be pulling them from something else. Again, you can be pulling them from a spreadsheet or a

**[12:53]** table. What would a ground truth answer look like? And here, for example, okay, what type

**[12:59]** of inquiry is it? Is it like simple? Is it reasoning? Simple is usually some sort of like

**[13:04]** closed factual or closed question. That's it. Now we don't have, let's say ground truths

**[13:10]** for context or ground truths for retrieved. But at this point, I don't think we need that.

**[13:16]** Again, we have the question, we have the ground truths, and from the chain,

**[13:19]** we are going to get the completions and the context. And we have all four elements to run

**[13:25]** our evaluations. So once we have that eval, let's say list of Q&A, we're going to

**[13:31]** assemble them together in a hugging face data set. So first, we are going to batch each question

**[13:39]** to the chain, store the responses and put everything, you know, structure everything back

**[13:47]** into a pandas data frame. Again, we're using the hugging face data set to facilitate this,

**[13:55]** but you're not forced to use hugging face data sets. Ultimately, in order to run your evaluation,

**[14:02]** what the expected variable to have is a table, a pandas data frame or spark data frame,

**[14:09]** containing all those four information. So for each inputs or questions, what was the answer

**[14:15]** or completion of the language model? What were retrieved context? And what is the ground

**[14:21]** truths? So again, let's take a quick look at what are the responses look like for the current chain

**[14:28]** on the current evaluation. So these are my questions. These are the answers from the

**[14:33]** rag chain. These were the retrieved context. So again, it is an array. I think we should

**[14:38]** expect two entries in every array. So this is entry number one and this entry number zero.

**[14:45]** And what the ground truths would be. So once we have these in a structured table,

**[14:51]** this is where you can apply the run your evaluation harness on it. And so for that,

**[14:58]** we are going to use MLflow and the MLflow evaluate API. Now the way the MLflow evaluate

**[15:06]** API works is you can create a bunch of, it will calculate a bunch of metrics out of the box

**[15:12]** and we'll list them. But if you can also bring in additional metrics, such as like answer

**[15:18]** similarity or the relevance that we talked about. And the way to create these metrics is

**[15:23]** via the metric.genai API. And then you're going to have a list of methods. Now these methods,

**[15:31]** again, they won't be calculated like they're not calculated automatically. You need to

**[15:35]** predefine them. Why? Because since we're going to use an LLM as a judge to assess the

**[15:42]** similarity of the answer and the relevance, you need to predefine those metrics yourself by

**[15:48]** telling it, okay, which model are you going to use as a judge? So here we are going to use

**[15:52]** our own Databricks DBRX model, DBRX instruct, which is available in our endpoints. And MLflow

**[15:59]** will automatically understand that because we told them that the set deployment target is

**[16:03]** Databricks. And when I just tell it endpoints with the model name, it will automatically know

**[16:09]** where the host URL is, what the model name is, and how to structure the prompt.

**[16:15]** You can also run these in open source world, but you're probably going to have to

**[16:19]** parameterize additional steps. So that's pretty much it. Again, what you need is

**[16:27]** let's say your evaluation data set as a Pandas data frame. You tell us at least

**[16:33]** the evaluate template. What are the ground truce colon? What is the prediction

**[16:37]** colon or completion? What are additional metrics that you want to calculate? And

**[16:44]** voila. So once you do that, it will create an experiment in the under the MLflow tracking

**[16:51]** server. So we'll be looking at that experiment in a couple of minutes. And let's just wait

**[16:56]** for a couple of seconds to see the outputs that are being generated by that eval framework.

**[17:02]** For every entry in your data set, it is going to append a bunch of scores. So

**[17:09]** answer similarity score with a potential justification given by the LLM and the

**[17:14]** relevant score, which are again the two metrics that we've asked the evaluate template to

**[17:19]** calculate. And again, now we're going to assume that we're happy with these results

**[17:24]** and things are at least in a good state to create a new version out of that model

**[17:31]** and push it to the registry. So this is what we are going to do here. So we're going to create

**[17:36]** a model, which will be called drag app demo four. And we're arguing to log the chain,

**[17:43]** that specific chain by feeding it the retriever and push it automatically to the model name

**[17:49]** and feeding it a specific question and an input example and an output. So once you do that,

**[17:55]** if I quickly go to my experiment tab, show you how things have happened. So here I'm in the

**[18:02]** MLflow tracking server. I have my two, I have the current experiment that I did, but I also

**[18:08]** have a previous one that I had cashed. And what you can do here, when we think about,

**[18:13]** let's say you want to, we were talking about using MLflow to evaluate or compare chains

**[18:18]** and runs and whatnot. What you can do automatically using the UI is compare different,

**[18:23]** all the different metrics of interest, maybe the variance, a couple of other things.

**[18:28]** But you can also, if I go back to my experiment, an interesting thing that you can do is,

**[18:34]** let's say, let's compare together our two models. For every one of the questions,

**[18:41]** I can compare, for example, the context. I can, so let's say I want to compare inputs

**[18:46]** and I want to compare and I want to look at answers. For example, I can compare,

**[18:52]** let's say the scores between specific chains or specific version of the chains.

**[18:59]** And for every one of the question, I can see what the answer is and I can compare the scores

**[19:06]** for each version of my chain. And I can also, if I want, I can also potentially manually

**[19:14]** create run with a new template. If I just remember how to do that. But yeah, let's,

**[19:23]** that's at least like showing the UI component of how experiments can be

**[19:27]** or different versions of your chain can be compared in terms of score.

**[19:31]** So going back, so let's just go to one run in particular. And so when we ran that MLflow

**[19:38]** evaluate call, it's automatically logging to the experiment all those specific metrics. So

**[19:44]** we can see them under the model metrics tab. So you can see for that specific run

**[19:50]** what all the metrics values are and pretty much it. And then the second run that we did,

**[19:58]** that's the one where we created that specific model. So if I go,

**[20:02]** so we logged the artifact and pushed it to the Unity catalog registry. So when I go here,

**[20:08]** I can see, so that's my model. I have version two, which has been created right now.

**[20:13]** I can also see the lineage of that chain. So when we talk about lineage, I can see that,

**[20:18]** okay, that chain is invoking that specific index and whatnot. So now that again,

**[20:23]** my model is, I've created this version. I can potentially tag it as, okay, my new champion

**[20:30]** version of the chain. Again, I do this via UI, but I can also do these things

**[20:36]** programmatically. And so I can trigger the LLM Ops chain of action.

