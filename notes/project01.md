Write a short document, one to two pages. This format answers four questions:
Problem. What task are you automating, and who feels the pain today?
Solution. What will the agent do? Name the inputs, the output shape, and the decisions it makes.
Scope. What’s in, and what’s explicitly out? For brownfield, name the existing system and state that you won’t change it.
Risks. Where could the agent be wrong, and what’s your guard against it?
Add a build sketch: the ADK constructs you expect to use and why. Keep it honest about size. A document that promises a five-agent system you can’t build in the time is worse than one that scopes a single agent well.
On the first day of the capstone, present your design to your instructor. Acting as your architect, they review and sign off on the design before you build, the way an architect or an operations lead would on a real project, checking that:
The scope matches the problem and fits the time
The output shape is concrete enough to validate
The risks are real and have guards
For brownfield, the black-box boundary is clear
You work mainly as a developer, but you own the design and carry some deployment responsibility, so your instructor also probes the architectural considerations below. You get a sign-off or a redirect. Don’t write agent code until you have the sign-off.

Siva idea:
One idea:
AskFedEx is an existing chatbot that uses a FAQ database as its primary knowledge source to answer customer queries. However, the database may not contain answers to every question users ask, resulting in unanswered queries or knowledge gaps.
The idea is to enhance the existing AskFedEx solution using AI agents and tools to identify knowledge gaps and automatically generate new FAQ candidates. When a user asks a question that cannot be answered using the existing FAQ database, an AI agent could analyze the query, search relevant and trusted information sources, draft a suitable answer, and generate a corresponding FAQ entry.
 
The generated FAQ could then go through validation and human approval before being added to the FAQ database, making it available for future customer queries. 

my comment:
AskFedEx existed.
When I read Siva's proposal, I think he's right that the current chatbot may not be very "smart" in the AI sense. My understanding is that it mainly relies on the existing FAQ database. If the answer isn't in that database, the chatbot can't do much beyond saying it doesn't know.
What I think Siva is proposing is more than just storing unanswered questions. The chatbot would:
Log questions it cannot answer.
Identify these as knowledge gaps.
Use AI agents to search trusted sources for relevant information.
Generate a draft answer and a proposed new FAQ entry.
Send that FAQ to a human reviewer for approval.
Add the approved FAQ to the knowledge base so future users can get an answer immediately.
So the system would continuously improve itself by learning where the FAQ content is missing and helping humans build new FAQ entries. In that sense, it becomes a feedback loop that keeps expanding the knowledge base over time ?

I don't think it's hard for 3 or 5 people, and can even be done with 2 perhaps, but of course if I miss anything major, then I'm open for any feedback. But the idea is to focus more on concepts. If you're not comfortable and want to work with 4-5 people, then it's understandable, but i think less is more and we're beyond capable 

we have to decide on roles. I vote Yasin to be the lead , i can try and do the github thing. 
Lead - Owns the project plan, manages scope, presents at approvals, and makes the final Go/No-Go recommendation.
Repository Owner - Manages the Git repository, branching strategy, clean-checkout testing, and final project package.
Evaluation Owner - Owns testing, evaluation scenarios, regression checks, and code review documentation. ( not needed )
Deck Owner - Creates and presents the 5-minute presentation, including problem statement, design decisions, evaluation results, and recommendation.