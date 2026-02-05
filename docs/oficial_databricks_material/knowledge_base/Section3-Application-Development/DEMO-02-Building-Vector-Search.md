# Demo Building Vector S

**Source:** `2-Building Retrieval Agents On Databricks - Demo Building Vector S.mp4`
**Duration:** 22:15
**Language:** en (detected with 100.0% confidence)

---

## Full Transcription

Hello, and welcome to this demo. In this demo, we are going to talk about how to build vector search for Tribal. So, vector search is a crucial component of retrieval agents. In Greg architecture, as we talk about, vector search is important as we need to search for similarity of the user prompt to retrieve documents, retrieve additional information, and pass that to the final generation model so that we can generate and provide better answer. So, in this demo, we are going to show how to create a vector search index using vector search. Vector search is Databricks' vector storage solution. Then, we are going to talk about some advanced search methods, and finally, we are going to talk about re-ranking. So, by the end of this demo, you should be able to identify the steps for computing embeddings. You should be able to configure and create vector search index using both SDK and UI. Then, you should be able to implement and compare three search methods. The first one is classic, similarity search, then hybrid, and full-text search methods. Then, you should be able to improve search precision through re-ranking. And finally, you should be able to apply best practices for balancing cost, accuracy, and refreshing strategies. So, to run this lab, these are the requirements. First, you need to have a vector search and point created and ready for you. In the lab environment, this is already created for you. So, if we go to compute and go to vector search, you can see that we have one vector search and point is ready. And everybody in this lab environment is going to use this vector search and point. Because you don't have admin rights to create vector search and point. That's why we already created that for you. So, you don't need to do anything. It's just going to use that and point. Then, you need to have a serverless compute version 4 to run this lab. And also required libraries are added to dependencies in serverless compute configuration. You shouldn't need to do anything extra here. If you just select serverless, and it is going to set the right environment version and install dependencies. But, if you face with any problems, that's how you do that. You go to an environment section here in serverless. And this shall be version, environment version 4 is selected. And the vector search, data bricks, vector search SDK is added here, which is dependencies, a dependency for this notebook. And then you will click apply. But, as I said, you shouldn't need to do this. It's going to be done for you. Then, we are going to run the setup. So, the setup script is going to check some configurations here. It's going to say which vector search endpoint you should use. So, in your workspace, this vector search endpoint might be named differently, but you should just see the name here. And this is the one that you are going to use. So, let's get started. The first step is to prepare the source table. So, source table is where we have our play chunk text. For this table, to be able to sync it with vector search index, we need to enable change data feed. This is the most. If you don't have CDF change data feed in a mold, you are going to get an error. To do that, we are using this SQL command. We are saying outer table. And this is the source table. This docs table is defined in the classroom setup. So, if we go to classroom setup, you can see that this is the docs source table. So, it is catalog schema and docs chunked. So, in the previous demo, you should have created this while running the demos. So, when the CDF is enabled, you should be ready to go to the next step. This was our table. So, we had a pad, column, chunk, and ID. ID is also a must to have column because we have to define a primary key for our vector search index. And that is also needed. So, we have an ID. Then, let's go to computing embeddings. So, when we are using an embedding model to compute embeddings, Databricks provides GTE large model for embedding. So, you can use this model and you don't need any external models to use for embeddings. Of course, if you are using your own custom embedding models, if you have fine-tuned embedding models, then you can deploy it as using model serving and then define the endpoint here. This is not in the scope of this demo. So, in this demo, we are going to use an existing GTE model that is pre-deployed and ready for us. When computing embeddings, Databricks supports two methods. The first one is called manage embedding. So, manage embeddings means Databricks is computing embeddings for you. But you can also use manual embeddings. You can create your own embeddings and then store them in vector search. Manual embeddings is not in scope of this demo. So, we are going to use manage embeddings. So, let us see how actually this embedding model works. So, here we are defining, let's say, prompt. So, here it's defined as question. And then we are calling the predict function, predict function of this endpoint, Databricks GT, a large endpoint, and we are passing this input. And then the response is embeddings. Here are the embeddings. This is how embeddings looks like. So, how generative AI impacts humans is converted to these embeddings. Any text you are passing is going to be converted to this embedding. And this is the embedding size. So, embedding size is based, you can vary by the embedding model that you are using. But for this embedding model, this is the embedding size that we have. Here's a question that you can further think about it or investigate what this embedding size means, how this is going to change model behavior, which embedding size you are going to use. It is a good reflection question between about it and maybe do some research about it. So, to create a vector search index, we have two methods. We can use SDK or UI. So, here, in this demo, we have instructions for both, but I'm going to go with SDK. To do that, what I need to do is I just need to import vector search SDK. And I'm initializing the vector search client. This is how we define it. And then I need to define the index name. So, this is going to be the index name of vector search index. It has stored the unity catalog. So, you need to define catalog schema and then index name. Then we are using the vector search clients create delta sing index and way. And this are the parameters we need to pass. First, we need to pass the endpoint name. As in the beginning, we showed this vector search endpoint name endpoint is compute basically. So, the endpoint is created for you. You pass that index name is the name of the index is going to be created source table. Is the delta the source delta table that is going to be indexed to embeddings. Then you define primary key. You define source column source column is the column that is going to be used compete and embeddings. Whatever the column you are going to use for searching for doing similarity search on unity define this as source column. Then you are defining the model embedding model endpoint name and pipeline type. So, this is triggered. Trigger means that we are manually triggering when it is going to sing. But you can also define it to do that continuously. But of course, it's going to cost more computer resources. So, we don't want to do that. It depends on your use case. Whether you need to continuously update the embeddings or is it just like manually updating them is okay for you. When this is created, let's go and look how it looks like. So, here you are going to go to the catalog and go to your schema. So, this schema is going to be unique for your username. This is going to be different for you. But it should start with lab user. Then we go to the tables. So, this was our source table docs chunk. And this is our index table. You can see that this is a vector search index. And it has a little bit different icon. And let us open this in catalog explorer to see the details. So, you can see here we have an overview as sources is here defined here. Vector search endpoint is here. You can see the rows indexed and also different details here. You can see the embedding model. This are the columns. So, the columns are all columns from the source table because we selected all of them. But you can see that there is also a DB chunk vector. So, this is created for you. That's how embeddings are computed. If you look at the sample data, you can see here. And this is the new column that is created with the computed embeddings. We are not going to go into details of the rest. But it is basically a delta based table. So, you can align it. You can have permissions and all those kind of details. Let's go back here. As I said, you can create this vector search index using SDK or UI. So, there are instructions for UI method too. But I'm going to skip this one. Now that we created our vector search index, we can do similarity search on that. To do that, we have three main methods. The first one is using query search with similarity. And the second one is hybrid search and the third one is full text search. So, let's get started with the first one with the similarity search. With the similarity search, this is the query that we are passing. And we are using the indexes similarity search method. This is how we pass the query. We pass the columns that we want to return. And the number of results, how many results do we want to return? So, here you can see that based on this query. It is a query about overheating. So, these are the three documents that are retrieved. The three documents that are similar to this query. So, you can see that there are some details here. And that in generation time and also this are the documents. The next method is hybrid search. Hybrid search is using both similarity search plus keywords. So, this is important if you want to search based on certain keywords. So, let's say here we want as specific this ISO. And we want to make sure that it is bringing this making search. Based on this. So, it is not going to be just this one but also safety verification. This number and ISO is going to be used as a priority. So, it is going to first try to match those and then retrieve the rest of the documents. So, here let's see. You can see that probably this one. Yeah, see this result has ISO. And the safety, there are some keywords that are related to safety. And yeah, so here the second one, let's see what it has. Yeah, see this one has this standard number and also there are safety keywords. So, it contains more words that are matching that. In this one, yeah, we don't see that standard ISO number. But we can see that there are some words that are related to safety. So, this is how you search based on certain keywords. The third method is full text search. In the full text search, kind of put certain keywords that must match there. We have this one, this comment is skipped. The reason is that this method is still in beta. And it should be enabled by the workspace admin, so to be able to use that. So, it's not enabled in this workspace yet, but in your lab environment too. But if it's enabled, then you can search, for example, if you search for PID coefficients, it is going to bring results that the only results that have that matches this queue, right? So, next, let's talk about filtering. So, when you are doing similarity search, in most of the cases, you are also going to have other requirements that you want to filter search results by. If you look at this documentation page, you can see all filter operators that you can use. These are kind of like SQL operators, so you can use not or equality or numerical values. You can use bigger or smaller or like and so forth. So, let's say here we want to use for this again, overheating example here. But what we want to do is, by the way, this is what you are going to see in your demo, but you must change it to your own path. Otherwise, it's not going to return anything because it's not going to match. So, I have this one in the path column up here. If you go to your table, if you go to this table, chunk table, there's a path column and in the path column that is your path that you can filter by. Right, so here I'm using the same queries, but this time I'm using filters and I want path to be like this one. So, if let's say you want to search for certain documents, then you can filter by those documents only. Here I passed in this document only and you can see that results are changed. It's results are returned based only that document. Even though a number of results is defined tree, I only have two results, so that's why you see only two results here. What you can use is an example use case will be filtered by page number. So, you can say bring me the results between these pages or you can search by certain number of numeric value to filter by. Now, let's talk about tree ranking. So, if you look here, we are filtering by certain fields, but it doesn't mean that actually this result is contextually relevant to our query. It is similar to our query, so the similarity search meaning similarity, but it is not looking for the context. Right, so here I'm going to show an example here. So, in our first similarity search, we search for or even overheating prevention. Right, so you can see that the documents returned are quite actually related to this one, but this is more related to safety instruction than maybe battery management or vision model. Right, so I will assume that the vision model is not going to have like really safety instruction. And in the re-ranking, we are going to see that very clearly. So, to define the re-ranking, all we need to do is we just need to pass a re-ranker. And we are going to use data bricks vector search as re-ranker that is already shipped with data bricks vector search. And we are going to define the column to re-rank by. So, in this case, this is our query and we want the similarities results to be re-ranked based on the chunk. And in this result, you can see that actually this time, the safety and compliance sheet is getting up and higher because this document is more relevant, right, in contextually relevant to this query and the document order is changed. So, this is how you do re-ranking. And this one was the first result in the example that I show you in the beginning. And this was again like the second. So, you can see that the order is changed and now you can see the safety and compliance document is actually the first one because contextually this one overheating prevention system is more related to this one. So, that is how you do re-ranking. While using data bricks vector search, there are some best practices. You can check data bricks documentation here for the best practices, but let's quickly discuss some of those best practices that you keep in mind. First, you need to minimize embedding dimension one possible. Of course, there's a trade-off between dimension reduction and also the retrieval quality. So, if your test shows that a similar bigger dimension and smaller dimension model finding similar accuracy, then it is always better to prefer smaller embedding size. Why? Because it's going to decrease latency, it's going to be faster, it's going to be cheaper. Then, you need to define the number of results and use a smaller number as much as you can, right? So, if instead of using, for example, 5,000, you should use a smaller number so that it's returning the rest result and because of it's going to decrease the scanning time, the latest is going to be low. Using the right CQ for your compute is very important. Databricks vector search supports standard and storage optimized. So, there are two options that you can go for. You can check documentation for each of this and assess those based on your use case and see which one is better. Storage optimized is very cheap compared to standard one and the standard one has lower latency. So, that's important to keep in mind. Use filters as much as possible to narrow the retrieval scope. So, if you use filters, then it's going to decrease the scanning time and it should be faster. You should prefer the standard retrieval search over hybrid when you don't really need hybrid search, right? So, A and N stands for approximate nearest neighbor. So, this is a standard algorithm that is used by vector search or standard similarity search. So, it is faster and it has the highest query per second compared to hybrid search. But, of course, it depends on your use case. If you have to use certain keywords for critical search cases, then you can use the hybrid. But keep in mind that the standard search has highest query per second and it has lower latency. Right? So, that was it for this demo just to wrap up. In this demo, we showed how to prepare the source table for vector search. So, we enabled change data feed for the table. Then, we showed how you can use the SDK to create a vector search index. Then, we showed different search methods. These were standard similarity search, hybrid search, and the full text. Then, we talked about re-ranking, how re-ranking works, and how you can use re-ranking with database vector search. And finally, we talked about some best practices to keep in mind while using database vector search. That was it for this demo. I hope you enjoyed it and see you in next demo.

