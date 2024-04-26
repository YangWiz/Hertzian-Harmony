## Hertzian Harmony

### Implementaion Details
FastAPI for the backend
We could launch a simple file system in the path of the name of vml

### Database design
Request a bunch of phone numbers to compose a phone number pool, and create the relations between the phone numbers and the questions numbers (Phone Number 1 <=> question 1, etc), every time we create a new question we just need to combine the related entries: the phone number, questions, vxml files.

Because we don't need to consider the language when voting, we could use many open source text2speech apps to generate the corresponding results.

Flow:
0. The user registers phone number on vovex, so it can add the phone number to the database via web interface.
1. User creates one question, the backend will fetches two avaiable phone numbers, one for yes and another for no.
2. The backend then binds the yes or no vxml with each phone number.
3. The yes or no vxml will submit the yes or no and hang up the phone.
4. The backend needs to add results options to home vxml page.
