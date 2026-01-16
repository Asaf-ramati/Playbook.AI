from fastapi import FastAPI
import uvicorn
from copilotkit.integrations.fastapi import add_copilotkit_endpoint
from copilotkit import CopilotKitRemoteEndpoint
from graph.workflow import create_graph

app = FastAPI()
graph = create_graph()

add_copilotkit_endpoint(
    app,
    CopilotKitRemoteEndpoint(
        name="basketball_coach",
        description="מאמן כדורסל אישי חכם",
    ),
    path="/copilotkit",
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)