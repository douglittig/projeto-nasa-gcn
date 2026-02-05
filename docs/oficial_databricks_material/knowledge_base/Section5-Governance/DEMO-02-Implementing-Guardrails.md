# Demo Imple

**Source:** `Generative AI Application Evaluation and Governance - Demo Imple.mp4`
**Duration:** 09:52
**Language:** en (detected with 100.0% confidence)

---

## Full Transcription

So the first demo, we're going to be talking about implementing AI guard rails, right? Except in this demo, instead of using prompt engineering, we're going to be talking about how we can do this via a large language model, in this case, with LamaGuard, right? So we're going to be taking LamaGuard from the neighbor's marketplace. We'll be deploying that into our environment. And then once we have that, we'll be testing that model with guard rails and then we'll customize the guard rails with LamaGuard with our own custom taxonomy and then integrate that with a chat model. So let's jump into a demo. We talked already about AI security and we talked about guard rails and we talked about the built-in features in Databricks of how we can go and use the safety filter or prompt engineering to build some of those capabilities, right? Now what happens if you want to go and build your own guardrail, right, or build your own model to go and do that? So the idea here is using a language model-based guardrail versus trying to leverage the prompt or the safety API as a way to go and do that. So in this case, we're going to be showing how we can use LamaGuard to act as a guardrail and how do we integrate that into our chat model. So that's what we're doing here, focusing on employing guard rails for a simple generative AI application. By the end of this demo, we'll talk about kind of why you need guard rails, which we've discussed before, right, how do we need it for a given response and then how we can use an Llem to go and do that for us, right? That's what we'll be doing here. Yeah, I ran this notebook again before. We have our requirements and our classroom setup that we always need to run to setup our configurations and everything. That's all good to go. And in this demo, we're going to go and use LamaGuard, understand how LamaGuard works and then integrate that into our chat. So step one is we need to go in implement LMB guardrail using LamaGuard. So if you're not familiar with LamaGuard, we can go and take a look at that. So let me go to the marketplace. So we'll open up the marketplace and in there, we have models, right? And the model we're looking for here is LamaGuard. Great. That should pop up our LamaGuard model. And you can see here, the LamaGuard is an open source model that is developed by Metta. And you can go and use it to go and build a guardrail, right? So that's the model that we're going to use here. So it's a seven billion parameter model that we have. So this is the model. You can read into it. We're going to talk about this in a little bit. And that's out there that we can import into our environment to go and deploy. So I've already actually did that. I've actually taken it out, brought it into my environment and made it ready to deploy. So you could actually see I have it deployed here in my serving endpoint as this model. That's this endpoint. And then we have this is the model that actually imported. So here it is inside the catalog, the model that I have. Anyway, so we have that. I've brought it into the environment. It's deployed to a model serving endpoint. I did this at a time because it does take quite a while. Sometimes you can take up the 30 minutes because it's bringing up infrastructure, deploying the model, doing all this stuff behind the scenes for you. But in this case, it's already deployed for me. Right. That's deployed. This is the name of the model. It's deployed as this endpoint. That's already there. We're good to go. And to use Lomogard, we're going to set up a starting point to script for unsafe categories. In this case, unsafe content is anything that maps to this. If it promotes violence in any way, anything explicit, criminal activity, controlled substances or self-harm or suicide. So it detects any of that inside of the response of the model or the user input. Then it's good to define this as unsafe is the idea that what we want to go do. If it sees any of this, that's what we want to do. Right. So now that we have that, we're going to go and deploy the model and take a use of it. The model's already been deployed. So in this case, we're setting up to do a query against it. Right. So to query Lomogard, we're going to define the chat message and then the categories. And then here's a little bit of our prompt that we're going to go and send it. So task, check for unsafe content and agent messages and conversations to our safety policy. Here's our policy and then here's our chat conversation. Ride your safety estimate for the agent in the above conversation. First, the line must read safe unsafe unsafe unsafe. The second line must include conversation of the violated categories. Right. So we have that and then we pass that over to the model model that processes the text and then gives us a response hopefully in the structure. Right. And then we extract that information out that we can then use. Right. So just doing some text splitting here. Right. So basically defining how we pass the chat data and the categorization the unsafe categorization data to the model and the model can use that to then process it. So we have that. So using Lomogard, here's an example once we have defined that, how we use it. So here's safe example, the usual user I want to love and we pass it through. And in this case, it returns back. It's true and no category with that. So pretty straightforward here. Right. Because it's a pretty safe message. Right. So here's an example unsafe message. So role user, how can I rob a bank? And in this case, it is unsafe. Right. This false saying that is unsafe. It's not safe here. Right. And then the category maps to which is a one. Right. So based on this, does anybody know what this means? So it's basically mapping to our categorization. So if I go back to the top, mapping to this saying that's unsafe content. Right. So it's mapping and this is everything that defines unsafe content. Right. Pretty straightforward. That's how we can use Lomogard. You can see how we can define these guard rails very easily and how Lomogard can use that in context to go and give a categorization of it's safe or unsafe. Right. So let's go and do another example. This example is a little bit different where the first two is really processing the user input. This one instead is processing the output. Right. This the user input is I want to love and for some reason a model doesn't say that is great. I want to love to. Right. So in this case, we have safe and safe outputs, safe input and safe output. So the model here says it's true. Right. And there's no issue with it. Right. And then here is an example where you have safe input, but unsafe output. Right. And I think the only way to rob a bank is to work with Robinhood. And you can see here it is unsafe and tells us unsafe categories as well. You can see how here you can be used not only just for the user input, but also be used to filter the output. So you can imagine using Lomogard both as input and output. So very common is using it at the beginning before feeding it to your primary LLM and again afterwards. Okay. So that's great. Now these outputs aren't very useful with telling us why it is unsafe because we put everything into one category. So let's customize our Lomogard guard rails and make that texonomy a little bit better. Right. So that's what we're going to do. So that's what we're going to do here. Instead, we're going to define each of those categories. Right. So violence and hate, sexual content, criminal planning, guns and illegal activity, regulated control substances. Right. And financial sensitive data. Right. So you can see here a lot more description in categorization. And with this, hopefully that gives us better output when we do classified as unsafe. Right. So that's going to be the goal. So with that, we're going to feed that into the model. So now if we go and feed that, right, hopefully we get a different result. Right. So unsafe user chat, unsafe categories, and you can see here in maps to three, right. And three here is a little bit more helpful because it's mapping to this particular category. Right. So a lot more useful for us versus the other one, which is just a catch all. Right. Okay. So we talked about how we can use Lomogard to basically classify safe and unsafe content. We talked about how we can customize Lomogard with a taxonomy to get us more detailed reasons why it was unsafe. So what do they look like to integrate with a chat model. So that's what we're going to do here in step three. We're actually going to integrate Lomogard with a chat model. So very common is to create a pipeline where we have model acting as a guardrail as input. Then the model that actually processes the user question. And then it acting again as a guardrail has X. So in this case, we're going to use Lomogard in conjunction with our primary model, which is in this case, we're going to use Mectrol as our primary model. And we're going to go and define the query for the chat. So here's the function to go and talk to Mectrol and then point and passing through the messages. And then here, we're going to go and define another chat version that is a safe version of it. So what it's going to do is it's first going to send it to Lomogard, and it's going to check if it's safe or not. If it is, then it's going to send it to the model. And then the model is going to send some output. We're going to then also check it again on output with Lomogard. And if it's good, we'll send out the response. You can see here, if it doesn't pass, it's going to say user prompt, classified as play, fail safety measures, or model responses, classified as blank, fail safety measures. So we get that there. So continuing down, let's go and give the parsing of the category here to help get the taxonomy. So instead of the numbers, getting the name of those numbers, and then here, we have an example of that. Here's a safe user chat. So user, I want love, and then running a query. So you can see here, the Llem's response, and the output. And then here is an example with how can I rob a bank? And you can see here, user prompt, classified as criminal planning, fail safety measures. And we can see that there. And then you can see here, us passing through an example of unsafe, right? And you can see here that unsafe check as well that we got. So you can see there kind of example how we can implement guard rails here with another custom model. And you can see how we can use Lomogard to really customize what we wanted to check. All right. So that wraps that up.

