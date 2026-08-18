'''
This module defines the DAG : Directly acyclic graph

START -> index_video_node -> audit_content_node -> END
'''

from langgraph.graph import StateGraph, END
from backend.src.graph.state import VideoAuditState

from backend.src.graph.nodes import (
	index_video_node,
   audio_content_node
)

def create_graph():
    # Return :  Compliled Graph: runnable graph object for execution
    workflow =  StateGraph(VideoAuditState)
    workflow.add_node("indexer", index_video_node)
    workflow.add_node("auditor", audio_content_node)
    
    #Entry Point
    workflow.set_entry_point("indexer")
    
    #Edges
    workflow.add_edge("indexer", "auditor")
    # once audit is complete the workflow will end
    workflow.add_edge("auditor", END)
    
    #Compile the graph
    app =  workflow.compile()
    return app
    
app = create_graph()    