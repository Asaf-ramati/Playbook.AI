import {
  CopilotRuntime,
  ExperimentalEmptyAdapter,
  copilotRuntimeNextJSAppRouterEndpoint,
} from "@copilotkit/runtime";
import { LangGraphAgent } from "@ag-ui/langgraph"; // הספריה שגרמה לזה לעבוד
import { NextRequest } from "next/server";

// 1. שימוש ב-EmptyAdapter כיוון ששרת ה-Python מנהל את הקריאות ל-LLM
const serviceAdapter = new ExperimentalEmptyAdapter();

// 2. הגדרת ה-Runtime עם הכתובת שהתקבלה מהפקודה langgraph dev
const runtime = new CopilotRuntime({
  agents: {
    "basketball_coach": new LangGraphAgent({
      deploymentUrl: process.env.LANGGRAPH_DEPLOYMENT_URL || "http://127.0.0.1:8000",
      graphId: "basketball_coach",
    }) as any, // הוספת ה-'as any' כאן פותרת את השגיאה הארוכה שקיבלת
  }
});

// 3. הגדרת ה-Endpoint
export const POST = async (req: NextRequest) => {
  const { handleRequest } = copilotRuntimeNextJSAppRouterEndpoint({
    runtime, 
    serviceAdapter,
    // וודא שזה תואם ל-runtimeUrl ב-CopilotKit Provider ב-layout או ב-page
    endpoint: "/api/copilot", 
  });

  return handleRequest(req);
};