---

## Timestamped Segments

**[00:00]** So the first demo, we're going to be talking about implementing AI guard rails, right?

**[00:04]** Except in this demo, instead of using prompt engineering, we're going to be talking about how we can

**[00:08]** do this via a large language model, in this case, with LamaGuard, right? So we're going to be taking

**[00:13]** LamaGuard from the neighbor's marketplace. We'll be deploying that into our environment.

**[00:18]** And then once we have that, we'll be testing that model with guard rails and then we'll customize

**[00:22]** the guard rails with LamaGuard with our own custom taxonomy and then integrate that with a chat model.

**[00:28]** So let's jump into a demo. We talked already about AI security and we talked about guard rails

**[00:34]** and we talked about the built-in features in Databricks of how we can go and use the safety filter

**[00:41]** or prompt engineering to build some of those capabilities, right? Now what happens if you want to

**[00:47]** go and build your own guardrail, right, or build your own model to go and do that? So the idea here

**[00:52]** is using a language model-based guardrail versus trying to leverage the prompt or the safety API

**[01:00]** as a way to go and do that. So in this case, we're going to be showing how we can use LamaGuard to act

**[01:05]** as a guardrail and how do we integrate that into our chat model. So that's what we're doing here,

**[01:10]** focusing on employing guard rails for a simple generative AI application.

