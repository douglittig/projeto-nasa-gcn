# Demo Explo

**Source:** `Generative AI Application Evaluation and Governance - Demo Explo.mp4`
**Duration:** 09:01
**Language:** en (detected with 100.0% confidence)

---

## Full Transcription

So let's go and start with one that we can talk about which is licensing that we mentioned, right? So when it comes to licensing, how do we go and understand that? What are the things that we should think about? And we're jumping into a demo here where we can talk about some data sets that Databricks provides. So in this demo, we'll be talking about the Databricks marketplace, looking at how we can access data sets, review the licensing information for it, and then how to ingest that into our Databricks environment. All right, so we just talked about evaluation when it comes to generative AI applications. We also talked about the challenge when it comes to evaluation, when it comes to control that a lot of these models will show bias and all these other concerns that we have. So it's really important in order to get those models perform well. We talked about how we can approach it from a systematic design standpoint with things like RAG, as well as multi-stage reasoning, but ultimately at some point in order to get good models and good performance, we need good data sets to either use to evaluate our models performance against or to go and use to train new models or fine-tune models. Right, so really what we're going to do in this demo is not really about code, but more about looking at data sets and understanding kind of licensing and copyright and things around that and understand that really well because when it comes to enterprise, the data that we use is very important in the licensing and the concerns around that are very important. Right, so in this demo we're going to focus about reviewing licensing associated with various data sets that we might want to use for our models, right, either for training or evaluation, and then we'll also want to go and understand that. So really end of this demo, recognize the potential legal concerns over data sets that we use for AI models and then look at the data sets that are available inside the data bricks platform through the data bricks marketplace, and then ultimately you would also want to go and assess your legal council, right, all these different data sets have different licensing around them. All right, so to go and get started, there's not really any code that we need to run here, but in the demo we're going to go to the marketplace, we're going to look at two different data sets, right, so one that would be okay for our application, and then we're going to look one that would not be okay for us. We're going to go into the data bricks marketplace and look at that in the nice thing about the different marketplaces instead of us having to go out and try to find these data sets or collect them ourselves. A lot of third-party providers have already done that hard work for us, and they've actually provided it as a asset that we can just go and leverage inside the marketplace, right, it's just a data set that we can download and import into our environment, right, that's really helpful because it makes things a little bit easier and faster for us, right, that's great. Two main reasons we might want to use it if we're looking at rag applications, it might bring in additional reference information to improve our rag applications, or it might be good use for training, things like that, so from this. So the first data set we're going to look at is from bright data, it's the Amazon reviews data set. So to find this data set, we need to go to the marketplace, and then when we go there, we can filter the product, the tables, and then we can look at the provider of bright data, and then we can go look at this specific data set, though Amazon Vesteller products, review products data set, though I already have it open, but let's just show you how to get there if you were to go and find this yourself. So let's go and do that. So on the sidebar, you can see marketplace, good open up a tab that looks like this, right, once we see that, we can see here all the third parties that have built data sets and provided it to us, right, you can see there's also shutter stock here, though we can go and look at products, and the one that we're looking for here in particular's tables, and then we're going to filter it by provider, I believe it was bright data I mentioned earlier. The bright data, and then you can see here, bright data has a whole bunch of data sets. Now, the one that we're looking for here is, Amazon, so let's go and search Amazon, and you can see here's that bright set data set, right, so you can see here this data set includes thousands, thousand rows, for more records, please contact provider. So it's really like a sample data set that we have here, and this is the Vesteller's data set, so key data points, it has brand product, Vesteller ranking, product category seller, price reviews, you can see a lot of rich information here that we can use, but it gives us examples of things that we can use it for, so like competitive analysis, trend tracking, it's more like real-time sentiment monitoring, better pricing, so it looks like a couple different use case sets that's cool, that they provide us some examples of that, right, and then more details into the data set itself, right, but one thing that we really want to know here is the licensing, so typically that's at the bottom, so here we can see notebooks for it, and sometimes it's at the bottom of the link, in this case I think we can go to the license page, so you can see here the bright data license page, right, so this is where you would want to go and work with your legal team to understand licensing and determine this works for you. So once you work with your licensing team and you determine if it works or not, then we can move to the next step, and one of the next step is to import this data into our workspace, right, and that's really easy to go and do, actually I already imported it earlier, right, but if you have a product that you haven't seen before, there will be this option to import into, and I'll show this for the next data set, but here I already have it imported, so we can go take a look at it, so let's go to open that up, so the cool thing you'll notice is that really tightly integrated with Databricks, it just gets imported as another table under a catalog, so you can see here the bright data Amazon best seller's data set, and then we have our data sets under there, and you can see here all the properties, right, so it's just a table that we can use, right, we have some sample data, so here we can actually take a look at what it looks like, you can see here, titles, different products that we can see, we can see the brand, the description of the product, a lot of other information as well, availability, pricing, review counts, and things like that, so pretty cool, right, really nice little data set that we could use if, especially if we were trying to, in online retail and things like that, we might want to use, right, okay, so that's the Amazon kind of best sellers data set from bright data, I encourage everyone to go and take a look at all the other data sets and stuff, right, but it's one of those data sets that we could go and use, all right, okay, so there's that, let's go and take a look at another one, going back to the lab, right, the product links, we open the licensing, and then we took a look at it, let's go and take a look at another one, the other one that we're going to look at is from ReArc, and ReArc, we're going to be looking at the personal information data set, income data set, and that's from Fred, right, so that's what we're going to do, we're going to pull that in, and we're going to go and look at that data set, right, so I actually haven't already preloaded the page for it, so here's the ReArc personal income, Fred data set, you can see the information of the data sources here, right, so this sources personal income data, right, you can see I was updated monthly, that we have, we can look at that there, we can look at getting instant access, the other one was already imported, so here, this is what it would look like to import the data set, so here we have that, we can bring it in, I can bring it on to Databricks here, all right, give it a name, it's like someone else on my team has already imported it, and then I can click this to agree to the terms and condition, but one thing that we want to look at is maybe look at the licensing here, looks like terms and service, right, from ReArc, and this would be same thing, you would want to go and look at this to see if that works with your legal team, right, okay, you have two data sets, let's actually import that one, sorry, let me go and open that up again, all right, I lost that page, let me open up again, this is it, so we can import it in, I think someone's already imported it, so let me go and try to find that in our catalog, so then we don't have to reload it again, so let me go to the catalog, so here's how you would find it, so here you can see someone's already loaded it up before, so here's that data set, and here's our catalog, our data here, and you can see the information, so it looks like it only has two columns, we can look at the sample data, I don't have permissions to see it here, so in this case, nothing that I can see, you can import it and take a look at it yourself, but we can see here it just includes information about personal income and the time, right, for it, right, okay, so with that, we took a look at two data sets, we looked at how it is to get instant access to it, and really the main thing is, Databricks makes this really easy to go and import data sets from third party providers, and it's really important that part of that is also understanding the legal license around each of those data sets, right, so just something to be aware about when you're working with that out there, when building generative AI applications or training them on those days,