---

## Timestamped Segments

**[00:00]** Hello, and welcome to this demo. In this demo, we are going to talk about how to build vector search for Tribal.

**[00:06]** So, vector search is a crucial component of retrieval agents.

**[00:12]** In Greg architecture, as we talk about, vector search is important as we need to search for similarity of the user prompt to retrieve documents, retrieve additional information,

**[00:28]** and pass that to the final generation model so that we can generate and provide better answer.

**[00:37]** So, in this demo, we are going to show how to create a vector search index using vector search.

**[00:43]** Vector search is Databricks' vector storage solution.

**[00:48]** Then, we are going to talk about some advanced search methods, and finally, we are going to talk about re-ranking.

**[00:58]** So, by the end of this demo, you should be able to identify the steps for computing embeddings.

**[01:06]** You should be able to configure and create vector search index using both SDK and UI.

**[01:14]** Then, you should be able to implement and compare three search methods.

**[01:19]** The first one is classic, similarity search, then hybrid, and full-text search methods.

**[01:25]** Then, you should be able to improve search precision through re-ranking.

**[01:30]** And finally, you should be able to apply best practices for balancing cost, accuracy, and refreshing strategies.

**[01:41]** So, to run this lab, these are the requirements.

**[01:45]** First, you need to have a vector search and point created and ready for you.

