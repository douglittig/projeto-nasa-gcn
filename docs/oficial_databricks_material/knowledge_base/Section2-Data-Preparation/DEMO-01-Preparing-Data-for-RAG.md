# Demo Preparing Data for RAG

**Source:** `Generative AI Solution Development - Demo Preparing Data for RAG.mp4`
**Duration:** 11:22
**Language:** en (detected with 100.0% confidence)

---

## Full Transcription

So in this demo, we'll prepare the data for a rag solution, so we'll have a list of PDFs available for us, out of which we'll extract the content, apply some chunking best practices and strategies that we addressed during the lecture. We'll create embeddings out of these chunks by leveraging Databricks Foundation Model API endpoint. So in order to show you how to use a foundation model and how you can compute the chunks embedding, especially at scale on your data, and then we'll materialize this embedding into a Delta table. So if I jump into my Databricks environment, so first demo preparing data for rag, you should have it in your course material. So what are we going to do here? We're going to have our PDFs preloaded for us into a Databricks volume. What we will do is we'll ingest these by using autoloader, just to showcase how we can program this job to run as a streaming incremental job. We'll read the content as a binary stream. We'll parse that stream, OCR it, calculate chunks, calculate some embeddings. And once we'll do that, we'll persist this in a Delta table. So this is how far our demo will go today. So first thing, a little bit of a laundry list item, because we're going to use under the hood a technique or a method called Pandas UDF to scale out the processing. Pandas UDF uses arrow under the hood. So in order to kind of control the memory and the batch size that for py arrow, we're going to set a spark configuration here. So don't mind that. So in that first section, again, assuming you're familiar with spark, spark has the capability to read any, let's say, type of unstructured data as a binary stream. So that's what we're doing here. We're loading this from our pass where we have our PDFs and we're materializing this as what we're going to call the row, the PDF row text table. We'll look at all the generated assets in Unity catalog at the end of the demo. So here I can see that for every file that I read, I will have probably length in terms of megabyte and the content, which obviously at this point, again, it's a binary stream, which doesn't mean anything. So now we could do a quick, in order to read that or deserialize that stream, we are going to use a method called extract doc text, which is made available for us. Here, just to do a quick sanity check on random PDF out of this collection, I can ensure that yes, I'm able to read that text. So what are we going to do here? How are we going to read all these documents at scale, OCR them out, split them? So we're going to use a couple of, let's say, high level libraries, which are going to help us through the process. The first one is going to be the sentence splitter from llama index. We're also going to use the transformer libraries to add a sanity check on our token count. And we are going to use, we're going to wrap all these into what we call a pandas UDF for pandas user defined function. So what we're going to do in that pandas on user defined function that we're going to call read as chunk is we're going to iterate through the spark data frame. We're going to get, we're going to set the global tokenizer to be the one for llama. Why? Because downstream for our rack chain, we are going to use the llama model to do the generation. So we're just ensuring to use the same tokenizer. So with that, we're going to initiate our sentence splitter with a chunk size and overlap. So here it's pretty easy. It's a fixed chunk size. Why did we pick 500? It is because the llama models that we're going to use in this demo, which is the llama 2, has a context window of 512 tokens. And that's it. So once the way, again, if you're familiar with how the sentence splitter work, you just, again, you feed it what we call a document that you create on top of your text. So what's happening inside that function, we are deserializing the binary stream into text. We are creating nodes, technically means, let's say different pieces of the document. So it's going to extract again, maybe the hierarchy of the paragraphs, the sections, the sentence and whatnot. So we're going to initiate the splitter again on the document that we created on top of our text. And we're going to return again, all the text that were extracted out of the node and we're going to apply the set scale. So that's what this UDF is doing and applying this. We're going to apply this at scale by using the pie spark API, using the whisk column method. So technically what we're doing here is that to the previous data frame, which is pointing to the row text delta table, we are going to add the column called content. Where we're going to apply this UDF, the 3 dash chunk UDF on the content, which is the binary stream. And because this pandas UDF is going to give us an one to many. So one document will return multiple chunks. We're going to explode these into their own rows in the newly created spark data frame. And from all the outcome, we're just going to take, we're just going to keep the pass, the PDF name, we're going to rename the column pass to PDF name and keep the content, which was the output of that column. Again, now for the chunking overlap, we set it to 20 as a random measure. We like there's no like there was no specific logic into why we chose that is a default value, which seems to work. Oftentimes all default parameters seem to work, but at least the chunk size again needs to be driven by the capacity of the language model that you're going to use downstream to do the generation. So here for the outcome, what can I see? I can see that like for the same document or the same PDF, I'm going to have all the different contents or chunks. So here is probably the header where I can see some maybe some date or the archive papers ID, the name of the authors and whatnot. And then again, maybe the abstract and the content of the paper. So that's it. What do we do at this point? Again, we ingested extracted chunked at scale using the pandas UDF. So now that we have that, the next step is to calculate the dense factor representation or the embeddings for each one of these chunks. And for that, again, you have many options. You can just download an embedding model from hugging face and run it at scale in a batch fashion. And you can also leverage out of the box found, let's say embedding models exposed by the foundation models API. So if you navigate to your serving tab, we're not going to do this now. You can see a family of model made available for you. As we're speaking or in recording at this training, the one of the embedding models that is made available by the Databricks foundation models API is the BGE large. So that's the model where we'll be leveraging through the foundation models API. And how are we going to invoke this model? We're going to invoke it using the MLflow deployment get deploy client. So here I'm just instantiating my client and I'm telling it to point to Databricks. And that client exposes a method called predict where I just need to specify my endpoint name. So that is again, it is a seven stone endpoint name for the BGE large model and it expecting an input stream with a specific format. So input and the text that I want to embed and what you're getting out of the outputs is an embedding vector from for that specific question. And that's it. Very easy. So next step is to run this embedding calculation at scale. And for that, we're going to do the same as before. We're going to create a pandas UDF. We're doing this in a batch fashion. You could do this as part of a streaming job. So as you might get new documents dropped on your volume, you want them to go through the same process. You can definitely do that as part of a streaming job or Delta live table pipeline to incrementally consume the updates. Here we're going to do that in a one time batch fashion. Using pandas UDF. So what's happening in that UDF is whatever we did just previously invoking the API. We're going to just wrap this get embeddings method using the MLflow deploy client on our spark data frame, which has all the chunks. Now, because those endpoints have, let's say, concurrency limitations, we can we are going to control the batch size. We're going to ensure that we're not sending more than 150 requests per second. That's just for that specific model and that specific environment. And that's it. Then we're going to process the batch and return this area as output. And so same as before, we're going to on the spark data frame, we're going to add a new column called embeddings on top of which we're going to apply the pandas UDF to get the embedding on the context and just select as output of that data frame. Just the name of the PDF. Keep the content and the corresponding embedding or dense vector. And once we have that, this is what we are going to because this is all against happening in memory in a lazy evaluation using by spark. The ultimate step would be to materialize these in your storage. And for that, we're going to store that in a Delta table because Delta table support, you know, structured and array data. So as the calculation is happening, what the first step we're going to do is we're going to just create the DDL. So we're going to declare that table. We're going to call it PDF text embeddings with an identifier column, which is we're randomly generate the PDF name, which is again the link to the document, the raw content, because ultimately that's what we want to get retrieved and inject to the prompt and the corresponding embedding vector that we are currently calculating. Now, one thing here, again, maybe if you're new to Delta tables, you're near new to the DDL, you know, SQL formalism, you can also do that doing spy by spark. One thing to note that we did here is to enable a specific property of Delta tables called change data feed, which will allow to incrementally update the index as maybe new data or new documents gets appended to the Delta table. So once we declared that table, we're going to materialize and we're going to fill it with the spark data frame, which we've calculated previously containing the chunks. Again, the documents, the chunks and the embeddings. And that's it. That kind of that kind of wraps up the data preparation piece. We can take a look at the generated assets under unity catalog in the created catalog and schema so I can see my embeddings table being created. If I take a quick look at the content and the sample data, so I should see the materialize the source, the raw content, which is the text and the corresponding embedding vectors.

