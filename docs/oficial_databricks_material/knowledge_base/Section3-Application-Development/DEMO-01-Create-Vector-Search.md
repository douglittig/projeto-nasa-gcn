# Demo Create Vector Search I

**Source:** `Generative AI Solution Development - Demo Create Vector Search I.mp4`
**Duration:** 11:12
**Language:** en (detected with 100.0% confidence)

---

## Full Transcription

So in this demo, we'll just given an existing table, the one that we created in the previous lab or demo, we'll first set up a vector search endpoint, take a look at how it looks like in the UI and create an index out of the preexisting Delta table containing the chunks of PDFs and do a quick similarity search on the index and also try or give you a feel of how you can implement your own reranker on the search result. So let's jump back to the Databricks environment to notebook number three, create self-managed vector search index. So our starting point is going to be our pre-created Delta table containing the chunks and the pre-computed embeddings. So the first step here, what we are going to create is what we call a self-managed vector search index. So another term, we are providing a source Delta table that contains all the text data, but the pre-calculated embeddings. So we'll first create a vector search endpoint on top of which is going to be the compute infrastructure in which we're going to deploy the vector search index. So creating a vector search endpoint can be done via the UI. This is what we'll showcase in a couple of seconds, but can also be done using the data, using the REST API or the Databricks SDK. We won't be showcasing the SDK API as part of that course to create the vector search endpoint, but just to quickly give you a feel of how it's relatively easy to do that. So on the left side, if you go to the compute tab, under the vector search tab, you will be able to create an endpoint for yourself. You just give it a name. You can only choose the standard type right now, and then you confirm it will spin up that endpoint. So here I have a couple of shared endpoints. I'll be using endpoint number seven over here, which has no indexes deployed up until this point. So how can I deploy an index to here, to that endpoint? So the first option, as we said, is to do this via UI. So if I navigate to my source Delta table here, containing my chunked documents, the content and text and the associated embeddings, I'll have the ability via the create button to quickly create a vector search index. So I'll first need to give it a name. Again, you can respect any convention of choice. Let's say the default way we would recommend to do this is to provide the same table name and an additional suffix for underscore VS index. And then picking a primary key to ensure like uniqueness of results and pick to which endpoint we wanna deploy or expose that index. Here, you can see we have two options. So either compute embeddings. And if I am going to do that, I just need to tell it which column contain the embeddings and which embedding, which like Databricks model serving endpoint do I wanna use? So obviously you need to make sure to point to one, which where an embeddings model is served. So like that one, which is a foundation models API. Or again, if you created an endpoint pointing to an external open AI embedding, you should see it in the list here. Or again, if you fine tune your own embedding model and deploy it to again, your custom endpoint, you should be able to see it here as well. Now, in our case, we already have the embedding column here and we'll tell it that it's the embedding columns and specify the dimension. Also here in our case, BGE is giving out 4096 dimensions and that's it. Now for the sync mode, you have two options. So triggered means that you set the batch schedule to update the index and continuous will just manage this in the backend for you. So if there's any update happening to the source table, it will automatically push them. Either if it's a pens, it will just add the new entries to the index. If it's a merge or an update or an override, it will recalculate, potentially recalculate the whole index. So once we do that and you hit on the create button, you'll be able to watch the index getting created live. So as the index is being created, let's jump back into the notebook where we left off. Also showcase the REST API on how to create an index using the REST API. So for that you will need from the Databricks Python package or module to import the vector search client. Yeah, class, instantiate a client with that specific handle, doing a quick chain of T check that my endpoint is ready. And that's how I can do it programmatically. So point to my source table name. So always using the three level name space. So the catalog, the schema and my table name, and giving it what we want the index name to be. Again, it is just a data asset on the Unity catalog. So it will respect the three level name spacing convention right here. So here, obviously the names that I give to the existing embedding is different. So it's probably gonna create another one, but that's totally fine. We provided also a bunch of helper methods to ensure if an index already exists at a given endpoint. If it does not, technically the API exposed here that we are going to use is the create delta sync index. So what would this index, what would this method accept? So it accepts an endpoint name, the index name, what is my source table, how the pipeline type will be triggered. So when we say trigger, again, it means that you will manually have to do a refresh of the index. So you can do this via the UI, you can trigger it via API, but ultimately it will just check the source delta table, look at the change data feed log. If there were any changes, apply these to the index by either just the pending or full calculation of the index. And that's it. So once the index gets updated, we'll give it a couple of time. This is where we can run the search to similar context. And in order to run a query on an index, well, given that it is self-managed embedding, so the first step that we need to do is to calculate the embeddings for our query. So this is what we are going to do here. Now, again, we're gonna use the same embedding models, Databricks, VGE, large and provided with the query and calculate the embeddings. So while this is getting calculated, we can very quickly jump back to the catalog and take a peek if our index is now ready for use. So here I can see that it has been created, but it's still updating. Here I can see my sync now button. Again, if you wanna manually trigger some runs, I have a link to my source table and a link to the endpoint where that index is served. So that's gonna take a couple of minutes to spin it up while things get spun up. I can always potentially in your environment, if you don't wanna wait for the endpoint to spun up, there will probably be in the lab environment a shared index that you could already use. But all that to say, once let's say the index is ready and deployed to that specific search endpoint, what we are going to do is again, for a given query, calculate the embeddings and run a similarity search. So how does the similarity search work? Again, using that same vector store client, it exposes a get index method. How does this get index method works? You provide it with again, an endpoint name, an index name. So index name again is gonna be the index created out of the source Delta table. And once the index is out, it will expose a method called similarity search. And that similarity search accepts a query vector. Which column do I wanna retrieve out of the index? So here, ultimately you wanna retrieve the source, so the PDF name. And we wanna retrieve the content of the chunk, which is stored under the content column. And you can also limit how many results you want back from the similarity search. And so once this search is achieved, we can iterate through it because here we told it that, okay, number of results needs to be five. So we're gonna iterate through the five different results to see exactly what passages have been retrieved by the algorithm. And so now that the embedding is calculated, let's do a quick similarity search and see what outputs are retrieved. So here my question was, what was the question? Let me just check how generative AI impacts human. This is the embeddings. After we ran the similarity search, it's providing, let's take a quick peek at like the first article retrieved and the text is saying, this finding by LMPR so it will have some effect on scale economic impacts of underlying model LM such as a trade turn of purpose and again, they could have some of the economy. So yes, we can see that based on this result that it is relevant to a certain extent to the user's question. Now, how can we re-rank the results? Again, this is by no means the only way or the Databricks recommended way to do re-ranking. A flash rank is one of those state-of-the-art re-ranking library using cross encoders. So we'll use the rank T5 model, for example, here. The way it works is, again, as you can see relatively easy, you instantiate a re-ranker and you just need to feed it what question was originally provided and what were the list of passages or chunks retrieved by a retriever. And you can very easily tell it, okay, can you try to re-rank these and show potentially put on top what relevant documents might come out. So when you're gonna run this the first time, it is gonna download locally the rank T5 flan model but once things have been done and the results, I can see that, for example, the new scores for my newly, let's say, re-ranked documents. And yeah, that kind of concludes the demo on vector search, mosaic vector search and re-ranking.

