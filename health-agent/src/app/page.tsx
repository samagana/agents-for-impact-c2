"use client";

import { CopilotKitCSSProperties, CopilotChat } from "@copilotkit/react-ui";
import { useState } from "react";

export default function HealthAgentPage() {
  const [accentColor] = useState("#8b5cf6"); // Gemini purple

  return (
    <main
      style={{ "--copilot-kit-primary-color": accentColor } as CopilotKitCSSProperties}
      className="h-screen w-screen flex flex-col bg-white"
    >
      {/* Top Navigation Bar */}
      <div className="border-b border-gray-200 bg-white px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-full bg-gradient-to-br from-purple-500 via-pink-500 to-red-500 flex items-center justify-center">
            <span className="text-white font-bold text-lg">+</span>
          </div>
          <h1 className="text-2xl font-semibold text-gray-900">Health+</h1>
        </div>
        <div className="flex items-center gap-4">
          <button className="text-gray-600 hover:text-gray-900 text-sm font-medium">Help</button>
          <button className="text-gray-600 hover:text-gray-900 text-sm font-medium">Updates</button>
        </div>
      </div>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col bg-white justify-center">
        <div className="w-full max-w-2xl h-full mx-auto flex flex-col overflow-hidden">
          <CopilotChat
            instructions="You are Health+, a friendly and knowledgeable health agent with expertise in engaging users and understanding their health conditions. Your goal is to create a welcoming environment where users feel comfortable sharing their health concerns and receiving support. Be conversational, empathetic, and provide evidence-based guidance."
            labels={{
              initial: "👋 Welcome to Health+\n\nI'm your AI health companion. I can help you with:\n\n• Health metrics and wellness tracking\n• Finding nearby clinics and healthcare providers\n• Air quality and environmental health impacts\n• Vaccination information and recommendations\n• Personalized health insights and guidance\n\nWhat would you like to know about your health?",
              placeholder: "Ask me anything about your health...",
            }}
          />
        </div>
      </div>
    </main>
  );
}
