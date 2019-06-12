Problem Definition

New Era Cap custom cap builder was facing a poor turnaround time for accepting a cap design posted by the customer. The organization wants to spread its grab on a wider spectrum of customers and allow people to upload the logo that they want on the cap. This sounds exciting as human likes to try out things hands-on and the sense of satisfaction jumps quite folds when they can visualize what they want. We enter into a situation where customers post any image possible, they could be licensed images, which cannot be used without the permission of logo owner, they might contain provoking images, which can malign the organization’s reputation or they could be a perfectly legitimate image, which can be printed on the cap. Deciding if the logo is legitimate or not requires a set of teams collaborate and call out a unanimous decision, which generally takes 3-4 weeks depending upon the order backlog. Automating the decision-making process was the task at hand and we decided to do it using a machine learning algorithm to devise the logic of logo detection. We had estimated a reduction of almost 30% decision making time after employing this mechanism.


How did we go about it?

Logo detection or image classification comes in the realm of supervised learning, we approached the organization to give us the images to develop the machine learning algorithm. Due to the compliance issue, the organization refrained from sharing their image list. We then devised a way to scrape the images from the website with the permission of New Era Cap and created the image dataset.

Alpha -1 Design:

We started with identifying image if it was a brand or not a brand, using binary cross entropy loss we trained image classification model using a convoluted neural network with 6 hidden layers to generate an accurate model. We improvised on the model with the inputs from the client through a scheduled weekly meeting.

Alpha -2 Design:

Our next milestone was to create a machine learning model that can provide the name of the team/league with which the input image matches. The business case for this requirement was that giving information regarding whether the logo is a brand or not a brand looks provides a red herring to the user. However, it does not provide any concrete information about the steps the user must take to avoid copyright infringement. Providing the name of the team/league would help determine the root cause of the high likelihood score and then he/she can make changes to their logo and upload it again. This feature was achieved using Canny Edge Detection and some changes to the existing neural network model to emit the team/league name as part of model classification output.

Impediments faced:

Following are few of the impediments faced during the project:
1. Problem: In order to train a neural network model, a huge amount of training data is needed. Due to copyright issues, New Era cannot share its database of existing logos as their logo library consisted of roughly over 100k images. Apart from this, they had many images that were not released to the market.

Solution: We first started by training our neural network model on famous logos such as BMW, Coca Cola, Nike, etc. Using web scraping tools, we extracted around 2000 images. The neural network was then trained on these 2000 images and was fine-tuned for improved performance. Later on, following our discussions with the client, it was decided that we can use the logos that are publicly available on New Era’s website for developing the MVP.

2. Problem: Once the neural network model was able to classify whether an input image was a brand or not a brand, the requirement was to expose this model to the outside world in a user-friendly way wherein customers can upload the image and get the classification (brand/not brand) along with a likelihood score.

Solution: In this case, we needed real-time predictions from the model. Also, we need to come up with a front-end application which will allow the user to upload an image. The front end should be able to pass this image to the model for prediction and display the results of the prediction on the front-end screen. We used Pyflask framework to design a front end application. The architecture was designed in such a way that the model training and predictions can be done on separate servers to avoid any down times.

3. Problem: New Era had a requirement of integrating the model in their existing cap builder workflow. They didn’t want a separate application just for validation purposes.

Solution: The solution to this problem was to decouple the front-end and the backend. The application created in #2 above, needs to be updated to return a JSON response consisting of the likelihood score. This JSON response can then be consumed by the New Era cap builder to perform their own tasks. The application needs to be hosted on an AWS server so that New Era cap builder can call it using the endpoint address.

4. Problem: For Alpha-2 version, it was observed that higher preference was given to the Colors in the logo for calculating the likelihood score rather than the structure of the logo. Due to this, the accuracy of model was not high enough.

Solution: The solution to this problem was to convert the input logo to gray scale. Using a library named “Canny Edge” detection we can extract the structure of the logo. The neural network was then trained using this methodology and we were able to achieve the desired accuracy.

Summary:

The project was highly challenging both from technical as well as functional perspective. The use case was quite relevant to the market as many IT companies struggle with copyright issues and spend tons of legal costs. This application can surely make a huge impact on the existing workflow at New Era. A task that used to take 27 days can now be done within 27 seconds. Apart from the New Era cap builder, the company can leverage this application to clean up their existing database by removing redundant copies of images thereby increasing their storage space.

Overall, it was a good learning experience for the entire team. We received a good amount of exposure to product development and were able to connect top personalities at New Era.