**[01:51]** In the lab environment, this is already created for you.

**[01:55]** So, if we go to compute and go to vector search, you can see that we have one vector search and point is ready.

**[02:08]** And everybody in this lab environment is going to use this vector search and point.

**[02:13]** Because you don't have admin rights to create vector search and point.

**[02:18]** That's why we already created that for you.

**[02:20]** So, you don't need to do anything. It's just going to use that and point.

**[02:24]** Then, you need to have a serverless compute version 4 to run this lab.

**[02:29]** And also required libraries are added to dependencies in serverless compute configuration.

**[02:36]** You shouldn't need to do anything extra here.

**[02:39]** If you just select serverless, and it is going to set the right environment version and install dependencies.

**[02:46]** But, if you face with any problems, that's how you do that.

**[02:49]** You go to an environment section here in serverless.

**[02:52]** And this shall be version, environment version 4 is selected.

**[02:56]** And the vector search, data bricks, vector search SDK is added here, which is dependencies, a dependency for this notebook.

**[03:06]** And then you will click apply.

**[03:08]** But, as I said, you shouldn't need to do this. It's going to be done for you.

**[03:14]** Then, we are going to run the setup. So, the setup script is going to check some configurations here.

**[03:19]** It's going to say which vector search endpoint you should use.

**[03:24]** So, in your workspace, this vector search endpoint might be named differently, but you should just see the name here.

