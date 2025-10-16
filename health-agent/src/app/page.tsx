"use client";

import { useCoAgent, useCopilotAction } from "@copilotkit/react-core";
import { CopilotKitCSSProperties, CopilotSidebar } from "@copilotkit/react-ui";
import { useState } from "react";

export default function HealthAgentPage() {
  const [accentColor, setAccentColor] = useState("#10b981"); // Health green

  // 🪁 Frontend Actions: https://docs.copilotkit.ai/guides/frontend-actions
  useCopilotAction({
    name: "setAccentColor",
    parameters: [{
      name: "accentColor",
      description: "The accent color to set for the health dashboard.",
      required: true,
    }],
    handler({ accentColor }) {
      setAccentColor(accentColor);
    },
  });

  return (
    <main style={{ "--copilot-kit-primary-color": accentColor } as CopilotKitCSSProperties}>
      <HealthDashboard accentColor={accentColor} />
      <CopilotSidebar
        clickOutsideToClose={false}
        defaultOpen={true}
        labels={{
          title: "Health Assistant",
          initial: "👋 Welcome to your Health Assistant! I'm here to help you with your health concerns and provide personalized support.\n\nYou can ask me to:\n- **Check your health metrics** - Get insights about your health data\n- **Find nearby clinics** - Locate healthcare facilities near you\n- **Check air quality** - See how air quality affects your health\n- **Vaccination info** - Get vaccination statistics and recommendations\n- **Health insights** - Receive personalized health recommendations\n\nFeel free to share your health concerns, and I'll provide support and guidance!"
        }}
      />
    </main>
  );
}

// State of the agent, make sure this aligns with your agent's state.
type HealthMetric = {
  id: string;
  label: string;
  value: string | number;
  unit?: string;
  icon: string;
  status: "good" | "warning" | "alert";
};

type HealthInsight = {
  id: string;
  title: string;
  description: string;
  type: "tip" | "alert" | "info";
  timestamp: string;
};

type AgentState = {
  metrics: HealthMetric[];
  insights: HealthInsight[];
  userName?: string;
};

function HealthDashboard({ accentColor }: { accentColor: string }) {
  // 🪁 Shared State: https://docs.copilotkit.ai/coagents/shared-state
  const { state, setState } = useCoAgent<AgentState>({
    name: "health_agent",
    initialState: {
      metrics: [
        {
          id: "heart-rate",
          label: "Heart Rate",
          value: 72,
          unit: "bpm",
          icon: "❤️",
          status: "good",
        },
        {
          id: "steps",
          label: "Steps Today",
          value: 8234,
          unit: "steps",
          icon: "👟",
          status: "good",
        },
        {
          id: "water",
          label: "Water Intake",
          value: 6,
          unit: "glasses",
          icon: "💧",
          status: "warning",
        },
        {
          id: "sleep",
          label: "Sleep Last Night",
          value: 7.5,
          unit: "hours",
          icon: "😴",
          status: "good",
        },
      ],
      insights: [
        {
          id: "insight-1",
          title: "Stay Hydrated",
          description: "You've had 6 glasses of water today. Try to reach 8 glasses for optimal hydration.",
          type: "tip",
          timestamp: new Date().toISOString(),
        },
      ],
      userName: "User",
    },
  });

  const removeInsight = (id: string) => {
    setState({
      ...state,
      insights: state.insights?.filter((insight) => insight.id !== id),
    });
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case "good":
        return "bg-green-100 text-green-800 border-green-300";
      case "warning":
        return "bg-yellow-100 text-yellow-800 border-yellow-300";
      case "alert":
        return "bg-red-100 text-red-800 border-red-300";
      default:
        return "bg-gray-100 text-gray-800 border-gray-300";
    }
  };

  const getInsightColor = (type: string) => {
    switch (type) {
      case "tip":
        return "bg-blue-50 border-blue-200 text-blue-900";
      case "alert":
        return "bg-red-50 border-red-200 text-red-900";
      case "info":
        return "bg-purple-50 border-purple-200 text-purple-900";
      default:
        return "bg-gray-50 border-gray-200 text-gray-900";
    }
  };

  return (
    <div className="min-h-screen w-screen bg-gradient-to-br from-slate-50 to-slate-100 p-6">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-8 pb-6 border-b-2" style={{ borderColor: accentColor }}>
          <h1 className="text-4xl font-bold text-slate-900 mb-2">
            Health Dashboard
          </h1>
          <p className="text-slate-600">
            Welcome back, {state.userName}! Here's your health overview.
          </p>
        </div>

        {/* Health Metrics Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          {state.metrics?.map((metric) => (
            <div
              key={metric.id}
              className={`p-6 rounded-xl border-2 transition-all ${getStatusColor(
                metric.status
              )}`}
            >
              <div className="flex items-start justify-between mb-3">
                <span className="text-3xl">{metric.icon}</span>
                <span className="text-xs font-semibold uppercase tracking-wide opacity-70">
                  {metric.status}
                </span>
              </div>
              <p className="text-sm font-medium opacity-75 mb-1">{metric.label}</p>
              <p className="text-2xl font-bold">
                {metric.value}
                {metric.unit && <span className="text-sm ml-1">{metric.unit}</span>}
              </p>
            </div>
          ))}
        </div>

        {/* Health Insights */}
        <div className="bg-white rounded-xl shadow-md p-6">
          <h2 className="text-2xl font-bold text-slate-900 mb-4">Health Insights</h2>
          {state.insights && state.insights.length > 0 ? (
            <div className="space-y-3">
              {state.insights.map((insight) => (
                <div
                  key={insight.id}
                  className={`p-4 rounded-lg border-l-4 relative group ${getInsightColor(
                    insight.type
                  )}`}
                >
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <h3 className="font-semibold mb-1">{insight.title}</h3>
                      <p className="text-sm opacity-90">{insight.description}</p>
                    </div>
                    <button
                      onClick={() => removeInsight(insight.id)}
                      className="ml-4 opacity-0 group-hover:opacity-100 transition-opacity
                        text-lg hover:scale-110 flex-shrink-0"
                    >
                      ✕
                    </button>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-center text-slate-500 py-8">
              No insights yet. Ask the assistant for health recommendations!
            </p>
          )}
        </div>
      </div>
    </div>
  );
}


