import React from "react";
import Link from "next/link";
import Image from "next/image";

const LogIn = () => {
  return (
    <section className="flex-center size-full max-sm:px-6 bg-[#222222]">
        <section className="auth-form">
      <header className="flex flex-col gap-1 justify-center items-center md:gap-3">
        <Image
          src="/Cal-icon.png"
          width={300}
          height={300}
          alt="menu icon"
        />
        <h1 className="text-26 font-ibm-plex-serif font-bold text-black-1 text-[#fefefe]">
          TodoCalendar
        </h1>
        <div className="flex flex-col gap-1 md:gap-3">
          <h1 className="text-24 lg:text-36 mt-2 font-semibold text-[#fefefe]">
            <p className="text-16 font-normal text-[#bbbbbb]">
              Interactive calendar with todos
            </p>
            <Link
              className="bg-black text-20 font-bold justify-center flex flexbox m-2 p-2 mt-10 rounded-2xl"
              href="/sign-in">
              Sign In
            </Link>
            <Link
              className="bg-black text-20 font-bold justify-center flex flexbox m-2 p-2 rounded-2xl"
              href="/sign-up">
              Sign Up
            </Link>
          </h1>
        </div>
      </header>
    </section>
    </section>
  )
}

export default LogIn