**[03:32]** And this is the one that you are going to use.

**[03:35]** So, let's get started.

**[03:36]** The first step is to prepare the source table.

**[03:40]** So, source table is where we have our play chunk text.

**[03:46]** For this table, to be able to sync it with vector search index, we need to enable change data feed.

**[03:53]** This is the most.

**[03:55]** If you don't have CDF change data feed in a mold, you are going to get an error.

**[04:02]** To do that, we are using this SQL command.

**[04:04]** We are saying outer table.

**[04:06]** And this is the source table.

**[04:09]** This docs table is defined in the classroom setup.

**[04:13]** So, if we go to classroom setup, you can see that this is the docs source table.

**[04:22]** So, it is catalog schema and docs chunked.

**[04:26]** So, in the previous demo, you should have created this while running the demos.

**[04:34]** So, when the CDF is enabled, you should be ready to go to the next step.

**[04:40]** This was our table.

**[04:43]** So, we had a pad, column, chunk, and ID.

**[04:48]** ID is also a must to have column because we have to define a primary key for our vector search index.

**[04:58]** And that is also needed.

**[05:00]** So, we have an ID.

**[05:03]** Then, let's go to computing embeddings.

**[05:07]** So, when we are using an embedding model to compute embeddings, Databricks provides GTE large model for embedding.

**[05:18]** So, you can use this model and you don't need any external models to use for embeddings.

**[05:24]** Of course, if you are using your own custom embedding models, if you have fine-tuned embedding models,

**[05:29]** then you can deploy it as using model serving and then define the endpoint here.

**[05:34]** This is not in the scope of this demo.

**[05:37]** So, in this demo, we are going to use an existing GTE model that is pre-deployed and ready for us.

**[05:43]** When computing embeddings, Databricks supports two methods.

**[05:47]** The first one is called manage embedding.

**[05:49]** So, manage embeddings means Databricks is computing embeddings for you.