---

## Timestamped Segments

**[00:00]** So in this demo, we'll just given an existing table,

**[00:04]** the one that we created in the previous lab or demo,

**[00:07]** we'll first set up a vector search endpoint,

**[00:10]** take a look at how it looks like in the UI

**[00:12]** and create an index out of the preexisting Delta table

**[00:17]** containing the chunks of PDFs

**[00:19]** and do a quick similarity search on the index

**[00:23]** and also try or give you a feel

**[00:26]** of how you can implement your own reranker

**[00:28]** on the search result.

**[00:30]** So let's jump back to the Databricks environment

**[00:32]** to notebook number three,

**[00:34]** create self-managed vector search index.

**[00:38]** So our starting point is going to be our pre-created Delta

**[00:42]** table containing the chunks and the pre-computed embeddings.

**[00:47]** So the first step here,

**[00:48]** what we are going to create is what we call

**[00:50]** a self-managed vector search index.

**[00:53]** So another term,

**[00:53]** we are providing a source Delta table

**[00:55]** that contains all the text data,

**[00:59]** but the pre-calculated embeddings.

**[01:01]** So we'll first create a vector search endpoint

**[01:04]** on top of which is going to be the compute infrastructure

**[01:07]** in which we're going to deploy the vector search index.

**[01:11]** So creating a vector search endpoint

**[01:14]** can be done via the UI.

**[01:15]** This is what we'll showcase in a couple of seconds,

**[01:17]** but can also be done using the data,

**[01:20]** using the REST API or the Databricks SDK.

**[01:23]** We won't be showcasing the SDK API

**[01:25]** as part of that course

**[01:27]** to create the vector search endpoint,

**[01:29]** but just to quickly give you a feel

**[01:31]** of how it's relatively easy to do that.

**[01:34]** So on the left side, if you go to the compute tab,

**[01:37]** under the vector search tab,

**[01:39]** you will be able to create an endpoint for yourself.

**[01:43]** You just give it a name.

**[01:45]** You can only choose the standard type right now,

**[01:48]** and then you confirm it will spin up that endpoint.

**[01:51]** So here I have a couple of shared endpoints.

**[01:54]** I'll be using endpoint number seven over here,

