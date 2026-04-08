# import google.generativeai as genai
from django.conf import settings
from neo4j import GraphDatabase


# ---------------------------
# CONFIGURATION
# ---------------------------

# Temporarily disabled - causing import errors
# genai.configure(api_key=settings.GEMINI_API_KEY)
# model = genai.GenerativeModel("models/gemini-2.5-flash")

driver = GraphDatabase.driver(
    settings.NEO4J_URI,
    auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
)

PROMPT_TEMPLATE = """
You are an intent parser.

Convert the user input into JSON.

Allowed intent types:
- search_node
- neighbors

Return ONLY valid JSON.
No explanation.

User input:
"{user_text}"
"""


def generate_intent(user_text):
    # Temporarily disabled - model not available
    # prompt = PROMPT_TEMPLATE.format(user_text=user_text)
    # response = model.generate_content(
    #     prompt,
    #     generation_config={
    #         "response_mime_type": "application/json"
    #     }
    # )
    # text = response.text.strip()
    # try:
    #     return json.loads(text)
    # except json.JSONDecodeError:
    #     print("RAW MODEL OUTPUT:", text)
    #     return {"intent": "invalid"}

    # Return a default response for now
    return {"intent": "search_node", "node": user_text}

# ---------------------------
# 2️⃣ INTENT → CYPHER
# ---------------------------

def intent_to_cypher(intent_dict):
    intent_type = intent_dict.get("intent")
    node = (
        intent_dict.get("node")
        or intent_dict.get("entity")
        or intent_dict.get("node_name")
    )

    if not intent_type or not node:
        return None, None

    if intent_type == "neighbors":
        return """
        MATCH (n {name: $name})-[r]-(m)
        RETURN n, r, m
        """, {"name": node}

    if intent_type == "search_node":
        return """
        MATCH (n {name: $name})
        RETURN n
        """, {"name": node}

    return None, None
# ---------------------------
# 3️⃣ RUN CYPHER
# ---------------------------

def run_cypher(query, params):
    if not query:
        return []

    with driver.session() as session:
        result = session.run(query, **params)
        return [record["m"]["name"] for record in result]

# ---------------------------
# 4️⃣ FULL PIPELINE
# ---------------------------

def process_user_query(user_input):
    intent = generate_intent(user_input)
    print("INTENT RAW:", intent)

    query, params = intent_to_cypher(intent)
    print("QUERY:", query)
    print("PARAMS:", params)

    if not query:
        return {"error": "Unsupported intent"}

    result = run_cypher(query, params)

    return {
        "intent": intent,
        "result": result
    }