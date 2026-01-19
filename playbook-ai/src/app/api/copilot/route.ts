import {
  CopilotRuntime,
  ExperimentalEmptyAdapter,
  copilotRuntimeNextJSAppRouterEndpoint,
} from "@copilotkit/runtime";
import { LangGraphAgent } from "@ag-ui/langgraph";
import { NextRequest } from "next/server";

// 1. Using EmptyAdapter because the Python server handles LLM calls
const serviceAdapter = new ExperimentalEmptyAdapter();

// 2. Configure the Runtime with the deployment URL from langgraph dev
const runtime = new CopilotRuntime({
  agents: {
    "basketball_coach": new LangGraphAgent({
      deploymentUrl: process.env.LANGGRAPH_DEPLOYMENT_URL || "http://127.0.0.1:8000",
      graphId: "basketball_coach",
    }) as any, // Type assertion to resolve compatibility issues
  }
});

// 3. Configure the Endpoint
export const POST = async (req: NextRequest) => {
  const { handleRequest } = copilotRuntimeNextJSAppRouterEndpoint({
    runtime,
    serviceAdapter,
    // Ensure this matches the runtimeUrl in CopilotKit Provider
    endpoint: "/api/copilot",
  });

  return handleRequest(req);
};