---

## Timestamped Segments

**[00:00]** So let's go and start with one that we can talk about which is licensing that we mentioned, right?

**[00:04]** So when it comes to licensing, how do we go and understand that?

**[00:07]** What are the things that we should think about?

**[00:09]** And we're jumping into a demo here where we can talk about some data sets that Databricks provides.

**[00:13]** So in this demo, we'll be talking about the Databricks marketplace,

**[00:16]** looking at how we can access data sets, review the licensing information for it,

**[00:21]** and then how to ingest that into our Databricks environment.

**[00:25]** All right, so we just talked about evaluation when it comes to generative AI applications.

**[00:32]** We also talked about the challenge when it comes to evaluation, when it comes to

**[00:36]** control that a lot of these models will show bias and all these other concerns that we have.

**[00:43]** So it's really important in order to get those models perform well.

**[00:47]** We talked about how we can approach it from a systematic design standpoint with things like RAG,

**[00:52]** as well as multi-stage reasoning, but ultimately at some point in order to get good models and

**[00:57]** good performance, we need good data sets to either use to evaluate our models performance against

**[01:04]** or to go and use to train new models or fine-tune models.

**[01:09]** Right, so really what we're going to do in this demo is not really about code, but more about

**[01:14]** looking at data sets and understanding kind of licensing and copyright and things around that