**[01:14]** By the end of this demo, we'll talk about kind of why you need guard rails, which we've discussed

**[01:18]** before, right, how do we need it for a given response and then how we can use an Llem to go and do

**[01:24]** that for us, right? That's what we'll be doing here. Yeah, I ran this notebook again before. We have

**[01:30]** our requirements and our classroom setup that we always need to run to setup our configurations

**[01:36]** and everything. That's all good to go. And in this demo, we're going to go and use LamaGuard,

**[01:41]** understand how LamaGuard works and then integrate that into our chat. So step one is we need to go

**[01:47]** in implement LMB guardrail using LamaGuard. So if you're not familiar with LamaGuard, we can go and

**[01:52]** take a look at that. So let me go to the marketplace. So we'll open up the marketplace and in there,

**[01:59]** we have models, right? And the model we're looking for here is LamaGuard. Great. That should pop up

**[02:07]** our LamaGuard model. And you can see here, the LamaGuard is an open source model that is developed

**[02:13]** by Metta. And you can go and use it to go and build a guardrail, right? So that's the model that

**[02:19]** we're going to use here. So it's a seven billion parameter model that we have. So this is the model.

**[02:24]** You can read into it. We're going to talk about this in a little bit. And that's out there that we can

**[02:29]** import into our environment to go and deploy. So I've already actually did that. I've actually

**[02:33]** taken it out, brought it into my environment and made it ready to deploy. So you could actually see

**[02:38]** I have it deployed here in my serving endpoint as this model. That's this endpoint. And then we have

**[02:45]** this is the model that actually imported. So here it is inside the catalog, the model that I have.

**[02:50]** Anyway, so we have that. I've brought it into the environment. It's deployed to a model serving

**[02:55]** endpoint. I did this at a time because it does take quite a while. Sometimes you can take up the 30 minutes

**[02:59]** because it's bringing up infrastructure, deploying the model, doing all this stuff behind the scenes

**[03:04]** for you. But in this case, it's already deployed for me. Right. That's deployed. This is the name of

**[03:08]** the model. It's deployed as this endpoint. That's already there. We're good to go. And to use Lomogard,

**[03:14]** we're going to set up a starting point to script for unsafe categories. In this case, unsafe content

**[03:19]** is anything that maps to this. If it promotes violence in any way, anything explicit, criminal activity,

**[03:27]** controlled substances or self-harm or suicide. So it detects any of that inside of the response of

**[03:33]** the model or the user input. Then it's good to define this as unsafe is the idea that what we want to

**[03:38]** go do. If it sees any of this, that's what we want to do. Right. So now that we have that, we're going to go

**[03:42]** and deploy the model and take a use of it. The model's already been deployed. So in this case, we're

**[03:47]** setting up to do a query against it. Right. So to query Lomogard, we're going to define the chat message

**[03:53]** and then the categories. And then here's a little bit of our prompt that we're going to go and send it.

**[03:59]** So task, check for unsafe content and agent messages and conversations to our safety policy.

**[04:04]** Here's our policy and then here's our chat conversation. Ride your safety estimate for the agent

**[04:09]** in the above conversation. First, the line must read safe unsafe unsafe unsafe. The second line must

**[04:14]** include conversation of the violated categories. Right. So we have that and then we pass that

**[04:18]** over to the model model that processes the text and then gives us a response hopefully in the structure.

**[04:24]** Right. And then we extract that information out that we can then use. Right. So just doing some text

**[04:28]** splitting here. Right. So basically defining how we pass the chat data and the categorization the

**[04:35]** unsafe categorization data to the model and the model can use that to then process it. So we have that.

**[04:41]** So using Lomogard, here's an example once we have defined that, how we use it. So here's safe example,

**[04:46]** the usual user I want to love and we pass it through. And in this case, it returns back. It's true

**[04:52]** and no category with that. So pretty straightforward here. Right. Because it's a pretty safe

**[04:58]** message. Right. So here's an example unsafe message. So role user, how can I rob a bank? And in this

**[05:03]** case, it is unsafe. Right. This false saying that is unsafe. It's not safe here. Right. And then

**[05:09]** the category maps to which is a one. Right. So based on this, does anybody know what this means?

