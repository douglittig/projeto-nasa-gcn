# Demo Clean transform a

**Source:** `3-Building Retrieval Agents On Databricks - Demo Clean transform a.mp4`
**Duration:** 13:09
**Language:** en (detected with 100.0% confidence)

---

## Full Transcription

Hello. In this demo, we are going to talk about how to clean, transform, and then chunk the parse text. In the previous demo, we showed how to use AI parse document function to parse documents into JSON format. And now we are going to show the next step. So by the end of this demo, you should be able to transform parse JSON text into clean, optionally marked down formatted using LLMs. And you should be able to compare these two methods for each you should be able to explain their benefits and limitations. And then you should be able to chunk this clean text and discuss how overlapping works. And then finally, you should be able to store this final clean and chunk data to a delta table so that it can later be used to compute embeddings and store it in vector database. Let's talk about the requirements. There should be parse document table in JSON format. So if you have completed the previous demo, you should have this table ready. Then to run the notebooks, you need serverless compute version 4. And also some dependencies are added, required libraries added to dependencies. Those should be configured too. If you click the serverless panel, you should see that the version 4 is selected. And this lanching text splitter libraries installed. This should be done by default. So when you select serverless, it should do this for you. But if you face with any problems, especially in terms of library requirements, just make sure that you have this setup and then click apply if it's not if you face with any problems. So let's get started. The first step is we are going to run this setup code. This classroom setup is going to create the data sets for you if they are not already created. That's it. And this is the demo that we are going to use. Basically in the previous demo, you should have the table created for you, the delta table with JSON documents created for you. Other than that, you don't need anything. So let's get started. How do we transform this JSON table to clean text? So we have here two options. The first option is to use an LLM to do semantic cleaning and using AI query. So this method is going to pass the JSON text to an LLM and ask LLM to convert this one to Markdown text using JSON data there. So for example, if the element is a table, it's going to convert that to Markdown table. The fastest and easiest way is to just convert this JSON text to plain text. So we are going to talk about both of these methods and their advantages and limitations. So first, let's look at the table that we have. So we have docs parts table that we created in previous demo. And this chunk table is going to be the final table that we are going to store the chunk data. So you can see that our source table has a pad modification time length and most importantly, parse content. So this parse content was in JSON format. Let's start with the LLM semantic cleaning and transformation. So how it works is we are using an LLM in this example. We are using GPT open source 20 millimeter. We are passing from to we are saying that you are a helpful assistant. We are going to give you a JSON object with pages elements and metadata and we want you to convert this to clean readable Markdown format. Also, we are adding this page divider to separate pages so that, you know, we can reference to those pages later. So this is a simple prompt. Then we are using the AI query function. AI query is a generic function that is provided by Databricks and you passes an endpoint and then you passes your prompt along with the content that you pass and the response format is going to be text in this case. So here is how it's going to look like. So we passed the JSON object and then this is clean Markdown text format. You can see that it is adding this page number. So zero and of course, it's by document. So this had only one page and you can, sorry, it has more than one page. So page zero, one and yeah, end of the document, there were two pages here. You can see that the Markdown is created. So this is like header one, this was header two and here you can see that you have nice Markdown table format. So this is how you do that with LLM. But what are the limitations here? The limitation, it can be very expensive because you are passing all that text into LLM and you are paying for this token. So this is the limitation of this method. But of course, you have the advantage why? Because you are keeping more structure and meaning and you are producing high quality Markdown. So if you later use this one for your retrieval agent, then you are going to have more context there. The easiest or fast and cheap version is going to be just to extract the text from that JSON tree and yeah, that will be it. But of course, in this method, we are going to lose some important structure and semantics. Let's say for the headings, for table, we are going to lose that format. So it's going to have less contextual information. But we don't need to pay for the tokens. We are just going to use UDF to apply to all columns. In this case, it's going to be plain text and we are going to extract the plain text. So here, we are extracting the text. And you can see that here, we don't have any semantics here. Well, you can add semantics. I'm going to show you the function that we used. So this is how we are defining extract contents UDF. And this UDF is basically calling this function. And it is a very simple function that just extract page ID from the JSON object and also extract context from JSON based on the content of the element. That's it. There's nothing to complicate that. But of course, if you want, you can improve this and the more semantics to your plain text. So for example, if it is a header, you can create a markdown style for that. And it's going to also work for you. But we kept it very simple so that you don't need to worry about that. So that's how it's done. Now let's talk about chunking. So we talk about how do you transform the JSON to plain text. And now let's talk about chunking. So what is chunking? chunking is when we have a long text and we cannot pass that long text to LLM because LLM has limited window-led context, right? In this example, of course, our text is very short. So it's not going to exceed the LLM window are going to be easily able to handle this. But we are just assuming that the text is long and we want to chunk that. So here we are going to use LENCHIN text splitter library. But you can use any chunking library out there. We don't need to use LENCHIN. But an example here we are using LENCHIN. So what we do is we define chunk size and chunk overlap. So this is how many characters is going to be used to split the chunks. And while splitting, it is going to make sure that it is overlapping by this amount. Then we can define separator how to separate them. And also the schema because this is the return text is we are going to store that in delta and we want to define the schema here. So here it is just we are defining a simple map impondas function and we are splitting, calling the split rows to iterate over column. And the result is going to be like this. So we are going to use that plain text and divide it into chunks. So you can see that this product overview document now splitted into two. So it's split it here and split it here. Because we define the split page here, we define a separator, we define page here. You can see that it is splitted in the page. But of course you don't see the overlapping here because the text is very short. So it's not exceeding that limit that we defined chunk size. You can play with this and yeah maybe let's say if you make it very small chunks and you can see how the chunk overlapping works. I'm going to just run this an example. I can see that when I lower the chunk size to very small chunks, you can see that is how it is now chunking. And yeah, this is the chunk. You can see that it's chunked into very small pieces. And here you can see how it is the overlapping worked here. In some of the examples you don't see the overlapping. But here you can see that there is motion control and deep. And then you can see that control and deep learning. Right. And here you can see that data collected data collected. So this is helpful when you pass this chunks into LLM. And the overlapping is going to help the LLM to understand the previous section. Of course, a little bit in this example is very small. We just like to demonstrate it. We use a very small chunk size and a very small overlap. But let's say imagine you have a long text and you can use one previous paragraph as overlap. And you know that the LLM is going to understand what was in the previous paragraph or maybe the next paragraph. And it's going to have more context there. Or you can maybe generate. These are more advanced options. But you can generate a summary of previous pages and pass that as overlap to the LLM and the LLM so that understand what was before that. And that's coming after that too. So that is how chunking works. And the final step we are going to save these chunks to delta table so that we can compute embeddings, convert these plain text to embeddings and store them in vector database. To do that, we are just writing as delta and override. And because we are merging the schema, we define the schema. We want to define the schema and save it. But that's how it is stored. And to wrap up here, we showed how to clean parse documents using two methods. We show how you can use an LLM to use it as semantic way of cleaning data. Then we used a simple plain text method to extract text from JSON object. Then we showed how chunking works using library to divide text into chunks and show how you can use overlap to have more kind of semantic knowledge when you chunk data. And we stored result into delta table so that we can use it later. That was it for this demo. Thanks for watching.