**[05:55]** But you can also use manual embeddings.

**[05:57]** You can create your own embeddings and then store them in vector search.

**[06:02]** Manual embeddings is not in scope of this demo.

**[06:05]** So, we are going to use manage embeddings.

**[06:07]** So, let us see how actually this embedding model works.

**[06:11]** So, here we are defining, let's say, prompt.

**[06:15]** So, here it's defined as question.

**[06:17]** And then we are calling the predict function, predict function of this endpoint,

**[06:24]** Databricks GT, a large endpoint, and we are passing this input.

**[06:28]** And then the response is embeddings.

**[06:31]** Here are the embeddings.

**[06:33]** This is how embeddings looks like.

**[06:36]** So, how generative AI impacts humans is converted to these embeddings.

**[06:42]** Any text you are passing is going to be converted to this embedding.

**[06:48]** And this is the embedding size.

**[06:50]** So, embedding size is based, you can vary by the embedding model that you are using.

**[06:55]** But for this embedding model, this is the embedding size that we have.

**[06:58]** Here's a question that you can further think about it or investigate what this embedding size means,

**[07:05]** how this is going to change model behavior, which embedding size you are going to use.

**[07:11]** It is a good reflection question between about it and maybe do some research about it.

**[07:16]** So, to create a vector search index, we have two methods.

**[07:23]** We can use SDK or UI.

**[07:25]** So, here, in this demo, we have instructions for both, but I'm going to go with SDK.

**[07:31]** To do that, what I need to do is I just need to import vector search SDK.

**[07:37]** And I'm initializing the vector search client.

**[07:41]** This is how we define it.

**[07:43]** And then I need to define the index name.

**[07:45]** So, this is going to be the index name of vector search index.

**[07:50]** It has stored the unity catalog.

**[07:52]** So, you need to define catalog schema and then index name.

**[07:56]** Then we are using the vector search clients create delta sing index and way.

**[08:02]** And this are the parameters we need to pass.

**[08:06]** First, we need to pass the endpoint name.

**[08:08]** As in the beginning, we showed this vector search endpoint name endpoint is compute basically.

**[08:15]** So, the endpoint is created for you.

**[08:18]** You pass that index name is the name of the index is going to be created source table.

**[08:23]** Is the delta the source delta table that is going to be indexed to embeddings.

**[08:30]** Then you define primary key.

**[08:32]** You define source column source column is the column that is going to be used compete and embeddings.

**[08:39]** Whatever the column you are going to use for searching for doing similarity search on unity define this as source column.

**[08:49]** Then you are defining the model embedding model endpoint name and pipeline type.

**[08:55]** So, this is triggered.

**[08:57]** Trigger means that we are manually triggering when it is going to sing.

**[09:02]** But you can also define it to do that continuously.

**[09:06]** But of course, it's going to cost more computer resources.

**[09:09]** So, we don't want to do that.

**[09:10]** It depends on your use case.

**[09:12]** Whether you need to continuously update the embeddings or is it just like manually updating them is okay for you.

**[09:21]** When this is created, let's go and look how it looks like.

**[09:26]** So, here you are going to go to the catalog and go to your schema.

**[09:30]** So, this schema is going to be unique for your username.

**[09:34]** This is going to be different for you.

**[09:35]** But it should start with lab user.

**[09:38]** Then we go to the tables.

**[09:40]** So, this was our source table docs chunk.

**[09:44]** And this is our index table.

**[09:47]** You can see that this is a vector search index.

**[09:50]** And it has a little bit different icon.

**[09:53]** And let us open this in catalog explorer to see the details.

**[10:01]** So, you can see here we have an overview as sources is here defined here.

**[10:06]** Vector search endpoint is here.

**[10:09]** You can see the rows indexed and also different details here.

**[10:13]** You can see the embedding model.

**[10:15]** This are the columns.

**[10:16]** So, the columns are all columns from the source table because we selected all of them.

**[10:21]** But you can see that there is also a DB chunk vector.

**[10:25]** So, this is created for you.

**[10:27]** That's how embeddings are computed.

**[10:30]** If you look at the sample data, you can see here.

**[10:34]** And this is the new column that is created with the computed embeddings.

**[10:39]** We are not going to go into details of the rest.

**[10:43]** But it is basically a delta based table.

