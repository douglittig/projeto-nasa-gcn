# Demo Parse documents t

**Source:** `2-Building Retrieval Agents On Databricks - Demo Parse documents t.mp4`
**Duration:** 13:46
**Language:** en (detected with 100.0% confidence)

---

## Full Transcription

Hello, and welcome to this demo in this demo. We are going to talk about how to parse documents to structure data if you are using any document for agents you need to convert those documents to structured format and for drag, it is the same. So in this demo, we are going to show how to do that using data breaks AI parse document function. This is a special function that is going to help you to parse documents and convert them to plain text. So by the end of this demo, you should be able to parse different document formats such as PDF or images, for example, using the AI parse document function, then you should be able to understand the parse output schema. You should be able to identify and explain key metadata fields in the parse output of the AI parse document functions. And then you should be able to also visualize and debug the parse document content. Next, let's talk about some requirements. In this demo, you are required to have a volume containing sample documents. This is in the lab environment. This is created for you. So you don't need to do anything. And I'm going to show you the volume now. Then you should have serverless environment version for when you select the serverless and run it should select the environment version for you. But if not, just click here on this serverless environment icon and make sure that the environment for is selected and then click apply. If different environment version is selected, you need to change it and then click apply. So that's it. Next is going to be set up section. So the set up section is going to configure this demo environment for you. First is going to prepare a data set for you that we are going to use in this demo. So it's going to do some checks. And here this is the volume that you will need in this demo. It's going to be DB Academy is the catalog name and the schema name is going to be your schema name like user schema name. And in this schema, you will have a volume called Orion docs and let us view that. So if I go to the catalog and select the DB Academy catalog, select my schema and here you can see that I already ran the code. So I have a table and then volumes, you should have these two volumes. This one is going to be used in this demo and this one is going to be used for other demos. So make sure that you have this volume created for you. And to see that in this volume, you can see that we have a couple PDF documents. If I download this one, you can see that this are just simple PDF documents is called Orion robotics. This is a hypothetical robotic company that we just created this document for this demo purpose. And you can see that this is just some text and the images, graphics, tables in different documents, you are going to see different structures here. So just to make sure that we can test this AI parts document for different cases. So if it's already, then you can start with the first section. So the first section is going to be about using the AI parts document function to parse the documents. Please know that you should use version two of AI parts document and you define that version in the version section here. And yeah, so this is the only requirement that you have to use the AI parts documents with Python, we just need to read the file and then pass these parameters to AI parts document. First one is version, then there's image output pad. So when the function runs, let's say if it is going to parse a PDF file, it's going to convert each page to an image so that those images can later be used and then you can reference those. Then there's description element types. So when parsing the document, you can define which element to extract. So you can say everything table, images, text, an example would be, let's say, if you want to just extract text and you're not interested in table and images, then you can just define tags and skip to rest. So here's how it is done. First, we are going to read the files in binary format. So this is how we do spark read format binary and then we are passing this volume pad. We are creating a new column called parse content and this is the express section that we are calling the AI parts document function. We are passing the content and then we are passing the different parameters for the function. So we are defining the version and then image output pad. That's it. Now let's look how the parsed table looks like. So here you can see that we have a document path that is parsed. This is the file size and this is the parsed content. So when AI document parses a document, this is how it parses. First you can see that there is a document object is a JSON object here and then there is error status and metadata. So if there is any error while parsing the document, let's say if maybe couldn't parse one section or there was like a problem while reading the document, then you are going to see the details here. And this is the section, the document section, how it's parsed. So you can see that there is document and in this document object are elements and these elements are all elements that are in this document. And this document, so it's going to be, for example, coordinate of this box, which is original robotics and description is null. So and the type is section header. So a parsed document is not just parsing the text is also understand the context and it defines whether this object is a header, page footer or it is a text is a caption figure. All those kind of things are defined for you and this is important when you to provide a richer context for the documents. Don't we can list the documents using SQL list and the path. So it's just to list files that are parsed and you can see that here there is a parsed image folder. So a new folder created and the same path that we passed to AR parts and this is going to have all parsed images. So each page is going to be converted to also an image. Yeah, this is the same here. You can see that all parsed documents are created here. So each page is created as an image here. So you should have the same number of images as number of pages here. This was how AI parse document can be used with Python. There's also SQL support for that too. You can use SQL for SQL. It is kind of the same format is just in the Databricks SQL format. So you are using AI parse document and yeah, the only difference is this mapping format and that's it. Then you are reading files as binary file and you're passing this to the select statement. Yeah, it's going to be the same output. So I'm going to skip this section. I showed this one just to make sure that you know there is a Python way of doing that and also SQL way of doing that. So all AI function in Databricks has support for both Python and SQL. Then let's look at the metadata that is extracted. So the AI parse is going to return a document object in this document object that can be pages page number text table images and also some metadata. And here we showed how you can select using the select statement to extract those object. So here, for example, we are selecting the parse content document pages. Then we are selecting elements, then error status, corrupted data and metadata. And you will see that each of these is created in a new column. So if you scroll back here, yeah, there is no error. There's no corrupted data and for metadata. This is the metadata section and this are the elements. This is the pages and this is the path. Yeah, so elements again, it's just extracted. So this way we are extracting by document. We are going to look into how to view this element extracted elements on the document and to inspect that to see if that is done correctly. Here, we have a document renderer help look class. So this is not something that is shipped with AI parse document function. So this is just a class that we created and it is reading this JSON objects and displays them on the result that is parsed. I'm going to just show how it looks like. So here, this function create this nice visual output. Here you can see that we have documents summary. I'm just parsing, just selecting one of these documents. So not all of them. And here you can see that there are three pages in this document. There are 22 elements and here are the element colors and resolution everything. And here is how it is parsed. So you can see that this is a page header. Then there is a section header text text. This are all correct. Then there is a figure and then capture action. Can see that same for the second page and then third page. So this is important because it is not just extracting plain text, but it's also understanding each section and annotating that. So in this example, we had a figure here and it is annotating that this is a figure and this is a caption for that. So imagine if you are going to use this one as part of your retrieval agent and you want to let's say generate an output for a question and you can say that this is explained in page two and figure on the left, for example, because we know also the curtains of the image. And we know that this image is on page X. We can give a reference to that specific page and generate an answer that is letting user know where they can look at it. So this is why it is important. Alright, so that's it. That's how we used AI parse document to extract the content of the document. Now we need to store this text to a delta table and use that later in other demos. So in the next demo, for example, we are going to use how to clean the extracted data, how to divide it into chunks and then those chunks are going to be used for vector search to store and vector format and search based on that. So we are just here defining the output table and writing as delta. That's it. Nothing to complicate. So to wrap up in this demo, we showed how to use AI parse document both in Python and SQL to parse documents. We show different metadata fields that are extracted. And then as an optional section, we visualize this output and show how you can inspect and see if the parsing is done correctly. So that's it for this demo. And thanks for watching.

