from central_runner import DAGOrchestrator

def test_disconnected():
    print("Testing disconnected graph...")
    dag = DAGOrchestrator()
    dag.add_node("n1", "agent1", "task1")
    dag.add_node("n2", "agent2", "task2")
    # n1 and n2 are disconnected
    levels = dag.get_topological_sort()
    print("Disconnected levels:", levels)

def test_cycle():
    print("Testing cycle...")
    dag = DAGOrchestrator()
    dag.add_node("n1", "agent1", "task1")
    dag.add_node("n2", "agent2", "task2", ["n1"])
    dag.add_node("n3", "agent3", "task3", ["n2"])
    dag.add_edge("n1", "n2")
    dag.add_edge("n2", "n3")
    dag.add_edge("n3", "n1") # cycle!
    try:
        levels = dag.get_topological_sort()
        print("Cycle levels:", levels)
    except ValueError as e:
        print("Caught expected cycle error:", e)

if __name__ == "__main__":
    test_disconnected()
    test_cycle()
