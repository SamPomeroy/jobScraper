'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { supabase } from '@/app/supabase/client';
import type { UserJobStatus } from "@/app/types/application";
export default function HandleOAuthRedirect() {
  const router = useRouter();

  useEffect(() => {
    const handleRedirect = async () => {
      // Extract query param
      const authCode = new URLSearchParams(window.location.search).get("code");
      const codeVerifier = localStorage.getItem("supabase.code_verifier");

      console.log("🔐 authCode:", authCode);
      console.log("🧪 codeVerifier:", codeVerifier);

      if (!authCode || !codeVerifier) {
        console.error("🚫 Missing authCode or codeVerifier");
        return;
      }

      try {
        const { data, error } = await supabase.auth.exchangeCodeForSession(
          authCode
        );

        if (error) {
          console.error("❌ Supabase exchange error:", error.message);
          return;
        }

        console.log("✅ Session exchanged:", data?.session?.access_token);
        localStorage.removeItem("supabase.code_verifier"); // optional cleanup
        router.push("/dashboard");
      } catch (err) {
        console.error("❌ Unexpected OAuth error:", err);
      }
    };

    handleRedirect();
  }, []);

  return null;
}