---

## Timestamped Segments

**[00:00]** Hello, and welcome to this demo in this demo. We are going to talk about how to parse documents to structure data if you are using any document for agents you need to convert those documents to structured format and for

**[00:17]** drag, it is the same. So in this demo, we are going to show how to do that using data breaks AI parse document function. This is a special function that is going to help you to parse documents and convert them to plain text.

**[00:36]** So by the end of this demo, you should be able to parse different document formats such as PDF or images, for example, using the AI parse document function, then you should be able to understand the parse output schema.

**[00:53]** You should be able to identify and explain key metadata fields in the parse output of the AI parse document functions. And then you should be able to also visualize and debug the parse document content.

**[01:09]** Next, let's talk about some requirements. In this demo, you are required to have a volume containing sample documents. This is in the lab environment. This is created for you. So you don't need to do anything. And I'm going to show you the volume now.

**[01:26]** Then you should have serverless environment version for when you select the serverless and run it should select the environment version for you. But if not, just click here on this serverless environment icon and make sure that the environment for is selected and then click apply. If different environment version is selected, you need to change it and then click apply.

**[01:54]** So that's it. Next is going to be set up section. So the set up section is going to configure this demo environment for you. First is going to prepare a data set for you that we are going to use in this demo.

**[02:08]** So it's going to do some checks. And here this is the volume that you will need in this demo. It's going to be DB Academy is the catalog name and the schema name is going to be your schema name like user schema name.

**[02:23]** And in this schema, you will have a volume called Orion docs and let us view that. So if I go to the catalog and select the DB Academy catalog, select my schema and here you can see that I already ran the code. So I have a table and then volumes, you should have these two volumes. This one is going to be used in this demo and this one is going to be used for other demos.

**[02:53]** So make sure that you have this volume created for you. And to see that in this volume, you can see that we have a couple PDF documents. If I download this one, you can see that this are just simple PDF documents is called Orion robotics.

**[03:16]** This is a hypothetical robotic company that we just created this document for this demo purpose. And you can see that this is just some text and the images, graphics, tables in different documents, you are going to see different structures here. So just to make sure that we can test this AI parts document for different cases.

**[03:40]** So if it's already, then you can start with the first section. So the first section is going to be about using the AI parts document function to parse the documents.

**[03:53]** Please know that you should use version two of AI parts document and you define that version in the version section here.

**[04:03]** And yeah, so this is the only requirement that you have to use the AI parts documents with Python, we just need to read the file and then pass these parameters to AI parts document.

**[04:16]** First one is version, then there's image output pad. So when the function runs, let's say if it is going to parse a PDF file, it's going to convert each page to an image so that those images can later be used and then you can reference those.

**[04:36]** Then there's description element types. So when parsing the document, you can define which element to extract. So you can say everything table, images, text, an example would be, let's say, if you want to just extract text and you're not interested in table and images, then you can just define tags and skip to rest.