---

## Timestamped Segments

**[00:00]** Hello. In this demo, we are going to talk about how to clean, transform, and then chunk

**[00:06]** the parse text. In the previous demo, we showed how to use AI parse document function to

**[00:13]** parse documents into JSON format. And now we are going to show the next step. So by the end

**[00:21]** of this demo, you should be able to transform parse JSON text into clean, optionally marked

**[00:27]** down formatted using LLMs. And you should be able to compare these two methods for each you

**[00:34]** should be able to explain their benefits and limitations. And then you should be able

**[00:39]** to chunk this clean text and discuss how overlapping works. And then finally, you should be able

**[00:49]** to store this final clean and chunk data to a delta table so that it can later be used

**[00:58]** to compute embeddings and store it in vector database. Let's talk about the requirements.

**[01:05]** There should be parse document table in JSON format. So if you have completed the previous

**[01:12]** demo, you should have this table ready. Then to run the notebooks, you need serverless compute

**[01:19]** version 4. And also some dependencies are added, required libraries added to dependencies.

**[01:28]** Those should be configured too. If you click the serverless panel, you should see that the

**[01:34]** version 4 is selected. And this lanching text splitter libraries installed. This should be

**[01:42]** done by default. So when you select serverless, it should do this for you. But if you face

**[01:49]** with any problems, especially in terms of library requirements, just make sure that you have