**[01:19]** and understand that really well because when it comes to enterprise, the data that we use is

**[01:24]** very important in the licensing and the concerns around that are very important.

**[01:28]** Right, so in this demo we're going to focus about reviewing licensing associated with various

**[01:32]** data sets that we might want to use for our models, right, either for training or evaluation,

**[01:37]** and then we'll also want to go and understand that.

**[01:40]** So really end of this demo, recognize the potential legal concerns over data sets that we use for

**[01:45]** AI models and then look at the data sets that are available inside the data bricks platform through

**[01:50]** the data bricks marketplace, and then ultimately you would also want to go and assess your legal

**[01:55]** council, right, all these different data sets have different licensing around them.

**[02:00]** All right, so to go and get started, there's not really any code that we need to run here,

**[02:04]** but in the demo we're going to go to the marketplace, we're going to look at two different data sets,

**[02:08]** right, so one that would be okay for our application, and then we're going to look one that would

**[02:12]** not be okay for us. We're going to go into the data bricks marketplace and look at that in the

**[02:17]** nice thing about the different marketplaces instead of us having to go out and try to find these data

**[02:21]** sets or collect them ourselves. A lot of third-party providers have already done that hard work for us,

**[02:27]** and they've actually provided it as a asset that we can just go and leverage inside the marketplace,

**[02:32]** right, it's just a data set that we can download and import into our environment, right, that's really

**[02:37]** helpful because it makes things a little bit easier and faster for us, right, that's great.

**[02:40]** Two main reasons we might want to use it if we're looking at rag applications, it might bring in

**[02:44]** additional reference information to improve our rag applications, or it might be good use for training,

**[02:49]** things like that, so from this. So the first data set we're going to look at is from bright data,

**[02:55]** it's the Amazon reviews data set. So to find this data set, we need to go to the marketplace,

**[03:00]** and then when we go there, we can filter the product, the tables, and then we can look at the provider

**[03:04]** of bright data, and then we can go look at this specific data set, though Amazon Vesteller products,

**[03:09]** review products data set, though I already have it open, but let's just show you how to get there

**[03:13]** if you were to go and find this yourself. So let's go and do that. So on the sidebar, you can see marketplace,

**[03:18]** good open up a tab that looks like this, right, once we see that, we can see here all the third parties

**[03:24]** that have built data sets and provided it to us, right, you can see there's also shutter stock here,

**[03:29]** though we can go and look at products, and the one that we're looking for here in particular's

**[03:33]** tables, and then we're going to filter it by provider, I believe it was bright data I mentioned earlier.

**[03:38]** The bright data, and then you can see here, bright data has a whole bunch of data sets. Now,

**[03:42]** the one that we're looking for here is, Amazon, so let's go and search Amazon, and you can see here's

**[03:48]** that bright set data set, right, so you can see here this data set includes thousands, thousand rows,

**[03:54]** for more records, please contact provider. So it's really like a sample data set that we have here,

**[03:58]** and this is the Vesteller's data set, so key data points, it has brand product,

**[04:03]** Vesteller ranking, product category seller, price reviews, you can see a lot of

**[04:08]** rich information here that we can use, but it gives us examples of things that we can use it for,

**[04:13]** so like competitive analysis, trend tracking, it's more like real-time sentiment monitoring,

**[04:20]** better pricing, so it looks like a couple different use case sets that's cool, that they provide us

**[04:23]** some examples of that, right, and then more details into the data set itself, right, but one thing

**[04:29]** that we really want to know here is the licensing, so typically that's at the bottom,

**[04:34]** so here we can see notebooks for it, and sometimes it's at the bottom of the link, in this case I think