---

## Timestamped Segments

**[00:00]** So in this demo, we'll prepare the data for a rag solution, so we'll have a list of PDFs available for us,

**[00:07]** out of which we'll extract the content, apply some chunking best practices and strategies that we addressed during the lecture.

**[00:16]** We'll create embeddings out of these chunks by leveraging Databricks Foundation Model API endpoint.

**[00:23]** So in order to show you how to use a foundation model and how you can compute the chunks embedding, especially at scale on your data,

**[00:31]** and then we'll materialize this embedding into a Delta table.

**[00:35]** So if I jump into my Databricks environment, so first demo preparing data for rag, you should have it in your course material.

**[00:45]** So what are we going to do here? We're going to have our PDFs preloaded for us into a Databricks volume.

**[00:53]** What we will do is we'll ingest these by using autoloader, just to showcase how we can program this job to run as a streaming incremental job.

**[01:03]** We'll read the content as a binary stream. We'll parse that stream, OCR it, calculate chunks, calculate some embeddings.

**[01:13]** And once we'll do that, we'll persist this in a Delta table. So this is how far our demo will go today.

**[01:22]** So first thing, a little bit of a laundry list item, because we're going to use under the hood a technique or a method called Pandas UDF to scale out the processing.

**[01:36]** Pandas UDF uses arrow under the hood. So in order to kind of control the memory and the batch size that for py arrow, we're going to set a spark configuration here.

