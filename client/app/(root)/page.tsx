import Image from "next/image";
import Calendar from "../../components/ui/Calendar"
import React from "react";

export default function Home() {
  return (
    <section className="flex-center min-h-screen size-full max-sm:px-6 bg-[#222222]">
      <Calendar />
    </section>
  );
}