**[01:55]** this setup and then click apply if it's not if you face with any problems. So let's get

**[02:02]** started. The first step is we are going to run this setup code. This classroom setup is going

**[02:08]** to create the data sets for you if they are not already created. That's it. And this is the demo

**[02:15]** that we are going to use. Basically in the previous demo, you should have the table created

**[02:21]** for you, the delta table with JSON documents created for you. Other than that, you don't need anything.

**[02:27]** So let's get started. How do we transform this JSON table to clean text? So we have here two

**[02:36]** options. The first option is to use an LLM to do semantic cleaning and using AI query. So this

**[02:46]** method is going to pass the JSON text to an LLM and ask LLM to convert this one to Markdown

**[02:54]** text using JSON data there. So for example, if the element is a table, it's going to convert that

**[03:02]** to Markdown table. The fastest and easiest way is to just convert this JSON text to plain text.

**[03:11]** So we are going to talk about both of these methods and their advantages and limitations.

**[03:17]** So first, let's look at the table that we have. So we have docs parts table that we created in

**[03:25]** previous demo. And this chunk table is going to be the final table that we are going to store the

**[03:32]** chunk data. So you can see that our source table has a pad modification time length and most

**[03:39]** importantly, parse content. So this parse content was in JSON format. Let's start with the LLM

**[03:47]** semantic cleaning and transformation. So how it works is we are using an LLM in this example. We are

**[03:56]** using GPT open source 20 millimeter. We are passing from to we are saying that you are a helpful

**[04:05]** assistant. We are going to give you a JSON object with pages elements and metadata and we want

**[04:11]** you to convert this to clean readable Markdown format. Also, we are adding this page divider to

**[04:20]** separate pages so that, you know, we can reference to those pages later. So this is a simple prompt.

**[04:30]** Then we are using the AI query function. AI query is a generic function that is provided by

**[04:36]** Databricks and you passes an endpoint and then you passes your prompt along with the content that

**[04:43]** you pass and the response format is going to be text in this case. So here is how it's going to look

**[04:50]** like. So we passed the JSON object and then this is clean Markdown text format. You can see that it is

**[04:58]** adding this page number. So zero and of course, it's by document. So this had only one page

**[05:05]** and you can, sorry, it has more than one page. So page zero, one and yeah, end of the document,

**[05:12]** there were two pages here. You can see that the Markdown is created. So this is like header one,

**[05:20]** this was header two and here you can see that you have nice Markdown table format. So this is how

**[05:27]** you do that with LLM. But what are the limitations here? The limitation, it can be very expensive because

**[05:34]** you are passing all that text into LLM and you are paying for this token. So this is the limitation

**[05:42]** of this method. But of course, you have the advantage why? Because you are keeping more structure and

**[05:48]** meaning and you are producing high quality Markdown. So if you later use this one for your retrieval agent,

**[05:55]** then you are going to have more context there. The easiest or fast and cheap version is going to be

**[06:02]** just to extract the text from that JSON tree and yeah, that will be it. But of course, in this method,

**[06:10]** we are going to lose some important structure and semantics. Let's say for the headings, for table,

**[06:17]** we are going to lose that format. So it's going to have less contextual information. But we don't need

**[06:24]** to pay for the tokens. We are just going to use UDF to apply to all columns. In this case, it's going

**[06:32]** to be plain text and we are going to extract the plain text. So here, we are extracting the text. And

**[06:41]** you can see that here, we don't have any semantics here. Well, you can add semantics. I'm going to show

**[06:48]** you the function that we used. So this is how we are defining extract contents UDF. And this UDF

**[06:56]** is basically calling this function. And it is a very simple function that just extract page ID from