**[01:57]** which has no indexes deployed up until this point.

**[02:01]** So how can I deploy an index to here, to that endpoint?

**[02:05]** So the first option, as we said, is to do this via UI.

**[02:11]** So if I navigate to my source Delta table here,

**[02:15]** containing my chunked documents,

**[02:19]** the content and text and the associated embeddings,

**[02:24]** I'll have the ability via the create button

**[02:28]** to quickly create a vector search index.

**[02:31]** So I'll first need to give it a name.

**[02:34]** Again, you can respect any convention of choice.

**[02:38]** Let's say the default way we would recommend to do this

**[02:42]** is to provide the same table name

**[02:44]** and an additional suffix for underscore VS index.

**[02:48]** And then picking a primary key

**[02:50]** to ensure like uniqueness of results

**[02:53]** and pick to which endpoint we wanna deploy

**[02:57]** or expose that index.

**[02:59]** Here, you can see we have two options.

**[03:01]** So either compute embeddings.

**[03:02]** And if I am going to do that,

**[03:03]** I just need to tell it which column

**[03:05]** contain the embeddings and which embedding,

**[03:08]** which like Databricks model serving endpoint

**[03:10]** do I wanna use?

**[03:12]** So obviously you need to make sure to point to one,

**[03:16]** which where an embeddings model is served.

**[03:19]** So like that one, which is a foundation models API.

**[03:23]** Or again, if you created an endpoint

**[03:24]** pointing to an external open AI embedding,

**[03:26]** you should see it in the list here.

**[03:28]** Or again, if you fine tune your own embedding model

**[03:31]** and deploy it to again, your custom endpoint,

**[03:33]** you should be able to see it here as well.

**[03:36]** Now, in our case,

**[03:36]** we already have the embedding column here

**[03:38]** and we'll tell it that it's the embedding columns

**[03:41]** and specify the dimension.

**[03:43]** Also here in our case,

**[03:44]** BGE is giving out 4096 dimensions and that's it.

**[03:49]** Now for the sync mode, you have two options.

**[03:52]** So triggered means that you set the batch schedule

**[03:56]** to update the index and continuous

**[03:59]** will just manage this in the backend for you.

**[04:01]** So if there's any update happening to the source table,

**[04:05]** it will automatically push them.

**[04:07]** Either if it's a pens,

**[04:08]** it will just add the new entries to the index.

**[04:11]** If it's a merge or an update or an override,

**[04:13]** it will recalculate,

**[04:15]** potentially recalculate the whole index.

**[04:17]** So once we do that and you hit on the create button,

**[04:21]** you'll be able to watch the index getting created live.

**[04:25]** So as the index is being created,

**[04:28]** let's jump back into the notebook where we left off.

**[04:33]** Also showcase the REST API

**[04:37]** on how to create an index using the REST API.

**[04:40]** So for that you will need from the Databricks Python package

**[04:45]** or module to import the vector search client.

**[04:49]** Yeah, class, instantiate a client

**[04:53]** with that specific handle,

**[04:55]** doing a quick chain of T check

**[04:56]** that my endpoint is ready.

**[04:59]** And that's how I can do it programmatically.

**[05:01]** So point to my source table name.

**[05:04]** So always using the three level name space.

**[05:07]** So the catalog, the schema and my table name,

**[05:09]** and giving it what we want the index name to be.

**[05:14]** Again, it is just a data asset on the Unity catalog.

**[05:17]** So it will respect the three level name spacing convention

**[05:20]** right here.

**[05:21]** So here, obviously the names that I give

**[05:23]** to the existing embedding is different.

**[05:25]** So it's probably gonna create another one,

**[05:26]** but that's totally fine.

**[05:28]** We provided also a bunch of helper methods

**[05:31]** to ensure if an index already exists

**[05:35]** at a given endpoint.

**[05:36]** If it does not, technically the API exposed here

**[05:40]** that we are going to use is the create delta sync index.

**[05:44]** So what would this index,

**[05:45]** what would this method accept?

**[05:47]** So it accepts an endpoint name, the index name,

**[05:51]** what is my source table,

**[05:52]** how the pipeline type will be triggered.

**[05:54]** So when we say trigger, again,

**[05:56]** it means that you will manually have

**[05:59]** to do a refresh of the index.

**[06:01]** So you can do this via the UI,

**[06:03]** you can trigger it via API,

**[06:05]** but ultimately it will just check the source delta table,

**[06:09]** look at the change data feed log.

**[06:11]** If there were any changes,

**[06:13]** apply these to the index by either just the pending

**[06:16]** or full calculation of the index.

**[06:18]** And that's it.

**[06:19]** So once the index gets updated,

**[06:22]** we'll give it a couple of time.