**[01:46]** So don't mind that. So in that first section, again, assuming you're familiar with spark, spark has the capability to read any, let's say, type of unstructured data as a binary stream.

**[02:00]** So that's what we're doing here. We're loading this from our pass where we have our PDFs and we're materializing this as what we're going to call the row, the PDF row text table.

**[02:11]** We'll look at all the generated assets in Unity catalog at the end of the demo.

**[02:15]** So here I can see that for every file that I read, I will have probably length in terms of megabyte and the content, which obviously at this point, again, it's a binary stream, which doesn't mean anything.

**[02:28]** So now we could do a quick, in order to read that or deserialize that stream, we are going to use a method called extract doc text, which is made available for us.

**[02:39]** Here, just to do a quick sanity check on random PDF out of this collection, I can ensure that yes, I'm able to read that text.

**[02:48]** So what are we going to do here? How are we going to read all these documents at scale, OCR them out, split them?

**[02:56]** So we're going to use a couple of, let's say, high level libraries, which are going to help us through the process.

**[03:01]** The first one is going to be the sentence splitter from llama index.

**[03:05]** We're also going to use the transformer libraries to add a sanity check on our token count.

**[03:11]** And we are going to use, we're going to wrap all these into what we call a pandas UDF for pandas user defined function.

**[03:18]** So what we're going to do in that pandas on user defined function that we're going to call read as chunk is we're going to iterate through the spark data frame.

**[03:27]** We're going to get, we're going to set the global tokenizer to be the one for llama.

**[03:31]** Why? Because downstream for our rack chain, we are going to use the llama model to do the generation.

**[03:38]** So we're just ensuring to use the same tokenizer.

**[03:41]** So with that, we're going to initiate our sentence splitter with a chunk size and overlap.

**[03:47]** So here it's pretty easy. It's a fixed chunk size. Why did we pick 500?

**[03:51]** It is because the llama models that we're going to use in this demo, which is the llama 2, has a context window of 512 tokens.

**[03:58]** And that's it. So once the way, again, if you're familiar with how the sentence splitter work, you just, again, you feed it what we call a document that you create on top of your text.

**[04:09]** So what's happening inside that function, we are deserializing the binary stream into text.

**[04:15]** We are creating nodes, technically means, let's say different pieces of the document.

**[04:20]** So it's going to extract again, maybe the hierarchy of the paragraphs, the sections, the sentence and whatnot.

**[04:25]** So we're going to initiate the splitter again on the document that we created on top of our text.

**[04:30]** And we're going to return again, all the text that were extracted out of the node and we're going to apply the set scale.

**[04:36]** So that's what this UDF is doing and applying this.

**[04:39]** We're going to apply this at scale by using the pie spark API, using the whisk column method.

**[04:44]** So technically what we're doing here is that to the previous data frame, which is pointing to the row text delta table, we are going to add the column called content.

**[04:54]** Where we're going to apply this UDF, the 3 dash chunk UDF on the content, which is the binary stream.

**[05:01]** And because this pandas UDF is going to give us an one to many.

**[05:05]** So one document will return multiple chunks.

**[05:08]** We're going to explode these into their own rows in the newly created spark data frame.

**[05:15]** And from all the outcome, we're just going to take, we're just going to keep the pass, the PDF name,

**[05:21]** we're going to rename the column pass to PDF name and keep the content, which was the output of that column.

**[05:27]** Again, now for the chunking overlap, we set it to 20 as a random measure.

**[05:32]** We like there's no like there was no specific logic into why we chose that is a default value, which seems to work.

**[05:39]** Oftentimes all default parameters seem to work, but at least the chunk size again needs to be driven by the capacity of the language model that you're going to use downstream to do the generation.

**[05:52]** So here for the outcome, what can I see?

**[05:55]** I can see that like for the same document or the same PDF, I'm going to have all the different contents or chunks.

**[06:02]** So here is probably the header where I can see some maybe some date or the archive papers ID, the name of the authors and whatnot.