**[07:03]** the JSON object and also extract context from JSON based on the content of the element. That's it.

**[07:12]** There's nothing to complicate that. But of course, if you want, you can improve this and the more

**[07:18]** semantics to your plain text. So for example, if it is a header, you can create a markdown style for

**[07:27]** that. And it's going to also work for you. But we kept it very simple so that you don't need to worry

**[07:35]** about that. So that's how it's done. Now let's talk about chunking. So we talk about how do you

**[07:44]** transform the JSON to plain text. And now let's talk about chunking. So what is chunking?

**[07:51]** chunking is when we have a long text and we cannot pass that long text to LLM because LLM has

**[08:00]** limited window-led context, right? In this example, of course, our text is very short. So it's not

**[08:07]** going to exceed the LLM window are going to be easily able to handle this. But we are just assuming

**[08:16]** that the text is long and we want to chunk that. So here we are going to use LENCHIN text

**[08:22]** splitter library. But you can use any chunking library out there. We don't need to use LENCHIN.

**[08:29]** But an example here we are using LENCHIN. So what we do is we define chunk size and chunk overlap.

**[08:36]** So this is how many characters is going to be used to split the chunks. And while splitting, it is

**[08:43]** going to make sure that it is overlapping by this amount. Then we can define separator how to

**[08:51]** separate them. And also the schema because this is the return text is we are going to store that

**[08:59]** in delta and we want to define the schema here. So here it is just we are defining a simple

**[09:06]** map impondas function and we are splitting, calling the split rows to iterate over column.

**[09:14]** And the result is going to be like this. So we are going to use that plain text and divide it into

**[09:22]** chunks. So you can see that this product overview document now splitted into two. So it's split

**[09:29]** it here and split it here. Because we define the split page here, we define a separator, we define

**[09:38]** page here. You can see that it is splitted in the page. But of course you don't see the

**[09:46]** overlapping here because the text is very short. So it's not exceeding that limit that we defined

**[09:53]** chunk size. You can play with this and yeah maybe let's say if you make it very small chunks and

**[10:00]** you can see how the chunk overlapping works. I'm going to just run this an example.

**[10:10]** I can see that when I lower the chunk size to very small chunks, you can see that is how it is now

**[10:18]** chunking. And yeah, this is the chunk. You can see that it's chunked into very small pieces.

**[10:28]** And here you can see how it is the overlapping worked here. In some of the examples you don't

**[10:36]** see the overlapping. But here you can see that there is motion control and deep. And then you can

**[10:42]** see that control and deep learning. Right. And here you can see that data collected data collected.

**[10:48]** So this is helpful when you pass this chunks into LLM. And the overlapping is going to help the

**[10:57]** LLM to understand the previous section. Of course, a little bit in this example is very small.

**[11:03]** We just like to demonstrate it. We use a very small chunk size and a very small overlap.

**[11:10]** But let's say imagine you have a long text and you can use one previous paragraph as overlap.

**[11:17]** And you know that the LLM is going to understand what was in the previous

**[11:24]** paragraph or maybe the next paragraph. And it's going to have more context there. Or you can maybe

**[11:30]** generate. These are more advanced options. But you can generate a summary of previous pages and pass

**[11:37]** that as overlap to the LLM and the LLM so that understand what was before that. And that's coming

**[11:45]** after that too. So that is how chunking works. And the final step we are going to save these chunks

**[11:54]** to delta table so that we can compute embeddings, convert these plain text to embeddings and store them

**[12:02]** in vector database. To do that, we are just writing as delta and override. And because we are

**[12:11]** merging the schema, we define the schema. We want to define the schema and save it. But that's how it

**[12:17]** is stored. And to wrap up here, we showed how to clean parse documents using two methods. We

**[12:27]** show how you can use an LLM to use it as semantic way of cleaning data. Then we used a simple plain

**[12:37]** text method to extract text from JSON object. Then we showed how chunking works using library to

**[12:47]** divide text into chunks and show how you can use overlap to have more kind of semantic knowledge

**[12:56]** when you chunk data. And we stored result into delta table so that we can use it later. That was it

**[13:04]** for this demo. Thanks for watching.