**[10:47]** So, you can align it.

**[10:49]** You can have permissions and all those kind of details.

**[10:53]** Let's go back here.

**[10:55]** As I said, you can create this vector search index using SDK or UI.

**[11:01]** So, there are instructions for UI method too.

**[11:04]** But I'm going to skip this one.

**[11:06]** Now that we created our vector search index, we can do similarity search on that.

**[11:12]** To do that, we have three main methods.

**[11:15]** The first one is using query search with similarity.

**[11:19]** And the second one is hybrid search and the third one is full text search.

**[11:24]** So, let's get started with the first one with the similarity search.

**[11:29]** With the similarity search, this is the query that we are passing.

**[11:32]** And we are using the indexes similarity search method.

**[11:35]** This is how we pass the query.

**[11:37]** We pass the columns that we want to return.

**[11:40]** And the number of results, how many results do we want to return?

**[11:46]** So, here you can see that based on this query.

**[11:50]** It is a query about overheating.

**[11:53]** So, these are the three documents that are retrieved.

**[11:57]** The three documents that are similar to this query.

**[12:00]** So, you can see that there are some details here.

**[12:06]** And that in generation time and also this are the documents.

**[12:10]** The next method is hybrid search.

**[12:13]** Hybrid search is using both similarity search plus keywords.

**[12:18]** So, this is important if you want to search based on certain keywords.

**[12:25]** So, let's say here we want as specific this ISO.

**[12:29]** And we want to make sure that it is bringing this making search.

**[12:35]** Based on this.

**[12:36]** So, it is not going to be just this one but also safety verification.

**[12:41]** This number and ISO is going to be used as a priority.

**[12:47]** So, it is going to first try to match those and then retrieve the rest of the documents.

**[12:52]** So, here let's see.

**[12:54]** You can see that probably this one.

**[12:58]** Yeah, see this result has ISO.

**[13:01]** And the safety, there are some keywords that are related to safety.

**[13:08]** And yeah, so here the second one, let's see what it has.

**[13:13]** Yeah, see this one has this standard number and also there are safety keywords.

**[13:19]** So, it contains more words that are matching that.

**[13:23]** In this one, yeah, we don't see that standard ISO number.

**[13:30]** But we can see that there are some words that are related to safety.

**[13:34]** So, this is how you search based on certain keywords.

**[13:39]** The third method is full text search.

**[13:42]** In the full text search, kind of put certain keywords that must match there.

**[13:48]** We have this one, this comment is skipped.

**[13:51]** The reason is that this method is still in beta.

**[13:55]** And it should be enabled by the workspace admin, so to be able to use that.

**[14:02]** So, it's not enabled in this workspace yet, but in your lab environment too.

**[14:07]** But if it's enabled, then you can search, for example, if you search for PID coefficients,

**[14:14]** it is going to bring results that the only results that have that matches this queue, right?

**[14:24]** So, next, let's talk about filtering.

**[14:28]** So, when you are doing similarity search, in most of the cases,

**[14:32]** you are also going to have other requirements that you want to filter search results by.

**[14:40]** If you look at this documentation page, you can see all filter operators that you can use.

**[14:47]** These are kind of like SQL operators, so you can use not or equality or numerical values.

**[14:54]** You can use bigger or smaller or like and so forth.

**[14:59]** So, let's say here we want to use for this again, overheating example here.

**[15:06]** But what we want to do is, by the way, this is what you are going to see in your demo,

**[15:11]** but you must change it to your own path.

**[15:15]** Otherwise, it's not going to return anything because it's not going to match.

**[15:20]** So, I have this one in the path column up here.

**[15:24]** If you go to your table, if you go to this table, chunk table, there's a path column

**[15:32]** and in the path column that is your path that you can filter by.

**[15:37]** Right, so here I'm using the same queries, but this time I'm using filters

**[15:43]** and I want path to be like this one.

**[15:46]** So, if let's say you want to search for certain documents, then you can filter by those documents only.

**[15:54]** Here I passed in this document only and you can see that results are changed.

**[15:59]** It's results are returned based only that document.

**[16:03]** Even though a number of results is defined tree, I only have two results, so that's why you see only two results here.

**[16:10]** What you can use is an example use case will be filtered by page number.

**[16:16]** So, you can say bring me the results between these pages or you can search by certain number