**[06:11]** And then again, maybe the abstract and the content of the paper.

**[06:15]** So that's it.

**[06:16]** What do we do at this point?

**[06:18]** Again, we ingested extracted chunked at scale using the pandas UDF.

**[06:24]** So now that we have that, the next step is to calculate the dense factor representation or the embeddings for each one of these chunks.

**[06:33]** And for that, again, you have many options.

**[06:36]** You can just download an embedding model from hugging face and run it at scale in a batch fashion.

**[06:41]** And you can also leverage out of the box found, let's say embedding models exposed by the foundation models API.

**[06:49]** So if you navigate to your serving tab, we're not going to do this now.

**[06:54]** You can see a family of model made available for you.

**[06:58]** As we're speaking or in recording at this training, the one of the embedding models that is made available by the Databricks foundation models API is the BGE large.

**[07:08]** So that's the model where we'll be leveraging through the foundation models API.

**[07:12]** And how are we going to invoke this model?

**[07:14]** We're going to invoke it using the MLflow deployment get deploy client.

**[07:19]** So here I'm just instantiating my client and I'm telling it to point to Databricks.

**[07:25]** And that client exposes a method called predict where I just need to specify my endpoint name.

**[07:34]** So that is again, it is a seven stone endpoint name for the BGE large model and it expecting an input stream with a specific format.

**[07:43]** So input and the text that I want to embed and what you're getting out of the outputs is an embedding vector from for that specific question.

**[07:52]** And that's it. Very easy.

**[07:54]** So next step is to run this embedding calculation at scale.

**[08:00]** And for that, we're going to do the same as before.

**[08:03]** We're going to create a pandas UDF.

**[08:05]** We're doing this in a batch fashion.

**[08:07]** You could do this as part of a streaming job.

**[08:09]** So as you might get new documents dropped on your volume, you want them to go through the same process.

**[08:15]** You can definitely do that as part of a streaming job or Delta live table pipeline to incrementally consume the updates.

**[08:21]** Here we're going to do that in a one time batch fashion.

**[08:23]** Using pandas UDF.

**[08:24]** So what's happening in that UDF is whatever we did just previously invoking the API.

**[08:30]** We're going to just wrap this get embeddings method using the MLflow deploy client on our spark data frame, which has all the chunks.

**[08:39]** Now, because those endpoints have, let's say, concurrency limitations, we can we are going to control the batch size.

**[08:46]** We're going to ensure that we're not sending more than 150 requests per second.

**[08:51]** That's just for that specific model and that specific environment.

**[08:55]** And that's it.

**[08:56]** Then we're going to process the batch and return this area as output.

**[09:00]** And so same as before, we're going to on the spark data frame, we're going to add a new column called embeddings on top of which we're going to apply the pandas UDF to get the embedding on the context and just select as output of that data frame.

**[09:16]** Just the name of the PDF.

**[09:18]** Keep the content and the corresponding embedding or dense vector.

**[09:23]** And once we have that, this is what we are going to because this is all against happening in memory in a lazy evaluation using by spark.

**[09:31]** The ultimate step would be to materialize these in your storage.

**[09:35]** And for that, we're going to store that in a Delta table because Delta table support, you know, structured and array data.

**[09:42]** So as the calculation is happening, what the first step we're going to do is we're going to just create the DDL.

**[09:48]** So we're going to declare that table.

**[09:50]** We're going to call it PDF text embeddings with an identifier column, which is we're randomly generate the PDF name, which is again the link to the document, the raw content, because ultimately that's what we want to get retrieved and inject to the prompt and the corresponding embedding vector that we are currently calculating.

**[10:09]** Now, one thing here, again, maybe if you're new to Delta tables, you're near new to the DDL, you know, SQL formalism, you can also do that doing spy by spark.

**[10:19]** One thing to note that we did here is to enable a specific property of Delta tables called change data feed, which will allow to incrementally update the index as maybe new data or new documents gets appended to the Delta table.

**[10:35]** So once we declared that table, we're going to materialize and we're going to fill it with the spark data frame, which we've calculated previously containing the chunks.

**[10:44]** Again, the documents, the chunks and the embeddings.

**[10:47]** And that's it.

**[10:48]** That kind of that kind of wraps up the data preparation piece.

**[10:53]** We can take a look at the generated assets under unity catalog in the created catalog and schema so I can see my embeddings table being created.

**[11:04]** If I take a quick look at the content and the sample data, so I should see the materialize the source, the raw content, which is the text and the corresponding embedding vectors.

