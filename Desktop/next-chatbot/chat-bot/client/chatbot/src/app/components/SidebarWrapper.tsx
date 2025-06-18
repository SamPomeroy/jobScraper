"use client";

import { usePathname } from "next/navigation";
import ChatSidebar from "./ChatSidebar";

export default function SidebarWrapper({ userId }: { userId: string }) {
  const pathname = usePathname();
  const hideSidebar = pathname.startsWith("/sign-in") || pathname.startsWith("/sign-out");

  console.log("SidebarWrapper rendering. Hide sidebar?", hideSidebar); // ✅ Debug

  return hideSidebar ? null : <ChatSidebar userId={userId} onSelectConversation={(msg) => console.log("Load past message:", msg)} />;
}