**[16:24]** of numeric value to filter by.

**[16:28]** Now, let's talk about tree ranking.

**[16:30]** So, if you look here, we are filtering by certain fields, but it doesn't mean that

**[16:37]** actually this result is contextually relevant to our query.

**[16:44]** It is similar to our query, so the similarity search meaning similarity, but it is not looking for the context.

**[16:52]** Right, so here I'm going to show an example here.

**[16:57]** So, in our first similarity search, we search for or even overheating prevention.

**[17:03]** Right, so you can see that the documents returned are quite actually related to this one, but this is more related to safety instruction than maybe battery management or vision model.

**[17:18]** Right, so I will assume that the vision model is not going to have like really safety instruction.

**[17:26]** And in the re-ranking, we are going to see that very clearly.

**[17:30]** So, to define the re-ranking, all we need to do is we just need to pass a re-ranker.

**[17:36]** And we are going to use data bricks vector search as re-ranker that is already shipped with data bricks vector search.

**[17:44]** And we are going to define the column to re-rank by.

**[17:47]** So, in this case, this is our query and we want the similarities results to be re-ranked based on the chunk.

**[17:55]** And in this result, you can see that actually this time, the safety and compliance sheet is getting up and higher because this document is more relevant, right, in contextually relevant to this query and the document order is changed.

**[18:19]** So, this is how you do re-ranking.

**[18:21]** And this one was the first result in the example that I show you in the beginning.

**[18:27]** And this was again like the second.

**[18:30]** So, you can see that the order is changed and now you can see the safety and compliance document is actually the first one because contextually this one overheating prevention system is more related to this one.

**[18:47]** So, that is how you do re-ranking.

**[18:51]** While using data bricks vector search, there are some best practices.

**[18:55]** You can check data bricks documentation here for the best practices, but let's quickly discuss some of those best practices that you keep in mind.

**[19:04]** First, you need to minimize embedding dimension one possible.

**[19:08]** Of course, there's a trade-off between dimension reduction and also the retrieval quality.

**[19:14]** So, if your test shows that a similar bigger dimension and smaller dimension model finding similar accuracy, then it is always better to prefer smaller embedding size.

**[19:29]** Why? Because it's going to decrease latency, it's going to be faster, it's going to be cheaper.

**[19:34]** Then, you need to define the number of results and use a smaller number as much as you can, right?

**[19:41]** So, if instead of using, for example, 5,000, you should use a smaller number so that it's returning the rest result and because of it's going to decrease the scanning time, the latest is going to be low.

**[19:56]** Using the right CQ for your compute is very important.

**[20:01]** Databricks vector search supports standard and storage optimized.

**[20:06]** So, there are two options that you can go for.

**[20:09]** You can check documentation for each of this and assess those based on your use case and see which one is better.

**[20:17]** Storage optimized is very cheap compared to standard one and the standard one has lower latency.

**[20:24]** So, that's important to keep in mind.

**[20:27]** Use filters as much as possible to narrow the retrieval scope.

**[20:32]** So, if you use filters, then it's going to decrease the scanning time and it should be faster.

**[20:39]** You should prefer the standard retrieval search over hybrid when you don't really need hybrid search, right?

**[20:48]** So, A and N stands for approximate nearest neighbor.

**[20:53]** So, this is a standard algorithm that is used by vector search or standard similarity search.

**[21:01]** So, it is faster and it has the highest query per second compared to hybrid search.

**[21:08]** But, of course, it depends on your use case.

**[21:11]** If you have to use certain keywords for critical search cases, then you can use the hybrid.

**[21:19]** But keep in mind that the standard search has highest query per second and it has lower latency.

**[21:26]** Right? So, that was it for this demo just to wrap up.

**[21:31]** In this demo, we showed how to prepare the source table for vector search.

**[21:36]** So, we enabled change data feed for the table.

**[21:39]** Then, we showed how you can use the SDK to create a vector search index.

**[21:44]** Then, we showed different search methods.

**[21:46]** These were standard similarity search, hybrid search, and the full text.

**[21:51]** Then, we talked about re-ranking, how re-ranking works, and how you can use re-ranking with database vector search.

**[21:58]** And finally, we talked about some best practices to keep in mind while using database vector search.

**[22:06]** That was it for this demo.

**[22:08]** I hope you enjoyed it and see you in next demo.

