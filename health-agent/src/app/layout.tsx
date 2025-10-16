import type { Metadata } from "next";

import { CopilotKit } from "@copilotkit/react-core";
import "./globals.css";
import "@copilotkit/react-ui/styles.css";

export const metadata: Metadata = {
  title: "Health Agent - AI-Powered Health Assistant",
  description: "Your personal AI health assistant powered by Google ADK. Get health insights, find clinics, check air quality, and receive personalized health recommendations.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={"antialiased"}>
        <CopilotKit runtimeUrl="/api/copilotkit" agent="health_agent">
          {children}
        </CopilotKit>
      </body>
    </html>
  );
}
