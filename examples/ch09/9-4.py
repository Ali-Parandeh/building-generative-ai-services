domain = "Building GenAI Services"

criteria = """
Assess the presence of explicit guidelines for API development for GenAI models.
The content should contain only general evergreen advice
not specific tools and libraries to use
"""

steps = """
1. Read the content and the criteria carefully.
2. Assess how much explicit guidelines for API development
for GenAI models is contained in the content.
3. Assign an advice score from 1 to 5,
with 1 being evergreen general advice and 5 containing explicit
mentions of various tools and libraries to use.
"""


f"""
You are a moderation assistant.
Your role is to detect content about {domain} in the text provided,
and mark the severity of that content.

## {domain}

### Criteria

{criteria}

### Instructions

{steps}

### Content

<content>

### Evaluation (score only!)
"""
