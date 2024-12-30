from fastapi import FastAPI, HTTPException
import requests

from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langchain_core.messages.system import SystemMessage
from langchain_core.prompts.chat import SystemMessagePromptTemplate
from langchain_core.prompts import PromptTemplate
from langchain import hub
from langchain.agents import create_tool_calling_agent, AgentExecutor, create_react_agent

app = FastAPI()

template = """You are a banking assistant. Answer the customer queries as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}"""


@tool
def getComplaintStatus(customerId: int, complaintId: str) -> str:
    """Returns the complaint status for a customer and complaint id"""
    print("getComplaintStatus")
    complaint = [{"customerId": 123, "complaintId": "abcdef", "status": "pending", "description": "complaint description"}, {"customerId": 123, "complaintId": "ghefds", "status": "resolved", "description": "complaint description"}]
    for c in complaint:
        if c["customerId"] == customerId and c["complaintId"] == complaintId:
            return c["status"]
    return "Complaint not found for given customer id {{customerId}} and complaint id {{complaintId}}"

@tool
def getFinanceSummary(customerId: int) -> str:
    """Returns the finance summary for a customer"""
    print("getFinanceSummary")
    finance = [{"customerId": 123, "balance": 1000, "lastTransaction": "2021-01-01"}, {"customerId": 124, "balance": 2000, "lastTransaction": "2021-01-01"}]
    for f in finance:
        if f["customerId"] == customerId:
            return f
    return "Finance summary not found for given customer id {{customerId}}"

@tool
def getCustomerDetails(customerId: int) -> str:
    """Returns the customer details for a customer id"""
    print("getCustomerDetails")
    customer = [{"customerId": 123, "name": "John Doe", "email": "john.doe@gmail.com"}, {"customerId": 124, "name": "Jane Doe", "email": "jane.doe@gmail.com"}]
    for c in customer:
        if c["customerId"] == customerId:
            return c
    return "Customer details not found for given customer id {{customerId}}"

@tool
def getRecentTransactions(customerId: int, merchant_name: str) -> list:
    """Returns the recent transactions for a customer"""
    print("getRecentTransactions")
    transactions = [{"customerId": 123, "transactionId": 1, "amount": 100, "date": "2021-01-01", "merchantName": "Tesco"}, 
                    {"customerId": 123, "transactionId": 2, "amount": 200, "date": "2021-01-02", "merchantName": "Sainsbury"}, 
                    {"customerId": 123, "transactionId": 3, "amount": 300, "date": "2021-01-03", "merchantName": "Asda"},
                    {"customerId": 123, "transactionId": 4, "amount": 400, "date": "2021-01-04", "merchantName": "Morrisons"},
                    {"customerId": 123, "transactionId": 5, "amount": 500, "date": "2021-01-05", "merchantName": "Lidl"},
                    {"customerId": 123, "transactionId": 6, "amount": 600, "date": "2021-01-06", "merchantName": "Aldi"},
                    {"customerId": 123, "transactionId": 7, "amount": 700, "date": "2021-01-07", "merchantName": "Tesco"},
                    {"customerId": 123, "transactionId": 8, "amount": 800, "date": "2021-01-08", "merchantName": "Iceland"},
                    {"customerId": 123, "transactionId": 9, "amount": 900, "date": "2021-01-09", "merchantName": "Tesco"},
                    {"customerId": 123, "transactionId": 10, "amount": 1000, "date": "2021-01-10", "merchantName": "Tesco"}]
    recent_transactions = []
    for t in transactions:
        if t["customerId"] == customerId and t["merchantName"] == merchant_name:
            recent_transactions.append(t)
    return recent_transactions

tools = [getComplaintStatus, getFinanceSummary, getCustomerDetails, getRecentTransactions]

# llm = ChatOllama(model="llama3-groq-tool-use", temperature=0).bind_tools(tools)

llm = ChatOllama(model="mistral", temperature=0).bind_tools(tools)

prompt = hub.pull("hwchase17/openai-tools-agent")
prompt.messages[0] = SystemMessagePromptTemplate(
    prompt=PromptTemplate(
        input_variables=[],
        input_types={},
        partial_variables={},
        template=(
            "You are a banking assistant. Respond to customer queries accurately using the tools at your disposal. Use the tools to assist customers regarding their spending summary, compliants, recent transactions with bank\n"
            "If you can't confidently answer a query, escalate it to a human agent."
        ),
    )
)

# prompt = PromptTemplate.from_template(template)


prompt.pretty_print()

agent = create_tool_calling_agent(llm, tools, prompt)

# agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)

agent_executor = AgentExecutor(
    agent=agent, tools=tools, verbose=True, handle_parsing_errors=True
)

# agent_executor.invoke({"input": "get the customer details for customer id 123"})


@app.post("/banking-agent/")
async def handle_query(query: str):
    try:
        # Run agent
        response = agent_executor.invoke(
            {"input": query}
        )
        return {"response": response["output"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