**[04:58]** So here's how it is done. First, we are going to read the files in binary format. So this is how we do spark read format binary and then we are passing this volume pad.

**[05:12]** We are creating a new column called parse content and this is the express section that we are calling the AI parts document function.

**[05:22]** We are passing the content and then we are passing the different parameters for the function. So we are defining the version and then image output pad. That's it.

**[05:34]** Now let's look how the parsed table looks like. So here you can see that we have a document path that is parsed. This is the file size and this is the parsed content.

**[05:49]** So when AI document parses a document, this is how it parses. First you can see that there is a document object is a JSON object here and then there is error status and metadata.

**[06:06]** So if there is any error while parsing the document, let's say if maybe couldn't parse one section or there was like a problem while reading the document, then you are going to see the details here.

**[06:19]** And this is the section, the document section, how it's parsed. So you can see that there is document and in this document object are elements and these elements are all elements that are in this document.

**[06:36]** And this document, so it's going to be, for example, coordinate of this box, which is original robotics and description is null. So and the type is section header. So a parsed document is not just parsing the text is also understand the context and it defines whether this object is a header, page footer or it is a text is a caption figure.

**[07:02]** All those kind of things are defined for you and this is important when you to provide a richer context for the documents.

**[07:10]** Don't we can list the documents using SQL list and the path. So it's just to list files that are parsed and you can see that here there is a parsed image folder.

**[07:24]** So a new folder created and the same path that we passed to AR parts and this is going to have all parsed images. So each page is going to be converted to also an image.

**[07:40]** Yeah, this is the same here. You can see that all parsed documents are created here. So each page is created as an image here.

**[07:51]** So you should have the same number of images as number of pages here. This was how AI parse document can be used with Python. There's also SQL support for that too. You can use SQL for SQL. It is kind of the same format is just in the Databricks SQL format.

**[08:12]** So you are using AI parse document and yeah, the only difference is this mapping format and that's it. Then you are reading files as binary file and you're passing this to the select statement.

**[08:27]** Yeah, it's going to be the same output. So I'm going to skip this section. I showed this one just to make sure that you know there is a Python way of doing that and also SQL way of doing that.

**[08:39]** So all AI function in Databricks has support for both Python and SQL. Then let's look at the metadata that is extracted. So the AI parse is going to return a document object in this document object that can be pages page number text table images and also some metadata.

**[09:08]** And here we showed how you can select using the select statement to extract those object. So here, for example, we are selecting the parse content document pages.

**[09:23]** Then we are selecting elements, then error status, corrupted data and metadata. And you will see that each of these is created in a new column.

**[09:35]** So if you scroll back here, yeah, there is no error. There's no corrupted data and for metadata. This is the metadata section and this are the elements. This is the pages and this is the path.

**[09:52]** Yeah, so elements again, it's just extracted. So this way we are extracting by document. We are going to look into how to view this element extracted elements on the document and to inspect that to see if that is done correctly.

**[10:13]** Here, we have a document renderer help look class. So this is not something that is shipped with AI parse document function. So this is just a class that we created and it is reading this JSON objects and displays them on the result that is parsed.

**[10:34]** I'm going to just show how it looks like. So here, this function create this nice visual output. Here you can see that we have documents summary. I'm just parsing, just selecting one of these documents. So not all of them.

**[10:50]** And here you can see that there are three pages in this document. There are 22 elements and here are the element colors and resolution everything. And here is how it is parsed. So you can see that this is a page header. Then there is a section header text text. This are all correct. Then there is a figure and then capture action.

**[11:18]** Can see that same for the second page and then third page. So this is important because it is not just extracting plain text, but it's also understanding each section and annotating that. So in this example, we had a figure here and it is annotating that this is a figure and this is a caption for that.

**[11:47]** So imagine if you are going to use this one as part of your retrieval agent and you want to let's say generate an output for a question and you can say that this is explained in page two and figure on the left, for example, because we know also the curtains of the image.

**[12:10]** And we know that this image is on page X. We can give a reference to that specific page and generate an answer that is letting user know where they can look at it. So this is why it is important.

**[12:25]** Alright, so that's it. That's how we used AI parse document to extract the content of the document. Now we need to store this text to a delta table and use that later in other demos.

**[12:43]** So in the next demo, for example, we are going to use how to clean the extracted data, how to divide it into chunks and then those chunks are going to be used for vector search to store and vector format and search based on that.

**[13:02]** So we are just here defining the output table and writing as delta. That's it. Nothing to complicate.

**[13:12]** So to wrap up in this demo, we showed how to use AI parse document both in Python and SQL to parse documents. We show different metadata fields that are extracted.

**[13:28]** And then as an optional section, we visualize this output and show how you can inspect and see if the parsing is done correctly.

**[13:39]** So that's it for this demo. And thanks for watching.