**[04:44]** we can go to the license page, so you can see here the bright data license page, right, so this is where

**[04:50]** you would want to go and work with your legal team to understand licensing and determine this

**[04:54]** works for you. So once you work with your licensing team and you determine if it works or not,

**[05:00]** then we can move to the next step, and one of the next step is to import this data into our

**[05:06]** workspace, right, and that's really easy to go and do, actually I already imported it earlier,

**[05:09]** right, but if you have a product that you haven't seen before, there will be this option to import into,

**[05:15]** and I'll show this for the next data set, but here I already have it imported, so we can go take a look at

**[05:19]** it, so let's go to open that up, so the cool thing you'll notice is that really tightly integrated with

**[05:23]** Databricks, it just gets imported as another table under a catalog, so you can see here the bright data

**[05:28]** Amazon best seller's data set, and then we have our data sets under there, and you can see here all

**[05:33]** the properties, right, so it's just a table that we can use, right, we have some sample data, so here

**[05:39]** we can actually take a look at what it looks like, you can see here, titles, different products that we can

**[05:44]** see, we can see the brand, the description of the product, a lot of other information as well,

**[05:50]** availability, pricing, review counts, and things like that, so pretty cool, right, really nice little

**[05:57]** data set that we could use if, especially if we were trying to, in online retail and things like that,

**[06:01]** we might want to use, right, okay, so that's the Amazon kind of best sellers data set from bright data,

**[06:09]** I encourage everyone to go and take a look at all the other data sets and stuff, right, but it's one

**[06:13]** of those data sets that we could go and use, all right, okay, so there's that, let's go and take a look at

**[06:19]** another one, going back to the lab, right, the product links, we open the licensing, and then we took a

**[06:25]** look at it, let's go and take a look at another one, the other one that we're going to look at is from

**[06:29]** ReArc, and ReArc, we're going to be looking at the personal information data set, income data set,

**[06:35]** and that's from Fred, right, so that's what we're going to do, we're going to pull that in, and we're

**[06:39]** going to go and look at that data set, right, so I actually haven't already preloaded the page for it,

**[06:43]** so here's the ReArc personal income, Fred data set, you can see the information of the data sources

**[06:48]** here, right, so this sources personal income data, right, you can see I was updated monthly,

**[06:55]** that we have, we can look at that there, we can look at getting instant access, the other one was

**[07:00]** already imported, so here, this is what it would look like to import the data set, so here we have that,

**[07:04]** we can bring it in, I can bring it on to Databricks here, all right, give it a name, it's like someone

**[07:10]** else on my team has already imported it, and then I can click this to agree to the terms and condition,

**[07:15]** but one thing that we want to look at is maybe look at the licensing here, looks like terms and

**[07:21]** service, right, from ReArc, and this would be same thing, you would want to go and look at this

**[07:27]** to see if that works with your legal team, right, okay, you have two data sets, let's actually import

**[07:34]** that one, sorry, let me go and open that up again, all right, I lost that page, let me open up again,

**[07:48]** this is it, so we can import it in, I think someone's already imported it, so let me go and try to

**[07:53]** find that in our catalog, so then we don't have to reload it again, so let me go to the catalog,

**[07:59]** so here's how you would find it, so here you can see someone's already loaded it up before, so here's

**[08:03]** that data set, and here's our catalog, our data here, and you can see the information, so it looks like

**[08:10]** it only has two columns, we can look at the sample data, I don't have permissions to see it here,

**[08:15]** so in this case, nothing that I can see, you can import it and take a look at it yourself,

**[08:20]** but we can see here it just includes information about personal income and the time, right, for it,

**[08:28]** right, okay, so with that, we took a look at two data sets, we looked at how it is to get

**[08:34]** instant access to it, and really the main thing is, Databricks makes this really easy to go and

**[08:40]** import data sets from third party providers, and it's really important that part of that is also

**[08:45]** understanding the legal license around each of those data sets, right, so just something to be

**[08:51]** aware about when you're working with that out there, when building generative AI applications or

**[08:55]** training them on those days,