**[05:14]** So it's basically mapping to our categorization. So if I go back to the top,

**[05:19]** mapping to this saying that's unsafe content. Right. So it's mapping and this is everything that defines

**[05:24]** unsafe content. Right. Pretty straightforward. That's how we can use Lomogard. You can see how we can

**[05:29]** define these guard rails very easily and how Lomogard can use that in context to go and give a

**[05:37]** categorization of it's safe or unsafe. Right. So let's go and do another example. This example is a

**[05:42]** little bit different where the first two is really processing the user input. This one instead is

**[05:47]** processing the output. Right. This the user input is I want to love and for some reason a model

**[05:53]** doesn't say that is great. I want to love to. Right. So in this case, we have safe and safe outputs,

**[05:58]** safe input and safe output. So the model here says it's true. Right. And there's no issue with it.

**[06:04]** Right. And then here is an example where you have safe input, but unsafe output. Right. And I think

**[06:08]** the only way to rob a bank is to work with Robinhood. And you can see here it is unsafe and tells us

**[06:15]** unsafe categories as well. You can see how here you can be used not only just for the user input,

**[06:20]** but also be used to filter the output. So you can imagine using Lomogard both as input and output.

**[06:24]** So very common is using it at the beginning before feeding it to your primary LLM and again afterwards.

**[06:32]** Okay. So that's great. Now these outputs aren't very useful with telling us why it is unsafe because

**[06:38]** we put everything into one category. So let's customize our Lomogard guard rails and make that

**[06:43]** texonomy a little bit better. Right. So that's what we're going to do. So that's what we're going

**[06:48]** to do here. Instead, we're going to define each of those categories. Right. So violence and hate,

**[06:52]** sexual content, criminal planning, guns and illegal activity, regulated control substances. Right.

**[06:58]** And financial sensitive data. Right. So you can see here a lot more description in categorization.

**[07:04]** And with this, hopefully that gives us better output when we do classified as unsafe. Right. So that's

**[07:10]** going to be the goal. So with that, we're going to feed that into the model. So now if we go and feed

**[07:14]** that, right, hopefully we get a different result. Right. So unsafe user chat, unsafe categories,

**[07:18]** and you can see here in maps to three, right. And three here is a little bit more helpful because it's

**[07:23]** mapping to this particular category. Right. So a lot more useful for us versus the other one,

**[07:28]** which is just a catch all. Right. Okay. So we talked about how we can use Lomogard to basically classify

**[07:38]** safe and unsafe content. We talked about how we can customize Lomogard with a taxonomy to get us

**[07:44]** more detailed reasons why it was unsafe. So what do they look like to integrate with a chat model.

**[07:50]** So that's what we're going to do here in step three. We're actually going to integrate Lomogard

**[07:52]** with a chat model. So very common is to create a pipeline where we have model acting as a guardrail

**[07:57]** as input. Then the model that actually processes the user question. And then it acting again as a

**[08:03]** guardrail has X. So in this case, we're going to use Lomogard in conjunction with our primary model,

**[08:08]** which is in this case, we're going to use Mectrol as our primary model. And we're going to go and

**[08:12]** define the query for the chat. So here's the function to go and talk to Mectrol and then point and

**[08:18]** passing through the messages. And then here, we're going to go and define another chat version that

**[08:24]** is a safe version of it. So what it's going to do is it's first going to send it to Lomogard,

**[08:28]** and it's going to check if it's safe or not. If it is, then it's going to send it to the model.

**[08:32]** And then the model is going to send some output. We're going to then also check it again on output

**[08:36]** with Lomogard. And if it's good, we'll send out the response. You can see here, if it doesn't pass,

**[08:42]** it's going to say user prompt, classified as play, fail safety measures, or model responses,

**[08:47]** classified as blank, fail safety measures. So we get that there. So continuing down, let's go

**[08:53]** and give the parsing of the category here to help get the taxonomy. So instead of the numbers,

**[09:00]** getting the name of those numbers, and then here, we have an example of that. Here's a safe

**[09:05]** user chat. So user, I want love, and then running a query. So you can see here, the Llem's response,

**[09:13]** and the output. And then here is an example with how can I rob a bank? And you can see here,

**[09:19]** user prompt, classified as criminal planning, fail safety measures. And we can see that there. And then

**[09:25]** you can see here, us passing through an example of unsafe, right? And you can see here that unsafe

**[09:33]** check as well that we got. So you can see there kind of example how we can implement guard rails

**[09:39]** here with another custom model. And you can see how we can use Lomogard to really customize what

**[09:44]** we wanted to check. All right. So that wraps that up.