**[06:24]** This is where we can run the search to similar context.

**[06:27]** And in order to run a query on an index,

**[06:31]** well, given that it is self-managed embedding,

**[06:34]** so the first step that we need to do is

**[06:37]** to calculate the embeddings for our query.

**[06:40]** So this is what we are going to do here.

**[06:42]** Now, again, we're gonna use the same embedding models,

**[06:45]** Databricks, VGE, large and provided with the query

**[06:50]** and calculate the embeddings.

**[06:52]** So while this is getting calculated,

**[06:54]** we can very quickly jump back to the catalog

**[07:01]** and take a peek if our index is now ready for use.

**[07:07]** So here I can see that it has been created,

**[07:11]** but it's still updating.

**[07:15]** Here I can see my sync now button.

**[07:17]** Again, if you wanna manually trigger some runs,

**[07:20]** I have a link to my source table

**[07:24]** and a link to the endpoint where that index is served.

**[07:28]** So that's gonna take a couple of minutes to spin it up

**[07:30]** while things get spun up.

**[07:33]** I can always potentially in your environment,

**[07:36]** if you don't wanna wait for the endpoint to spun up,

**[07:40]** there will probably be in the lab environment

**[07:42]** a shared index that you could already use.

**[07:46]** But all that to say,

**[07:48]** once let's say the index is ready

**[07:50]** and deployed to that specific search endpoint,

**[07:55]** what we are going to do is again,

**[07:58]** for a given query, calculate the embeddings

**[08:00]** and run a similarity search.

**[08:02]** So how does the similarity search work?

**[08:05]** Again, using that same vector store client,

**[08:08]** it exposes a get index method.

**[08:10]** How does this get index method works?

**[08:13]** You provide it with again, an endpoint name,

**[08:16]** an index name.

**[08:18]** So index name again is gonna be the index created

**[08:21]** out of the source Delta table.

**[08:23]** And once the index is out,

**[08:26]** it will expose a method called similarity search.

**[08:30]** And that similarity search accepts a query vector.

**[08:34]** Which column do I wanna retrieve out of the index?

**[08:37]** So here, ultimately you wanna retrieve the source,

**[08:40]** so the PDF name.

**[08:41]** And we wanna retrieve the content of the chunk,

**[08:45]** which is stored under the content column.

**[08:48]** And you can also limit how many results you want back

**[08:53]** from the similarity search.

**[08:55]** And so once this search is achieved,

**[09:00]** we can iterate through it because here we told it that,

**[09:03]** okay, number of results needs to be five.

**[09:05]** So we're gonna iterate through the five different results

**[09:09]** to see exactly what passages have been retrieved

**[09:13]** by the algorithm.

**[09:17]** And so now that the embedding is calculated,

**[09:20]** let's do a quick similarity search

**[09:24]** and see what outputs are retrieved.

**[09:27]** So here my question was, what was the question?

**[09:29]** Let me just check how generative AI impacts human.

**[09:33]** This is the embeddings.

**[09:35]** After we ran the similarity search,

**[09:37]** it's providing, let's take a quick peek

**[09:39]** at like the first article retrieved

**[09:41]** and the text is saying, this finding by LMPR

**[09:43]** so it will have some effect on scale economic impacts

**[09:46]** of underlying model LM such as a trade turn of purpose

**[09:49]** and again, they could have some of the economy.

**[09:51]** So yes, we can see that based on this result

**[09:53]** that it is relevant to a certain extent

**[09:57]** to the user's question.

**[09:59]** Now, how can we re-rank the results?

**[10:01]** Again, this is by no means the only way

**[10:03]** or the Databricks recommended way to do re-ranking.

**[10:06]** A flash rank is one of those state-of-the-art

**[10:09]** re-ranking library using cross encoders.

**[10:12]** So we'll use the rank T5 model, for example, here.

**[10:15]** The way it works is, again,

**[10:17]** as you can see relatively easy,

**[10:19]** you instantiate a re-ranker

**[10:21]** and you just need to feed it

**[10:22]** what question was originally provided

**[10:25]** and what were the list of passages

**[10:28]** or chunks retrieved by a retriever.

**[10:31]** And you can very easily tell it,

**[10:33]** okay, can you try to re-rank these

**[10:36]** and show potentially put on top

**[10:39]** what relevant documents might come out.

**[10:41]** So when you're gonna run this the first time,

**[10:42]** it is gonna download locally the rank T5 flan model

**[10:46]** but once things have been done and the results,

**[10:50]** I can see that, for example,

**[10:52]** the new scores for my newly, let's say,

**[10:56]** re-ranked documents.

**[10:59]** And yeah, that kind of concludes the demo

**[11:03]** on vector search, mosaic vector search and re-ranking.

