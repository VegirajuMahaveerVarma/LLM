from dataclasses import dataclass

@dataclass(frozen=True)
class KnowledgeItem:
    topic: str
    subject: str
    branch: str
    content: str

KNOWLEDGE=[
    KnowledgeItem("tcp", "Computer Networks", "CSE", "TCP is connection-oriented and provides reliable, ordered delivery using acknowledgements, sequencing, retransmission and congestion control."),
    KnowledgeItem("udp", "Computer Networks", "CSE", "UDP is connectionless and provides a lightweight datagram service without built-in delivery, ordering or retransmission guarantees."),
    KnowledgeItem("backpropagation", "Machine Learning", "CSE", "Backpropagation computes gradients of a loss with respect to neural-network parameters by applying the chain rule from the output toward earlier layers."),
    KnowledgeItem("gradient descent", "Machine Learning", "CSE", "Gradient descent updates parameters in the direction opposite the loss gradient. The learning rate controls the step size."),
    KnowledgeItem("dijkstra", "Algorithms", "CSE", "Dijkstra's algorithm finds shortest paths from a source in a graph with non-negative edge weights, typically using a priority queue."),
    KnowledgeItem("ohms law", "Electrical Engineering", "EEE", "Ohm's law relates voltage, current and resistance as V = I R for an ohmic element under its applicable operating conditions."),
    KnowledgeItem("thermodynamics", "Mechanical Engineering", "ME", "Thermodynamics studies energy, heat, work and the relationships between system properties and processes."),
    KnowledgeItem("control system", "Robotics", "Robotics", "A control system measures or estimates a system state and applies an input to move the system toward a desired behavior."),
]

def retrieve(query:str, branch:str, limit:int=3)->list[KnowledgeItem]:
    words=set(query.lower().replace("?"," ").replace(","," ").split())
    scored=[]
    for item in KNOWLEDGE:
        text=f"{item.topic} {item.subject} {item.content}".lower()
        score=sum(1 for w in words if len(w)>2 and w in text)
        if branch.lower() in item.branch.lower() or item.branch=="CSE":
            score+=1
        if score:
            scored.append((score,item))
    return [item for _,item in sorted(scored,key=lambda x:x[0],reverse=True)[:limit]]
